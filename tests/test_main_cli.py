"""
Tests for the manual entry point.

``main.py`` is the hand-driven counterpart to ``python -m
agentic_controller.run``: same builders, same engine, no vision verifier and no
repair loop. The contract worth protecting is that ``--data`` and ``--blank``
never reach the OCR path, so iterating on a layout costs nothing.

    .venv/bin/python tests/test_main_cli.py
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import main as cli  # noqa: E402
from document_builder.registry import DOCUMENTS  # noqa: E402

_WORKDIR: Path | None = None


def _out(name: str) -> Path:
    assert _WORKDIR is not None
    return _WORKDIR / name


def test_blank_builds_every_registered_type():
    for document_type in sorted(DOCUMENTS):
        target = _out(f"{document_type}.html")
        code = cli.main(["--type", document_type, "--blank", "--output", str(target)])
        assert code == 0, document_type
        html = target.read_text(encoding="utf-8")
        assert html.startswith("<!DOCTYPE html>"), document_type


def test_data_path_skips_ocr():
    """
    Proven by breaking the OCR import: if the extractor were reached, this
    would raise instead of returning 0.
    """
    data_file = _out("letter.json")
    data_file.write_text(
        json.dumps({"subject": "Test subject", "signed_name": "Ram Bahadur"}),
        encoding="utf-8",
    )
    sentinel = "information_extraction.extractor"
    saved = sys.modules.get(sentinel)
    sys.modules[sentinel] = None  # any attribute access on this raises
    try:
        code = cli.main(
            ["--type", "letter", "--data", str(data_file), "--output", str(_out("d.html"))]
        )
    finally:
        if saved is None:
            sys.modules.pop(sentinel, None)
        else:
            sys.modules[sentinel] = saved
    assert code == 0
    assert "Test subject" in _out("d.html").read_text(encoding="utf-8")


def test_data_path_converts_null_values_to_empty_strings():
    data_file = _out("letter-null.json")
    data_file.write_text(
        json.dumps({"subject": None, "signed_name": "Ram Bahadur"}), encoding="utf-8"
    )

    code = cli.main(
        ["--type", "letter", "--data", str(data_file), "--output", str(_out("null.html"))]
    )

    assert code == 0
    html = _out("null.html").read_text(encoding="utf-8")
    assert "None" not in html
    assert "Ram Bahadur" in html


def test_blank_fills_every_required_schema_key():
    schema_path = Path(DOCUMENTS["letter"]["schema"])
    required = json.loads(schema_path.read_text(encoding="utf-8"))["required"]
    blank = cli._blank_data("letter")
    assert set(blank) == set(required)
    assert set(blank.values()) == {""}


def test_exactly_one_data_source_is_required():
    for argv in [
        ["--type", "letter"],  # none
        ["--type", "letter", "--blank", "--data", "x.json"],  # two
    ]:
        try:
            cli.main(argv)
        except SystemExit as exc:
            assert exc.code == 2, argv
        else:
            raise AssertionError(f"{argv} was accepted")


def test_missing_data_file_errors_before_building():
    try:
        cli.main(["--type", "letter", "--data", str(_out("absent.json"))])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("a missing --data file was accepted")


def test_strict_turns_a_css_typo_into_a_failure():
    """
    The engine warns on an unrecognized property rather than raising, so
    ``--strict`` is how a run gets told to stop on one.
    """
    import warnings

    from html_engine import Style, StyleWarning

    with warnings.catch_warnings():
        warnings.simplefilter("error", StyleWarning)
        try:
            Style(fnot_size="12px")
        except StyleWarning:
            return
    raise AssertionError("--strict's mechanism does not raise")


def _run() -> int:
    global _WORKDIR
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = 0
    _WORKDIR = Path(tempfile.mkdtemp(prefix="main_cli_"))
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
