"""Compare a source document PNG with a rendered PNG without modifying either."""

import argparse
import base64
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class Discrepancy(BaseModel):
    """One visible difference between the source and rendered document."""

    category: Literal[
        "text", "layout", "table", "image", "missing_content", "extra_content",
        "reading_order", "other",
    ]
    location: str = Field(description="Where the issue appears, such as 'top-right logo'.")
    source_observation: str
    rendered_observation: str
    severity: Literal["minor", "major", "critical"]
    confidence: float = Field(ge=0, le=1)


class VerificationReport(BaseModel):
    """The machine-readable result returned by the vision model."""

    overall_match: Literal["pass", "needs_review", "fail"]
    summary: str
    matches_well: list[str]
    discrepancies: list[Discrepancy]
    needs_human_review: bool


SYSTEM_PROMPT = """You are a meticulous document-rendering quality reviewer.
Compare the first image (SOURCE) with the second image (RENDERED OUTPUT).

Report only differences you can visually support. Check text presence and line
wrapping, reading order, alignment, spacing, tables, borders, images, stamps,
and page structure. Ignore small anti-aliasing or font-rasterization differences
unless they impair readability or layout. Do not suggest or apply a fix. If the
images are too unclear to judge a material point, say so and request human
review. The source image is the reference of truth.
"""


def png_data_url(path: Path) -> str:
    """Validate a local PNG and encode it for a multimodal model message."""
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")
    content = path.read_bytes()
    if not content.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Expected a PNG file: {path}")
    return "data:image/png;base64," + base64.b64encode(content).decode("ascii")


def verify(source: Path, rendered: Path) -> VerificationReport:
    """Return a validated visual-comparison report. This function makes no edits."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
        )

    reviewer = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"), temperature=0
    ).with_structured_output(VerificationReport)
    message = HumanMessage(
        content=[
            {"type": "text", "text": "SOURCE document (reference):"},
            {"type": "image_url", "image_url": {"url": png_data_url(source), "detail": "high"}},
            {"type": "text", "text": "RENDERED OUTPUT (compare against source):"},
            {"type": "image_url", "image_url": {"url": png_data_url(rendered), "detail": "high"}},
        ]
    )
    return reviewer.invoke([SystemMessage(SYSTEM_PROMPT), message])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare a source document PNG with a rendered PNG."
    )
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=Path("controller/input.png"),
        help="Reference/source PNG (default: input.png)",
    )
    parser.add_argument(
        "rendered",
        nargs="?",
        type=Path,
        default=Path("controller/output.png"),
        help="PNG rendered from your layout (default: output.png)",
    )
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
