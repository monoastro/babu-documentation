"""RAG engine — a queryable semantic index over the codebase.

Phase 1 of the agentic controller. The Architect Agent uses ``query_context()``
to retrieve the layout patterns, component signatures, and extraction schemas it
needs before proposing a repair, instead of being handed the whole codebase.

WHAT IS INDEXED
    html_engine/               the component vocabulary the agent builds with
    document_builder/          existing layout builders to pattern-match against
    information_extraction/    the extractor and the JSON schemas
    documentation/*.md         architecture overview + verification rules

``controller-old/`` is deliberately NOT indexed. It is deprecated; everything
worth keeping has been salvaged into this package (see SALVAGE.md). Indexing it
would let the agent retrieve and imitate code that is scheduled for deletion.

CHUNKING
Python files are split on top-level ``def``/``class`` boundaries via ``ast``, so
a retrieved chunk is a whole function or class with its docstring rather than an
arbitrary window. JSON schemas are chunked per top-level property, so a query
about one field does not drag in the entire schema. Markdown is split on
headings.

EMBEDDINGS
``sentence-transformers/all-MiniLM-L6-v2`` by default (384-dim, CPU-friendly),
stored in a FAISS ``IndexFlatIP`` over L2-normalised vectors, so inner product
is cosine similarity. The index and its metadata sidecar live in
``agentic_controller/.rag_index/``.

The index is content-addressed: a manifest of file mtimes and sizes is stored
alongside it, and ``build_index(force=False)`` is a no-op when nothing changed.
``html_engine`` is explicitly not final — rebuild after adding components.

CLI
    python -m agentic_controller.rag_engine build [--force]
    python -m agentic_controller.rag_engine query "how do I render a table" [-k 5]
    python -m agentic_controller.rag_engine stats
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import pickle
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

# ── Configuration ─────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = Path(__file__).resolve().parent / ".rag_index"
FAISS_PATH = INDEX_DIR / "vectors.faiss"
META_PATH = INDEX_DIR / "chunks.pkl"
MANIFEST_PATH = INDEX_DIR / "manifest.json"

DEFAULT_MODEL = os.getenv("RAG_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

#: Directories to index, relative to the project root.
SOURCE_DIRS: tuple[str, ...] = (
    "html_engine",
    "document_builder",
    "information_extraction",
)

#: Individual documentation files to index.
SOURCE_DOCS: tuple[str, ...] = (
    "documentation/DOCUMENTATION.md",
    "documentation/verification-rules.md",
    "documentation/agentic-generator.md",
)

#: Never index these, even under a SOURCE_DIR.
EXCLUDE_PATTERNS: tuple[str, ...] = (
    "__pycache__",
    ".venv",
    ".rag_index",
    "controller-old",   # deprecated — salvaged into agentic_controller/
    "graphify-out",
    "_patched.json",    # generated artifacts, not source of truth
    "test-",            # hand-written HTML fixtures, not engine code
)

INDEXED_SUFFIXES: tuple[str, ...] = (".py", ".json", ".md")

#: Chunks shorter than this (characters) carry no retrievable signal.
MIN_CHUNK_CHARS = 40


# ── Chunk model ───────────────────────────────────────────────────

@dataclass
class Chunk:
    """One retrievable unit of context."""

    text: str
    source_file: str          # repo-relative, forward slashes
    kind: str                 # "function" | "class" | "module" | "schema_field" | "section"
    name: str                 # symbol or heading name
    lineno: int = 0
    extras: dict = field(default_factory=dict)

    def header(self) -> str:
        """A one-line provenance banner prepended to the embedded text."""
        loc = f":{self.lineno}" if self.lineno else ""
        return f"# {self.source_file}{loc} — {self.kind} {self.name}"

    def embed_text(self) -> str:
        return f"{self.header()}\n{self.text}"

    def render(self) -> str:
        """How a retrieved chunk is presented to the agent."""
        return f"{self.header()}\n{self.text.rstrip()}"


# ── File discovery ────────────────────────────────────────────────

def _excluded(path: Path) -> bool:
    s = path.as_posix()
    return any(pat in s for pat in EXCLUDE_PATTERNS)


def iter_source_files(root: Path = PROJECT_ROOT) -> list[Path]:
    """Every file that belongs in the index, deterministically ordered."""
    found: list[Path] = []

    for rel in SOURCE_DIRS:
        base = root / rel
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix in INDEXED_SUFFIXES and not _excluded(path):
                found.append(path)

    for rel in SOURCE_DOCS:
        path = root / rel
        if path.is_file() and not _excluded(path):
            found.append(path)

    return found


# ── Chunkers ──────────────────────────────────────────────────────

def chunk_python(path: Path, root: Path = PROJECT_ROOT) -> list[Chunk]:
    """Split a Python file on top-level def/class boundaries.

    Falls back to a single module-level chunk if the file does not parse — a
    half-written ``layout_1.py`` from a previous agent iteration should not
    break the whole index build.
    """
    rel = path.relative_to(root).as_posix()
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [Chunk(text=source, source_file=rel, kind="module", name=path.stem)]

    lines = source.splitlines()
    chunks: list[Chunk] = []
    covered: set[int] = set()

    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        start = min((d.lineno for d in node.decorator_list), default=node.lineno) - 1
        end = node.end_lineno or node.lineno
        covered.update(range(start, end))

        kind = "class" if isinstance(node, ast.ClassDef) else "function"
        body = "\n".join(lines[start:end])
        chunks.append(
            Chunk(
                text=body,
                source_file=rel,
                kind=kind,
                name=node.name,
                lineno=start + 1,
                extras={"docstring": (ast.get_docstring(node) or "")[:400]},
            )
        )

        # Index methods separately too — "how do I render a table cell" should
        # retrieve TableCell.to_html, not the entire TableCell class.
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                if not isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                s = min((d.lineno for d in sub.decorator_list), default=sub.lineno) - 1
                e = sub.end_lineno or sub.lineno
                chunks.append(
                    Chunk(
                        text="\n".join(lines[s:e]),
                        source_file=rel,
                        kind="method",
                        name=f"{node.name}.{sub.name}",
                        lineno=s + 1,
                        extras={"docstring": (ast.get_docstring(sub) or "")[:400]},
                    )
                )

    # Whatever is left at module level: imports, __all__, constants like
    # SYSTEM_PROMPT or DOCUMENTS. This is where the registry lives.
    remainder = "\n".join(l for i, l in enumerate(lines) if i not in covered).strip()
    if len(remainder) >= MIN_CHUNK_CHARS:
        chunks.append(
            Chunk(
                text=remainder,
                source_file=rel,
                kind="module",
                name=path.stem,
                lineno=1,
                extras={"docstring": (ast.get_docstring(tree) or "")[:400]},
            )
        )

    return chunks


def chunk_json_schema(path: Path, root: Path = PROJECT_ROOT) -> list[Chunk]:
    """Split an extraction schema into one chunk per top-level property.

    Field ``description`` values are the OCR extraction prompts — they are the
    highest-signal text in the whole corpus for schema-repair queries, so each
    one is retrievable on its own.
    """
    rel = path.relative_to(root).as_posix()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []

    if not isinstance(data, dict):
        return []

    chunks: list[Chunk] = []
    properties = data.get("properties")
    required = set(data.get("required", []) or [])

    if isinstance(properties, dict):
        for name, spec in properties.items():
            body = json.dumps({name: spec}, indent=2, ensure_ascii=False)
            chunks.append(
                Chunk(
                    text=body,
                    source_file=rel,
                    kind="schema_field",
                    name=name,
                    extras={
                        "required": name in required,
                        "description": str(spec.get("description", ""))[:400]
                        if isinstance(spec, dict) else "",
                    },
                )
            )

    # A skeleton chunk so "what fields does the laalpurja schema have" hits the
    # schema as a whole rather than one arbitrary field.
    skeleton = {k: v for k, v in data.items() if k != "properties"}
    skeleton["properties"] = sorted(properties) if isinstance(properties, dict) else []
    chunks.append(
        Chunk(
            text=json.dumps(skeleton, indent=2, ensure_ascii=False),
            source_file=rel,
            kind="schema",
            name=path.stem,
            extras={"field_count": len(properties or {})},
        )
    )
    return chunks


_HEADING = re.compile(r"^(#{1,6})\s+(.*)$", re.M)


def chunk_markdown(path: Path, root: Path = PROJECT_ROOT) -> list[Chunk]:
    """Split a markdown file on headings."""
    rel = path.relative_to(root).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    matches = list(_HEADING.finditer(text))
    if not matches:
        return [Chunk(text=text, source_file=rel, kind="section", name=path.stem)]

    chunks: list[Chunk] = []
    if matches[0].start() > 0:
        preamble = text[: matches[0].start()].strip()
        if len(preamble) >= MIN_CHUNK_CHARS:
            chunks.append(
                Chunk(text=preamble, source_file=rel, kind="section", name=f"{path.stem} (preamble)")
            )

    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.start() : end].strip()
        if len(body) < MIN_CHUNK_CHARS:
            continue
        lineno = text.count("\n", 0, m.start()) + 1
        chunks.append(
            Chunk(
                text=body,
                source_file=rel,
                kind="section",
                name=m.group(2).strip(),
                lineno=lineno,
                extras={"level": len(m.group(1))},
            )
        )
    return chunks


def chunk_file(path: Path, root: Path = PROJECT_ROOT) -> list[Chunk]:
    if path.suffix == ".py":
        chunks = chunk_python(path, root)
    elif path.suffix == ".json":
        chunks = chunk_json_schema(path, root)
    elif path.suffix == ".md":
        chunks = chunk_markdown(path, root)
    else:
        return []
    return [c for c in chunks if len(c.text.strip()) >= MIN_CHUNK_CHARS]


def build_chunks(root: Path = PROJECT_ROOT) -> list[Chunk]:
    """Chunk every indexable file under *root*."""
    chunks: list[Chunk] = []
    for path in iter_source_files(root):
        chunks.extend(chunk_file(path, root))
    return chunks


# ── Embeddings ────────────────────────────────────────────────────

_model_cache: dict[str, object] = {}


def _load_model(name: str = DEFAULT_MODEL):
    """Load (and memoise) the sentence-transformers model."""
    if name in _model_cache:
        return _model_cache[name]
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise RuntimeError(
            "sentence-transformers is not installed.\n"
            "  pip install sentence-transformers faiss-cpu"
        ) from exc
    model = SentenceTransformer(name)
    _model_cache[name] = model
    return model


def _embed(texts: Sequence[str], model_name: str = DEFAULT_MODEL):
    """Embed *texts* and L2-normalise, so inner product == cosine similarity."""
    import numpy as np

    model = _load_model(model_name)
    vectors = model.encode(
        list(texts),
        batch_size=32,
        show_progress_bar=len(texts) > 200,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return np.asarray(vectors, dtype="float32")


# ── Manifest (staleness detection) ────────────────────────────────

def _manifest(root: Path = PROJECT_ROOT) -> dict:
    entries = {}
    for path in iter_source_files(root):
        try:
            st = path.stat()
        except OSError:
            continue
        entries[path.relative_to(root).as_posix()] = {
            "size": st.st_size,
            "mtime": int(st.st_mtime),
        }
    payload = json.dumps(entries, sort_keys=True)
    return {
        "files": entries,
        "digest": hashlib.sha256(payload.encode()).hexdigest(),
        "model": DEFAULT_MODEL,
    }


def index_is_stale(root: Path = PROJECT_ROOT) -> bool:
    """True when the index is missing or the corpus changed since it was built."""
    if not (FAISS_PATH.is_file() and META_PATH.is_file() and MANIFEST_PATH.is_file()):
        return True
    try:
        stored = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return True
    current = _manifest(root)
    return stored.get("digest") != current["digest"] or stored.get("model") != current["model"]


# ── Build / load ──────────────────────────────────────────────────

def build_index(root: Path = PROJECT_ROOT, *, force: bool = False, verbose: bool = True) -> int:
    """Build the FAISS index. Returns the number of chunks indexed.

    A no-op when the index is already current, unless *force*.
    """
    import faiss

    if not force and not index_is_stale(root):
        chunks, _ = load_index()
        if verbose:
            print(f"Index is current — {len(chunks)} chunks. Use --force to rebuild.")
        return len(chunks)

    chunks = build_chunks(root)
    if not chunks:
        raise RuntimeError(f"No indexable files found under {root}")

    if verbose:
        print(f"Embedding {len(chunks)} chunks with {DEFAULT_MODEL} …")

    vectors = _embed([c.embed_text() for c in chunks])
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(FAISS_PATH))
    META_PATH.write_bytes(pickle.dumps([asdict(c) for c in chunks]))
    MANIFEST_PATH.write_text(
        json.dumps(_manifest(root), indent=2, ensure_ascii=False), encoding="utf-8"
    )

    if verbose:
        by_file = len({c.source_file for c in chunks})
        print(f"Indexed {len(chunks)} chunks from {by_file} files → {INDEX_DIR}")
    return len(chunks)


_index_cache: dict[str, object] = {}


def load_index():
    """Load (and memoise) the FAISS index and its chunk metadata."""
    if "index" in _index_cache:
        return _index_cache["chunks"], _index_cache["index"]

    import faiss

    if not (FAISS_PATH.is_file() and META_PATH.is_file()):
        raise RuntimeError(
            "RAG index not built. Run:\n"
            "  python -m agentic_controller.rag_engine build"
        )

    index = faiss.read_index(str(FAISS_PATH))
    chunks = [Chunk(**d) for d in pickle.loads(META_PATH.read_bytes())]
    _index_cache["index"] = index
    _index_cache["chunks"] = chunks
    return chunks, index


# ── Query ─────────────────────────────────────────────────────────

def query_context(
    question: str,
    k: int = 5,
    *,
    source_filter: str | None = None,
    kind_filter: Iterable[str] | None = None,
    auto_rebuild: bool = True,
) -> list[dict]:
    """Return the *k* most relevant code snippets for *question*.

    This is the function the Architect Agent calls. Each result is a dict with
    ``text``, ``source_file``, ``kind``, ``name``, ``lineno``, and ``score``
    (cosine similarity, 0–1).

    Parameters
    ----------
    source_filter:
        Substring match on the repo-relative path, e.g. ``"html_engine"`` to
        restrict retrieval to the component library.
    kind_filter:
        Restrict to chunk kinds, e.g. ``("schema_field",)`` when reasoning about
        extraction descriptions.
    auto_rebuild:
        Rebuild the index first if the corpus changed. ``html_engine`` is still
        evolving, so this defaults on.
    """
    if auto_rebuild and index_is_stale():
        build_index(force=True, verbose=False)

    chunks, index = load_index()
    if not chunks:
        return []

    kinds = set(kind_filter) if kind_filter else None
    filtering = bool(source_filter or kinds)

    # Over-fetch when filtering so k survivors remain after the filter.
    fetch = min(len(chunks), k * 8 if filtering else k)
    qvec = _embed([question])
    scores, ids = index.search(qvec, fetch)

    results: list[dict] = []
    for score, idx in zip(scores[0], ids[0]):
        if idx < 0:
            continue
        chunk = chunks[idx]
        if source_filter and source_filter not in chunk.source_file:
            continue
        if kinds and chunk.kind not in kinds:
            continue
        results.append({**asdict(chunk), "score": round(float(score), 4)})
        if len(results) >= k:
            break
    return results


def format_context(results: Sequence[dict], *, max_chars: int = 12000) -> str:
    """Render retrieved chunks into a single prompt-ready block.

    Truncates at *max_chars* so a broad query cannot blow the agent's context
    window; the cut is reported rather than silent.
    """
    blocks: list[str] = []
    used = 0
    for i, r in enumerate(results, 1):
        loc = f":{r['lineno']}" if r.get("lineno") else ""
        block = (
            f"[{i}] {r['source_file']}{loc} — {r['kind']} {r['name']} "
            f"(score {r['score']})\n"
            f"{'-' * 70}\n{r['text'].rstrip()}\n"
        )
        if used + len(block) > max_chars:
            blocks.append(f"[… {len(results) - i + 1} more results truncated]")
            break
        blocks.append(block)
        used += len(block)
    return "\n".join(blocks)


def stats() -> dict:
    """Index composition — useful for verifying coverage after a rebuild."""
    chunks, index = load_index()
    by_kind: dict[str, int] = {}
    by_file: dict[str, int] = {}
    for c in chunks:
        by_kind[c.kind] = by_kind.get(c.kind, 0) + 1
        by_file[c.source_file] = by_file.get(c.source_file, 0) + 1
    return {
        "chunks": len(chunks),
        "files": len(by_file),
        "vectors": index.ntotal,
        "dim": index.d,
        "model": DEFAULT_MODEL,
        "by_kind": dict(sorted(by_kind.items(), key=lambda kv: -kv[1])),
        "by_file": dict(sorted(by_file.items(), key=lambda kv: -kv[1])),
        "stale": index_is_stale(),
    }


# ── CLI ───────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m agentic_controller.rag_engine",
        description="Semantic index over html_engine, document_builder, and information_extraction.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_build = sub.add_parser("build", help="Build or refresh the index.")
    p_build.add_argument("--force", action="store_true", help="Rebuild even if current.")

    p_query = sub.add_parser("query", help="Retrieve context for a question.")
    p_query.add_argument("question")
    p_query.add_argument("-k", type=int, default=5, help="Number of results (default: 5).")
    p_query.add_argument("--source", help="Restrict to paths containing this substring.")
    p_query.add_argument("--kind", nargs="*", help="Restrict to chunk kinds.")
    p_query.add_argument("--json", action="store_true", help="Emit raw JSON.")

    sub.add_parser("stats", help="Show index composition.")

    args = parser.parse_args(argv)

    if args.command == "build":
        build_index(force=args.force)
        return 0

    if args.command == "query":
        results = query_context(
            args.question, k=args.k, source_filter=args.source, kind_filter=args.kind
        )
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif not results:
            print("No results.")
        else:
            print(format_context(results))
        return 0

    if args.command == "stats":
        s = stats()
        print(f"Chunks:  {s['chunks']} from {s['files']} files")
        print(f"Vectors: {s['vectors']} × {s['dim']}d  ({s['model']})")
        print(f"Stale:   {s['stale']}")
        print("\nBy kind:")
        for kind, n in s["by_kind"].items():
            print(f"  {kind:14} {n}")
        print("\nBy file:")
        for f, n in s["by_file"].items():
            print(f"  {n:4}  {f}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
