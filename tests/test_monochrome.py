"""
Tests for the monochrome guarantee.

Project rule: a rendered document is purely black and white — ink ``#000000``,
surfaces ``#ffffff``. It is enforced structurally rather than by convention,
because the Architect Agent writes layouts unattended. This suite covers each
route CSS can take to the page, so a new route added without normalization
fails here instead of shipping colour.

Run directly, no pytest needed:

    .venv/bin/python tests/test_monochrome.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from html_engine import Document, Style, Text  # noqa: E402
from html_engine.monochrome import (  # noqa: E402
    BLACK,
    WHITE,
    find_violations,
    normalize_declarations,
    normalize_html,
    normalize_value,
)


def test_ink_goes_black_surfaces_go_white():
    assert normalize_value("color", "#4a90d9") == BLACK
    assert normalize_value("border-top", "1.8px solid crimson") == f"1.8px solid {BLACK}"
    assert normalize_value("background", "#eef") == WHITE
    assert normalize_value("background-color", "rgb(12, 40, 200)") == WHITE


def test_target_depends_on_property_not_luminance():
    """
    Thresholding by luminance would map a dark fill to black and its light text
    to white, or the reverse, and the two collide into an unreadable block.
    Pinning by property guarantees contrast for any input.
    """
    dark_fill = normalize_value("background-color", "#0b0b0b")
    light_text = normalize_value("color", "#f8f8f8")
    assert dark_fill == WHITE and light_text == BLACK, (dark_fill, light_text)


def test_every_named_colour_is_recognised():
    """
    A curated subset leaked ``rebeccapurple``. Any name the regex misses passes
    through as real colour, so the list has to be complete.
    """
    for name in ["rebeccapurple", "navajowhite", "darkslategray", "mediumvioletred"]:
        assert normalize_value("color", name) == BLACK, name


def test_longest_name_wins_over_prefix():
    """
    Alternation is scanned left to right. With "red" ordered before
    "rebeccapurple" the regex matches "red" and leaves "beccapurple" as text.
    """
    assert normalize_value("color", "rebeccapurple") == BLACK
    assert normalize_value("color", "lightgoldenrodyellow") == BLACK


def test_transparent_and_keywords_survive():
    """Rewriting transparent to white paints over content meant to show through."""
    for keep in ["transparent", "currentColor", "inherit", "initial", "unset", "none"]:
        assert normalize_value("background", keep) == keep, keep


def test_author_text_is_not_touched():
    """Corrupting document data is worse than leaking a colour."""
    assert normalize_value("content", '"#5 gold"') == '"#5 gold"'
    assert normalize_value("font-family", '"Times New Roman", serif') == (
        '"Times New Roman", serif'
    )


def test_url_contents_are_protected():
    """A url(...) may hold a "#" fragment that is not a colour."""
    value = "url(crest#gold.png) no-repeat"
    assert normalize_value("background", value) == value


def test_selector_is_not_mistaken_for_a_property():
    css = normalize_declarations("a:hover { color: red; }")
    assert "a:hover" in css, css
    assert BLACK in css and "red" not in css, css


def test_route_1_style_to_css():
    assert Style(color="#4a90d9").to_css() == f"color:{BLACK}"


def test_route_2_raw_style_string_in_attrs():
    """A component can carry a hand-written style attribute, bypassing Style."""
    html = Text("x", attrs={"style": "color:#ff0000"}).to_html()
    assert "#ff0000" not in html, html
    assert BLACK in html, html


def test_route_3_style_raw_escape_hatch():
    css = Style(raw="box-shadow: 0 0 4px #123456").to_css()
    assert "#123456" not in css, css
    assert BLACK in css, css


def test_route_4_renderer_style_block_and_extra_css():
    doc = Document(
        "t",
        background="#fafad2",
        extra_css=".x { color: seagreen; border: 1px solid #abc; }",
    )
    doc.add(Text("body text"))
    html = doc.render()
    for leak in ["#fafad2", "seagreen", "#abc"]:
        assert leak not in html, f"{leak} survived into the render"


def test_route_4_hardcoded_to_html_fstring():
    """
    A component's own ``to_html()`` can hardcode a style the engine never sees
    as a Style object. The renderer pass is the net that catches it.
    """

    class Rogue(Text):
        def to_html(self) -> str:
            return '<div style="color:#ff00ff">rogue</div>'

    doc = Document("t")
    doc.add(Rogue("x"))
    assert "#ff00ff" not in doc.render()


def test_all_bypass_routes_are_closed():
    """One document exercising every route at once, audited by find_violations."""
    doc = Document("audit", background="lightblue", extra_css="p { color: tomato; }")
    doc.add(Text("a", style=Style(color="#4a90d9", raw="outline: 1px solid gold")))
    doc.add(Text("b", attrs={"style": "background:#333"}))
    html = doc.render()

    assert not find_violations(html), find_violations(html)


def test_normalize_html_leaves_body_text_alone():
    html = '<p style="color:red">Plot #4a90d9 is gold</p>'
    out = normalize_html(html)
    assert "Plot #4a90d9 is gold" in out, out
    assert 'style="color:#000000"' in out, out


def test_find_violations_reports_pairs():
    assert find_violations("margin:0;color:#000000;background:#ffffff") == []
    assert ("color", "red") in find_violations("color:red")


def test_registered_layouts_render_monochrome():
    """The guarantee that actually matters: every shipped document type."""
    from document_builder.registry import DOCUMENTS

    for name, config in DOCUMENTS.items():
        html = config["builder"]({}).render()
        leaks = find_violations(html)
        assert not leaks, f"{name}: {leaks[:5]}"


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
