"""
Style descriptor for the HTML Document Engine.

``Style`` is an **open** property bag, not a closed schema. Any CSS property
can be set, whether or not this module has heard of it::

    Style(user_select="none", backdrop_filter="blur(2px)")

That openness is deliberate. Layouts in this project are written by the
Architect Agent as well as by hand, and an agent writes CSS from its general
knowledge of CSS — not from whatever list somebody remembered to enumerate
here. When ``Style`` was a fixed dataclass, every unlisted property was a
``TypeError`` raised deep inside a builder, and the layout-validation gate
could not see it coming (the call sits inside ``build_<type>()``, which the
gate's import probe never executes). A missing property is a cosmetic gap;
crashing the pipeline over one is not.

The trade is that a typo (``font_wieght``) no longer raises — it would emit a
declaration the browser silently drops. So unrecognized names raise a
``StyleWarning`` instead: visible in a run log, fatal to nothing.
"""

from __future__ import annotations

import re
import warnings
from typing import Any, Iterator, Optional


class StyleWarning(UserWarning):
    """An unrecognized CSS property name reached ``Style``. Probably a typo."""


# Emission order for properties this module knows about.
#
# Order is load-bearing: CSS resolves duplicate declarations last-one-wins, so
# a shorthand must be emitted *before* its longhands or ``Style(margin="0",
# margin_top="5px")`` would collapse the top margin. Keyword order in the
# caller cannot be trusted to get that right, so it is ignored for known
# properties — they emit in the order below regardless of how they were passed.
# Unknown properties follow, in insertion order.
_KNOWN_ORDER: tuple[str, ...] = (
    # Typography
    "font", "font_family", "font_size", "font_weight", "font_style",
    "font_variant", "font_stretch", "font_feature_settings", "font_kerning",
    "color", "text_align", "text_align_last", "text_decoration",
    "text_decoration_color", "text_decoration_style", "text_indent",
    "text_overflow", "text_shadow", "text_transform", "line_height",
    "letter_spacing", "word_spacing", "white_space", "word_break",
    "overflow_wrap", "word_wrap", "hyphens", "tab_size", "vertical_align",
    "direction", "unicode_bidi", "writing_mode", "text_orientation",
    "font_synthesis", "text_rendering", "quotes",
    # Box model
    "box_sizing", "width", "height", "min_width", "max_width", "min_height",
    "max_height", "aspect_ratio",
    "padding", "padding_top", "padding_right", "padding_bottom",
    "padding_left", "padding_inline", "padding_block",
    "margin", "margin_top", "margin_right", "margin_bottom", "margin_left",
    "margin_inline", "margin_block",
    "border", "border_width", "border_style", "border_color",
    "border_top", "border_right", "border_bottom", "border_left",
    "border_top_width", "border_right_width", "border_bottom_width",
    "border_left_width", "border_top_style", "border_right_style",
    "border_bottom_style", "border_left_style", "border_top_color",
    "border_right_color", "border_bottom_color", "border_left_color",
    "border_radius", "border_top_left_radius", "border_top_right_radius",
    "border_bottom_left_radius", "border_bottom_right_radius",
    "border_collapse", "border_spacing",
    "outline", "outline_width", "outline_style", "outline_color",
    "outline_offset",
    # Background
    "background", "background_color", "background_image", "background_size",
    "background_position", "background_repeat", "background_attachment",
    "background_clip", "background_origin", "background_blend_mode",
    # Layout / positioning
    "display", "position", "top", "right", "bottom", "left", "inset",
    "z_index", "float", "clear", "visibility",
    "overflow", "overflow_x", "overflow_y",
    # Flexbox
    "flex", "flex_direction", "flex_wrap", "flex_flow", "flex_grow",
    "flex_shrink", "flex_basis", "order",
    "justify_content", "justify_items", "justify_self",
    "align_content", "align_items", "align_self",
    "place_content", "place_items", "place_self",
    "gap", "row_gap", "column_gap",
    # Grid
    "grid", "grid_template", "grid_template_columns", "grid_template_rows",
    "grid_template_areas", "grid_auto_flow", "grid_auto_columns",
    "grid_auto_rows", "grid_area", "grid_column", "grid_row",
    "grid_column_start", "grid_column_end", "grid_row_start", "grid_row_end",
    # Multi-column
    "columns", "column_count", "column_width", "column_rule", "column_span",
    # Tables
    "table_layout", "caption_side", "empty_cells",
    # Lists
    "list_style", "list_style_type", "list_style_position",
    "list_style_image",
    # Visual effects
    "box_shadow", "opacity", "transform", "transform_origin", "transition",
    "animation", "filter", "backdrop_filter", "mix_blend_mode", "isolation",
    "will_change", "clip_path", "mask",
    # Interaction
    "cursor", "pointer_events", "user_select", "touch_action", "resize",
    "caret_color", "appearance", "scroll_behavior",
    # Media
    "object_fit", "object_position", "image_rendering",
    # Paged media — load-bearing for print output
    "page_break_before", "page_break_after", "page_break_inside",
    "break_before", "break_after", "break_inside", "orphans", "widows",
    # Generated content / counters
    "content", "counter_reset", "counter_increment",
)

_KNOWN: frozenset[str] = frozenset(_KNOWN_ORDER)

# A property name CSS would plausibly accept: kebab or snake identifier,
# optionally vendor-prefixed (``-webkit-``) or a custom property (``--brand``).
_VALID_NAME = re.compile(r"^-{0,2}[a-zA-Z][a-zA-Z0-9_-]*$")

def _css_name(attr: str) -> str:
    """Map a Python keyword to its CSS property name.

    ``font_size`` -> ``font-size``. A leading underscore becomes a leading
    hyphen, which is how a vendor prefix is spelled as a Python keyword:
    ``_webkit_user_select`` -> ``-webkit-user-select``. Names that are already
    CSS-shaped (passed through ``**{"--brand": "..."}``) survive unchanged.
    """
    if attr.startswith("--"):
        return attr
    return attr.replace("_", "-")


class Style:
    """
    An open set of CSS declarations.

    Any keyword is accepted and emitted as a CSS property. Unset properties are
    simply absent from the output, so you only declare what you care about::

        bold = Style(font_weight="bold")
        big = Style(font_size="28px")
        both = bold.merge(big)          # font-weight:bold;font-size:28px
        print(both.to_css())

    Reading an unset property gives ``None`` rather than raising, so
    ``style.filter`` is safe on a Style that never set ``filter``.

    Values are stringified on the way out, so numbers are fine for unitless
    properties::

        Style(z_index=5, opacity=0.5, flex_grow=1)

    Parameters:
        **props: CSS properties as Python keywords. ``raw`` is reserved — its
            value is appended verbatim (still colour-normalized) after every
            other declaration.
    """

    __slots__ = ("_props",)

    def __init__(self, **props: Any):
        self._props: dict[str, Any] = {}
        for name, value in props.items():
            self._set(name, value)

    # ── internals ───────────────────────────────────────────────

    def _set(self, name: str, value: Any) -> None:
        """Record one declaration, warning if the property looks misspelled."""
        if value is None:
            return  # An explicit None means "unset" — same as never passing it.
        if name != "raw" and name not in _KNOWN:
            if not _VALID_NAME.match(name.replace("_", "-")):
                raise ValueError(
                    f"{name!r} is not a usable CSS property name."
                )
            # A vendor prefix (``_webkit_``) or custom property (``--brand``)
            # is spelled deliberately; only a bare unknown name is typo-shaped.
            if name.startswith("_") or name.startswith("--"):
                self._props[name] = value
                return
            warnings.warn(
                f"Unrecognized CSS property {name!r} "
                f"(emitted as {_css_name(name)!r}). If that is a typo the "
                f"browser will drop the declaration silently.",
                StyleWarning,
                stacklevel=4,
            )
        self._props[name] = value

    def __getattr__(self, name: str) -> Any:
        # Only reached when normal lookup fails, so this never shadows a real
        # method. Unset properties read as None.
        if name.startswith("__"):
            raise AttributeError(name)
        return self._props.get(name)

    def __bool__(self) -> bool:
        return bool(self._props)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Style) and self._props == other._props

    def __repr__(self) -> str:
        inner = ", ".join(f"{k}={v!r}" for k, v in self._props.items())
        return f"Style({inner})"

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        """Iterate ``(python_name, value)`` for every set property."""
        return iter(self._props.items())

    def _ordered(self) -> list[tuple[str, Any]]:
        """Set properties in emission order: known first, then unknown.

        Known properties emit in ``_KNOWN_ORDER``, which puts each shorthand
        ahead of its longhands. Without that, ``Style(margin="0",
        margin_top="5px")`` would depend on keyword order to survive CSS's
        last-one-wins rule.
        """
        known = [(n, self._props[n]) for n in _KNOWN_ORDER if n in self._props]
        unknown = [
            (n, v) for n, v in self._props.items()
            if n not in _KNOWN and n != "raw"
        ]
        return known + unknown

    # ── serialization ───────────────────────────────────────────

    def to_css(self) -> str:
        """
        Serialize to an inline CSS declaration string.

        Colours are normalized to black-and-white on the way out — see
        ``html_engine.monochrome``. ``raw`` is normalized too, so the escape
        hatch cannot smuggle colour past the rule.

        Returns:
            A string like ``"font-weight:bold;font-size:28px"``.
        """
        from html_engine.monochrome import normalize_value

        parts: list[str] = []
        for name, value in self._ordered():
            prop = _css_name(name)
            parts.append(f"{prop}:{normalize_value(prop, str(value))}")

        raw = self._props.get("raw")
        if raw:
            from html_engine.monochrome import normalize_declarations

            parts.append(normalize_declarations(str(raw).rstrip(";")))
        return ";".join(parts)

    def to_attr(self) -> str:
        """Return a full ``style="..."`` attribute, or ``""`` if empty."""
        css = self.to_css()
        return f' style="{css}"' if css else ""

    # ── combination ─────────────────────────────────────────────

    def merge(self, other: Optional[Style]) -> Style:
        """
        Return a new Style with *other*'s declarations overriding this one's.

        Properties set only on ``self`` survive. ``raw`` fragments concatenate
        rather than replace, since two raw blocks are usually two unrelated
        rules and dropping one silently would be surprising.
        """
        if other is None:
            return self

        merged = Style()
        merged._props = dict(self._props)
        for name, value in other._props.items():
            if name == "raw" and "raw" in merged._props:
                left = str(merged._props["raw"]).rstrip(";")
                merged._props["raw"] = f"{left};{value}"
            else:
                merged._props[name] = value
        return merged

    def clone(self, **overrides: Any) -> Style:
        """
        Return a copy with specific properties overridden.

        Passing ``None`` removes a property, which is how a preset default
        gets cleared::

            Card._default_style.clone(border=None)
        """
        clone = Style()
        clone._props = dict(self._props)
        for name, value in overrides.items():
            if value is None:
                clone._props.pop(name, None)
            else:
                clone._set(name, value)
        return clone

    def __add__(self, other: Style) -> Style:
        """Shorthand for ``merge``: ``combined = style_a + style_b``."""
        return self.merge(other)


def px(value: int | float) -> str:
    """Return value as CSS pixel string."""
    return f"{value}px"


def pct(value: int | float) -> str:
    """Return value as CSS percentage string."""
    return f"{value}%"


def em(value: int | float) -> str:
    """Return value as CSS em string."""
    return f"{value}em"


def rem(value: int | float) -> str:
    """Return value as CSS rem string."""
    return f"{value}rem"


def pt(value: int | float) -> str:
    """Return value as CSS pt string."""
    return f"{value}pt"
