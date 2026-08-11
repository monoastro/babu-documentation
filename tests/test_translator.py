"""
Tests for the translation stage.

``information_extraction/translator.py`` sits between extraction and the layout
builder, so a mistake here is a mistake printed onto a document. Everything
below runs offline: the model call is stubbed, because what is worth protecting
is not the model's word choice but the code around it — which values are sent,
which are refused, how nested structures survive the trip, and what happens
when the call fails.

    .venv/bin/python tests/test_translator.py
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from information_extraction import translator as tr  # noqa: E402
from information_extraction.languages import language_spec  # noqa: E402


# ── Stubbing the model ────────────────────────────────────────────

class _Recorder:
    """Stands in for ``_translate_batch`` and remembers what it was asked."""

    def __init__(self, reply: dict[str, str] | None = None, raises: str | None = None):
        self.reply = reply
        self.raises = raises
        self.calls: list[dict] = []

    def __call__(self, values, *, prose, model, spec):
        self.calls.append(
            {"values": dict(values), "prose": prose, "model": model, "spec": spec}
        )
        if self.raises:
            raise RuntimeError(self.raises)
        if self.reply is not None:
            return dict(self.reply)
        # Default: mark every value so a translated string is recognisable.
        return {k: f"EN::{v}" for k, v in values.items()}

    @property
    def sent(self) -> list[str]:
        """Every distinct value handed to the model, across all calls."""
        return [v for call in self.calls for v in call["values"].values()]


def _run(data, recorder=None, **kwargs):
    """Translate ``data`` with the model call stubbed and the cache disabled."""
    recorder = recorder or _Recorder()
    original = tr._translate_batch
    tr._translate_batch = recorder
    try:
        kwargs.setdefault("use_cache", False)
        kwargs.setdefault("model", "test-model")
        return tr.translate_data(data, **kwargs), recorder
    finally:
        tr._translate_batch = original


# ── What gets sent, and what does not ─────────────────────────────

def test_devanagari_values_are_sent():
    result, rec = _run({"owner_name": "उमा देवी"})
    assert rec.sent == ["उमा देवी"], rec.sent
    assert result.data["owner_name"] == "EN::उमा देवी"


def test_sentinel_values_are_never_sent():
    """
    ``present``/``absent`` are an OCR contract, not content: a layout reads them
    to decide whether to draw a thumb-impression box at all. Rewording one
    removes an element from the page.
    """
    data = {
        "right_thumb_impression": "present",
        "left_thumb_impression": "absent",
        "issuing_officer_signature": "unreadable signature",
    }
    result, rec = _run(data)
    assert rec.calls == [], rec.calls
    assert result.data == data


def test_english_values_are_not_sent():
    data = {"sex": "Male", "citizenship_no": "29-01-78-03898", "full_name": "JENISH PANT"}
    result, rec = _run(data)
    assert rec.calls == [], rec.calls
    assert result.data == data


def test_empty_and_whitespace_are_not_sent():
    result, rec = _run({"doc_id": "", "note": "   "})
    assert rec.calls == [], rec.calls


def test_prose_keys_go_in_a_separate_call():
    """
    A sentence and a field label want different instructions, so they are
    batched separately and the prose batch carries the prose note.
    """
    result, rec = _run({"remarks": "यो प्रमाणपत्र", "owner_name": "उमा देवी"})
    kinds = sorted(call["prose"] for call in rec.calls)
    assert kinds == [False, True], kinds


def test_duplicate_values_are_sent_once():
    """A district repeated down a table is one string, not twenty."""
    data = {"a": "काठमाण्डौ", "b": "काठमाण्डौ", "c": "काठमाण्डौ"}
    result, rec = _run(data)
    assert len(rec.sent) == 1, rec.sent
    assert set(result.data.values()) == {"EN::काठमाण्डौ"}


# ── Local conversions, no model involved ──────────────────────────

def test_bs_dates_are_converted_locally():
    result, rec = _run({"issue_date": "२०४९/०३/०९"})
    assert rec.calls == [], "a date must never reach the model"
    assert result.data["issue_date"] == "1992-06-23", result.data


def test_an_unparseable_bs_date_is_left_alone():
    """A half-converted date prints a year that looks Gregorian and is not."""
    assert tr.bs_to_ad("not a date") == "not a date"
    assert tr.bs_to_ad("१९००/०१/०१") == "१९००/०१/०१"  # outside the supported range


def test_devanagari_digits_become_ascii_without_a_call():
    result, rec = _run({"owner_ward": "८"})
    assert rec.calls == [], rec.calls
    assert result.data["owner_ward"] == "8"


# ── Bilingual field pairs ─────────────────────────────────────────

def test_a_bilingual_title_keeps_its_nepali_half():
    """
    The SEE certificate prints ``certificate_title_np`` on one line and
    ``certificate_title_en`` on the next. Translating the first makes the
    document say "Certificate" twice, which is a page change, not a wording
    change.
    """
    data = {"certificate_title_np": "प्रमाण-पत्र", "certificate_title_en": "Certificate"}
    result, rec = _run(data)
    assert rec.calls == [], rec.calls
    assert result.data == data


def test_a_lone_np_field_is_still_translated():
    """Without the English sibling, that value is the only one on the page."""
    result, rec = _run({"heading_np": "प्रमाण-पत्र"})
    assert rec.sent == ["प्रमाण-पत्र"], rec.sent
    assert result.data["heading_np"] == "EN::प्रमाण-पत्र"


def test_a_bs_date_printed_beside_its_ad_twin_is_left_alone():
    data = {"date_of_birth_bs": "२०६४-०२-१७", "date_of_birth_ad": "2007-05-31"}
    result, _ = _run(data)
    assert result.data["date_of_birth_bs"] == "२०६४-०२-१७", result.data


def test_a_bs_date_with_no_twin_still_converts():
    result, _ = _run({"issue_date_bs": "२०४९/०३/०९"})
    assert result.data["issue_date_bs"] == "1992-06-23"


# ── Structure ─────────────────────────────────────────────────────

def test_nested_lists_of_dicts_are_walked():
    """A laalpurja's ``plots`` is a list of dicts; every row must be reached."""
    data = {"plots": [{"vdc": "नाङ्गलेभारे"}, {"vdc": "साखु"}]}
    result, rec = _run(data)
    assert sorted(rec.sent) == sorted(["नाङ्गलेभारे", "साखु"]), rec.sent
    assert result.data["plots"][0]["vdc"] == "EN::नाङ्गलेभारे"
    assert result.data["plots"][1]["vdc"] == "EN::साखु"
    assert len(result.data["plots"]) == 2


def test_extractor_metadata_is_never_translated():
    """
    ``<field>_meta`` and ``<field>_citations`` are provenance the extractor
    attaches. They are never rendered, and their prose would otherwise be
    translated at full cost.
    """
    meta = {"extraction_status": "EXTRACTED", "verification": {"feedback": "Plot number is ५५५."}}
    data = {"plots": [{"plot_no": "५५५", "plot_no_citations": ["/page/0"], "plot_no_meta": meta}]}
    result, rec = _run(data)
    assert "Plot number is ५५५." not in rec.sent, rec.sent
    row = result.data["plots"][0]
    assert row["plot_no_meta"] == meta
    assert row["plot_no_citations"] == ["/page/0"]


def test_non_string_leaves_survive():
    data = {"count": 3, "ok": True, "missing": None, "ratio": 1.5}
    result, _ = _run(data)
    assert result.data == data


def test_originals_are_recorded_for_everything_changed():
    data = {"owner_name": "उमा देवी", "sex": "Male"}
    result, _ = _run(data)
    assert result.original == {"owner_name": "उमा देवी"}, result.original


# ── Failure is reported, not raised ───────────────────────────────

def test_a_failed_call_returns_the_original_data():
    """
    A document rendered in Devanagari beats no document at all, so a failed
    translation is surfaced on the result rather than raised.
    """
    data = {"owner_name": "उमा देवी"}
    result, _ = _run(data, _Recorder(raises="no API key"))
    assert result.error is not None
    assert "no API key" in result.error
    assert result.data == data
    assert "translation skipped" in result.describe()


def test_local_conversions_survive_a_failed_call():
    """The date does not depend on the model, so it must convert anyway."""
    data = {"issue_date": "२०४९/०३/०९", "owner_name": "उमा देवी"}
    result, _ = _run(data, _Recorder(raises="boom"))
    assert result.data["issue_date"] == "1992-06-23"
    assert result.data["owner_name"] == "उमा देवी"


def test_a_partial_reply_keeps_the_missing_originals():
    """Keys the model drops fall back to their source value, not to empty."""
    data = {"a": "उमा देवी", "b": "काठमाण्डौ"}
    recorder = _Recorder(reply={"v0": "Uma Devi"})  # v1 omitted
    result, _ = _run(data, recorder)
    values = set(result.data.values())
    assert "Uma Devi" in values, values
    assert "" not in values, values
    assert len(values) == 2


def test_an_unchanged_reply_is_not_counted_as_a_translation():
    data = {"a": "उमा देवी"}
    result, _ = _run(data, _Recorder(reply={"v0": "उमा देवी"}))
    assert result.translated == 0, result.describe()
    assert result.data == data


# ── Cache ─────────────────────────────────────────────────────────

def test_the_cache_spares_the_second_call():
    """The repair loop re-runs extraction each iteration; it should not re-pay."""
    saved_path = tr.CACHE_PATH
    with tempfile.TemporaryDirectory() as tmp:
        tr.CACHE_PATH = Path(tmp) / "cache.json"
        try:
            data = {"owner_name": "उमा देवी"}
            first, rec1 = _run(data, use_cache=True)
            second, rec2 = _run(data, use_cache=True)
            assert rec1.calls, "the first run must call the model"
            assert rec2.calls == [], "the second run must be served from cache"
            assert first.data == second.data
        finally:
            tr.CACHE_PATH = saved_path


def test_the_cache_is_keyed_on_the_model():
    saved_path = tr.CACHE_PATH
    with tempfile.TemporaryDirectory() as tmp:
        tr.CACHE_PATH = Path(tmp) / "cache.json"
        try:
            data = {"owner_name": "उमा देवी"}
            _run(data, use_cache=True, model="model-a")
            _, rec = _run(data, use_cache=True, model="model-b")
            assert rec.calls, "a different model must not reuse the entry"
        finally:
            tr.CACHE_PATH = saved_path


def test_an_unwritable_cache_does_not_fail_the_run():
    saved_path = tr.CACHE_PATH
    tr.CACHE_PATH = Path("/nonexistent-directory-for-tests/cache.json")
    try:
        result, _ = _run({"owner_name": "उमा देवी"}, use_cache=True)
        assert result.data["owner_name"] == "EN::उमा देवी"
    finally:
        tr.CACHE_PATH = saved_path


# ── Target language ───────────────────────────────────────────────

def test_the_target_language_reaches_the_model_call():
    _, rec = _run({"owner_name": "उमा देवी"}, target_language="ja")
    assert [call["spec"].code for call in rec.calls] == ["ja"], rec.calls


def test_the_result_reports_the_language_it_translated_into():
    result, _ = _run({"owner_name": "उमा देवी"}, target_language="ja")
    assert result.target_language == "ja"
    assert "ja" in result.describe(), result.describe()


def test_an_unsupported_language_is_refused_by_name():
    try:
        tr.translate_data({"a": "उमा देवी"}, target_language="xx")
    except ValueError as exc:
        assert "xx" in str(exc) and "en" in str(exc), str(exc)
    else:
        raise AssertionError("an unknown language code must raise")


def test_each_language_prompt_carries_its_own_examples():
    """
    The rules do not vary between languages; the worked examples in the target
    script do. A prompt built for Japanese that shows Latin transliterations
    would teach the model the wrong script.
    """
    english = tr.build_prompt(language_spec("en"))
    japanese = tr.build_prompt(language_spec("ja"))
    assert "Uma Devi Chaulagai" in english
    assert "ウマ・デヴィ・チャウラガイ" in japanese
    assert "Uma Devi Chaulagai" not in japanese


def test_the_prose_note_names_the_target_language():
    prompt = tr.build_prompt(language_spec("ja"), prose=True)
    assert "Japanese prose" in prompt, prompt[-200:]


def test_english_text_is_sent_when_the_target_is_not_latin():
    """
    A document's printed English half, or a field OCR read as English, is still
    untranslated for a Japanese reader — the value being ASCII means nothing
    when ASCII is not the target script.
    """
    _, rec = _run({"sex": "Male"}, target_language="ja")
    assert rec.sent == ["Male"], rec.sent


def test_identifiers_are_never_sent_to_any_language():
    """A certificate number is printed as it is, in katakana-land too."""
    data = {"citizenship_no": "29-01-78-03898", "cert_no": "NM0000095"}
    _, rec = _run(data, target_language="ja")
    assert rec.calls == [], rec.calls


def test_the_cache_is_keyed_on_the_language():
    """Without the language in the key, a Japanese run is served English hits."""
    saved_path = tr.CACHE_PATH
    with tempfile.TemporaryDirectory() as tmp:
        tr.CACHE_PATH = Path(tmp) / "cache.json"
        try:
            data = {"owner_name": "उमा देवी"}
            _run(data, use_cache=True, target_language="en")
            _, rec = _run(data, use_cache=True, target_language="ja")
            assert rec.calls, "a different language must not reuse the entry"
        finally:
            tr.CACHE_PATH = saved_path


# ── Real extracted data ───────────────────────────────────────────

def test_a_real_extraction_round_trips():
    """
    Shape check against a saved extraction, if one is present: the translated
    data must keep every key and every row the builder expects.
    """
    sample = Path(__file__).resolve().parent.parent / "test-output" / "laalpurja.json"
    if not sample.is_file():
        return  # nothing saved locally; the offline tests above still cover it
    data = json.loads(sample.read_text(encoding="utf-8"))
    result, _ = _run(data)
    assert set(result.data) == set(data)
    assert len(result.data["plots"]) == len(data["plots"])
    for before, after in zip(data["plots"], result.data["plots"]):
        assert set(before) == set(after)


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
