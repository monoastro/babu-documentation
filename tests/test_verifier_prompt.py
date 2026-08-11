"""
Tests for the verification prompt's target language.

``agentic_controller/verifier.py`` tells a vision model which differences
between the scan and the render are intended. The largest of those is that the
render is translated, so the prompt has to name the language the document was
actually translated into. Judged against the wrong language, every correctly
translated value is reported as a data-accuracy failure and the repair loop
chases them forever.

No model is called here — the prompt is a pure function of the language spec.

    .venv/bin/python tests/test_verifier_prompt.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agentic_controller import verifier as vf  # noqa: E402


def test_the_prompt_names_the_target_language():
    assert "The rendered output is in Japanese" in vf.build_prompt("ja")
    assert "The rendered output is in English" in vf.build_prompt("en")


def test_each_language_carries_its_own_worked_examples():
    """Latin examples in a Japanese prompt would teach the wrong script."""
    japanese = vf.build_prompt("ja")
    assert "ウマ・デヴィ・チャウラガイ" in japanese
    assert "Uma Devi Chaulagai" not in japanese


def test_the_non_language_rules_are_shared():
    """Only rule 1 varies; placeholders, formatting, and colour do not."""
    for language in ("en", "ja"):
        prompt = vf.build_prompt(language)
        for fragment in (
            "VISUAL ELEMENTS",
            "FORMATTING",
            "HANDWRITTEN ELEMENTS",
            "COLOUR",
            "WHAT TO ACTUALLY CHECK",
            "SEVERITY GUIDE",
            "needs_human_review",
        ):
            assert fragment in prompt, (language, fragment)


def test_the_rules_stay_numbered_one_to_five():
    """``verification-rules.md`` mirrors this prompt rule by rule."""
    prompt = vf.build_prompt("ja")
    for number, name in enumerate(
        ["LANGUAGE", "VISUAL ELEMENTS", "FORMATTING", "HANDWRITTEN", "COLOUR"], start=1
    ):
        assert f"{number}. {name}" in prompt, (number, name)


def test_the_module_constant_is_the_english_prompt():
    """``SYSTEM_PROMPT`` is what ``verification-rules.md`` documents."""
    assert vf.SYSTEM_PROMPT == vf.build_prompt("en")


def test_an_unsupported_language_is_refused():
    try:
        vf.build_prompt("xx")
    except ValueError as exc:
        assert "xx" in str(exc)
    else:
        raise AssertionError("an unknown language code must raise")


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failed += 1
            print(f"FAIL {test.__name__}: {type(exc).__name__}: {exc}")
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
