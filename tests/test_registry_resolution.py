"""
Tests for ``document_builder/resolver.py`` — which layout is live, and which
document types exist.

These two questions used to be answered by hand-written import statements in
``registry.py``, and every case below is a way that arrangement broke. The
pointer went stale, so the repair loop rebuilt the layout it started from. The
pointer went dangling, and because the imports were eager and top-level, one
missing module took down all four document types at once.

The resolver takes ``builder_dir`` and ``schema_dir`` overrides, so each case
builds a throwaway tree in ``tempfile`` and never touches the real one.

    .venv/bin/python tests/test_registry_resolution.py
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from document_builder.resolver import (  # noqa: E402
    active_layout_name,
    active_layout_path,
    discover_document_types,
    latest_layout_path,
    load_builder,
    next_layout_path,
    promote_layout,
    resolve_schema_path,
)

_WORKDIR: Path | None = None
_counter = 0

_LAYOUT = '''
from html_engine import Document, Text

def build_{type}(data):
    doc = Document("{marker}")
    doc.add(Text("{marker}"))
    return doc
'''


def _tree() -> tuple[Path, Path]:
    """A fresh empty ``(builder_dir, schema_dir)`` pair.

    One per case: discovery reads the whole directory, so cases sharing a tree
    would see each other's document types.
    """
    global _counter
    assert _WORKDIR is not None
    _counter += 1
    root = _WORKDIR / f"case_{_counter}"
    builder_dir = root / "document_builder"
    schema_dir = root / "schemas"
    builder_dir.mkdir(parents=True)
    schema_dir.mkdir(parents=True)
    return builder_dir, schema_dir


def _add_type(
    builder_dir: Path,
    schema_dir: Path | None,
    document_type: str,
    *,
    layouts: dict[str, str] | None = None,
    active: str | None = None,
) -> Path:
    """Write a document type's directory: layouts, optional schema, optional ``ACTIVE``."""
    directory = builder_dir / document_type
    directory.mkdir(parents=True, exist_ok=True)
    for name, marker in (layouts or {"layout.py": "original"}).items():
        (directory / name).write_text(
            _LAYOUT.format(type=document_type, marker=marker), encoding="utf-8"
        )
    if active is not None:
        (directory / "ACTIVE").write_text(active, encoding="utf-8")
    if schema_dir is not None:
        (schema_dir / f"{document_type}.json").write_text(
            json.dumps({"type": "object", "properties": {}, "required": []}),
            encoding="utf-8",
        )
    return directory


# ── Which layout is live ──────────────────────────────────────────

def test_no_active_file_falls_back_to_layout_py():
    """A directory that never patched anything needs no bookkeeping."""
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter")
    path = active_layout_path("letter", builder_dir=builder_dir)
    assert path is not None and path.name == "layout.py", path


def test_active_file_selects_the_named_layout():
    builder_dir, schema_dir = _tree()
    _add_type(
        builder_dir,
        schema_dir,
        "letter",
        layouts={"layout.py": "original", "layout_2.py": "patched"},
        active="layout_2.py\n",
    )
    path = active_layout_path("letter", builder_dir=builder_dir)
    assert path is not None and path.name == "layout_2.py", path


def test_active_pointing_at_a_missing_file_falls_back():
    """
    A stale pointer should cost a stale render, not a crash. The eager import
    it replaced raised ``ModuleNotFoundError`` and took every other type with
    it.
    """
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter", active="layout_9.py\n")
    path = active_layout_path("letter", builder_dir=builder_dir)
    assert path is not None and path.name == "layout.py", path


def test_blank_active_file_falls_back():
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter", active="  \n")
    path = active_layout_path("letter", builder_dir=builder_dir)
    assert path is not None and path.name == "layout.py", path


def test_active_naming_a_traversal_path_is_rejected():
    """
    ``ACTIVE`` is written by the agent, so its contents are untrusted input.
    Anything that is not a bare ``layout*.py`` filename must not be loaded.
    """
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter")
    (builder_dir / "elsewhere.py").write_text("SENTINEL = 1\n", encoding="utf-8")

    for hostile in ("../elsewhere.py", "/etc/passwd", "..\\layout.py",
                    "subdir/layout.py", "layout.py; rm -rf /"):
        (builder_dir / "letter" / "ACTIVE").write_text(hostile, encoding="utf-8")
        path = active_layout_path("letter", builder_dir=builder_dir)
        assert path is not None, hostile
        assert path.name == "layout.py", f"{hostile!r} resolved to {path}"
        assert path.parent == builder_dir / "letter", f"{hostile!r} escaped to {path}"


def test_unknown_type_resolves_to_none():
    builder_dir, _ = _tree()
    assert active_layout_path("nonexistent", builder_dir=builder_dir) is None


def test_active_layout_name_is_display_safe():
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter")
    assert active_layout_name("letter", builder_dir=builder_dir) == "layout.py"
    assert active_layout_name("nonexistent", builder_dir=builder_dir) == "(none)"


# ── Promotion ─────────────────────────────────────────────────────

def test_promote_layout_round_trips():
    builder_dir, schema_dir = _tree()
    directory = _add_type(
        builder_dir, schema_dir, "letter",
        layouts={"layout.py": "original", "layout_1.py": "patched"},
    )
    pointer = promote_layout("letter", directory / "layout_1.py", builder_dir=builder_dir)
    assert pointer.read_text(encoding="utf-8").strip() == "layout_1.py"

    path = active_layout_path("letter", builder_dir=builder_dir)
    assert path is not None and path.name == "layout_1.py", path

    # And back — rollback is one line, which is the whole point of a pointer.
    promote_layout("letter", directory / "layout.py", builder_dir=builder_dir)
    path = active_layout_path("letter", builder_dir=builder_dir)
    assert path is not None and path.name == "layout.py", path


def test_promotion_never_touches_layout_py():
    """
    Manual promotion copied the patch over ``layout.py`` and destroyed the
    rollback original. Promotion writes a pointer and nothing else.
    """
    builder_dir, schema_dir = _tree()
    directory = _add_type(
        builder_dir, schema_dir, "letter",
        layouts={"layout.py": "original", "layout_1.py": "patched"},
    )
    before = (directory / "layout.py").read_bytes()
    promote_layout("letter", directory / "layout_1.py", builder_dir=builder_dir)
    assert (directory / "layout.py").read_bytes() == before


def test_promoting_a_non_layout_name_raises():
    builder_dir, schema_dir = _tree()
    directory = _add_type(builder_dir, schema_dir, "letter")
    (directory / "helper.py").write_text("x = 1\n", encoding="utf-8")
    try:
        promote_layout("letter", directory / "helper.py", builder_dir=builder_dir)
    except ValueError:
        pass
    else:
        raise AssertionError("promoted a file that is not a layout")


def test_promoting_a_missing_layout_raises():
    builder_dir, schema_dir = _tree()
    directory = _add_type(builder_dir, schema_dir, "letter")
    try:
        promote_layout("letter", directory / "layout_7.py", builder_dir=builder_dir)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("promoted a layout that does not exist")


# ── Version numbering ─────────────────────────────────────────────

def test_next_layout_path_never_collides():
    builder_dir, schema_dir = _tree()
    directory = _add_type(builder_dir, schema_dir, "letter")
    for expected in ("layout_1.py", "layout_2.py", "layout_3.py"):
        path = next_layout_path("letter", builder_dir=builder_dir)
        assert path.name == expected, path
        assert not path.exists()
        path.write_text("# placeholder\n", encoding="utf-8")
    assert (directory / "layout.py").is_file(), "the original must survive"


def test_latest_is_not_active():
    """
    The newest layout is not necessarily the live one. An unpromoted
    ``layout_3.py`` sits on disk while ``ACTIVE`` still names ``layout_1.py`` —
    which is exactly what a failed gate leaves behind.
    """
    builder_dir, schema_dir = _tree()
    _add_type(
        builder_dir, schema_dir, "letter",
        layouts={"layout.py": "o", "layout_1.py": "a", "layout_3.py": "b"},
        active="layout_1.py\n",
    )
    latest = latest_layout_path("letter", builder_dir=builder_dir)
    active = active_layout_path("letter", builder_dir=builder_dir)
    assert latest is not None and latest.name == "layout_3.py", latest
    assert active is not None and active.name == "layout_1.py", active


# ── Discovery ─────────────────────────────────────────────────────

def test_discovery_finds_a_new_type_with_no_code_edit():
    """A generated type is usable on the next run. That is the whole feature."""
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter")
    assert discover_document_types(builder_dir=builder_dir, schema_dir=schema_dir) == ["letter"]

    _add_type(builder_dir, schema_dir, "tax_clearance")
    found = discover_document_types(builder_dir=builder_dir, schema_dir=schema_dir)
    assert found == ["letter", "tax_clearance"], found


def test_discovery_skips_a_layout_with_no_schema():
    """
    Without a schema the pipeline has nothing to extract with, so offering the
    type in ``--type`` would only produce a confusing failure later.
    """
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter")
    _add_type(builder_dir, None, "orphan")
    found = discover_document_types(builder_dir=builder_dir, schema_dir=schema_dir)
    assert found == ["letter"], found


def test_discovery_skips_non_identifier_directories():
    """A builder name becomes part of ``build_<type>``, so it must be an identifier."""
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter")
    for junk in ("__pycache__", "tax-clearance", "_scratch"):
        _add_type(builder_dir, schema_dir, junk)
    found = discover_document_types(builder_dir=builder_dir, schema_dir=schema_dir)
    assert found == ["letter"], found


def test_discovery_ignores_loose_files():
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter")
    (builder_dir / "registry.py").write_text("# not a document type\n", encoding="utf-8")
    found = discover_document_types(builder_dir=builder_dir, schema_dir=schema_dir)
    assert found == ["letter"], found


# ── Schema resolution ─────────────────────────────────────────────

def test_schema_resolution_prefers_the_patched_sidecar():
    """
    The registry hard-coded ``<doc>.json`` while the agent wrote
    ``<doc>_patched.json``, so a schema repair re-extracted against the
    unpatched base and looked like a silent no-op.
    """
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter")
    assert resolve_schema_path("letter", schema_dir=schema_dir).name == "letter.json"

    (schema_dir / "letter_patched.json").write_text("{}", encoding="utf-8")
    assert resolve_schema_path("letter", schema_dir=schema_dir).name == "letter_patched.json"


# ── Loading ───────────────────────────────────────────────────────

def test_load_builder_returns_the_active_layout():
    builder_dir, schema_dir = _tree()
    _add_type(
        builder_dir, schema_dir, "letter",
        layouts={"layout.py": "original", "layout_2.py": "patched"},
        active="layout_2.py\n",
    )
    doc = load_builder("letter", builder_dir=builder_dir)({})
    assert "patched" in doc.render(), "loaded the wrong layout"


def test_promotion_takes_effect_inside_one_process():
    """
    The mid-run promotion the whole mechanism exists to allow. A module-name
    import would serve the first-loaded layout from ``sys.modules`` forever, so
    the repair loop would keep rebuilding its own input.
    """
    builder_dir, schema_dir = _tree()
    directory = _add_type(
        builder_dir, schema_dir, "letter",
        layouts={"layout.py": "original", "layout_1.py": "patched"},
    )
    assert "original" in load_builder("letter", builder_dir=builder_dir)({}).render()

    promote_layout("letter", directory / "layout_1.py", builder_dir=builder_dir)
    assert "patched" in load_builder("letter", builder_dir=builder_dir)({}).render()

    promote_layout("letter", directory / "layout.py", builder_dir=builder_dir)
    assert "original" in load_builder("letter", builder_dir=builder_dir)({}).render()


def test_a_broken_layout_does_not_stop_another_type():
    """
    The eager top-level imports made one bad layout unimportable for all four
    types. Resolution is per-entry now, so the blast radius is one type.
    """
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter")
    _add_type(builder_dir, schema_dir, "broken")
    (builder_dir / "broken" / "layout.py").write_text(
        "this is not valid python <<<\n", encoding="utf-8"
    )

    found = discover_document_types(builder_dir=builder_dir, schema_dir=schema_dir)
    assert found == ["broken", "letter"], found

    try:
        load_builder("broken", builder_dir=builder_dir)
    except SyntaxError:
        pass
    else:
        raise AssertionError("a broken layout loaded without raising")

    # The point: the healthy type still builds.
    assert "original" in load_builder("letter", builder_dir=builder_dir)({}).render()


def test_missing_builder_function_is_reported():
    builder_dir, schema_dir = _tree()
    _add_type(builder_dir, schema_dir, "letter")
    (builder_dir / "letter" / "layout.py").write_text(
        "def build_something_else(data):\n    return None\n", encoding="utf-8"
    )
    try:
        load_builder("letter", builder_dir=builder_dir)
    except AttributeError as exc:
        assert "build_letter" in str(exc), exc
    else:
        raise AssertionError("a layout with no builder loaded without raising")


def test_load_builder_on_an_unknown_type_raises():
    builder_dir, _ = _tree()
    try:
        load_builder("nonexistent", builder_dir=builder_dir)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("loaded a type that does not exist")


# ── The registry facade ───────────────────────────────────────────

def test_registry_exposes_the_real_project():
    """
    ``DOCUMENTS`` resolves against the real tree, so this asserts on shape
    rather than on a fixed list — adding a document type must not fail a test.
    """
    from document_builder.registry import DOCUMENTS

    types = sorted(DOCUMENTS)
    assert types, "the registry discovered no document types"
    assert "citizenship_back" in types, types

    entry = DOCUMENTS["citizenship_back"]
    assert entry["schema"].is_file(), entry["schema"]
    assert entry["layout"].name.startswith("layout"), entry["layout"]
    assert callable(entry["builder"])

    assert "citizenship_back" in DOCUMENTS
    assert "no_such_type" not in DOCUMENTS
    assert len(DOCUMENTS) == len(types)

    try:
        DOCUMENTS["no_such_type"]
    except KeyError:
        pass
    else:
        raise AssertionError("the registry served an unknown type")


def test_registry_iteration_does_not_import_layouts():
    """
    Reading every schema must not execute every layout, or one broken layout
    would again take the whole registry with it.
    """
    from document_builder.registry import DOCUMENTS

    before = set(sys.modules)
    for _type, config in DOCUMENTS.items():
        assert config["schema"].is_file()
    new_layouts = [m for m in set(sys.modules) - before if m.startswith("_babu_layout_")]
    assert not new_layouts, new_layouts


def _run() -> int:
    global _WORKDIR
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = 0
    _WORKDIR = Path(tempfile.mkdtemp(prefix="registry_resolution_"))
    sys.path.insert(0, str(_WORKDIR))
    try:
        for test in tests:
            try:
                test()
            except Exception as exc:
                failures += 1
                print(f"FAIL {test.__name__}: {type(exc).__name__}: {exc}")
            else:
                print(f"ok   {test.__name__}")
    finally:
        shutil.rmtree(_WORKDIR, ignore_errors=True)
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(_run())
