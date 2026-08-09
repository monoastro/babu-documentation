"""
Tests for the open property bag that replaced the closed ``Style`` dataclass.

The bug this suite exists to prevent: a layout used ``user_select`` and the
whole pipeline died with ``Style.__init__() got an unexpected keyword argument
'user_select'``. Layouts are written by the Architect Agent from general CSS
knowledge, not from a list somebody remembered to enumerate, so an unlisted
property has to render rather than crash.

Run directly, no pytest needed:

    .venv/bin/python tests/test_styles.py
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from html_engine.styles import Style, StyleWarning  # noqa: E402


def test_unlisted_property_renders():
    """The reported crash. Any valid CSS property must survive to the output."""
    css = Style(user_select="none").to_css()
    assert css == "user-select:none", css

    # A sample of properties the old allowlist did not carry.
    for kwarg, expected in [
        ("pointer_events", "pointer-events"),
        ("backdrop_filter", "backdrop-filter"),
        ("scroll_margin_top", "scroll-margin-top"),
        ("aspect_ratio", "aspect-ratio"),
    ]:
        out = Style(**{kwarg: "inherit"}).to_css()
        assert out == f"{expected}:inherit", out


def test_underscores_become_hyphens():
    assert Style(font_weight="bold").to_css() == "font-weight:bold"


def test_vendor_prefix_and_custom_property():
    """Both are deliberate, so neither should look like a typo."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", StyleWarning)
        assert Style(_webkit_line_clamp="3").to_css() == "-webkit-line-clamp:3"
        assert Style(**{"--brand-gap": "4px"}).to_css() == "--brand-gap:4px"


def test_typo_warns_but_does_not_raise():
    """
    The trade for accepting anything: a misspelling is no longer a TypeError.
    It has to be *visible* instead — in a run log, and promotable to an error
    with ``main.py --strict``.
    """
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        css = Style(fnot_size="12px").to_css()
    assert css == "fnot-size:12px", css
    assert len(caught) == 1, caught
    assert issubclass(caught[0].category, StyleWarning)
    assert "fnot_size" in str(caught[0].message)


def test_strict_mode_promotes_the_warning():
    """What ``main.py --strict`` relies on."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", StyleWarning)
        try:
            Style(fnot_size="12px")
        except StyleWarning:
            pass
        else:
            raise AssertionError("--strict did not turn the warning into an error")


def test_unusable_name_raises():
    """A name CSS could never accept is a bug worth stopping for."""
    for bad in ["9lives", "font size", "colour;color"]:
        try:
            Style(**{bad: "x"})
        except ValueError:
            continue
        raise AssertionError(f"{bad!r} was accepted as a property name")


def test_shorthand_precedes_longhand():
    """
    CSS resolves duplicates last-one-wins, so ``margin`` emitted after
    ``margin-top`` would silently erase the specific value. Declaration order
    is a correctness concern, not cosmetics.
    """
    css = Style(margin_top="5px", margin="0").to_css()
    assert css.index("margin:") < css.index("margin-top:"), css


def test_none_is_dropped_not_rendered():
    assert Style(color=None, margin="0").to_css() == "margin:0"


def test_unset_property_reads_as_none():
    style = Style(margin="0")
    assert style.margin == "0"
    assert style.z_index is None


def test_merge_overrides_and_concatenates_raw():
    base = Style(margin="0", color="#000000", raw="a:1")
    over = Style(margin="4px", raw="b:2")
    merged = base.merge(over)
    assert merged.margin == "4px"
    assert merged.color == "#000000"
    # Raw fragments accumulate. Replacing them would drop whichever side lost.
    css = merged.to_css()
    assert "a:1" in css and "b:2" in css, css
    # Neither input was mutated.
    assert base.margin == "0"


def test_merge_with_none_returns_self_equivalent():
    assert Style(margin="0").merge(None).to_css() == "margin:0"


def test_clone_removes_with_none():
    original = Style(margin="0", color="#000000")
    stripped = original.clone(color=None)
    assert stripped.to_css() == "margin:0"
    assert original.color == "#000000"


def test_to_attr_is_empty_when_no_properties():
    assert Style().to_attr() == ""
    assert Style(margin="0").to_attr() == ' style="margin:0"'


def test_to_css_normalizes_colour():
    """Monochrome is enforced on the way out, including for unlisted props."""
    assert Style(color="#4a90d9").to_css() == "color:#000000"
    assert Style(background="red").to_css() == "background:#ffffff"
    assert Style(outline_color="rebeccapurple").to_css() != "outline-color:rebeccapurple"


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
