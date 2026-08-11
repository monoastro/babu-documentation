"""Datalab ``/convert``: the block tree a scan's geometry comes from.

``extractor.py`` calls ``/extract`` and gets schema-keyed values with no
coordinates. This module calls ``/convert`` and gets the opposite: every block
on the page with its bounding box, in the page's own coordinate space.

``document_builder/autolayout.py`` turns that tree into a layout. Keeping the
call here means the geometry path can be developed and tested against a saved
JSON with no API key — see :func:`load_conversion`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from datalab_sdk import ConvertOptions, DatalabClient
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODE = "balanced"


def convert(image_path: str | Path, mode: str = DEFAULT_MODE) -> dict[str, Any]:
    """Convert *image_path* to a block tree and return the parsed JSON.

    Args:
        image_path: The scan to convert.
        mode: ``fast``, ``balanced``, or ``accurate``. Slower modes segment
            small text more reliably, which is the whole point here.

    The result is a ``Page`` root whose ``children`` are the blocks, each with
    ``id``, ``block_type``, ``bbox``, ``polygon``, and ``html``.
    """
    client = DatalabClient()
    # ``add_block_ids`` is deliberately absent: it only applies to HTML output,
    # and the JSON tree already carries an ``id`` per block. Image extraction is
    # off because a rendered document uses placeholder boxes, never the source
    # imagery — the ``alt`` caption is the part that survives.
    options = ConvertOptions(
        output_format="json",
        mode=mode,
        disable_image_extraction=True,
    )
    result = client.convert(str(image_path), options=options)

    if not result.success:
        raise RuntimeError(f"conversion failed: {result.error or 'no error given'}")
    if not result.json:
        raise RuntimeError("conversion returned no JSON block tree")
    return result.json


def load_conversion(path: str | Path) -> dict[str, Any]:
    """Read a conversion JSON saved earlier.

    Datalab deletes results an hour after the call, so a saved tree is the only
    way to re-run the geometry without paying for the conversion again.
    """
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_conversion(conversion: dict[str, Any], path: str | Path) -> Path:
    """Write *conversion* to *path* and return it."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(conversion, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return target
