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

# Translate into Japanese instead of English
python main.py test-data/demo.png --type letter --lang ja

# Keep the extracted values in their original script
python main.py test-data/demo.png --type letter --no-translate

# Build with empty values, to check layout and spacing alone
python main.py --type laalpurja --blank --png
"""
#claude --resume 2c0b20bb-0c2c-48ac-bc42-4e38b7df89e6
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from document_builder.registry import DOCUMENTS
from information_extraction.languages import DEFAULT_LANGUAGE, LANGUAGES

DEFAULT_OUTPUT_DIR = Path("translated")

# Key under which a saved JSON carries the pre-translation values. Underscored
# so it cannot collide with a schema field, and popped on load so it never
# reaches a builder.
ORIGINAL_KEY = "_translation_original"


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
    translate: bool = True,
    target_language: str = DEFAULT_LANGUAGE,
) -> dict:
    """Resolve the document's field values from whichever source was given.

    The OCR branch translates the extracted values into *target_language* before
    they reach a builder. ``--data`` is taken as-is: a saved JSON has already
    been through translation, and translating a translation only invites drift.
    """
    if blank:
        return _blank_data(document_type)

    if data_path is not None:
        data = json.loads(data_path.read_text(encoding="utf-8"))
        # OCR and hand-edited saved data can contain JSON nulls.  Layouts
        # render required field values as strings, including by concatenation.
        data = {key: value if value is not None else "" for key, value in data.items()}
        # The originals ride along in the saved file; they are provenance, not
        # a field, so they never reach the builder.
        data.pop(ORIGINAL_KEY, None)
        return data

    # OCR path — the only branch that costs an API call.
    from information_extraction.extractor import build_data, extract

    schema_path = DOCUMENTS[document_type]["schema"]
    extracted, schema = extract(image_path=str(image), schema_path=schema_path)
    data = build_data(extracted, schema)

    original: dict[str, str] = {}
    if translate:
        from information_extraction.translator import translate_data

        result = translate_data(data, target_language=target_language, verbose=True)
        print(f"  translation: {result.describe()}")
        data, original = result.data, result.original

    if save_data is not None:
        save_data.parent.mkdir(parents=True, exist_ok=True)
        # Both halves in one file: the translated values a builder consumes, and
        # the pre-translation originals, so nothing is lost to the OCR spend.
        payload = dict(data)
        if original:
            payload[ORIGINAL_KEY] = original
        save_data.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
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
        "-l",
        "--lang",
        dest="target_language",
        default=DEFAULT_LANGUAGE,
        choices=sorted(LANGUAGES),
        help=f"Language to translate into (default: {DEFAULT_LANGUAGE})",
    )
    parser.add_argument(
        "--no-translate",
        dest="translate",
        action="store_false",
        help="Keep extracted values in their original script instead of "
        "translating them.",
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
            translate=args.translate,
            target_language=args.target_language,
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
