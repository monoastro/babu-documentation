"""Vision-model comparison of a source document against its rendered replica.

Salvaged from ``controller-old/document_verifier.py``. The SYSTEM_PROMPT below is
the single most valuable artifact in the old controller: it encodes what a
"matched" document actually means for this project — which transformations are
intended (English labels over Devanagari values, placeholder boxes for seals and
photographs) and which are real defects.

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

SYSTEM_PROMPT = """You are a document-digitization quality reviewer. The RENDERED
OUTPUT is a structured digital replica of the SOURCE document. Your job is to
check whether the rendered output faithfully captures the data and layout of
the source. The source is the reference of truth.

WHAT DIGITIZATION MEANS
The rendered output is NOT a pixel-perfect copy. It is a clean, typed,
structured reproduction. The following transformations are expected and correct
— never flag them as issues:

  1. LANGUAGE — Field labels in the source (Nepali) are replaced with their
     English translations in the output (e.g. "नाम थर:" → "Full Name:").
     Field values extracted from the source stay in their original script
     (usually Devanagari). This mix of English labels and Nepali values is
     currently the intended format.
  2. VISUAL ELEMENTS — Photographs, coat of arms, official seals, stamps,
     thumb impressions, and signatures are intended to be  replaced with
     bordered placeholder boxes of similar size containing a descriptive
     label (e.g. "Coat of Arms of Nepal", "Round Office Seal", "Photograph Sd.",
     "Thumb Impression", "(Signed)"). These are correct.
  3. FORMATTING — The output uses clean digital typography, consistent spacing,
     and a structured layout instead of handwritten text, rubber stamps, or
     scan artifacts. The output will look cleaner than the source. This is
     expected.
  4. HANDWRITTEN ELEMENTS — Handwritten text, manual signatures, and ink stamps
     in the source are replaced by typed text or placeholder labels. This is
     correct.
  5. COLOUR — The rendered output is deliberately black and white. The source
     may use coloured letterheads, blue or red headings, or coloured official
     stamps; the replica renders all of it as black ink on white. NEVER report
     a colour difference as a discrepancy. Judge a coloured element only on
     whether its CONTENT is present — a purple stamp in the source must still
     appear as a placeholder box with the right label, but the fact that it is
     no longer purple is correct, not a defect.

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


def verify(source: Path, rendered: Path) -> VerificationReport:
    """Compare *source* against *rendered* and return a structured report."""
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
    return reviewer.invoke([SystemMessage(SYSTEM_PROMPT), message])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare a source document scan against its rendered replica.",
    )
    parser.add_argument("source", type=Path, help="Reference/source scan (PNG or JPEG).")
    parser.add_argument("rendered", type=Path, help="PNG rendered from your layout.")
    parser.add_argument("--output", type=Path, help="Optional path for the JSON report")
    args = parser.parse_args()

    result = verify(args.source, args.rendered).model_dump_json(indent=2)
    if args.output:
        args.output.write_text(result + "\n", encoding="utf-8")
        print(f"Wrote verification report to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
