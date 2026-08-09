"""
Manual entry point: turn one document into HTML (and optionally PNG).

This is the hand-driven counterpart to ``python -m agentic_controller.run``.
Same builders, same engine, no vision verifier and no repair loop — use it when
you are iterating on a layout and want to see the render, not spend credits on
a critique of it.

    # OCR a scan, then build
    python main.py test-data/demo.png --type letter

    # Re-render from data already extracted, no OCR call
    python main.py --type letter --data output/letter.json

    # Save the extracted JSON so later runs can skip OCR entirely
    python main.py test-data/demo.png --type letter --save-data output/letter.json

    # Build with empty values, to check layout and spacing alone
    python main.py --type laalpurja --blank --png
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from document_builder.registry import DOCUMENTS

DEFAULT_OUTPUT_DIR = Path("test-output")


def _blank_data(document_type: str) -> dict:
    """Every field the schema requires, empty.

    Renders the layout's own structure with no content in it, which is the
    quickest way to see whether a spacing problem belongs to the layout or to
    the extracted values.
    """
    schema_path = DOCUMENTS[document_type]["schema"]
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    return {key: "" for key in schema.get("required", [])}


def resolve_data(
    document_type: str,
    *,
    image: Path | None = None,
    data_path: Path | None = None,
    blank: bool = False,
    save_data: Path | None = None,
) -> dict:
    """Resolve the document's field values from whichever source was given."""
    if blank:
        return _blank_data(document_type)

    if data_path is not None:
        return json.loads(data_path.read_text(encoding="utf-8"))

    # OCR path — the only branch that costs an API call.
    from information_extraction.extractor import build_data, extract

    schema_path = DOCUMENTS[document_type]["schema"]
    extracted, schema = extract(image_path=str(image), schema_path=schema_path)
    data = build_data(extracted, schema)

    if save_data is not None:
        save_data.parent.mkdir(parents=True, exist_ok=True)
        save_data.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  data: {save_data}")
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Build one document to HTML without the agentic loop.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "image",
        nargs="?",
        type=Path,
        help="Source scan to OCR. Omit when using --data or --blank.",
    )
    parser.add_argument(
        "-t",
        "--type",
        dest="document_type",
        default="laalpurja",
        choices=sorted(DOCUMENTS),
        help="Document type (default: laalpurja)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output HTML path (default: output/<type>.html)",
    )
    parser.add_argument(
        "--data",
        type=Path,
        help="Build from this JSON instead of running OCR.",
    )
    parser.add_argument(
        "--save-data",
        type=Path,
        help="Write the extracted JSON here, so later runs can use --data.",
    )
    parser.add_argument(
        "--blank",
        action="store_true",
        help="Build with every field empty — layout check, no OCR.",
    )
    parser.add_argument(
        "--png",
        action="store_true",
        help="Also render a PNG next to the HTML (needs Chrome/Chromium).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Turn unrecognized-CSS-property warnings into errors.",
    )
    args = parser.parse_args(argv)

    # Argument sanity, checked before anything expensive runs.
    if sum([bool(args.image), args.data is not None, args.blank]) != 1:
        parser.error(
            "give exactly one data source: an image to OCR, --data, or --blank"
        )
    if args.image and not args.image.is_file():
        parser.error(f"image not found: {args.image}")
    if args.data and not args.data.is_file():
        parser.error(f"data file not found: {args.data}")

    if args.strict:
        import warnings

        from html_engine import StyleWarning

        warnings.simplefilter("error", StyleWarning)

    output = args.output or DEFAULT_OUTPUT_DIR / f"{args.document_type}.html"

    try:
        data = resolve_data(
            args.document_type,
            image=args.image,
            data_path=args.data,
            blank=args.blank,
            save_data=args.save_data,
        )
    except Exception as exc:
        print(f"Extraction failed: {exc}", file=sys.stderr)
        return 1

    builder = DOCUMENTS[args.document_type]["builder"]
    try:
        doc = builder(data)
        html_path = doc.save(output)
    except Exception as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1

    filled = sum(1 for v in data.values() if v not in ("", None, []))
    print(f"  html: {html_path}  ({filled}/{len(data)} fields populated)")

    if args.png:
        from agentic_controller.rendering import render_png

        png_name = html_path.with_suffix(".png").name
        if render_png(html_path, html_path.parent, png_name):
            print(f"  png:  {html_path.parent / png_name}")
        else:
            print("  png:  skipped", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
