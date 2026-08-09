"""
Tests for ``architect.validate_layout`` — the gate that let the reported bug
through.

The gate used to only *import* the layout module. A function body does not
execute until it is called, so a layout whose ``build_*()`` raised passed the
gate and then crashed inside ``build_document()`` several stages later, where
the traceback no longer points at the layout. Every case below is one that the
import-only probe reported as OK.

Spawns a subprocess per case, so it is the slowest suite here.

    .venv/bin/python tests/test_layout_gate.py
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agentic_controller.architect import validate_layout  # noqa: E402

_WORKDIR: Path | None = None

_GOOD = '''
from html_engine import Document, Text

def build_letter(data):
    doc = Document("t")
    doc.add(Text(data.get("subject", "")))
    return doc
'''


def _layout(source: str, name: str = "probe_layout.py") -> Path:
    assert _WORKDIR is not None
    path = _WORKDIR / name
    path.write_text(source, encoding="utf-8")
    return path


def _schema(required: list[str]) -> Path:
    assert _WORKDIR is not None
    path = _WORKDIR / "probe_schema.json"
    path.write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {key: {"type": "string"} for key in required},
                "required": required,
            }
        ),
        encoding="utf-8",
    )
    return path


def test_good_layout_passes():
    ok, message = validate_layout(_layout(_GOOD), "letter", _schema(["subject"]))
    assert ok, message
    assert "renders" in message, message


def test_missing_file_is_reported():
    assert _WORKDIR is not None
    ok, message = validate_layout(_WORKDIR / "nope.py", "letter")
    assert not ok
    assert "not found" in message.lower(), message


def test_syntax_error_is_reported_with_a_line():
    ok, message = validate_layout(_layout("def build_letter(data:\n    pass\n"), "letter")
    assert not ok
    assert "SyntaxError" in message, message
    assert "line" in message, message


def test_missing_builder_function_is_caught():
    ok, message = validate_layout(_layout("def build_something_else(d):\n    pass\n"), "letter")
    assert not ok
    assert "build_letter" in message, message


def test_bad_keyword_inside_the_body_is_caught():
    """
    The original failure mode, in miniature: valid module, valid import, a bad
    keyword one level down inside the function.
    """
    source = _GOOD.replace(
        'doc.add(Text(data.get("subject", "")))',
        'doc.add(Text("x", nonexistent_kwarg="1"))',
    )
    ok, message = validate_layout(_layout(source), "letter")
    assert not ok
    assert "TypeError" in message, message


def test_unguarded_key_lookup_is_caught():
    """
    Blank probe data is the harsh case. A layout indexing a key the schema does
    not carry fails here, not on the one scan that happens to omit it.
    """
    source = _GOOD.replace('data.get("subject", "")', 'data["definitely_missing_key"]')
    ok, message = validate_layout(_layout(source), "letter", _schema(["subject"]))
    assert not ok
    assert "KeyError" in message, message


def test_builder_returning_a_non_document_is_caught():
    ok, message = validate_layout(
        _layout('def build_letter(data):\n    return "<html>not a Document</html>"\n'),
        "letter",
    )
    assert not ok, message


def test_unrecognized_css_property_still_passes():
    """
    A property outside the known list is a cosmetic gap, not a reason to fail a
    layout the agent just wrote. The engine warns; the gate does not block.
    """
    source = _GOOD.replace(
        "from html_engine import Document, Text",
        "from html_engine import Document, Style, Text",
    ).replace('Text(data.get("subject", ""))', 'Text("x", style=Style(fnot_size="12px"))')
    ok, message = validate_layout(_layout(source), "letter")
    assert ok, message


def test_schema_is_optional():
    """Without a schema the builder is probed with ``{}``."""
    ok, message = validate_layout(_layout(_GOOD), "letter", None)
    assert ok, message


def _run() -> int:
    global _WORKDIR
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = 0
    _WORKDIR = Path(tempfile.mkdtemp(prefix="layout_gate_"))
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
