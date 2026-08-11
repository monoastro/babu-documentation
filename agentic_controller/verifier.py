"""Vision-model comparison of a source document against its rendered replica.

Salvaged from ``controller-old/document_verifier.py``. The SYSTEM_PROMPT below is
the single most valuable artifact in the old controller: it encodes what a
"matched" document actually means for this project — which transformations are
intended (translated labels over Devanagari values, placeholder boxes for seals
and photographs) and which are real defects.

That prompt is mirrored in prose in ``documentation/verification-rules.md``. If
you change one, change the other; the agent reads the markdown and the verifier
reads this constant.
"""

from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from agentic_controller.models import VerificationReport
from information_extraction.languages import DEFAULT_LANGUAGE, LANGUAGES, language_spec

# The language rule is built per call, because a Japanese render must be judged
# against a Japanese target. The one fragment of the prompt that changes is the
# named target and its worked examples; everything else is shared.
_LANGUAGE_RULE_TEMPLATE = """  1. LANGUAGE — The rendered output is in {language}. Field labels in the
     source (Nepali) appear as their {language} translations, and field VALUES
     are translated too: common nouns and phrases are translated for meaning,
     person and place names are transliterated, Devanagari numerals become ASCII
     digits ("८" -> "8"), and Bikram Sambat dates are converted to Gregorian
     ("२०४९/०३/०९" -> "1992-06-22"). Worked examples of both kinds:
{transliteration}
{meaning}
     A fully {language} output is the intended format. NEVER report a value as a
     discrepancy merely because its script differs from the source. Judge a
     value on whether it is the CORRECT {language} rendering of the source value
     — a wrong name, a wrong number, or a mistranslation that changes meaning is
     a real discrepancy; a faithful translation or transliteration is not. Where
     a date has been converted, check the conversion rather than the digits."""

_SYSTEM_PROMPT_HEADER = """You are a document-digitization quality reviewer. The RENDERED
OUTPUT is a structured digital replica of the SOURCE document. Your job is to
check whether the rendered output faithfully captures the data and layout of
the source. The source is the reference of truth.

WHAT DIGITIZATION MEANS
The rendered output is NOT a pixel-perfect copy. It is a clean, typed,
structured reproduction. The following transformations are expected and correct
— never flag them as issues:

"""

_SYSTEM_PROMPT_FOOTER = """
WHAT TO ACTUALLY CHECK
Focus only on whether the digitized output accurately represents the source
document's information:

  - DATA ACCURACY — Do all extracted field values match the source? Check
    names, numbers, dates, addresses character by character.
  - FIELD COMPLETENESS — Is every data field present in the source also present
    in the output? Are any fields missing or extra?
  - STRUCTURAL MATCH — Does the output preserve the logical structure (header,
    data fields, sections) of the source? Are fields in a sensible order?
  - PLACEHOLDER CORRECTNESS — Are placeholder boxes in roughly the right
    position and size? Do their labels match what they replace?

SEVERITY GUIDE
  - minor — Small inaccuracy that does not change meaning (e.g. a minor
    spacing difference, slight position offset of a placeholder).
  - major — A data value is wrong, a field is missing, or a placeholder is
    mislabeled.
  - critical — Multiple fields are wrong or missing, or the document structure
    is fundamentally broken.

If the source image is too blurry to confirm a value, say so and flag
needs_human_review. Do not guess. Do not suggest fixes.
"""

_VISUAL_ELEMENTS_RULE = """  2. VISUAL ELEMENTS — Photographs, coat of arms, official seals, stamps,
     thumb impressions, and signatures are intended to be  replaced with
     bordered placeholder boxes of similar size containing a descriptive
     label (e.g. "Coat of Arms of Nepal", "Round Office Seal", "Photograph Sd.",
     "Thumb Impression", "(Signed)"). These are correct."""

_FORMATTING_RULE = """  3. FORMATTING — The output uses clean digital typography, consistent spacing,
     and a structured layout instead of handwritten text, rubber stamps, or
     scan artifacts. The output will look cleaner than the source. This is
     expected."""

_HANDWRITTEN_RULE = """  4. HANDWRITTEN ELEMENTS — Handwritten text, manual signatures, and ink stamps
     in the source are replaced by typed text or placeholder labels. This is
     correct."""

_COLOUR_RULE = """  5. COLOUR — The rendered output is deliberately black and white. The source
     may use coloured letterheads, blue or red headings, or coloured official
     stamps; the replica renders all of it as black ink on white. NEVER report
     a colour difference as a discrepancy. Judge a coloured element only on
     whether its CONTENT is present — a purple stamp in the source must still
     appear as a placeholder box with the right label, but the fact that it is
     no longer purple is correct, not a defect."""


def build_prompt(target_language: str = DEFAULT_LANGUAGE) -> str:
    """The full verification system prompt for one target language."""
    spec = language_spec(target_language)
    language_rule = _LANGUAGE_RULE_TEMPLATE.format(
        language=spec.name,
        transliteration=spec.transliteration,
        meaning=spec.meaning,
    )
    rules = "\n".join(
        [
            language_rule,
            _VISUAL_ELEMENTS_RULE,
            _FORMATTING_RULE,
            _HANDWRITTEN_RULE,
            _COLOUR_RULE,
        ]
    )
    return _SYSTEM_PROMPT_HEADER + rules + "\n" + _SYSTEM_PROMPT_FOOTER


# Backward-compatible constant: the English prompt, as it always was.
SYSTEM_PROMPT = build_prompt()


def image_data_url(path: Path) -> str:
    """Validate a local raster image and encode it for a multimodal model message.

    Sources arrive as scans in whatever format the user has (PNG or JPEG);
    renders are always PNG. The format is taken from the magic bytes rather
    than the extension, so a mislabelled file still gets the correct MIME type.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")
    content = path.read_bytes()
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        mime = "image/png"
    elif content.startswith(b"\xff\xd8\xff"):
        mime = "image/jpeg"
    else:
        raise ValueError(f"Expected a PNG or JPEG image: {path}")
    return f"data:{mime};base64," + base64.b64encode(content).decode("ascii")


def verify(
    source: Path,
    rendered: Path,
    *,
    target_language: str = DEFAULT_LANGUAGE,
) -> VerificationReport:
    """Compare *source* against *rendered* and return a structured report.

    *target_language* must match the language the document was translated into.
    Judging a Japanese render against the English rule turns every correctly
    translated value into a reported discrepancy, and the repair loop then
    chases them forever.
    """
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
        )

    reviewer = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        temperature=0,
    ).with_structured_output(VerificationReport)

    message = HumanMessage(
        content=[
            {"type": "text", "text": "SOURCE document (reference):"},
            {"type": "image_url", "image_url": {"url": image_data_url(source), "detail": "high"}},
            {"type": "text", "text": "RENDERED OUTPUT (compare against source):"},
            {"type": "image_url", "image_url": {"url": image_data_url(rendered), "detail": "high"}},
        ]
    )
    return reviewer.invoke(
        [SystemMessage(build_prompt(target_language)), message]
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare a source document scan against its rendered replica.",
    )
    parser.add_argument("source", type=Path, help="Reference/source scan (PNG or JPEG).")
    parser.add_argument("rendered", type=Path, help="PNG rendered from your layout.")
    parser.add_argument("--output", type=Path, help="Optional path for the JSON report")
    parser.add_argument(
        "-l",
        "--lang",
        dest="target_language",
        default=DEFAULT_LANGUAGE,
        choices=sorted(LANGUAGES),
        help=f"Language the render was translated into (default: {DEFAULT_LANGUAGE})",
    )
    args = parser.parse_args()

    result = verify(
        args.source, args.rendered, target_language=args.target_language
    ).model_dump_json(indent=2)
    if args.output:
        args.output.write_text(result + "\n", encoding="utf-8")
        print(f"Wrote verification report to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
