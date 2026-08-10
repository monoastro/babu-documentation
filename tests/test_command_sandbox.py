"""
Tests for the ``execute_command`` sandbox in the Architect Agent.

These exist because the sandbox was not one. ``python -c`` sat on the command
allowlist — arbitrary code execution — and the allowlist was a prefix check
against a string handed to ``shell=True``. One agent run deleted
``document_builder/citizenship_back/layout.py`` and truncated
``information_extraction/schemas/citizenship_back.json`` to zero bytes, both of
which ``_write_allowed()`` refuses through the ``write_file`` tool. The docs
promised "originals are never overwritten"; nothing enforced it.

Every test below is a route that previously reached the filesystem.

Run directly, no pytest needed:

    .venv/bin/python tests/test_command_sandbox.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agentic_controller.architect import (  # noqa: E402
    BUILDER_DIR,
    PROJECT_ROOT,
    SCHEMA_DIR,
    _ALLOWED_COMMAND_PREFIXES,
    _protected_originals,
    _restore_changed,
    _snapshot,
    _tool_execute_command,
    _write_allowed,
)

SCHEMA = PROJECT_ROOT / "information_extraction" / "schemas" / "citizenship_back.json"
LAYOUT = PROJECT_ROOT / "document_builder" / "citizenship_back" / "layout.py"


def _refused(cmd: str) -> str:
    out = _tool_execute_command(cmd)
    assert out.startswith("Refused:"), f"{cmd!r} was not refused: {out[:200]}"
    return out


def test_python_dash_c_is_off_the_allowlist():
    # The exact hole. `python -c` is a general-purpose interpreter; an allowlist
    # containing one is not an allowlist.
    assert "python -c" not in _ALLOWED_COMMAND_PREFIXES


def test_python_dash_c_is_refused():
    _refused("python -c \"import os; os.remove('x')\"")


def test_redirection_cannot_truncate_a_file():
    # `cat x > schema.json` passed the old prefix check as a "cat" command while
    # destroying the target. This is how the schema reached zero bytes.
    before = SCHEMA.read_bytes() if SCHEMA.exists() else None
    out = _refused("cat README.md > information_extraction/schemas/citizenship_back.json")
    assert ">" in out
    after = SCHEMA.read_bytes() if SCHEMA.exists() else None
    assert after == before, "redirection modified a protected schema"


def test_chaining_cannot_smuggle_a_second_command():
    for cmd in (
        "ls; rm -rf document_builder",
        "ls && rm document_builder/citizenship_back/layout.py",
        "wc -l README.md | tee /tmp/x",
    ):
        _refused(cmd)


def test_command_substitution_is_refused():
    _refused("cat $(find . -name layout.py)")
    _refused("echo `whoami`")


def test_newline_cannot_hide_a_second_line():
    # A prefix check only ever describes the first line.
    _refused("ls\nrm -rf document_builder")


def test_allowlisted_command_still_runs():
    out = _tool_execute_command("wc -c README.md")
    assert not out.startswith("Refused:"), out
    assert "README.md" in out, out


def test_arguments_survive_shlex_splitting():
    # Dropping shell=True must not break ordinary quoted arguments.
    out = _tool_execute_command('grep -c "def " agentic_controller/architect.py')
    assert not out.startswith("Refused:"), out
    assert out.strip().isdigit(), out


def test_non_allowlisted_binary_is_refused():
    _refused("rm -rf /")
    _refused("git checkout .")
    _refused("pip install requests")


def test_protected_originals_cover_layouts_and_base_schemas():
    protected = set(_protected_originals())
    assert LAYOUT in protected, "layout.py must be protected"
    assert SCHEMA in protected, "a base schema must be protected"

    patched = [p for p in protected if p.stem.endswith("_patched")]
    assert not patched, f"patched sidecars are the agent's workspace, not originals: {patched}"

    numbered = [p for p in protected if p.name.startswith("layout_")]
    assert not numbered, f"layout_N.py is a repair iteration, not an original: {numbered}"


# ── _write_allowed: protect what exists, allow what does not ──────

def test_write_refuses_an_existing_layout_py():
    """The invariant the docs promise: an original that exists is never a target."""
    ok, message = _write_allowed(LAYOUT)
    assert not ok, "layout.py is the rollback original and must not be writable"
    assert "layout_N.py" in message, message


def test_write_refuses_an_existing_base_schema():
    ok, message = _write_allowed(SCHEMA)
    assert not ok, "a base schema must not be writable"
    assert "_patched" in message, message


def test_write_allows_layout_py_for_a_brand_new_type():
    """
    A type with no directory yet has no original to destroy, and the first
    layout written *is* the original. Refusing it unconditionally is what left
    the generated types as a bare ``layout_1.py`` with no rollback floor: a
    later dangling ``ACTIVE`` then resolved to nothing and dropped the type out
    of discovery altogether.
    """
    target = BUILDER_DIR / "definitely_not_a_real_type_xyz" / "layout.py"
    assert not target.exists(), "test assumes this type does not exist"
    ok, message = _write_allowed(target)
    assert ok, message


def test_write_allows_a_base_schema_that_does_not_exist_yet():
    target = SCHEMA_DIR / "definitely_not_a_real_type_xyz.json"
    assert not target.exists(), "test assumes this schema does not exist"
    ok, message = _write_allowed(target)
    assert ok, message


def test_write_still_refuses_paths_outside_the_writable_trees():
    for outside in (PROJECT_ROOT / "main.py",
                    PROJECT_ROOT / "html_engine" / "document.py",
                    Path("/etc/passwd")):
        ok, message = _write_allowed(outside)
        assert not ok, f"{outside} must not be writable"
        assert "outside the writable trees" in message, message


def test_write_refuses_non_python_non_json():
    ok, message = _write_allowed(BUILDER_DIR / "letter" / "notes.txt")
    assert not ok
    assert ".txt" in message, message


def test_guard_restores_a_modified_original():
    # Simulate a command that slipped through and edited an original.
    original = LAYOUT.read_bytes()
    before = _snapshot([LAYOUT])
    try:
        LAYOUT.write_bytes(b"# clobbered\n")
        restored = _restore_changed(before)
        assert restored, "the guard did not report a restore"
        assert LAYOUT.read_bytes() == original, "the guard did not restore the content"
    finally:
        LAYOUT.write_bytes(original)


def test_guard_restores_a_deleted_original():
    original = LAYOUT.read_bytes()
    before = _snapshot([LAYOUT])
    try:
        LAYOUT.unlink()
        restored = _restore_changed(before)
        assert restored, "the guard did not report a restore"
        assert LAYOUT.exists(), "the guard did not recreate a deleted original"
        assert LAYOUT.read_bytes() == original
    finally:
        LAYOUT.write_bytes(original)


def test_guard_leaves_untouched_originals_alone():
    before = _snapshot(_protected_originals())
    assert _restore_changed(before) == [], "a no-op run should restore nothing"


def _run() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures += 1
            print(f"FAIL {test.__name__}: {type(exc).__name__}: {exc}")
        else:
            print(f"ok   {test.__name__}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(_run())
