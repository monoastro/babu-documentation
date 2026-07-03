"""
Style dataclass for the HTML Document Engine.

Captures all CSS properties needed to style any component.
Supports merging, inheritance, and conversion to inline CSS strings.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Optional


@dataclass
class Style:
    """
    Immutable-ish style descriptor that maps 1:1 to CSS properties.

    Any attribute left as ``None`` is simply omitted from the generated
    CSS, so you only need to set the properties you care about.

    Usage::

        bold = Style(font_weight="bold")
        big  = Style(font_size="28px")
        combined = bold.merge(big)   # font_weight="bold", font_size="28px"
        print(combined.to_css())     # "font-weight:bold;font-size:28px;"
    """

    # ── Typography ──────────────────────────────────────────────
    font_family: Optional[str] = None
    font_size: Optional[str] = None
    font_weight: Optional[str] = None
    font_style: Optional[str] = None
    color: Optional[str] = None
    text_align: Optional[str] = None
    text_decoration: Optional[str] = None
    line_height: Optional[str] = None
    letter_spacing: Optional[str] = None
    white_space: Optional[str] = None
    word_break: Optional[str] = None
    vertical_align: Optional[str] = None
    text_transform: Optional[str] = None

    # ── Box Model ───────────────────────────────────────────────
    width: Optional[str] = None
    height: Optional[str] = None
    min_width: Optional[str] = None
    max_width: Optional[str] = None
    min_height: Optional[str] = None
    max_height: Optional[str] = None
    padding: Optional[str] = None
    padding_top: Optional[str] = None
    padding_right: Optional[str] = None
    padding_bottom: Optional[str] = None
    padding_left: Optional[str] = None
    margin: Optional[str] = None
    margin_top: Optional[str] = None
    margin_right: Optional[str] = None
    margin_bottom: Optional[str] = None
    margin_left: Optional[str] = None
    border: Optional[str] = None
    border_top: Optional[str] = None
    border_right: Optional[str] = None
    border_bottom: Optional[str] = None
    border_left: Optional[str] = None
    border_radius: Optional[str] = None
    border_collapse: Optional[str] = None
    box_sizing: Optional[str] = None

    # ── Background ──────────────────────────────────────────────
    background: Optional[str] = None
    background_color: Optional[str] = None
    background_image: Optional[str] = None
    background_size: Optional[str] = None
    background_position: Optional[str] = None
    background_repeat: Optional[str] = None

    # ── Layout / Positioning ────────────────────────────────────
    display: Optional[str] = None
    position: Optional[str] = None
    top: Optional[str] = None
    right: Optional[str] = None
    bottom: Optional[str] = None
    left: Optional[str] = None
    z_index: Optional[str] = None
    float: Optional[str] = None
    clear: Optional[str] = None
    overflow: Optional[str] = None
    overflow_x: Optional[str] = None
    overflow_y: Optional[str] = None

    # ── Flexbox ─────────────────────────────────────────────────
    flex: Optional[str] = None
    flex_direction: Optional[str] = None
    flex_wrap: Optional[str] = None
    justify_content: Optional[str] = None
    align_items: Optional[str] = None
    align_self: Optional[str] = None
    gap: Optional[str] = None
    row_gap: Optional[str] = None
    column_gap: Optional[str] = None
    flex_shrink: Optional[str] = None
    flex_grow: Optional[str] = None
    flex_basis: Optional[str] = None

    # ── Grid ────────────────────────────────────────────────────
    grid_template_columns: Optional[str] = None
    grid_template_rows: Optional[str] = None
    grid_column: Optional[str] = None
    grid_row: Optional[str] = None

    # ── Visual Effects ──────────────────────────────────────────
    box_shadow: Optional[str] = None
    opacity: Optional[str] = None
    transform: Optional[str] = None
    transition: Optional[str] = None
    filter: Optional[str] = None
    cursor: Optional[str] = None
    pointer_events: Optional[str] = None
    object_fit: Optional[str] = None
    object_position: Optional[str] = None

    # ── Table-specific ──────────────────────────────────────────
    table_layout: Optional[str] = None

    # ── Misc ────────────────────────────────────────────────────
    inset: Optional[str] = None
    content: Optional[str] = None
    list_style: Optional[str] = None

    # ── Raw CSS ─────────────────────────────────────────────────
    raw: Optional[str] = None  # Escape hatch: appended verbatim

    # ─────────────────────────────────────────────────────────────
    # Methods
    # ─────────────────────────────────────────────────────────────

    def _attr_to_css_property(self, attr: str) -> str:
        """Convert a Python attribute name to its CSS property equivalent."""
        return attr.replace("_", "-")

    def to_css(self) -> str:
        """
        Serialize all non-None attributes into a CSS inline style string.

        Returns:
            A string like ``"font-weight:bold;font-size:28px;"``
        """
        parts: list[str] = []
        for f in fields(self):
            if f.name == "raw":
                continue
            value = getattr(self, f.name)
            if value is not None:
                css_prop = self._attr_to_css_property(f.name)
                parts.append(f"{css_prop}:{value}")
        if self.raw:
            parts.append(self.raw.rstrip(";"))
        return ";".join(parts)

    def to_attr(self) -> str:
        """
        Return a full ``style="..."`` HTML attribute string,
        or an empty string if there are no styles.
        """
        css = self.to_css()
        if not css:
            return ""
        return f' style="{css}"'

    def merge(self, other: Style | None) -> Style:
        """
        Return a **new** Style with values from *other* overriding
        values in *self* wherever *other*'s value is not None.
        """
        if other is None:
            return self
        merged_kwargs = {}
        for f in fields(self):
            other_val = getattr(other, f.name)
            self_val = getattr(self, f.name)
            merged_kwargs[f.name] = other_val if other_val is not None else self_val
        return Style(**merged_kwargs)

    def clone(self, **overrides) -> Style:
        """
        Return a copy of this Style with specific fields overridden.

        Usage::

            base = Style(font_size="16px", color="#333")
            header = base.clone(font_size="28px", font_weight="bold")
        """
        kwargs = {}
        for f in fields(self):
            kwargs[f.name] = overrides.get(f.name, getattr(self, f.name))
        return Style(**kwargs)

    def __add__(self, other: Style) -> Style:
        """Shorthand: ``combined = style_a + style_b``."""
        return self.merge(other)
