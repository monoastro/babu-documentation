"""
Tests for ``document_builder/autolayout.py`` — the geometry half of layout
generation.

The point of this module is that it is arithmetic: the same scan gives the same
layout every time, no model and no network. So the suite runs entirely offline
against a real ``/convert`` reply saved at ``tests/fixtures/``, and every
number below was derived from that file rather than from the code.

The invariant the whole design rests on is the *uniform* scale. Two factors
would fit A4 exactly and distort every box doing it, which is precisely the
failure the overhaul was meant to remove, so it is asserted directly rather
than inferred from a rendered page.

    .venv/bin/python tests/test_autolayout.py
"""

from __future__ import annotations

import ast
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agentic_controller.architect import (  # noqa: E402
    plan_to_schema,
    validate_layout,
    validate_schema,
    write_plan_schema,
)
from document_builder.autolayout import (  # noqa: E402
    A4_LANDSCAPE,
    A4_PORTRAIT,
    MARGIN_PX,
    MAX_LABEL_CHARS,
    Block,
    _short_label,
    blocks_from_conversion,
    fit_text,
    ink_extent,
    layout_source,
    page_geometry,
    place,
    value_fields,
)
from html_engine.monochrome import find_violations  # noqa: E402
from information_extraction.conversion import load_conversion  # noqa: E402
from information_extraction.extractor import build_data  # noqa: E402

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "citizenship_conversion.json"

_WORKDIR: Path | None = None
_cache: dict[str, object] = {}


def _blocks() -> list[Block]:
    """The fixture's blocks, parsed once — every case reads the same 39."""
    if "blocks" not in _cache:
        _cache["blocks"] = blocks_from_conversion(load_conversion(FIXTURE))
    return _cache["blocks"]  # type: ignore[return-value]


def _placed():
    if "placed" not in _cache:
        blocks = _blocks()
        _cache["placed"] = place(blocks, page_geometry(blocks))
    return _cache["placed"]


def _plan() -> dict[str, dict[str, object]]:
    """A stand-in for ``architect.plan_blocks``, so no model is called.

    Every third text block becomes a value, which is enough to exercise the
    field-bearing emission path and the schema round trip.
    """
    plan: dict[str, dict[str, object]] = {}
    for i, block in enumerate(_placed()):
        if block.kind == "Picture":
            plan[block.block_id] = {"role": "placeholder", "label": block.alt or "Image"}
        elif i % 3 == 0:
            plan[block.block_id] = {
                "role": "value",
                "field": f"field_{i}",
                "description": f"Value at block {i}",
                "text": block.text,
            }
        else:
            plan[block.block_id] = {"role": "static", "text": block.text}
    return plan


def _synthetic(boxes: list[tuple[float, float, float, float]]) -> list[Block]:
    return [
        Block(block_id=f"/page/0/Text/{i}", kind="Text", bbox=b, text="x")
        for i, b in enumerate(boxes)
    ]


# ── Parsing ───────────────────────────────────────────────────────

def test_the_whole_page_is_parsed():
    """34 Text + 5 Picture. A dropped block is content silently lost."""
    blocks = _blocks()
    kinds = [b.kind for b in blocks]
    assert len(blocks) == 39, len(blocks)
    assert kinds.count("Text") == 34, kinds.count("Text")
    assert kinds.count("Picture") == 5, kinds.count("Picture")


def test_picture_alt_does_not_become_prose():
    """
    An ``<img alt="...">`` stripped of tags leaves a sentence describing the
    picture, which would render as a paragraph where the picture belongs.
    """
    pictures = [b for b in _blocks() if b.kind == "Picture"]
    assert all(b.text == "" for b in pictures), [b.text for b in pictures if b.text]
    assert any("seal" in b.alt.lower() for b in pictures)


def test_blocks_without_geometry_are_dropped():
    """A block with no usable bbox contributes nothing and skews the extent."""
    conversion = {
        "children": [
            {
                "children": [
                    {"id": "a", "block_type": "Text", "bbox": [0, 0, 10, 10], "html": "a"},
                    {"id": "b", "block_type": "Text", "html": "no bbox"},
                    {"id": "c", "block_type": "Text", "bbox": [5, 5, 5, 9], "html": "flat"},
                    {"id": "d", "block_type": "Text", "bbox": [0, 0, 9, 9], "html": " "},
                ]
            }
        ]
    }
    assert [b.block_id for b in blocks_from_conversion(conversion)] == ["a"]


# ── Geometry ──────────────────────────────────────────────────────

def test_extent_is_the_ink_not_the_page():
    """
    The conversion page is 1372x980 around ink that is 1201x799. Normalizing
    against the page would bake Datalab's own padding into the A4 sheet.
    """
    assert ink_extent(_blocks()) == (13.0, 24.0, 1214.0, 823.0)


def test_the_sheet_is_exactly_a4():
    geometry = page_geometry(_blocks())
    assert (geometry.page_width, geometry.page_height) == A4_LANDSCAPE
    assert abs(geometry.aspect - 1.4142) < 0.001, geometry.aspect


def test_orientation_follows_the_source():
    """A tall document must not be letterboxed onto a landscape sheet."""
    tall = page_geometry(_synthetic([(0, 0, 100, 300), (10, 20, 90, 280)]))
    assert not tall.landscape
    assert (tall.page_width, tall.page_height) == A4_PORTRAIT

    wide = page_geometry(_synthetic([(0, 0, 300, 100), (10, 20, 280, 90)]))
    assert wide.landscape
    assert (wide.page_width, wide.page_height) == A4_LANDSCAPE


def test_one_scale_for_both_axes():
    """
    The aspect-ratio guarantee, asserted at its source. Two factors would fit
    the sheet exactly and stretch the document doing it.
    """
    geometry = page_geometry(_blocks())
    x0, y0, x1, y1 = geometry.extent
    placed = _placed()

    widths = [(p.box_width, p.bbox[2] - p.bbox[0]) for p in placed if p.box_width > 0]
    heights = [(p.box_height, p.bbox[3] - p.bbox[1]) for p in placed if p.box_height > 0]
    factors = [round(out / src, 6) for out, src in widths + heights]
    assert len(set(factors)) == 1, sorted(set(factors))[:5]
    assert factors[0] == round(geometry.scale, 6)


def test_the_fit_is_centred_and_inside_the_margin():
    """Nothing may sit where a printer's unprintable edge would clip it."""
    geometry = page_geometry(_blocks())
    placed = _placed()

    left = min(p.left for p in placed)
    top = min(p.top for p in placed)
    right = max(p.left + p.box_width for p in placed)
    bottom = max(p.top + p.box_height for p in placed)

    assert left >= MARGIN_PX - 0.01, left
    assert top >= MARGIN_PX - 0.01, top
    assert right <= geometry.page_width - MARGIN_PX + 0.01, right
    assert bottom <= geometry.page_height - MARGIN_PX + 0.01, bottom

    # Centred: the slack the uniform scale leaves is split evenly.
    assert abs(left - (geometry.page_width - right)) < 0.01
    assert abs(top - (geometry.page_height - bottom)) < 0.01


def test_relative_position_survives_the_trip():
    """A label left of its value on the scan stays left of it on the sheet."""
    by_id = {p.block_id: p for p in _placed()}
    label, value = by_id["/page/0/Text/8"], by_id["/page/0/Text/9"]
    assert label.left < value.left
    assert abs(label.top - value.top) < 1.0, (label.top, value.top)

    header, body = by_id["/page/0/Text/2"], by_id["/page/0/Text/7"]
    assert header.top < body.top


def test_placement_is_reading_order():
    placed = _placed()
    keys = [(round(p.top, 1), round(p.left, 1)) for p in placed]
    assert keys == sorted(keys)


def test_geometry_is_deterministic():
    """Same scan, same layout — the reason this half is not a model call."""
    blocks = blocks_from_conversion(load_conversion(FIXTURE))
    again = place(blocks, page_geometry(blocks))
    assert [(p.block_id, p.left, p.top, p.font_size) for p in again] == [
        (p.block_id, p.left, p.top, p.font_size) for p in _placed()
    ]


def test_an_empty_page_is_refused_not_guessed():
    try:
        page_geometry([])
    except ValueError:
        return
    raise AssertionError("page_geometry accepted an empty block list")


# ── Text fitting ──────────────────────────────────────────────────

def test_font_comes_from_the_line_box():
    """The bbox is the line box; glyphs are roughly 62 % of it."""
    value = next(p for p in _placed() if p.block_id == "/page/0/Text/9")
    assert abs(value.font_size - round(value.box_height * 0.62, 1)) < 0.15


def test_a_long_string_is_shrunk_to_fit():
    """A translated label runs longer than the Devanagari it replaces."""
    block = next(p for p in _placed() if p.text)
    roomy = fit_text(block, chars=1)
    cramped = fit_text(block, chars=400)
    assert roomy.font_size == block.font_size
    assert cramped.font_size < block.font_size
    assert cramped.font_size >= 8.0


def test_a_caption_is_cut_to_the_box():
    """Datalab's alt is a full sentence and overflows the box it labels."""
    long_alt = (
        "A color photograph of a man with short black hair, wearing a dark suit"
    )
    assert _short_label(long_alt) == "A color photograph of a man"
    assert len(_short_label(long_alt)) <= MAX_LABEL_CHARS
    # A leading fragment is not a caption — clip on a word instead. "A small"
    # is all the first clause holds, so the whole text is word-clipped.
    fragment = "A small, square, textured object, possibly a piece of paper"
    assert _short_label(fragment) == "A small, square, textured"
    assert _short_label("") == "Image"


def test_a_seal_is_round_and_a_photo_box_is_not():
    """
    Shape follows whichever the caption mentions *first*: a caption names its
    subject before saying where the subject sits, so "a red circular stamp
    overlapping the photo" is a circle, not a photo box.
    """
    source = layout_source(_placed(), _plan(), "probe", page_geometry(_blocks()))
    shapes = {
        block_id: shape
        for block_id, shape in _shapes(source)
    }
    assert shapes["/page/0/Picture/0"] == "circle", shapes  # "Red circular ... seal"
    assert shapes["/page/0/Picture/6"] == "rect", shapes    # "A rectangular box ..."
    assert shapes["/page/0/Picture/36"] == "rect", shapes   # "A color photograph ..."
    assert shapes["/page/0/Picture/38"] == "circle", shapes  # "A red circular ... stamp"


def _shapes(source: str):
    """``(block_id, shape)`` for every PlaceholderBox in emitted source."""
    block_id = None
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("doc.add(  #"):
            block_id = stripped.split("#", 1)[1].strip()
        elif stripped.startswith("shape=") and block_id:
            yield block_id, stripped.split("'")[1]


# ── Emission ──────────────────────────────────────────────────────

def test_emitted_source_is_a_layout_module():
    source = layout_source(_placed(), _plan(), "probe", page_geometry(_blocks()))
    tree = ast.parse(source)
    functions = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    assert functions == ["build_probe"], functions
    assert 'PAGE_WIDTH = "1123px"' in source
    assert 'PAGE_HEIGHT = "794px"' in source
    # Every block is emitted, none dropped, each traceable to its source block.
    for block in _placed():
        assert f"# {block.block_id}\n" in source, block.block_id


def test_values_bind_through_field_not_a_private_helper():
    """``field=`` is what makes a box editable and extractable."""
    plan = _plan()
    source = layout_source(_placed(), plan, "probe", page_geometry(_blocks()))
    for name in value_fields(plan):
        assert f"field={name!r}" in source, name
        assert f"d[{name!r}]" in source, name
    assert "_ea(" not in source


def test_static_text_is_baked_in_and_never_becomes_a_field():
    plan = _plan()
    source = layout_source(_placed(), plan, "probe", page_geometry(_blocks()))
    statics = [
        entry["text"]
        for entry in plan.values()
        if entry["role"] == "static" and entry["text"]
    ]
    assert statics
    for text in statics[:5]:
        assert repr(text) in source, text


def test_an_unplanned_block_still_renders():
    """
    Dropping it would lose content the scan clearly had, and the agent
    reviewing the render cannot ask back for something it cannot see.
    """
    source = layout_source(_placed(), {}, "probe", page_geometry(_blocks()))
    ast.parse(source)
    for block in _placed():
        assert f"# {block.block_id}\n" in source, block.block_id
    assert "FIELDS: tuple[str, ...] = ()" in source


def test_the_emitted_layout_passes_the_gate():
    """
    The four gates end in a live blank-data render, so this is the same check
    ``build_from_geometry`` makes before it promotes anything.
    """
    assert _WORKDIR is not None
    plan = _plan()
    layout_path = _WORKDIR / "probe_layout.py"
    layout_path.write_text(
        layout_source(_placed(), plan, "probe", page_geometry(_blocks())),
        encoding="utf-8",
    )
    schema_path = write_plan_schema(plan, "probe", path=_WORKDIR / "probe.json")

    ok_schema, schema_message = validate_schema(schema_path)
    assert ok_schema, schema_message

    ok, message = validate_layout(layout_path, "probe", schema_path)
    assert ok, message
    assert "renders" in message, message


def test_every_field_survives_extraction():
    """
    ``build_data`` keeps only what the schema lists as required, so a field the
    layout renders but the schema omits is permanently blank.
    """
    plan = _plan()
    schema = plan_to_schema(plan, "probe")
    fields = value_fields(plan)
    assert fields
    assert set(fields) <= set(schema["required"]), set(fields) - set(schema["required"])
    assert set(schema["properties"]) == set(schema["required"])

    extracted = {name: f"v-{name}" for name in fields}
    assert build_data(extracted, schema) == extracted


def test_extraction_null_required_fields_become_empty_strings():
    schema = {"required": ["present", "missing"]}
    assert build_data({"present": "value", "missing": None}, schema) == {
        "present": "value",
        "missing": "",
    }


def test_the_generated_page_is_monochrome():
    """The project rule holds for generated layouts too, not just written ones."""
    assert _WORKDIR is not None
    plan = _plan()
    path = _WORKDIR / "mono_layout.py"
    path.write_text(
        layout_source(_placed(), plan, "mono", page_geometry(_blocks())), encoding="utf-8"
    )

    namespace: dict[str, object] = {}
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), namespace)
    html = namespace["build_mono"]({}).render()  # type: ignore[operator]

    assert not find_violations(html), find_violations(html)[:5]


def test_the_rendered_page_is_the_a4_it_claims():
    assert _WORKDIR is not None
    path = _WORKDIR / "size_layout.py"
    path.write_text(
        layout_source(_placed(), _plan(), "size", page_geometry(_blocks())),
        encoding="utf-8",
    )
    namespace: dict[str, object] = {}
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), namespace)
    html = namespace["build_size"]({}).render()  # type: ignore[operator]

    assert "1123px" in html and "794px" in html
    assert json.dumps(A4_LANDSCAPE)  # the constant the assertion above encodes


def _run() -> int:
    global _WORKDIR
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = 0
    _WORKDIR = Path(tempfile.mkdtemp(prefix="autolayout_"))
    try:
        for test in tests:
            try:
                test()
            except Exception as exc:
                failures += 1
                print(f"FAIL {test.__name__}: {type(exc).__name__}: {exc}")
            else:
                print(f"ok   {test.__name__}")
    finally:
        shutil.rmtree(_WORKDIR, ignore_errors=True)
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(_run())
