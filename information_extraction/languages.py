"""Target languages the translator can render a document into.

One :class:`LanguageSpec` per language, holding the parts of the translation
prompt that differ between them. Adding a language is adding an entry to
``LANGUAGES``; no logic elsewhere changes.

The prompt parts are split rather than written as whole prompts because the
rules themselves do not vary — proper nouns are transliterated, everything else
is translated for meaning, nothing is annotated. What varies is what those rules
look like in the target script, so each spec supplies worked examples and the
shared template in ``translator`` supplies the structure.

This module deliberately imports nothing: ``main.py`` reads ``LANGUAGES`` to
build its ``--lang`` choices, and must be able to do that without pulling in the
OpenAI client or the OCR path.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageSpec:
    """Everything the translator needs to know about one target language.

    Parameters:
        code: The short code callers pass — ``en``, ``ja``.
        name: The language's English name, interpolated into the prompt.
        script_is_ascii: Whether the language is written in Latin script.
            Decides whether a source value that is already ASCII can be left
            alone or still needs translating.
        transliteration: Worked transliteration examples in the target script.
        meaning: Worked meaning-translation examples.
        office: One worked example of an office name, which combines both rules.
    """

    code: str
    name: str
    script_is_ascii: bool
    transliteration: str
    meaning: str
    office: str


LANGUAGES: dict[str, LanguageSpec] = {
    "en": LanguageSpec(
        code="en",
        name="English",
        script_is_ascii=True,
        transliteration=(
            '   "उमा देवी चौलागाई" -> "Uma Devi Chaulagai", "काठमाण्डौ" -> "Kathmandu",\n'
            '   "नाङ्गलेभारे" -> "Nangalebhare". Use the conventional English spelling\n'
            "   when one exists (Kathmandu, not Kathmandau)."
        ),
        meaning=(
            '   "वंशज" -> "By descent", "मृत्युपछिको नामसारी" -> "Transfer after death",\n'
            '   "प्रशासकीय अधिकृत" -> "Administrative Officer".'
        ),
        office=(
            '   "जिल्ला प्रशासन कार्यालय, काठमाण्डौ" -> "District Administration Office,\n'
            '   Kathmandu".'
        ),
    ),
    "ja": LanguageSpec(
        code="ja",
        name="Japanese",
        script_is_ascii=False,
        transliteration=(
            "   Write personal and place names in katakana, following the Nepali\n"
            '   pronunciation: "उमा देवी चौलागाई" -> "ウマ・デヴィ・チャウラガイ",\n'
            '   "काठमाण्डौ" -> "カトマンズ", "गुल्मी" -> "グルミ". Use the established\n'
            "   Japanese form when one exists (カトマンズ, not カトマンドゥ). Separate the\n"
            "   parts of a personal name with a middle dot."
        ),
        meaning=(
            '   "वंशज" -> "血統による", "मृत्युपछिको नामसारी" -> "死亡後の名義変更",\n'
            '   "प्रशासकीय अधिकृत" -> "行政官".'
        ),
        office='   "जिल्ला प्रशासन कार्यालय, काठमाण्डौ" -> "カトマンズ郡行政事務所".',
    ),
}

DEFAULT_LANGUAGE = "en"


def language_spec(code: str) -> LanguageSpec:
    """Look up a target language, naming the supported codes on failure."""
    try:
        return LANGUAGES[code]
    except KeyError:
        supported = ", ".join(sorted(LANGUAGES))
        raise ValueError(
            f"unsupported target language {code!r} — supported: {supported}"
        ) from None
