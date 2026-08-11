"""A first layout from the scan's own geometry.

Datalab's ``/convert`` endpoint returns the page as a tree of blocks, each with
a bounding box in the page's coordinate space. This module turns that tree into
layout source: an A4 sheet with every block absolutely positioned where the
scan had it, scaled uniformly so the source's aspect ratio and the relative
positions of text and pictures survive the trip.

The split of work matters. Everything here is arithmetic — no model, no
network, no API key — so the same scan gives the same layout every time and a
bad result is debuggable rather than resampled. What each block *means* (a
heading, a label, an extractable value, a seal) is a semantic question, and
that half lives in ``agentic_controller.architect.plan_blocks``. This module
takes that classification as the ``plan`` argument and does not guess it.

    conversion  ->  blocks_from_conversion  ->  page_geometry  ->  place
                                                                     |
                              plan (from the agent)  ------------->  |
                                                                     v
                                                              layout_source

The emitted source is an ordinary layout module: it defines
``build_<document_type>(data) -> Document`` and is expected to pass
``architect.validate_layout`` unchanged.
"""

from __future__ import annotations

import html as _html
import re
from dataclasses import dataclass, replace
from typing import Any, Iterable

# A4 at 96 DPI. 210 x 297 mm, the size every one of these documents is
# ultimately printed on, so it is the page size rather than a fitted guess.
A4_PORTRAIT = (794, 1123)
A4_LANDSCAPE = (1123, 794)

# 10 mm, the same 96 DPI. Nothing is placed outside this, so a printer's
# unprintable edge never clips a field.
MARGIN_PX = 37.8

# A bbox is the line box, not the glyphs. Cap height plus descender comes to
# roughly this fraction of it; a font sized to the full box overflows.
_GLYPH_RATIO = 0.62

MIN_FONT_PX = 8.0
MAX_FONT_PX = 48.0

# A placeholder box carries a caption, not a description. Datalab's ``alt`` is a
# full sentence — "A color photograph of a man with short black hair, wearing a
# dark suit jacket over a white shirt and a blue tie." — which overflows the box
# it labels. The first clause is the subject, so cut there.
MAX_LABEL_CHARS = 32
_MIN_LABEL_CHARS = 12

# Words in a picture's caption that describe a round seal or stamp, and words
# that describe a rectangle. A caption routinely contains both, so whichever is
# mentioned *first* wins: the caption names its subject before it describes
# where the subject sits. "A rectangular box ... intended for a photograph or
# official stamp" is a rectangle; "A red circular official stamp ... overlapping
# the photo" is a circle.
_ROUND_WORDS = ("seal", "emblem", "crest", "circular", "circle", "round")
_SQUARE_WORDS = ("rectangular", "rectangle", "square", "photograph", "photo", "box")

_TAG = re.compile(r"<[^>]+>")
_ALT = re.compile(r'alt="([^"]*)"')
_WS = re.compile(r"\s+")


# ── Blocks ────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Block:
    """One block from the conversion tree, in the source's coordinate space.

    Attributes:
        block_id: Datalab's own id, e.g. ``/page/0/Text/9``. This is the key
            the plan is written against.
        kind: ``Text`` or ``Picture``, from ``block_type``.
        bbox: ``(x0, y0, x1, y1)``.
        text: Tags stripped out of ``html``.
        alt: The ``alt`` caption, for pictures.
        bold: Whether the source markup wrapped the text in ``<b>``.
    """

    block_id: str
    kind: str
    bbox: tuple[float, float, float, float]
    text: str = ""
    alt: str = ""
    bold: bool = False

    @property
    def width(self) -> float:
        return self.bbox[2] - self.bbox[0]

    @property
    def height(self) -> float:
        return self.bbox[3] - self.bbox[1]


@dataclass(frozen=True)
class Placed(Block):
    """A :class:`Block` mapped onto the A4 sheet, in CSS pixels."""

    left: float = 0.0
    top: float = 0.0
    box_width: float = 0.0
    box_height: float = 0.0
    font_size: float = 0.0


@dataclass(frozen=True)
class PageGeometry:
    """How the source's ink extent maps onto the A4 sheet.

    Attributes:
        page_width/page_height: The A4 sheet, in CSS pixels.
        landscape: Which way round that sheet is.
        scale: One factor for both axes. Two factors would fit the sheet
            exactly and distort every box doing it.
        offset_x/offset_y: Where the scaled extent starts, centring it.
        extent: The source-space ink extent the scale was derived from.
    """

    page_width: int
    page_height: int
    landscape: bool
    scale: float
    offset_x: float
    offset_y: float
    extent: tuple[float, float, float, float]

    @property
    def aspect(self) -> float:
        return self.page_width / self.page_height


def _clean(fragment: str) -> str:
    """Strip tags and collapse whitespace, leaving the readable text."""
    return _WS.sub(" ", _html.unescape(_TAG.sub(" ", fragment or ""))).strip()


def blocks_from_conversion(conversion: dict[str, Any], page: int = 0) -> list[Block]:
    """Flatten one page of a ``/convert`` tree into :class:`Block` objects.

    Blocks with no usable bbox, and text blocks that carry no text, are
    dropped: they contribute nothing to place and would skew the ink extent.
    """
    pages = conversion.get("children") or []
    if page >= len(pages):
        return []

    blocks: list[Block] = []
    for raw in pages[page].get("children") or []:
        bbox = raw.get("bbox")
        if not bbox or len(bbox) != 4:
            continue
        x0, y0, x1, y1 = (float(v) for v in bbox)
        if x1 <= x0 or y1 <= y0:
            continue

        markup = raw.get("html") or ""
        kind = raw.get("block_type") or "Text"
        alt_match = _ALT.search(markup)
        alt = _clean(alt_match.group(1)) if alt_match else ""
        # An <img> tag's alt would otherwise land in the stripped text and be
        # rendered as a paragraph of prose describing the picture.
        text = "" if kind == "Picture" else _clean(markup)

        if kind != "Picture" and not text:
            continue

        blocks.append(
            Block(
                block_id=raw.get("id") or f"/page/{page}/{kind}/{len(blocks)}",
                kind=kind,
                bbox=(x0, y0, x1, y1),
                text=text,
                alt=alt,
                bold="<b>" in markup or "<strong>" in markup,
            )
        )
    return blocks


# ── Geometry ──────────────────────────────────────────────────────

def ink_extent(blocks: Iterable[Block]) -> tuple[float, float, float, float]:
    """The bounding box of every block, in source space.

    Deliberately not the page bbox. The conversion page carries whatever
    padding the scan had — for the citizenship sample it is 1372x980 (aspect
    1.400) around ink that is 1201x799 (aspect 1.503) — and normalizing
    against it would bake that padding into the A4 sheet.
    """
    boxes = [b.bbox for b in blocks]
    if not boxes:
        raise ValueError("no blocks to measure")
    return (
        min(b[0] for b in boxes),
        min(b[1] for b in boxes),
        max(b[2] for b in boxes),
        max(b[3] for b in boxes),
    )


def page_geometry(
    blocks: Iterable[Block], *, margin: float = MARGIN_PX
) -> PageGeometry:
    """Fit the ink extent onto an A4 sheet with one uniform scale.

    Orientation follows the extent's own aspect, so a landscape citizenship
    certificate does not get letterboxed onto a portrait page.
    """
    blocks = list(blocks)
    x0, y0, x1, y1 = ink_extent(blocks)
    extent_w, extent_h = x1 - x0, y1 - y0

    landscape = extent_w > extent_h
    page_w, page_h = A4_LANDSCAPE if landscape else A4_PORTRAIT

    inner_w = page_w - 2 * margin
    inner_h = page_h - 2 * margin
    # min(), not two factors: this is what preserves the aspect ratio. The
    # slack on the other axis becomes margin.
    scale = min(inner_w / extent_w, inner_h / extent_h)

    return PageGeometry(
        page_width=page_w,
        page_height=page_h,
        landscape=landscape,
        scale=scale,
        offset_x=(page_w - extent_w * scale) / 2,
        offset_y=(page_h - extent_h * scale) / 2,
        extent=(x0, y0, x1, y1),
    )


def place(blocks: Iterable[Block], geometry: PageGeometry) -> list[Placed]:
    """Map every block onto the sheet, in reading order (top, then left)."""
    ex0, ey0, _, _ = geometry.extent
    s = geometry.scale

    placed = [
        Placed(
            block_id=b.block_id,
            kind=b.kind,
            bbox=b.bbox,
            text=b.text,
            alt=b.alt,
            bold=b.bold,
            left=geometry.offset_x + (b.bbox[0] - ex0) * s,
            top=geometry.offset_y + (b.bbox[1] - ey0) * s,
            box_width=b.width * s,
            box_height=b.height * s,
            font_size=_font_size(b.height * s),
        )
        for b in blocks
    ]
    return sorted(placed, key=lambda p: (round(p.top, 1), round(p.left, 1)))


def _font_size(box_height: float) -> float:
    return round(min(max(box_height * _GLYPH_RATIO, MIN_FONT_PX), MAX_FONT_PX), 1)


def fit_text(placed: Placed, *, chars: int | None = None) -> Placed:
    """Shrink a block's font until its text plausibly fits the box width.

    A translated label is routinely longer than the Devanagari it replaces, and
    a value box sized for the scan's handwriting overflows into its neighbour.
    Average glyph advance for a serif face is about 0.5 em, which is close
    enough to catch the bad cases without a text-measurement pass.
    """
    n = chars if chars is not None else len(placed.text)
    if n <= 0 or placed.box_width <= 0:
        return placed
    fits = placed.box_width / (n * 0.5)
    if fits >= placed.font_size:
        return placed
    return replace(placed, font_size=round(max(fits, MIN_FONT_PX), 1))


# ── Source emission ───────────────────────────────────────────────

def _py(value: str) -> str:
    """A Python string literal for *value*, safe to paste into source."""
    return repr(value)


def _px(value: float) -> str:
    return f"{value:.1f}px"


def _role(plan: dict[str, dict[str, Any]], block: Block) -> dict[str, Any]:
    """The plan entry for *block*, defaulting to static text.

    An unplanned block still renders. Dropping it would silently lose content
    the scan clearly had, and the agent reviewing the render cannot ask for
    back something it cannot see.
    """
    entry = plan.get(block.block_id)
    if entry:
        return entry
    if block.kind == "Picture":
        return {"role": "placeholder", "label": block.alt or "Image"}
    return {"role": "static", "text": block.text}


def _short_label(caption: str) -> str:
    """A box-sized caption from a possibly sentence-long description."""
    text = (caption or "").strip().rstrip(".")
    if not text:
        return "Image"
    if len(text) <= MAX_LABEL_CHARS:
        return text
    # Cut at the first clause boundary, but only when that clause is a phrase
    # rather than a fragment: "A small, square, textured object" opens with a
    # clause that is only "A small". Otherwise clip on a word boundary.
    head = re.split(r"[,;:]", text, maxsplit=1)[0].strip()
    if _MIN_LABEL_CHARS <= len(head) <= MAX_LABEL_CHARS:
        return head
    clipped = text[:MAX_LABEL_CHARS].rsplit(" ", 1)[0].strip()
    return clipped or text[:MAX_LABEL_CHARS].strip()


def _first_mention(caption: str, words: Iterable[str]) -> int:
    """Index of the earliest of *words* in *caption*, or ``-1`` for none."""
    hits = [i for i in (caption.find(w) for w in words) if i >= 0]
    return min(hits) if hits else -1


def _shape_for(entry: dict[str, Any], block: Placed) -> str:
    caption = f"{entry.get('label', '')} {block.alt}".lower()
    round_at = _first_mention(caption, _ROUND_WORDS)
    if round_at < 0:
        return "rect"
    square_at = _first_mention(caption, _SQUARE_WORDS)
    if 0 <= square_at < round_at:
        return "rect"
    ratio = block.box_width / block.box_height if block.box_height else 0
    # A wide banner mentioning a seal is not a round seal. The band is loose
    # because a seal overlapping the page edge is clipped to a non-square bbox.
    return "circle" if 0.5 <= ratio <= 2.0 else "rect"


def value_fields(plan: dict[str, dict[str, Any]]) -> list[str]:
    """Every field name the plan binds to a value, in plan order."""
    seen: list[str] = []
    for entry in plan.values():
        if entry.get("role") == "value":
            name = entry.get("field")
            if name and name not in seen:
                seen.append(name)
    return seen


_MODULE_HEADER = '''"""Generated layout for {title}.

Positions are derived from the source scan's own block geometry: every box was
scaled by a single factor ({scale:.4f}) onto an A4 {orientation} sheet, so the
document's aspect ratio and the relative placement of its text and pictures
match the original. Regenerate rather than hand-tune the coordinates — see
``document_builder/autolayout.py``.
"""

from __future__ import annotations

from typing import Any

from html_engine import (
    AbsoluteBox,
    Document,
    PlaceholderBox,
    Style,
    Text,
)

_EDITABLE_CSS = """
[contenteditable]:hover {{ outline: 2px dashed #000000; cursor: text; }}
[contenteditable]:focus {{ outline: 2px solid #000000; background: #ffffff; }}
"""

PAGE_WIDTH = "{page_width}px"
PAGE_HEIGHT = "{page_height}px"

'''

_BUILDER_HEADER = '''
def build_{document_type}(data: dict[str, Any]) -> Document:
    d = {{key: "" for key in FIELDS}}
    d.update(data or {{}})

    doc = Document(
        {title!r},
        page_width=PAGE_WIDTH,
        page_height=PAGE_HEIGHT,
        background="#ffffff",
        font_family='"Times New Roman", serif',
        border="2px solid #000000",
        extra_css=_EDITABLE_CSS,
    )
'''


def layout_source(
    placed: Iterable[Placed],
    plan: dict[str, dict[str, Any]],
    document_type: str,
    geometry: PageGeometry,
    *,
    title: str | None = None,
) -> str:
    """Emit a complete layout module for *document_type*.

    Args:
        placed: Blocks already mapped onto the sheet by :func:`place`.
        plan: ``block_id -> {"role": ..., "text"/"field"/"label": ...}``, from
            ``architect.plan_blocks``.
        document_type: Names the builder — ``build_<document_type>``.
        geometry: The page the blocks were placed on.
        title: Document title. Defaults to a title-cased *document_type*.
    """
    placed = list(placed)
    doc_title = title or document_type.replace("_", " ").title()
    fields = value_fields(plan)

    if fields:
        field_block = "FIELDS = (\n" + "".join(f"    {n!r},\n" for n in fields) + ")\n"
    else:
        field_block = "FIELDS: tuple[str, ...] = ()\n"

    body = "".join(_emit_block(b, _role(plan, b)) for b in placed)
    return (
        _MODULE_HEADER.format(
            title=doc_title,
            scale=geometry.scale,
            orientation="landscape" if geometry.landscape else "portrait",
            page_width=geometry.page_width,
            page_height=geometry.page_height,
        )
        + field_block
        + _BUILDER_HEADER.format(
            document_type=document_type,
            title=doc_title,
        )
        + body
        + "    return doc\n"
    )


def _emit_block(block: Placed, entry: dict[str, Any]) -> str:
    role = entry.get("role", "static")
    comment = f"  # {block.block_id}"

    if role == "placeholder":
        label = _short_label(entry.get("label") or block.alt)
        shape = _shape_for(entry, block)
        return (
            f"\n    doc.add(  {comment.strip()}\n"
            f"        AbsoluteBox(\n"
            f"            PlaceholderBox(\n"
            f"                {_py(label)},\n"
            f"                width={_px(block.box_width)!r},\n"
            f"                height={_px(block.box_height)!r},\n"
            f"                shape={shape!r},\n"
            f"                font_size={_px(min(block.font_size, 14.0))!r},\n"
            f"            ),\n"
            f"            left={_px(block.left)!r},\n"
            f"            top={_px(block.top)!r},\n"
            f"        )\n"
            f"    )\n"
        )

    weight = "bold" if block.bold else "normal"

    if role == "value":
        field = entry.get("field") or ""
        sized = fit_text(block, chars=max(len(entry.get("text") or ""), 12))
        content = f"d[{field!r}]"
        field_arg = f"\n            field={field!r},"
    else:
        text = entry.get("text") or block.text
        sized = fit_text(replace(block, text=text))
        content = _py(text)
        field_arg = ""

    # The box is sized from the source, but a translated string is often longer
    # than the Devanagari it replaces. Wrapping inside the box keeps an
    # overlong value on the page instead of pushing it off the sheet.
    return (
        f"\n    doc.add(  {comment.strip()}\n"
        f"        AbsoluteBox(\n"
        f"            Text(\n"
        f"                {content},\n"
        f"                style=Style(\n"
        f"                    font_size={_px(sized.font_size)!r},\n"
        f"                    font_weight={weight!r},\n"
        f"                    line_height='1.1',\n"
        f"                    display='inline-block',\n"
        f"                    max_width={_px(max(block.box_width * 1.35, 40.0))!r},\n"
        f"                ),{field_arg}\n"
        f"            ),\n"
        f"            left={_px(block.left)!r},\n"
        f"            top={_px(block.top)!r},\n"
        f"        )\n"
        f"    )\n"
    )
