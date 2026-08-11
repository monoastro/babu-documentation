"""The Architect Agent — autonomous layout and schema generation.

Replaces the LangGraph state machine with a tool-calling agent loop.

WHAT THE AGENT SEES
-------------------
Every call carries the four context sources named in the design brief:

1. the **source scan** (image block),
2. the **rendered output** (image block, absent on a from-scratch run),
3. the current **layout builder** and **extraction schema** (paths, read on demand),
4. **html_engine** and the existing builders, via the RAG index.

`documentation/verification-rules.md` is injected *directly* into the system
prompt rather than retrieved. It is small, needed on every call, and prose-to-prose
retrieval scored 0.32-0.39 against it — too weak to rely on.

TWO ENTRY POINTS
----------------
- :func:`analyze_and_repair` — a render exists and failed verification. The agent
  gets the ``VerificationReport`` plus both images and writes ``layout_N.py`` /
  ``<doc>_patched.json``.
- :func:`generate_resources` — no layout or schema exists yet. The agent gets the
  source scan alone and writes both from scratch. This is the ``NotImplementedError``
  stub from ``controller-old/graph.py``, now the feature.

AUTONOMY vs CONSTRAINT
----------------------
The old controller used a **constrained patch vocabulary** — the LLM emitted
``SchemaPatch``/``LayoutPatch`` operations, never raw code. Safe, but it could not
generalize to an unseen document type.

This agent writes layout code directly, gated by :func:`validate_layout`: the
generated module must compile, import, and expose a ``build_<doc_type>`` callable
before a caller may use it. Schema edits still go through
:func:`agentic_controller.schema_patcher.apply_patches` when the agent chooses the
patch route, so the ``*_patched.json`` sidecar convention holds either way.

BEHAVIOURS CARRIED FROM ``controller-old`` (SALVAGE.md §"Behaviour to reproduce")
--------------------------------------------------------------------------------
1. Re-extraction ordering — schema lands before OCR re-runs; the caller honours
   ``RepairResult.needs_reextraction``.
2. Patched-schema preference — :func:`resolve_schema_path` prefers an existing
   ``*_patched.json`` sidecar. Without this the pipeline silently re-extracts with
   the unpatched schema and the repair appears to do nothing.
3. Iteration cap — ``MAX_REPAIR_ITERATIONS = 3``, with a forced stop.
4. Append-only history — every tool call is appended to ``RepairResult.history``.
5. Dotted-path edits — ``plots.0.plot_no`` is the user-guided edit syntax, and the
   ``data-field`` attributes the layout must preserve for it to work.

USAGE
-----
```python
from agentic_controller.architect import analyze_and_repair, resolve_schema_path
from agentic_controller.verifier import verify

report = verify(source_png, rendered_png)
if report.overall_match != "pass":
    result = analyze_and_repair(
        report=report,
        source_image=source_png,
        rendered_image=rendered_png,
        document_type="laalpurja",
        current_schema_path=resolve_schema_path("laalpurja"),
        current_layout_path=Path("document_builder/laalpurja/layout.py"),
    )
```
"""

from __future__ import annotations
import argparse
import ast
import base64
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal
from dotenv import load_dotenv
from agentic_controller.models import VerificationReport
from agentic_controller.rag_engine import format_context, query_context
from information_extraction.languages import DEFAULT_LANGUAGE, language_spec

load_dotenv()

#Constants
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = PROJECT_ROOT / "information_extraction" / "schemas"
BUILDER_DIR = PROJECT_ROOT / "document_builder"
RULES_PATH = PROJECT_ROOT / "documentation" / "verification-rules.md"

MAX_REPAIR_ITERATIONS = 3
MAX_TOOL_CALLS = 24
#Budget for the inner tool-use loop of a single agent invocation
COMMAND_TIMEOUT = 120

_ALLOWED_COMMAND_PREFIXES = (
    "python -m agentic_controller",
    "python -m information_extraction",
    "python -m py_compile",
    "ls",
    "cat",
    "head",
    "tail",
    "grep",
    "rg",
    "find",
    "wc",
)
# execute_command allowlist. The agent may inspect and re-run the pipeline; it
# may not install packages, touch git, or reach the network.
#
# `python -c` is deliberately absent. It was on this list, and it is arbitrary
# code execution: one run deleted document_builder/citizenship_back/layout.py and
# truncated information_extraction/schemas/citizenship_back.json to zero bytes —
# both writes that _write_allowed() refuses through the write_file tool. An
# allowlist that contains a general-purpose interpreter is not an allowlist. Use
# `python -m py_compile` to check syntax; validate_layout() already build-probes a
# layout in a subprocess, which is what `python -c` was really being used for.

# Characters that turn a single allowlisted command into something else:
# redirection truncates a file, and the separators chain a second command that
# never sees the prefix check. `cat x > schema.json` passed the old check as a
# "cat" command while destroying the target.
_SHELL_METACHARACTERS = (">", "<", "|", ";", "&", "$(", "`", "\n", "\r")

# Files the agent must never modify, whatever route it takes. These are the
# rollback originals promised in the docs; the guard below verifies the promise
# instead of trusting it.
def _protected_originals() -> list[Path]:
    roots = (BUILDER_DIR.resolve(), SCHEMA_DIR.resolve())
    out: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        out.extend(p for p in root.rglob("layout.py") if p.is_file())
        out.extend(
            p for p in root.rglob("*.json")
            if p.is_file() and not p.stem.endswith("_patched")
        )
    return sorted(out)


def _snapshot(paths: list[Path]) -> dict[Path, bytes | None]:
    """Content of each protected file, or None if it does not exist."""
    snap: dict[Path, bytes | None] = {}
    for p in paths:
        try:
            snap[p] = p.read_bytes()
        except OSError:
            snap[p] = None
    return snap


def _restore_changed(before: dict[Path, bytes | None]) -> list[str]:
    """Undo any modification to a protected original. Returns what was restored."""
    restored: list[str] = []
    for p, original in before.items():
        try:
            current = p.read_bytes() if p.exists() else None
        except OSError:
            continue
        if current == original:
            continue
        try:
            if original is None:
                p.unlink(missing_ok=True)
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(original)
        except OSError:
            continue
        verb = "deleted" if current is None else "modified"
        restored.append(f"{p.relative_to(PROJECT_ROOT)} ({verb})")
    return restored

_IMAGE_MEDIA_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


#  Result model

@dataclass
class RepairResult:
    """What the Architect Agent produced on one invocation."""

    summary: str
    """One-paragraph explanation of what was wrong and what changed."""

    needs_reextraction: bool
    """True when the schema changed — OCR must re-run before the rebuild."""

    schema_path: Path | None = None
    """The patched schema, if one was written (``<doc>_patched.json``)."""

    layout_path: Path | None = None
    """The updated layout, if one was written (``layout_N.py``)."""

    iteration: int = 1
    """Which repair iteration produced this result."""

    layout_valid: bool | None = None
    """
    Whether the written layout passed :func:`validate_layout`.

    ``None`` means no layout was written, so there was nothing to validate.
    This is structured rather than prose in ``summary`` because callers have to
    branch on it: a layout that fails the gate must not be handed to a human as
    though it were ready to register. It previously existed only as a
    ``[VALIDATION FAILED]`` string appended to the summary, which nothing read,
    so a broken layout was announced as a successful generation.
    """

    validation_message: str = ""
    """The gate's verdict — the traceback tail when it failed."""

    promoted: Path | None = None
    """
    The ``ACTIVE`` pointer, if this layout became the live one.

    Promotion happens only when :attr:`layout_valid` is True, so a layout that
    fails the gate leaves the previous good one live. ``None`` means nothing was
    promoted — either no layout was written, or the one written did not build.
    """

    history: list[dict[str, Any]] = field(default_factory=list)
    """Append-only trace: one entry per tool call, in order."""

    def describe(self) -> str:
        """Human-readable one-screen summary, for the Phase 3 checkpoint."""
        lines = [f"Iteration {self.iteration}: {self.summary}"]
        if self.schema_path:
            lines.append(f"  schema → {self.schema_path}")
        if self.layout_path:
            status = {True: "PASSED", False: "FAILED", None: "not run"}[self.layout_valid]
            lines.append(f"  layout → {self.layout_path}  (validation: {status})")
        if self.promoted:
            lines.append(f"  promoted → {self.layout_path.name} is now live")
        elif self.layout_valid is False:
            lines.append("  not promoted — previous layout stays live")
        if self.layout_valid is False:
            lines.append(f"  validation error: {self.validation_message}")
        lines.append(f"  re-extraction needed: {self.needs_reextraction}")
        lines.append(f"  tool calls: {len(self.history)}")
        return "\n".join(lines)


# Path resolution
#
# These live in ``document_builder/resolver.py`` so the registry and the agent
# cannot disagree about which layout is live. They were duplicated here, and the
# copies drifted: the registry hard-coded ``<doc>.json`` while this module
# preferred ``<doc>_patched.json``, so every schema repair was invisible to
# ``main.py`` and the extraction pipeline. Re-exported under their original
# names because ``run.py`` imports them from here.
from document_builder.resolver import (  # noqa: E402
    active_layout_path,
    latest_layout_path,
    next_layout_path,
    promote_layout,
    resolve_schema_path,
)


def current_layout_path(document_type: str, *, builder_dir: Path | None = None) -> Path | None:
    """The layout that will actually be built — whatever ``ACTIVE`` names.

    This used to return the highest-numbered ``layout_N.py``: the newest file
    written, not the one in use. The agent was therefore shown, and asked to
    repair, a layout the pipeline was not building.
    """
    return active_layout_path(document_type, builder_dir=builder_dir)


# Validation gate

def validate_layout(
    layout_path: Path,
    document_type: str,
    schema_path: Path | None = None,
) -> tuple[bool, str]:
    """Check that a generated layout module is safe for the caller to use.

    Four gates, cheapest first: the file parses as Python, it imports without
    raising, it exposes a ``build_<document_type>`` callable, and that callable
    actually **runs** — invoked on blank data and rendered to HTML.

    The last gate is the one that matters. An import-only check passes a layout
    whose body raises, because a function body does not execute until it is
    called; the failure then surfaces inside ``build_document()``, well past the
    point where it reads as a layout problem.

    Parameters:
        schema_path: Schema whose ``required`` keys seed the blank probe data.
            Optional — without it the builder is called with ``{}``, which still
            catches a bad keyword but not an unguarded key lookup.

    Returns ``(ok, message)``. Phase 3 runs this before repointing the registry.
    """
    if not layout_path.is_file():
        return False, f"Layout not found: {layout_path}"

    source = layout_path.read_text(encoding="utf-8")
    try:
        ast.parse(source, filename=str(layout_path))
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"

    builder_name = f"build_{document_type}"
    # The probe *calls* the builder, it does not merely import it. Importing
    # only executes module top level, so anything wrong inside the function
    # body — a bad keyword, a helper that does not exist, an unguarded lookup
    # on a missing key — passed this gate and then crashed in build_document()
    # several stages later, where the traceback no longer points at the layout.
    # Blank data is the harsh case: every value empty, so a lookup that assumes
    # content fails here rather than on the one scan that happens to omit it.
    probe = (
        "import importlib.util, json, sys, warnings\n"
        "warnings.simplefilter('ignore')\n"
        f"spec = importlib.util.spec_from_file_location('_probe_layout', r'{layout_path}')\n"
        "mod = importlib.util.module_from_spec(spec)\n"
        "sys.modules['_probe_layout'] = mod\n"
        "spec.loader.exec_module(mod)\n"
        f"fn = getattr(mod, {builder_name!r}, None)\n"
        "assert callable(fn), 'missing callable "
        f"{builder_name}'\n"
        f"schema = {str(schema_path)!r} if {schema_path is not None!r} else None\n"
        "required = json.loads(open(schema, encoding='utf-8').read()).get('required', []) if schema else []\n"
        "doc = fn({k: '' for k in required})\n"
        "html = doc.render()\n"
        "assert html.strip().startswith('<!DOCTYPE html>'), 'render() did not "
        "return a full HTML page'\n"
        "print('OK')\n"
    )
    # ``sys.executable``, not ``"python"``: the probe imports html_engine and
    # pydantic, so it has to run under the same interpreter as the caller. A
    # bare ``python`` resolves through PATH, which on a pyenv or conda machine
    # is a shim pointing somewhere without this project's dependencies — every
    # layout would then fail the gate with an ImportError that says nothing
    # about the layout.
    completed = subprocess.run(
        [os.getenv("PYTHON_EXECUTABLE") or sys.executable, "-c", probe],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=COMMAND_TIMEOUT,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        return False, f"Import failed: {detail[-1200:]}"
    return True, (
        f"{layout_path.name} compiles, imports, and {builder_name}() renders "
        f"a full page on blank data."
    )


def validate_schema(schema_path: Path) -> tuple[bool, str]:
    """Check that a written schema is valid JSON with the keys the extractor needs.

    ``information_extraction.extractor.build_data`` reads ``schema["required"]``
    and drops everything else, so a schema whose new fields are absent from
    ``required`` extracts fine and then renders nothing.
    """
    if not schema_path.is_file():
        return False, f"Schema not found: {schema_path}"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    if not isinstance(schema, dict):
        return False, "Schema root must be a JSON object."

    properties = schema.get("properties")
    required = schema.get("required")
    if not isinstance(properties, dict) or not properties:
        return False, "Schema has no 'properties' object."
    if not isinstance(required, list) or not required:
        return False, (
            "Schema has no 'required' list. build_data() only keeps required keys, "
            "so nothing would reach the layout."
        )
    orphans = [k for k in required if k not in properties]
    if orphans:
        return False, f"'required' names fields absent from 'properties': {orphans}"
    unrequired = [k for k in properties if k not in required]
    note = f" ({len(unrequired)} property/properties not in 'required' will be dropped by build_data)" if unrequired else ""
    return True, f"{schema_path.name}: {len(properties)} properties, {len(required)} required{note}."


# System prompt
def _load_rules() -> str:
    try:
        return RULES_PATH.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return (
            "(verification-rules.md unavailable. Fall back to first principles: "
            "English labels over Devanagari values, placeholder boxes for seals, "
            "photos and signatures, and clean typography are all INTENDED "
            "transformations and must never be reported as defects. Only wrong or "
            "missing data and genuine structural mismatches are defects.)"
        )


_OUTPUT_CONTRACT = """{
  "summary": "string - what was wrong and what you changed",
  "needs_reextraction": true or false,
  "schema_path": "absolute path or null",
  "layout_path": "absolute path or null"
}"""


def _build_system_prompt(mode: Literal["repair", "generate"]) -> str:
    """Assemble the system prompt, with the verification rules embedded."""
    if mode == "repair":
        job = """Your job: read a VerificationReport produced by a vision model that compared a
source document scan against its digitally rendered replica, then repair the layout
builder and/or the extraction schema so the next render passes verification."""
        workflow = """# WORKFLOW

1. **Read the report against the images.** Both the source scan and the rendered
   output are attached. Trust your own eyes over the report's prose when they
   disagree, but only act on discrepancies the report marks major or critical.

2. **Classify each blocking discrepancy** as one of:
   - *missing or wrong data* — OCR did not capture it, or captured it badly.
     This is a schema problem. Usually the field description is too weak, not
     the schema structure.
   - *data present but not rendered* — the schema has it and the layout drops it,
     or renders it in the wrong cell. This is a layout problem.
   - *structural mismatch* — column counts, row spans, section order, placeholder
     position. Layout problem.

3. **Retrieve what you need.** `query_context` covers html_engine, the existing
   builders, and the schemas. Look up the component before you use it.

4. **Read before you write.** `read_file` the current layout and schema. Do not
   assume a helper exists.

5. **Write.** Schema edits go to `<doc_type>_patched.json`; layouts go to the
   `layout_N.py` path given in the task message. Never overwrite an original.

6. **Emit the JSON contract** as your final message."""
    else:
        job = """Your job: a document type has no layout builder and no extraction schema yet.
The source scan is attached. Design both from scratch, so the pipeline can extract
this document and render a faithful replica of it."""
        workflow = """# WORKFLOW

1. **Read the scan.** Identify the document's real structure: header block, the
   label/value information panel, any tabular region and its exact column count,
   the footer, and every seal, photo, or signature that needs a placeholder box.

2. **Study a sibling builder first.** `query_context` for an existing layout and
   its schema, then `read_file` that layout in full. Your output must look like it
   was written by the same hand: same helper names, same section comments, same
   component vocabulary.

3. **Write the schema first.** One property per field you can actually see, each
   with a description precise enough for an OCR model to find it. Every field you
   intend to render must also appear in `required` — `build_data()` drops the rest.

4. **Then write the layout.** It must define `build_<doc_type>(data: dict) -> Document`,
   read only keys present in the schema's `required` list, and guard every lookup
   against None so a missing value renders as an empty string rather than the
   literal text "None".

5. **Emit the JSON contract** as your final message, with `needs_reextraction`
   set to true — no extraction has happened yet."""

    return f"""You are the Architect Agent for an autonomous Nepali document digitization pipeline.

{job}

The pipeline is: scan -> schema-guided OCR -> JSON data -> layout builder ->
html_engine Document -> HTML -> headless-Chrome PNG -> vision verification.

# VERIFICATION RULES (your optimization target)

{_load_rules()}

# TOOLS

- **query_context(question, k)** — semantic search over `html_engine/` (the
  component library), `document_builder/` (existing builders), and
  `information_extraction/` (extractor and schemas). Ask in prose: "how to render a
  table", "laalpurja header structure", "citizenship schema father fields".
- **read_file(path)** — read a file. Absolute paths, or paths relative to the
  project root.
- **write_file(path, content)** — write a file. Only paths inside the project's
  `document_builder/` and `information_extraction/schemas/` trees are accepted.
- **execute_command(cmd)** — read-only inspection and pipeline re-runs only.
  Package installs, git, and network access are rejected. There is no shell, so
  no redirection, pipes, or chaining, and one call runs one command. `python -c`
  is unavailable: change files with `write_file` and check them with
  `python -m py_compile`. `layout.py` and the base schemas are restored
  automatically if a command modifies them.

{workflow}

# HARD RULES

- **Blocking issues only.** A `minor` discrepancy is not worth a layout change;
  churning the file to chase one costs a verification cycle and usually regresses
  something else.
- **Schema-first.** A missing field is more often a weak extraction description
  than a missing property. Sharpen the description before you add structure.
- **Never overwrite an original.** `layout.py` and `<doc_type>.json` are the
  rollback point. Write `layout_N.py` and `<doc_type>_patched.json`.
- **Preserve contenteditable.** If the current layout attaches
  `contenteditable="true"` and `data-field="..."` attributes, carry every one of
  them across, with identical field names. The dotted paths (`plots.0.plot_no`)
  are the contract the user-guided edit flow binds to; renaming one silently
  breaks it.
- **Guard against None.** OCR returns absent fields as None. Convert to "" before
  rendering — a literal "None" in the output is a critical defect.
- **Containers take components, not strings.** `Div`, `FlexRow`, `FlexCol`,
  `AbsoluteBox`, and `Card` take child *components* positionally. To put text in
  one, wrap it: `Div(Text("(Signed)"))`, never `Div("(Signed)")`. A bare string is
  coerced to `Text` for you, but a list, dict, or component *class* is a `TypeError`.
- **Use the placeholder components; do not hand-roll them.** For every seal, photo,
  crest, QR block, thumb impression, watermark, or signature space, the engine
  already has the right component — `PlaceholderBox(label, size=..., shape=...)`
  (`shape` is `"rect"`, `"rounded"`, or `"circle"`; `dashed=True` for something a
  human still has to sign), `Watermark(text, opacity=...)`,
  `SignatureBlock(name=..., title=..., signature_label=..., stamp_label=...)`, and
  `corner_box(label, corner="top-left")`. A bordered `Div` with a flex-centring trio
  is the pattern these replace; writing one by hand means re-deriving the border
  weight, the caption size, and the overflow guard, and getting one of them wrong.
- **Attach fields with `field=`, not by hand.** Every component takes
  `field="dotted.path"`, which expands to the `contenteditable`/`data-field` pair.
  Do not redeclare a private `_ea()` helper — `LabelValue(field=...)` puts the
  attributes on the value, where they belong, not on the label.
- **Output is black and white.** Use only `#000000` for ink (text, borders, rules)
  and `#ffffff` for surfaces. `html_engine` normalizes every colour on render, so
  anything else you write is silently rewritten — your source would then disagree
  with the output, which makes the layout harder to reason about. Do not reach for
  colour to convey emphasis; use weight, size, borders, and spacing instead. If the
  source scan is colourful, that is expected — the replica is still monochrome, and
  a colour difference is never a discrepancy worth reporting.
- **`needs_reextraction` is true whenever the schema changed.** Adding or
  rewording a field means nothing until OCR runs again.
- **Write complete files.** No ellipses, no "unchanged above" markers, no TODOs.
  The file you write is the file that runs.

# OUTPUT

Your final message — the one with no tool call — must be exactly this JSON object
and nothing else. No prose before it, no markdown fence around it:

{_OUTPUT_CONTRACT}

Use null, not a guess, for a file you did not write.
"""


# Tool schemas
TOOLS: list[dict[str, Any]] = [
    {
        "name": "query_context",
        "description": (
            "Semantic search over the project's own source: html_engine (component "
            "library), document_builder (existing layout builders), and "
            "information_extraction (OCR extractor and JSON schemas). Ask in prose. "
            "Use this to find component usage, layout patterns worth imitating, and "
            "schema field definitions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Prose query, e.g. 'how to render a table with merged header cells'.",
                },
                "k": {
                    "type": "integer",
                    "description": "How many chunks to return. Default 5, max 12.",
                },
                "source_filter": {
                    "type": "string",
                    "description": (
                        "Optional path prefix to restrict results, e.g. 'html_engine' "
                        "or 'document_builder/laalpurja'."
                    ),
                },
            },
            "required": ["question"],
        },
    },
    {
        "name": "read_file",
        "description": (
            "Read a text file. Accepts an absolute path or one relative to the project "
            "root. Use it on the current layout and schema before proposing changes."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute or project-relative path."},
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": (
            "Write a complete file. Restricted to document_builder/ and "
            "information_extraction/schemas/. Originals (layout.py, <doc>.json) are "
            "rejected — write layout_N.py and <doc>_patched.json instead."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute or project-relative path."},
                "content": {"type": "string", "description": "The entire file content."},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "execute_command",
        "description": (
            "Run a read-only inspection command or re-run the pipeline. Allowed: "
            "python -m agentic_controller..., python -m information_extraction..., "
            "python -m py_compile, ls, cat, head, tail, grep, rg, find, wc. "
            "Anything else is rejected. There is no shell: redirection (>), pipes, "
            "and chaining (;, &&) are refused, and one call runs exactly one "
            "command. `python -c` is not available — use write_file to change a "
            "file and python -m py_compile to check that it parses."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "cmd": {"type": "string", "description": "The shell command."},
            },
            "required": ["cmd"],
        },
    },
]


# ── Tool implementations ──────────────────────────────────────────

def _resolve(path_str: str) -> Path:
    """Resolve a model-supplied path against the project root."""
    p = Path(path_str).expanduser()
    if not p.is_absolute():
        p = PROJECT_ROOT / p
    return p.resolve()


def _write_allowed(path: Path) -> tuple[bool, str]:
    """Gate write_file: inside the writable trees, and never *onto* an original.

    "Original" means a file that already exists. A `layout.py` or base schema
    that has never been written has no rollback value to destroy, and refusing
    it would leave a generated document type with no original at all — which is
    how the generated types ended up as a bare `layout_1.py` with nothing to
    fall back to. Once the file exists, it is protected for good.
    """
    writable = (BUILDER_DIR.resolve(), SCHEMA_DIR.resolve())
    if not any(path == root or root in path.parents for root in writable):
        return False, (
            f"Refused: {path} is outside the writable trees "
            f"(document_builder/, information_extraction/schemas/)."
        )
    if path.suffix == ".py" and path.name == "layout.py" and path.exists():
        return False, (
            "Refused: layout.py is the rollback original. Write layout_N.py instead."
        )
    if (path.suffix == ".json" and not path.stem.endswith("_patched")
            and path.exists()):
        return False, (
            f"Refused: {path.name} is the base schema. Write {path.stem}_patched.json instead."
        )
    if path.suffix not in (".py", ".json"):
        return False, f"Refused: only .py and .json writes are allowed, got {path.suffix or '(none)'}."
    return True, ""


def _tool_query_context(question: str, k: int = 5, source_filter: str | None = None) -> str:
    k = max(1, min(int(k or 5), 12))
    try:
        results = query_context(question, k=k, source_filter=source_filter)
    except Exception as e:  # index missing, model download failure, ...
        return f"Error: retrieval failed ({type(e).__name__}: {e})"
    if not results:
        return "No results. Try broader wording, or drop source_filter."
    return format_context(results, max_chars=9000)


def _tool_read_file(path: str) -> str:
    p = _resolve(path)
    try:
        text = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Error: file not found: {p}"
    except IsADirectoryError:
        listing = "\n".join(sorted(c.name for c in p.iterdir()))
        return f"{p} is a directory. Contents:\n{listing}"
    except UnicodeDecodeError:
        return f"Error: {p} is not UTF-8 text."
    except OSError as e:
        return f"Error reading {p}: {e}"
    if len(text) > 60_000:
        return text[:60_000] + f"\n\n... [truncated, {len(text)} bytes total]"
    return text


def _tool_write_file(path: str, content: str) -> str:
    p = _resolve(path)
    ok, why = _write_allowed(p)
    if not ok:
        return why
    if not content.strip():
        return "Refused: empty content."
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    except OSError as e:
        return f"Error writing {p}: {e}"

    # Immediate feedback so the agent can fix its own mistake in-loop rather than
    # handing a broken file to the caller.
    if p.suffix == ".py":
        try:
            ast.parse(content, filename=str(p))
        except SyntaxError as e:
            return (
                f"Wrote {len(content)} bytes to {p}, but it does NOT parse: "
                f"SyntaxError line {e.lineno}: {e.msg}. Rewrite the file."
            )
    elif p.suffix == ".json":
        valid, msg = validate_schema(p)
        if not valid:
            return f"Wrote {len(content)} bytes to {p}, but it is not usable: {msg}"
        return f"Wrote {len(content)} bytes to {p}. {msg}"
    return f"Wrote {len(content)} bytes to {p} (parses cleanly)."


def _tool_execute_command(cmd: str) -> str:
    stripped = cmd.strip()
    if not stripped.startswith(_ALLOWED_COMMAND_PREFIXES):
        return (
            f"Refused: {stripped.split()[0] if stripped else '(empty)'} is not on the "
            f"allowlist. Allowed prefixes: {', '.join(_ALLOWED_COMMAND_PREFIXES)}."
        )

    # The prefix check only describes the first word. Without this, redirection
    # and chaining smuggle a second, unchecked command past it.
    found = [m for m in _SHELL_METACHARACTERS if m in stripped]
    if found:
        return (
            f"Refused: shell metacharacter(s) {' '.join(repr(m) for m in found)} are not "
            f"allowed. Commands run as a single argument list, so redirection, pipes, "
            f"and chaining are unavailable. Run one command at a time."
        )

    try:
        argv = shlex.split(stripped)
    except ValueError as e:  # unbalanced quotes
        return f"Refused: could not parse command ({e})."
    if not argv:
        return "Refused: empty command."

    # `python` must mean this interpreter, not whatever a PATH shim resolves to.
    if argv[0] == "python":
        argv[0] = sys.executable

    before = _snapshot(_protected_originals())
    try:
        completed = subprocess.run(
            argv,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        _restore_changed(before)
        return f"Error: command exceeded {COMMAND_TIMEOUT}s and was killed."
    except (OSError, ValueError) as e:
        _restore_changed(before)
        return f"Error executing command: {e}"

    out = (completed.stdout + completed.stderr).strip()
    if len(out) > 20_000:
        out = out[:20_000] + "\n... [truncated]"
    result = out or f"(exit code {completed.returncode}, no output)"

    # Defence in depth: an allowlisted command that still managed to touch a
    # rollback original gets undone, and the agent is told so rather than
    # silently succeeding.
    restored = _restore_changed(before)
    if restored:
        result += (
            "\n\n[GUARD] This command modified protected originals, which has been "
            "undone: " + ", ".join(restored) + ". Never write to layout.py or a base "
            "schema — use layout_N.py and <schema>_patched.json via write_file."
        )
    return result


def _dispatch_tool(name: str, args: dict[str, Any]) -> str:
    try:
        if name == "query_context":
            return _tool_query_context(
                args["question"], args.get("k", 5), args.get("source_filter")
            )
        if name == "read_file":
            return _tool_read_file(args["path"])
        if name == "write_file":
            return _tool_write_file(args["path"], args["content"])
        if name == "execute_command":
            return _tool_execute_command(args["cmd"])
    except KeyError as e:
        return f"Error: tool {name} called without required argument {e}."
    except Exception as e:
        return f"Error: tool {name} raised {type(e).__name__}: {e}"
    return f"Error: unknown tool {name!r}."


# ── Content blocks (backend-neutral) ──────────────────────────────
#
# The loop runs on either the Anthropic or the OpenAI SDK. Prompts are assembled
# as neutral blocks and converted per backend at send time, so the entry points
# below never mention a provider.

def _text(text: str) -> dict[str, Any]:
    return {"kind": "text", "text": text}


def _image(path: Path) -> dict[str, Any]:
    """A neutral image block. Validates eagerly — a bad path should fail here,
    not three tool calls into a paid loop."""
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")
    media_type = _IMAGE_MEDIA_TYPES.get(path.suffix.lower())
    if media_type is None:
        raise ValueError(
            f"Unsupported image type {path.suffix!r} for {path}. "
            f"Supported: {', '.join(sorted(_IMAGE_MEDIA_TYPES))}"
        )
    return {
        "kind": "image",
        "media_type": media_type,
        "data": base64.b64encode(path.read_bytes()).decode("ascii"),
    }


def _to_anthropic_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for b in blocks:
        if b["kind"] == "text":
            out.append({"type": "text", "text": b["text"]})
        else:
            out.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": b["media_type"],
                    "data": b["data"],
                },
            })
    return out


def _to_openai_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for b in blocks:
        if b["kind"] == "text":
            out.append({"type": "text", "text": b["text"]})
        else:
            out.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{b['media_type']};base64,{b['data']}",
                    "detail": "high",
                },
            })
    return out


# ── Backend selection ─────────────────────────────────────────────

def _select_backend() -> tuple[str, Any, str]:
    """Return ``(backend, client, model)``.

    Prefers Anthropic when its key is present — the tool-calling loop was designed
    against it and image reasoning is stronger. Falls back to any OpenAI-compatible
    endpoint, which is what the verifier already uses, so a project with only
    ``OPENAI_API_KEY`` still runs end to end.

    ``ARCHITECT_BACKEND=anthropic|openai`` forces the choice.
    """
    forced = (os.getenv("ARCHITECT_BACKEND") or "").strip().lower()
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))

    if forced == "anthropic" or (not forced and has_anthropic):
        if not has_anthropic:
            raise RuntimeError("ARCHITECT_BACKEND=anthropic but ANTHROPIC_API_KEY is not set.")
        try:
            from anthropic import Anthropic
        except ImportError as e:
            raise RuntimeError("pip install anthropic") from e
        model = os.getenv("ARCHITECT_MODEL", "claude-sonnet-4-5-20250929")
        return "anthropic", Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")), model

    if forced == "openai" or (not forced and has_openai):
        if not has_openai:
            raise RuntimeError("ARCHITECT_BACKEND=openai but OPENAI_API_KEY is not set.")
        try:
            from openai import OpenAI
        except ImportError as e:
            raise RuntimeError("pip install openai") from e
        model = os.getenv("ARCHITECT_MODEL", "gpt-4.1")
        return "openai", OpenAI(api_key=os.getenv("OPENAI_API_KEY")), model

    raise RuntimeError(
        "No API key found. The Architect Agent needs ANTHROPIC_API_KEY "
        "(preferred) or OPENAI_API_KEY. Add one to .env."
    )


_OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": t["name"],
            "description": t["description"],
            "parameters": t["input_schema"],
        },
    }
    for t in TOOLS
]


# Agent loop

_BUDGET_NOTICE = (
    "Tool budget exhausted. Do not call any more tools. Reply now with the final "
    "JSON object only, describing the files you actually wrote."
)


def _record(history: list[dict[str, Any]], name: str, args: dict[str, Any], result: str) -> None:
    """Append-only trace — SALVAGE.md behaviour 4."""
    history.append({
        "tool": name,
        "input": {k: (f"<{len(v)} bytes>" if k == "content" else v) for k, v in args.items()},
        "result": result[:400],
    })


def _log_call(verbose: bool, n: int, name: str, args: dict[str, Any]) -> None:
    if verbose:
        preview = args.get("question") or args.get("path") or args.get("cmd") or ""
        print(f"  [{n}] {name}({str(preview)[:80]})")


def _run_agent_anthropic(
    client: Any, model: str, system_prompt: str,
    blocks: list[dict[str, Any]], max_tool_calls: int, verbose: bool,
) -> tuple[str, list[dict[str, Any]]]:
    messages: list[dict[str, Any]] = [{"role": "user", "content": _to_anthropic_blocks(blocks)}]
    history: list[dict[str, Any]] = []
    calls = 0
    forced_finish = False

    while True:
        response = client.messages.create(
            model=model, max_tokens=16_000, system=system_prompt,
            messages=messages, tools=TOOLS,
        )
        messages.append({"role": "assistant", "content": response.content})

        tool_uses = [b for b in response.content if getattr(b, "type", None) == "tool_use"]
        if not tool_uses:
            texts = [b.text for b in response.content if getattr(b, "type", None) == "text"]
            final = "\n".join(texts).strip()
            if not final:
                raise RuntimeError(
                    f"Agent stopped with neither text nor a tool call "
                    f"(stop_reason={response.stop_reason})."
                )
            return final, history

        if forced_finish or calls + len(tool_uses) > max_tool_calls:
            messages.append({"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": tu.id,
                 "content": _BUDGET_NOTICE, "is_error": True}
                for tu in tool_uses
            ]})
            _record(history, "(budget)", {}, _BUDGET_NOTICE)
            forced_finish = True
            continue

        results = []
        for tu in tool_uses:
            calls += 1
            args = dict(tu.input or {})
            _log_call(verbose, calls, tu.name, args)
            result = _dispatch_tool(tu.name, args)
            _record(history, tu.name, args, result)
            results.append({"type": "tool_result", "tool_use_id": tu.id, "content": result})
        messages.append({"role": "user", "content": results})


def _run_agent_openai(
    client: Any, model: str, system_prompt: str,
    blocks: list[dict[str, Any]], max_tool_calls: int, verbose: bool,
) -> tuple[str, list[dict[str, Any]]]:
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": _to_openai_blocks(blocks)},
    ]
    history: list[dict[str, Any]] = []
    calls = 0
    forced_finish = False

    while True:
        response = client.chat.completions.create(
            model=model, messages=messages, tools=_OPENAI_TOOLS, max_tokens=16_000,
        )
        message = response.choices[0].message
        tool_calls = list(message.tool_calls or [])

        # Echo the assistant turn back verbatim; the API rejects a tool result
        # whose originating tool_call is absent from the history.
        messages.append({
            "role": "assistant",
            "content": message.content or "",
            **({"tool_calls": [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in tool_calls
            ]} if tool_calls else {}),
        })

        if not tool_calls:
            final = (message.content or "").strip()
            if not final:
                raise RuntimeError(
                    f"Agent stopped with neither text nor a tool call "
                    f"(finish_reason={response.choices[0].finish_reason})."
                )
            return final, history

        if forced_finish or calls + len(tool_calls) > max_tool_calls:
            for tc in tool_calls:
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": _BUDGET_NOTICE})
            _record(history, "(budget)", {}, _BUDGET_NOTICE)
            forced_finish = True
            continue

        for tc in tool_calls:
            calls += 1
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError as e:
                result = f"Error: arguments were not valid JSON ({e}). Retry the call."
                _record(history, tc.function.name, {}, result)
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
                continue
            _log_call(verbose, calls, tc.function.name, args)
            result = _dispatch_tool(tc.function.name, args)
            _record(history, tc.function.name, args, result)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})


def _run_agent(
    system_prompt: str,
    blocks: list[dict[str, Any]],
    *,
    max_tool_calls: int = MAX_TOOL_CALLS,
    verbose: bool = True,
) -> tuple[str, list[dict[str, Any]]]:
    """Drive the tool-use loop until the model answers with text.

    Returns ``(final_text, history)``.
    """
    backend, client, model = _select_backend()
    if verbose:
        print(f"  backend: {backend} ({model})")
    runner = _run_agent_anthropic if backend == "anthropic" else _run_agent_openai
    return runner(client, model, system_prompt, blocks, max_tool_calls, verbose)



def _parse_json_object(final_text: str) -> dict[str, Any]:
    """Extract a single JSON object from a model's final message.

    Models fence their JSON about half the time and occasionally wrap it in a
    sentence, so both are unwrapped here rather than at each call site.
    """
    text = final_text.strip()
    if text.startswith("```"):
        # ```json ... ``` or ``` ... ```
        body = text.split("```")
        text = body[1] if len(body) > 1 else text
        if text.lstrip().lower().startswith("json"):
            text = text.lstrip()[4:]
        text = text.strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # Last resort: the outermost {...} span.
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end <= start:
            raise RuntimeError(f"Agent returned no JSON object:\n\n{final_text[:2000]}") from None
        try:
            parsed = json.loads(text[start:end + 1])
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Agent returned invalid JSON: {e}\n\n{final_text[:2000]}") from e
    if not isinstance(parsed, dict):
        raise RuntimeError(f"Agent JSON is not an object:\n\n{final_text[:2000]}")
    return parsed


def _parse_contract(final_text: str) -> dict[str, Any]:
    """Extract the JSON contract from the agent's final message."""
    parsed = _parse_json_object(final_text)
    if "summary" not in parsed:
        raise RuntimeError(f"Agent JSON is missing 'summary':\n\n{final_text[:2000]}")
    return parsed


def _result_from_contract(
    contract: dict[str, Any],
    history: list[dict[str, Any]],
    iteration: int,
) -> RepairResult:
    """Build a RepairResult, trusting the filesystem over the agent's claims."""
    schema_path = contract.get("schema_path")
    layout_path = contract.get("layout_path")

    schema = _resolve(schema_path) if schema_path else None
    layout = _resolve(layout_path) if layout_path else None

    # The agent sometimes names a file it decided not to write. Drop phantoms.
    if schema is not None and not schema.is_file():
        schema = None
    if layout is not None and not layout.is_file():
        layout = None

    needs_reextraction = bool(contract.get("needs_reextraction", False))
    if schema is not None and not needs_reextraction:
        # A schema change is inert until OCR re-runs (SALVAGE.md behaviour 1).
        needs_reextraction = True

    return RepairResult(
        summary=str(contract["summary"]),
        needs_reextraction=needs_reextraction,
        schema_path=schema,
        layout_path=layout,
        iteration=iteration,
        history=history,
    )


# ── Public entry point: repair ────────────────────────────────────

def analyze_and_repair(
    report: VerificationReport,
    source_image: Path,
    document_type: str,
    current_schema_path: Path,
    current_layout_path: Path | None = None,
    *,
    rendered_image: Path | None = None,
    user_concerns: str | None = None,
    iteration: int = 1,
    max_tool_calls: int = MAX_TOOL_CALLS,
    verbose: bool = True,
) -> RepairResult:
    """Repair the layout and/or schema so the next render passes verification.

    Parameters
    ----------
    report:
        The report from comparing source against rendered.
    source_image:
        The source scan. Attached to the prompt as an image.
    document_type:
        Slug, e.g. ``"laalpurja"``.
    current_schema_path:
        The schema currently in use. Pass :func:`resolve_schema_path` output so a
        prior ``*_patched.json`` wins over the base.
    current_layout_path:
        The layout currently in use, or None.
    rendered_image:
        The failed render. Attached alongside the source when given — the agent
        reasons far better from the pair than from the report's prose alone.
    user_concerns:
        Free text from the user-guided branch. When present it takes priority over
        the report's own ranking.
    iteration:
        Which repair iteration this is; names ``layout_N.py``.
    max_tool_calls:
        Budget for the inner tool loop.

    Returns
    -------
    RepairResult
    """
    blocking = report.blocking()
    layout_target = next_layout_path(document_type)
    schema_target = SCHEMA_DIR / f"{document_type}_patched.json"

    if blocking:
        blocking_text = "\n".join(
            f"- [{d.severity.upper()}] {d.category} @ {d.location}\n"
            f"    source:   {d.source_observation}\n"
            f"    rendered: {d.rendered_observation}"
            for d in blocking
        )
    else:
        blocking_text = (
            "(none marked major or critical — the user is dissatisfied anyway; "
            "work from their concerns and from the images)"
        )

    concerns_block = (
        f"\n## The user's own concerns (these take priority)\n\n{user_concerns.strip()}\n"
        if user_concerns and user_concerns.strip()
        else ""
    )

    task = f"""# Repair task

The render below failed verification. Fix the layout and/or schema so the next
render passes.

## Context

- Document type:  {document_type}
- Source scan:    {source_image}
- Rendered output:{f" {rendered_image}" if rendered_image else " (not available)"}
- Current schema: {current_schema_path}
- Current layout: {current_layout_path or "(none — you are writing the first one)"}
- Iteration:      {iteration}

## Where to write

- Schema changes -> {schema_target}
- Layout changes -> {layout_target}

Use exactly these paths. Do not invent others, and do not touch the originals.

## Verification report

```json
{report.model_dump_json(indent=2)}
```

## Blocking discrepancies ({len(blocking)} of {len(report.discrepancies)} total)

{blocking_text}
{concerns_block}
## Now

Retrieve the context you need, read the current files, decide whether this is a
schema problem, a layout problem, or both, write the fix, and return the JSON
object. Begin."""

    blocks: list[dict[str, Any]] = [
        _text(task),
        _text("SOURCE scan (the reference):"),
        _image(source_image),
    ]
    if rendered_image is not None:
        blocks.append(_text("RENDERED output (what your pipeline produced):"))
        blocks.append(_image(rendered_image))

    if verbose:
        print(f"Architect (repair, iteration {iteration}) — {len(blocking)} blocking issue(s)")

    final_text, history = _run_agent(
        _build_system_prompt("repair"),
        blocks,
        max_tool_calls=max_tool_calls,
        verbose=verbose,
    )
    result = _result_from_contract(_parse_contract(final_text), history, iteration)

    if result.layout_path is not None:
        # Prefer a schema the agent just wrote over the one it started from —
        # a layout is validated against the fields it was written for.
        ok, msg = validate_layout(
            result.layout_path,
            document_type,
            result.schema_path or current_schema_path,
        )
        result.history.append({"tool": "(validate_layout)", "input": {}, "result": msg})
        result.layout_valid = ok
        result.validation_message = msg
        if verbose:
            print(f"  validate_layout: {'OK' if ok else 'FAILED'} — {msg}")
        if ok:
            # The gate passed, so this layout becomes live. Nothing else has to
            # happen for the next iteration to build from it — that is the
            # point. Before ``ACTIVE`` existed, the registry kept importing the
            # layout the run started with, so a repair loop rebuilt its own
            # input every iteration and could never converge.
            result.promoted = promote_layout(document_type, result.layout_path)
            if verbose:
                print(f"  promoted: {result.layout_path.name} is now the live layout")
        else:
            # Deliberately leave ``ACTIVE`` alone. A layout that does not build
            # must not replace one that does.
            result.summary += f"\n\n[VALIDATION FAILED] {msg}"
    return result


# ── Geometry-first planning ───────────────────────────────────────
#
# ``document_builder.autolayout`` derives every coordinate from the scan's own
# block geometry, which leaves exactly one question arithmetic cannot answer:
# what each block *means*. :func:`plan_blocks` answers it in a single structured
# call — no tool loop, because nothing here writes files — and
# :func:`plan_to_schema` turns that answer into the extraction schema.

_PLAN_ROLES = ("static", "value", "placeholder")

_PLAN_CONTRACT = """{
  "blocks": [
    {
      "block_id": "exactly as listed, e.g. /page/0/Text/9",
      "role": "static | value | placeholder",
      "text": "static: the block's text in the target language. value: the value visible in the scan, translated — used only to size the box.",
      "field": "value only: a snake_case key, e.g. full_name",
      "description": "value only: one sentence telling an extractor what to pull",
      "label": "placeholder only: a short English caption, e.g. Official seal"
    }
  ]
}"""

_PLAN_SYSTEM = """You classify the blocks of a scanned official document.

Every block's position is already decided, from the scan's own geometry. You are
not writing code and not choosing coordinates. You decide only which of three
roles each block has:

- `static` — printed chrome, identical on every copy of this document: headings,
  office names, field labels such as "Full Name:", legal boilerplate. Give its
  `text` translated into {language}. That string is baked into the layout, so it
  must read as finished {language} rather than as a gloss.
- `value` — what differs per person or per copy: names, dates, numbers, places,
  the answer that follows a label. Give a snake_case `field` and a `description`
  an extractor can act on, plus `text`: the value visible in the scan,
  translated. The text is used only to size the box and is never rendered.
- `placeholder` — a seal, stamp, photograph, signature, or thumbprint. Give a
  short English `label`. Imagery is never reproduced, only outlined.

Rules:
- One entry per block, for every block listed, in the order given. Do not invent
  a block_id and do not merge two blocks into one entry.
- A label and its value are separate blocks. "Full Name:" is static; the name
  beside it is a value.
- `field` names are unique across the document. Where a label repeats, qualify
  it: `father_name`, `mother_name`, `father_citizenship_no`.
- Prefer fewer values. Anything preprinted on the blank form is static.

Reply with this JSON object and nothing else:

{contract}"""


def _plan_block_lines(placed: list[Any]) -> str:
    """The numbered block list the planner classifies, one block per line."""
    lines = []
    for block in placed:
        box = ", ".join(f"{v:.0f}" for v in block.bbox)
        detail = f"alt={block.alt!r}" if block.kind == "Picture" else repr(block.text)
        lines.append(f"{block.block_id}  {block.kind}  bbox=[{box}]  {detail}")
    return "\n".join(lines)


def _field_name(raw: str, taken: set[str], index: int) -> str:
    """A unique snake_case identifier for a planned value field.

    The model is asked for snake_case and mostly obliges, but a stray space or
    capital would emit a layout that reads ``d['Full Name']`` while the schema
    says ``full_name`` — a mismatch that renders blank rather than failing.
    """
    slug = re.sub(r"[^a-z0-9]+", "_", (raw or "").strip().lower()).strip("_")
    if not slug or slug[0].isdigit():
        slug = f"field_{index}" if not slug else f"f_{slug}"
    candidate, n = slug, 2
    while candidate in taken:
        candidate, n = f"{slug}_{n}", n + 1
    taken.add(candidate)
    return candidate


def plan_blocks(
    placed: list[Any],
    source_image: Path,
    *,
    target_language: str = DEFAULT_LANGUAGE,
    verbose: bool = True,
) -> dict[str, dict[str, Any]]:
    """Classify each placed block as static text, an extractable value, or imagery.

    One structured model call, not the tool-use loop: every coordinate is
    already fixed by :mod:`document_builder.autolayout`, so there is nothing to
    write and nothing to look up. The model sees the block list and the scan
    together — the list alone loses which value belongs to which label, and the
    scan alone loses the block ids the plan has to be keyed by.

    Args:
        placed: Blocks from ``autolayout.place``, in reading order.
        source_image: The scan, attached so the model can see the layout it is
            labelling.
        target_language: Language code static text is translated into.
        verbose: Print the backend and a role tally.

    Returns:
        ``block_id -> {"role": ..., "text"/"field"/"description"/"label": ...}``,
        ready for ``autolayout.layout_source``. Blocks the model omitted are
        absent; ``autolayout`` renders those as static text rather than dropping
        them.

    Raises:
        RuntimeError: No backend key, or the reply held no usable JSON.
    """
    spec = language_spec(target_language)
    system_prompt = _PLAN_SYSTEM.format(language=spec.name, contract=_PLAN_CONTRACT)
    task = (
        f"Classify all {len(placed)} blocks below. Coordinates are given for "
        f"context only — they are already final.\n\n"
        f"{_plan_block_lines(placed)}"
    )
    blocks = [_text(task), _text("The scan those blocks came from:"), _image(source_image)]

    backend, client, model = _select_backend()
    if verbose:
        print(f"  planner: {backend} ({model}), {len(placed)} blocks -> {spec.name}")

    if backend == "anthropic":
        response = client.messages.create(
            model=model, max_tokens=16_000, system=system_prompt,
            messages=[{"role": "user", "content": _to_anthropic_blocks(blocks)}],
        )
        final = "\n".join(
            b.text for b in response.content if getattr(b, "type", None) == "text"
        ).strip()
    else:
        response = client.chat.completions.create(
            model=model, max_tokens=16_000,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": _to_openai_blocks(blocks)},
            ],
        )
        final = (response.choices[0].message.content or "").strip()

    return _parse_plan(final, placed)


def _parse_plan(final_text: str, placed: list[Any]) -> dict[str, dict[str, Any]]:
    """Turn the planner's reply into a plan keyed by block id.

    Every entry is checked against the blocks that were actually sent. A model
    that invents a block id, or answers with a role outside the vocabulary, is
    corrected here rather than emitting a layout entry for a box that does not
    exist.
    """
    parsed = _parse_json_object(final_text)
    entries = parsed.get("blocks")
    if not isinstance(entries, list) or not entries:
        raise RuntimeError(f"Planner returned no 'blocks' list:\n\n{final_text[:2000]}")

    known = {b.block_id: b for b in placed}
    plan: dict[str, dict[str, Any]] = {}
    taken: set[str] = set()

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        block_id = str(entry.get("block_id") or "")
        block = known.get(block_id)
        if block is None or block_id in plan:
            continue

        role = str(entry.get("role") or "").strip().lower()
        if role not in _PLAN_ROLES:
            role = "placeholder" if block.kind == "Picture" else "static"
        # A picture has no text to bake and a text block has no imagery to
        # outline, so a role that contradicts the block's own kind is a
        # misread. Correct it rather than emitting an empty box.
        if block.kind == "Picture":
            role = "placeholder"
        elif role == "placeholder":
            role = "static"

        if role == "placeholder":
            plan[block_id] = {
                "role": "placeholder",
                "label": str(entry.get("label") or block.alt or "Image").strip(),
            }
        elif role == "value":
            plan[block_id] = {
                "role": "value",
                "field": _field_name(str(entry.get("field") or ""), taken, index),
                "description": str(entry.get("description") or "").strip(),
                "text": str(entry.get("text") or block.text).strip(),
            }
        else:
            plan[block_id] = {
                "role": "static",
                # Falling back to the source string keeps the block on the page
                # in its original script, which is worth more than a gap.
                "text": str(entry.get("text") or block.text).strip() or block.text,
            }
    if not plan:
        raise RuntimeError(
            f"Planner matched none of the {len(placed)} block ids:\n\n{final_text[:2000]}"
        )
    return plan


def plan_to_schema(
    plan: dict[str, dict[str, Any]],
    document_type: str,
    *,
    title: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Build the extraction schema for the value fields *plan* names.

    Every value field lands in ``required``: ``build_data`` keeps only required
    keys, so a field that is merely a property extracts and then renders blank.
    """
    properties: dict[str, Any] = {}
    for entry in plan.values():
        if entry.get("role") != "value":
            continue
        name = entry.get("field")
        if not name or name in properties:
            continue
        properties[name] = {
            "type": "string",
            "description": entry.get("description") or f"The {name.replace('_', ' ')}.",
        }

    pretty = document_type.replace("_", " ").title()
    return {
        "type": "object",
        "title": title or pretty,
        "description": description or f"Fields extracted from a {pretty} document.",
        "properties": properties,
        "required": list(properties),
    }


def write_plan_schema(
    plan: dict[str, dict[str, Any]], document_type: str, *, path: Path | None = None
) -> Path:
    """Write :func:`plan_to_schema` output to the schema directory and return it."""
    target = path or (SCHEMA_DIR / f"{document_type}.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(plan_to_schema(plan, document_type), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return target


def build_from_geometry(
    source_image: Path,
    document_type: str,
    *,
    layout_target: Path,
    schema_target: Path,
    conversion_path: Path | None = None,
    target_language: str = DEFAULT_LANGUAGE,
    iteration: int = 1,
    verbose: bool = True,
) -> RepairResult | None:
    """Build a layout and schema from the scan's own block geometry.

    The geometry-first path: Datalab's ``/convert`` gives every block's bounding
    box, :mod:`document_builder.autolayout` scales those onto an A4 sheet, and
    the model is asked only what each block means. The agent never chooses a
    coordinate, so the first draft already has the source's aspect ratio and the
    relative placement of its text and pictures.

    Args:
        source_image: The scan to convert.
        document_type: Slug; names ``build_<document_type>``.
        layout_target: Where to write the layout module.
        schema_target: Where to write the extraction schema.
        conversion_path: A ``/convert`` JSON saved earlier. Given, no API call is
            made — this is how the path runs offline and how a re-run avoids
            paying for the same conversion twice.
        target_language: Language static text is baked in.
        iteration: Recorded on the result.
        verbose: Print each stage.

    Returns:
        A :class:`RepairResult`, or **None** when any stage fails. None is the
        signal to fall back to the agent-writes-everything path: no API key, a
        refused conversion, a page that segmented into nothing, a reply that did
        not parse, or a layout that failed the gate. A worse first draft beats a
        failed run, so nothing here raises.
    """
    # Imported here, not at module scope: the conversion module constructs a
    # Datalab client at import time, and ``architect`` is imported by callers
    # that never touch the geometry path and may have no key at all.
    try:
        from document_builder.autolayout import (
            blocks_from_conversion,
            layout_source,
            page_geometry,
            place,
        )
        from information_extraction.conversion import convert, load_conversion
    except Exception as e:  # noqa: BLE001 - any import failure means fall back
        if verbose:
            print(f"  geometry path unavailable ({e.__class__.__name__}: {e})")
        return None

    # Anything this function creates and then abandons has to go. ``layout.py``
    # is what makes a type discoverable, so a broken one left on disk turns a
    # fall-back into a permanently broken document type. Files that already
    # existed are left alone — a rebuild must not delete the layout in use.
    created: list[Path] = [p for p in (layout_target, schema_target) if not p.exists()]

    def _discard() -> None:
        for path in created:
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass

    try:
        if conversion_path is not None:
            conversion = load_conversion(conversion_path)
            if verbose:
                print(f"  conversion: {conversion_path} (cached)")
        else:
            if verbose:
                print(f"  conversion: /convert on {source_image.name}")
            conversion = convert(source_image)

        blocks = blocks_from_conversion(conversion)
        if not blocks:
            if verbose:
                print("  geometry path skipped: the conversion held no usable blocks")
            return None

        geometry = page_geometry(blocks)
        placed = place(blocks, geometry)
        if verbose:
            orientation = "landscape" if geometry.landscape else "portrait"
            print(
                f"  geometry: {len(placed)} blocks -> A4 {orientation} "
                f"{geometry.page_width}x{geometry.page_height}, scale {geometry.scale:.4f}"
            )

        plan = plan_blocks(
            placed, source_image, target_language=target_language, verbose=verbose
        )
        schema_path = write_plan_schema(plan, document_type, path=schema_target)
        ok_schema, schema_msg = validate_schema(schema_path)
        if not ok_schema:
            if verbose:
                print(f"  geometry path abandoned: {schema_msg}")
            _discard()
            return None

        layout_target.parent.mkdir(parents=True, exist_ok=True)
        layout_target.write_text(
            layout_source(placed, plan, document_type, geometry), encoding="utf-8"
        )
    except Exception as e:  # noqa: BLE001 - fall back rather than fail the run
        if verbose:
            print(f"  geometry path failed ({e.__class__.__name__}: {e})")
        _discard()
        return None

    roles = [entry.get("role") for entry in plan.values()]
    result = RepairResult(
        summary=(
            f"Built {layout_target.name} from the scan's own block geometry: "
            f"{len(placed)} blocks scaled by {geometry.scale:.4f} onto an A4 "
            f"{'landscape' if geometry.landscape else 'portrait'} sheet "
            f"({roles.count('static')} static, {roles.count('value')} value, "
            f"{roles.count('placeholder')} placeholder). "
            f"{schema_msg}"
        ),
        needs_reextraction=True,  # nothing has been extracted yet, by definition
        schema_path=schema_path,
        layout_path=layout_target,
        iteration=iteration,
        history=[
            {"tool": "(autolayout)", "input": {"source": str(source_image)},
             "result": f"{len(placed)} blocks placed"},
            {"tool": "(plan_blocks)", "input": {"language": target_language},
             "result": f"{len(plan)} blocks classified"},
        ],
    )

    ok, msg = validate_layout(layout_target, document_type, schema_path)
    result.history.append({"tool": "(validate_layout)", "input": {}, "result": msg})
    result.layout_valid = ok
    result.validation_message = msg
    if verbose:
        print(f"  validate_layout: {'OK' if ok else 'FAILED'} — {msg}")
    if not ok:
        # The gate is the whole point of generating deterministically: a layout
        # that does not build is worth less than the agent's attempt, so hand
        # the run back rather than promoting it.
        if verbose:
            print("  geometry path abandoned: falling back to the agent")
        _discard()
        return None

    result.promoted = promote_layout(document_type, layout_target)
    if verbose:
        print(f"  promoted: {layout_target.name} is now the live layout")
    return result


# ── Public entry point: generate from scratch ─────────────────────

def generate_resources(
    source_image: Path,
    document_type: str,
    *,
    user_notes: str | None = None,
    conversion_path: Path | None = None,
    target_language: str = DEFAULT_LANGUAGE,
    use_geometry: bool = True,
    max_tool_calls: int = MAX_TOOL_CALLS,
    verbose: bool = True,
) -> RepairResult:
    """Create a layout builder and extraction schema for an unseen document type.

    Two routes, tried in order.

    **Geometry first** (:func:`build_from_geometry`). Datalab's ``/convert``
    already knows where every block on the scan sits, so the layout is computed
    rather than invented and the model is asked only what each block means. This
    is the default because a coordinate the agent guessed is a coordinate the
    repair loop then spends iterations undoing.

    **The agent, writing both files itself.** The original route, and the
    fallback whenever the geometry route cannot finish — no Datalab key, a page
    that segmented into nothing, a plan that did not parse, a layout that failed
    the gate. It sees only the source scan and must infer the structure,
    imitating an existing builder.

    Args:
        source_image: The scan. Attached to every model call as an image.
        document_type: Slug, e.g. ``"laalpurja"``.
        user_notes: Free text steering the agent route.
        conversion_path: A ``/convert`` JSON saved earlier, so the geometry
            route can run without calling the API again.
        target_language: Language static text is baked in, on the geometry route.
        use_geometry: Set False to force the agent route.
        max_tool_calls: Budget for the agent route's tool loop.

    The returned ``needs_reextraction`` is always True: nothing has been
    extracted yet.
    """
    # Base names on both sides, for the same reason: an unseen type has no
    # original to protect, so the first schema written is the base schema and the
    # first layout written is the rollback original. Generating into
    # ``_patched.json`` / ``layout_1.py`` left the type standing on a sidecar with
    # no base underneath it.
    schema_target = SCHEMA_DIR / f"{document_type}.json"
    # ``layout.py``, not ``layout_1.py``: for an unseen type there is no original
    # yet, and the first layout written is it. Generating straight to
    # ``layout_1.py`` left the directory with no ``layout.py`` at all, so the type
    # had no rollback floor — a later dangling ``ACTIVE`` would resolve to nothing
    # and drop the type out of discovery entirely instead of degrading to a
    # working layout. Repairs still write ``layout_N.py`` beside this one.
    layout_target = BUILDER_DIR / document_type / "layout.py"

    if verbose:
        print(f"Architect (generate) — new document type '{document_type}'")

    if use_geometry:
        result = build_from_geometry(
            source_image,
            document_type,
            layout_target=layout_target,
            schema_target=schema_target,
            conversion_path=conversion_path,
            target_language=target_language,
            verbose=verbose,
        )
        if result is not None:
            return result
        if verbose:
            print("  falling back to the agent-written layout")

    notes_block = (
        f"\n## Notes from the user\n\n{user_notes.strip()}\n" if user_notes and user_notes.strip() else ""
    )

    task = f"""# Generation task

The document type `{document_type}` has no layout builder and no extraction schema.
Create both from the attached scan.

## Where to write

- Schema -> {schema_target}
- Layout -> {layout_target}

Use exactly these paths.

## Requirements

- The layout module must define `build_{document_type}(data: dict) -> Document`,
  importing components from `html_engine`.
- It must read only keys that appear in your schema's `required` list —
  `build_data()` discards everything else.
- Every value lookup must survive a missing key: render "" rather than "None".
- Attach `contenteditable="true"` and `data-field="<dotted.path>"` to each editable
  value, matching the convention in the existing builders. Repeating rows use an
  index segment, e.g. `plots.0.plot_no`.
- Seals, photos, and signatures are placeholder boxes, never reproduced imagery.
{notes_block}
## Now

Study an existing builder and its schema before writing anything. Then write the
schema, then the layout, then return the JSON object. Begin."""

    blocks: list[dict[str, Any]] = [
        _text(task),
        _text(f"SOURCE scan of the {document_type} document:"),
        _image(source_image),
    ]

    final_text, history = _run_agent(
        _build_system_prompt("generate"),
        blocks,
        max_tool_calls=max_tool_calls,
        verbose=verbose,
    )
    result = _result_from_contract(_parse_contract(final_text), history, iteration=1)
    result.needs_reextraction = True  # nothing has been extracted yet, by definition

    if result.layout_path is not None:
        ok, msg = validate_layout(
            result.layout_path, document_type, result.schema_path
        )
        result.history.append({"tool": "(validate_layout)", "input": {}, "result": msg})
        # Recording the verdict, not just printing it: ``run.py`` branches on
        # ``layout_valid`` to decide whether a generated type is ready. This
        # branch never set it, so the guard read None and a layout that failed
        # the gate was still announced as ready to use.
        result.layout_valid = ok
        result.validation_message = msg
        if verbose:
            print(f"  validate_layout: {'OK' if ok else 'FAILED'} — {msg}")
        if ok:
            result.promoted = promote_layout(document_type, result.layout_path)
            if verbose:
                print(f"  promoted: {result.layout_path.name} is now the live layout")
        else:
            result.summary += f"\n\n[VALIDATION FAILED] {msg}"
    if result.schema_path is None:
        result.summary += "\n\n[WARNING] No schema was written — extraction cannot run."
    return result


# ── CLI ───────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m agentic_controller.architect",
        description="Run the Architect Agent against a verification report, or "
                    "generate a layout and schema for a new document type.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    rep = sub.add_parser("repair", help="Repair from an existing VerificationReport.")
    rep.add_argument("document_type")
    rep.add_argument("source", type=Path, help="Source scan PNG.")
    rep.add_argument("rendered", type=Path, help="Rendered output PNG.")
    rep.add_argument(
        "--report", type=Path,
        help="VerificationReport JSON. Omit to run the verifier now.",
    )
    rep.add_argument("--concerns", help="Free-text user concerns (user-guided branch).")
    rep.add_argument("--iteration", type=int, default=1)

    gen = sub.add_parser("generate", help="Create layout + schema for a new document type.")
    gen.add_argument("document_type")
    gen.add_argument("source", type=Path, help="Source scan PNG.")
    gen.add_argument("--notes", help="Free-text guidance for the generator.")

    args = parser.parse_args(argv)

    if args.command == "generate":
        result = generate_resources(
            source_image=args.source,
            document_type=args.document_type,
            user_notes=args.notes,
        )
    else:
        if args.report:
            report = VerificationReport.model_validate_json(
                args.report.read_text(encoding="utf-8")
            )
        else:
            from agentic_controller.verifier import verify
            print("No --report given; running the verifier...")
            report = verify(args.source, args.rendered)
            print(f"  overall_match: {report.overall_match}")

        result = analyze_and_repair(
            report=report,
            source_image=args.source,
            rendered_image=args.rendered,
            document_type=args.document_type,
            current_schema_path=resolve_schema_path(args.document_type),
            current_layout_path=current_layout_path(args.document_type),
            user_concerns=args.concerns,
            iteration=args.iteration,
        )

    print("\n" + result.describe())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

