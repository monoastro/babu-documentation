from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from one_shot import client

HERE = Path(__file__).resolve().parent
PROMPT_PATH = HERE / "prompt.txt"
EXAMPLE_PATH = HERE / "example.txt"
DRAFTS_DIR = HERE / "drafts"

MIME_BY_SUFFIX = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".pdf": "application/pdf"}


def build_prompt(example_html: str | None) -> str:
    parts = [PROMPT_PATH.read_text(encoding="utf-8")]
    if example_html:
        parts.append(
            "\n\n# Reference snippets\n\n"
            "Verbatim snippets from cleaned, verified finals:\n\n"
            f"{example_html}"
        )
    return "".join(parts)


def extract_html(text: str) -> str:
    text = text.strip()
    match = re.match(r"^```(?:html)?\s*\n(.*?)\n\s*```$", text, re.DOTALL)
    return match.group(1).strip() if match else text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="One-shot digitize a scan to HTML.")
    parser.add_argument("--image", required=True, help="Path to the scan image.")
    parser.add_argument("--example", help="Reference cleaned HTML (default: one_shot/example.txt).")
    parser.add_argument("--out", help="Output path (default: one_shot/drafts/<stem>.html).")
    args = parser.parse_args(argv)

    image = Path(args.image)
    if not image.is_file():
        print(f"no such image: {image}", file=sys.stderr)
        return 1

    mime = MIME_BY_SUFFIX.get(image.suffix.lower())
    if not mime:
        print(f"unsupported image type {image.suffix} (need png/jpg/jpeg/webp/pdf)", file=sys.stderr)
        return 1

    example = Path(args.example) if args.example else EXAMPLE_PATH
    example_html = example.read_text(encoding="utf-8") if example.is_file() else None
    if args.example and example_html is None:
        print(f"no such example: {example}", file=sys.stderr)
        return 1

    prompt = build_prompt(example_html)
    print(f"prompt: {len(prompt):,} chars | image: {image.name} | example: {example.name if example_html else '-'}")

    text = client.call(prompt, images=[(mime, image.read_bytes())])

    html = extract_html(text)
    if not html.lstrip().lower().startswith("<!doctype"):
        print("warning: output does not start with <!DOCTYPE html>", file=sys.stderr)

    out = Path(args.out) if args.out else DRAFTS_DIR / f"{image.stem}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"draft written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
