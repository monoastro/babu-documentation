"""
Tests for the components added for this project's documents, and for the
``field=`` editability contract they share.

The placeholder components exist because a source scan carries a photo, a seal,
an embossed crest, a signature — none of which survive OCR and none of which
should be invented. An outline in the right place at the right size lets the
vision verifier compare *layout* instead of reporting a missing seal as lost
content.

Run directly, no pytest needed:

    .venv/bin/python tests/test_components.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from html_engine import (  # noqa: E402
    Div,
    Document,
    FlexRow,
    FlexCol,
    Heading,
    LabelValue,
    ListItem,
    PlaceholderBox,
    SignatureBlock,
    Spacer,
    Style,
    TableCell,
    Text,
    Watermark,
    corner_box,
    editable_attrs,
)


def test_editable_attrs_is_the_single_source_of_the_contract():
    assert editable_attrs("plots.0.plot_no") == {
        "contenteditable": "true",
        "data-field": "plots.0.plot_no",
    }


def test_field_makes_a_component_editable():
    html = Text("x", field="ref_no").to_html()
    assert 'contenteditable="true"' in html, html
    assert 'data-field="ref_no"' in html, html


def test_explicit_attrs_win_over_field():
    """
    ``field=`` uses setdefault, so a layout that needs a non-editable but
    labelled node can still say so.
    """
    html = Text("x", field="ref_no", attrs={"contenteditable": "false"}).to_html()
    assert 'contenteditable="false"' in html, html
    assert 'data-field="ref_no"' in html, html


def test_field_passthrough_across_component_families():
    """
    Every container a layout might hang a value on has to accept ``field=``,
    or the layout falls back to hand-built attrs and the contract drifts.
    """
    for component in [
        Text("v", field="f"),
        Heading("v", field="f"),
        Div(field="f"),
        FlexRow(field="f"),
        TableCell("v", field="f"),
        ListItem("v", field="f"),
        PlaceholderBox("v", field="f"),
    ]:
        html = component.to_html()
        assert 'data-field="f"' in html, type(component).__name__


def test_labelvalue_field_lands_on_the_value_not_the_label():
    """The label is chrome; only the value is extracted data."""
    html = LabelValue("Ref. No.:", "084/85", field="ref_no").to_html()
    assert 'data-field="ref_no"' in html, html
    # The editable span must not swallow the label, or a browser edit writes
    # "Ref. No.: 084/85" back into the field.
    before_field = html[: html.index("data-field")]
    assert "Ref. No.:" in before_field, html


def test_placeholder_size_sets_both_dimensions():
    css = PlaceholderBox("Photo", size="110px").to_html()
    assert "width:110px" in css and "height:110px" in css, css


def test_placeholder_circle_uses_percent_radius():
    """A fixed pixel radius would not stay elliptical on a non-square box."""
    html = PlaceholderBox("Seal", size="98px", shape="circle").to_html()
    assert "border-radius:50%" in html, html


def test_placeholder_dashed_marks_human_supplied():
    """Dashed = a human still has to supply it. Solid = the document has it."""
    assert "dashed" in PlaceholderBox("(Signed)", dashed=True).to_html()
    assert "solid" in PlaceholderBox("Office Seal").to_html()


def test_placeholder_caption_wraps_instead_of_spilling():
    html = PlaceholderBox("A very long caption", size="60px").to_html()
    assert "overflow:hidden" in html, html
    assert "box-sizing:border-box" in html, html


def test_watermark_is_inert():
    """
    Three properties separate a watermark from a heading: it sits behind, it
    never intercepts a click meant for a field under it, and it never lands in
    the user's selection when they copy a paragraph.
    """
    html = Watermark("Clock Tower").to_html()
    for required in ["z-index:0", "pointer-events:none", "user-select:none"]:
        assert required in html, required


def test_watermark_centres_on_its_own_midpoint():
    html = Watermark("x").to_html()
    assert "translate(-50%, -50%)" in html, html


def test_watermark_rotation_composes_with_the_centring():
    html = Watermark("x", rotate=-30).to_html()
    assert "translate(-50%, -50%) rotate(-30deg)" in html, html


def test_signature_block_stacks_every_part():
    html = SignatureBlock(
        name="Ram Bahadur",
        title="Campus Chief",
        signature_label="(Signed)",
        stamp_label="Office Seal",
        name_field="signed_name",
        title_field="position",
    ).to_html()
    for part in ["(Signed)", "Ram Bahadur", "Campus Chief", "Office Seal"]:
        assert part in html, part
    assert 'data-field="signed_name"' in html, html
    assert 'data-field="position"' in html, html
    # Order: signing space, then name, then title, then stamp.
    assert html.index("(Signed)") < html.index("Ram Bahadur") < html.index("Office Seal")


def test_signature_block_parts_are_optional():
    html = SignatureBlock(name="Ram Bahadur").to_html()
    assert "Ram Bahadur" in html
    assert "border-radius:50%" not in html, "a stamp was drawn without a stamp_label"


def test_corner_box_places_by_corner_name():
    for corner, expected in [
        ("top-left", ("top:", "left:")),
        ("bottom-right", ("bottom:", "right:")),
    ]:
        html = corner_box("Crest", corner=corner, offset="18px").to_html()
        for side in expected:
            assert f"{side}18px" in html, (corner, side, html)


def test_corner_box_carries_the_field_to_the_caption():
    html = corner_box("QR Code", field="qr_placeholder").to_html()
    assert 'data-field="qr_placeholder"' in html, html


def test_spacer_gutter_is_not_squeezed_away():
    """A horizontal spacer inside a flex row needs flex-shrink:0 to survive."""
    assert "flex-shrink:0" in Spacer(width="20px").to_html()


def test_clip_false_lets_overflow_show():
    """
    A clipped overflow and a genuinely missing section look identical in the
    rendered PNG, and the verifier reports both as lost content.
    """
    body = Text("x")
    clipped = Document("t", page_height="800px")
    clipped.add(body)
    assert "overflow:hidden" in clipped.render()

    spilling = Document("t", page_height="800px", clip=False)
    spilling.add(body)
    assert "overflow:hidden" not in spilling.render()


def test_document_save_creates_parent_directories(tmp_name="output/_test_nested"):
    import shutil

    target = Path(tmp_name) / "deep" / "page.html"
    try:
        doc = Document("t")
        doc.add(Text("x"))
        written = doc.save(target)
        assert written.is_file(), written
        assert written.read_text(encoding="utf-8").startswith("<!DOCTYPE html>")
    finally:
        shutil.rmtree(Path(tmp_name), ignore_errors=True)


def test_container_coerces_a_bare_string_to_text():
    # A generated layout wrote Div("(Signed)"). The string used to be stored
    # unchanged and then blew up during rendering with
    # "'str' object has no attribute 'to_html'", naming neither the layout nor
    # the container. A bare string is unambiguous, so coerce it.
    html = Div("(Signed)").to_html()
    assert "(Signed)" in html, html


def test_container_coerces_numbers():
    assert "7" in FlexRow(7).to_html()
    assert "1.5" in FlexRow(1.5).to_html()


def test_container_skips_none_children():
    html = FlexCol(Text("a"), None, Text("b")).to_html()
    assert "a" in html and "b" in html
    assert "None" not in html, html


def test_container_rejects_a_list_with_position_and_type():
    # A list is a real mistake — the caller meant to splat it — so it raises
    # instead of coercing, and the message has to say where and what.
    try:
        FlexRow(Text("a"), ["b", "c"])
    except TypeError as exc:
        message = str(exc)
        assert "FlexRow" in message, message
        assert "position 1" in message, message
        assert "list" in message, message
    else:
        raise AssertionError("a list child should raise TypeError")


def test_container_rejects_a_dict_child():
    try:
        Div({"text": "hi"})
    except TypeError as exc:
        assert "dict" in str(exc), str(exc)
    else:
        raise AssertionError("a dict child should raise TypeError")


def test_container_rejects_a_bool_child():
    # bool is an int subclass, but rendering "True" onto an official document
    # is never what the caller meant.
    try:
        Div(True)
    except TypeError as exc:
        assert "bool" in str(exc), str(exc)
    else:
        raise AssertionError("a bool child should raise TypeError")


def test_add_coerces_like_the_constructor():
    assert "late" in Div().add("late").to_html()

    try:
        Div().add(object())
    except TypeError as exc:
        assert "Div" in str(exc), str(exc)
    else:
        raise AssertionError("add() should coerce with the same rules")


def test_document_add_coerces_and_names_itself():
    assert "heading text" in Document().add("heading text").render()

    try:
        Document().add(set())
    except TypeError as exc:
        assert "Document" in str(exc), str(exc)
    else:
        raise AssertionError("Document.add() should reject an unrenderable child")


def _run() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures += 1
            print(f"FAIL {test.__name__}: {type(exc).__name__}: {exc}")
        else:
            print(f"ok   {test.__name__}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(_run())
