"""
Regression tests for the black-and-white output rule.

The rule is only worth having if it cannot be bypassed, so most of these
tests are adversarial: they try to smuggle colour through each route CSS can
reach the page and assert that none of them work.

Run:  python -m pytest tests/test_monochrome.py -q
      python tests/test_monochrome.py          (no pytest needed)
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from document_builder.registry import DOCUMENTS
from html_engine import Div, Document, Style, Text
from html_engine.monochrome import (
    BLACK,
    WHITE,
    find_violations,
    normalize_value,
)


def test_ink_goes_black_surfaces_go_white():
    assert normalize_value("color", "#2d55ae") == BLACK
    assert normalize_value("color", "red") == BLACK
    assert normalize_value("border", "1.8px dashed #4a90d9") == f"1.8px dashed {BLACK}"
    assert normalize_value("background", "#2d55ae") == WHITE
    assert normalize_value("background-color", "rgba(0,0,0,0.2)") == WHITE


def test_non_colour_values_are_untouched():
    """Sizes must survive — a border-radius is not a colour."""
    assert normalize_value("height", "70px") == "70px"
    assert normalize_value("border-radius", "70px") == "70px"
    assert normalize_value("font-family", '"Times New Roman", serif') == (
        '"Times New Roman", serif'
    )


def test_transparent_is_preserved():
    """Rewriting transparent to white would paint over content."""
    assert normalize_value("background", "transparent") == "transparent"
    assert normalize_value("border", "none") == "none"
    assert normalize_value("color", "inherit") == "inherit"


def test_document_text_is_never_corrupted():
    """A '#333' inside author text is data, not a colour."""
    from html_engine.monochrome import normalize_html

    html = '<p style="color:#e02922">रु. #333 मात्र</p>'
    out = normalize_html(html)
    assert "रु. #333 मात्र" in out
    assert "#e02922" not in out


def test_url_fragments_survive():
    assert normalize_value("background-image", "url(/a#frag.png)") == "url(/a#frag.png)"


def test_every_registered_layout_renders_monochrome():
    for name, cfg in DOCUMENTS.items():
        schema = json.loads(pathlib.Path(cfg["schema"]).read_text(encoding="utf-8"))
        data = {
            key: ([] if spec.get("type") == "array"
                  else {} if spec.get("type") == "object"
                  else f"{key}-demo")
            for key, spec in schema.get("properties", {}).items()
        }
        html = cfg["builder"](data).render()
        assert find_violations(html) == [], f"{name} leaked colour"


def test_all_bypass_routes_are_closed():
    """Style.raw, attrs['style'], extra_css, and Document(background=...)."""
    doc = Document(
        "adversarial",
        background="#e02922",
        extra_css=".x{color:#ff0000;background:navy}",
    )
    doc.add(Text("a", style=Style(color="#ff0000")))
    doc.add(Text("b", style=Style(raw="color:#00ff00;background:red")))
    doc.add(Div(Text("c"), attrs={"style": "color:rgb(255,0,0);border:1px solid teal"}))

    html = doc.render()
    assert find_violations(html) == []
    for token in ("#e02922", "#ff0000", "#00ff00", "navy", "teal", "rgb(255,0,0)"):
        assert token not in html, f"{token} leaked"


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as exc:
            failures += 1
            print(f"  FAIL  {name}: {exc}")
    print("\nall green" if not failures else f"\n{failures} failure(s)")
    sys.exit(1 if failures else 0)
