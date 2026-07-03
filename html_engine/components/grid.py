"""
Layout components: FlexRow, FlexCol, AbsoluteBox, Div.

These are generic container components for composing document layouts
using CSS Flexbox and absolute positioning.
"""

from __future__ import annotations

from typing import Optional

from html_engine.components.base import Component
from html_engine.styles import Style


class Div(Component):
    """
    Generic block container rendered as a ``<div>``.

    The simplest building block — wraps children in a styled div.

    Parameters:
        children: Child components.
        style: Inline styles.
        css_class: Optional CSS class.
    """

    def __init__(
        self,
        *children: Component,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class, children=list(children))

    def to_html(self) -> str:
        attrs = self._build_attrs()
        inner = self._render_children()
        return f"<div{attrs}>{inner}</div>"


class FlexRow(Component):
    """
    Horizontal flex container (``flex-direction: row``).

    Parameters:
        children: Child components laid out horizontally.
        gap: CSS gap between children. Defaults to "0".
        style: Additional inline styles (merged with flex defaults).
        css_class: Optional CSS class.
    """

    def __init__(
        self,
        *children: Component,
        gap: Optional[str] = None,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        base = Style(display="flex", flex_direction="row")
        if gap:
            base = base.clone(gap=gap)
        merged = base.merge(style)
        super().__init__(style=merged, css_class=css_class, children=list(children))

    def to_html(self) -> str:
        attrs = self._build_attrs()
        inner = self._render_children()
        return f"<div{attrs}>{inner}</div>"


class FlexCol(Component):
    """
    Vertical flex container (``flex-direction: column``).

    Parameters:
        children: Child components laid out vertically.
        gap: CSS gap between children. Defaults to "0".
        style: Additional inline styles (merged with flex defaults).
        css_class: Optional CSS class.
    """

    def __init__(
        self,
        *children: Component,
        gap: Optional[str] = None,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        base = Style(display="flex", flex_direction="column")
        if gap:
            base = base.clone(gap=gap)
        merged = base.merge(style)
        super().__init__(style=merged, css_class=css_class, children=list(children))

    def to_html(self) -> str:
        attrs = self._build_attrs()
        inner = self._render_children()
        return f"<div{attrs}>{inner}</div>"


class AbsoluteBox(Component):
    """
    Absolutely positioned container.

    Use for elements that need precise pixel placement on the page
    (logos, stamps, signatures, watermarks).

    Parameters:
        children: Child components.
        top/right/bottom/left: CSS positioning values.
        style: Additional inline styles (merged with position defaults).
        css_class: Optional CSS class.
    """

    def __init__(
        self,
        *children: Component,
        top: Optional[str] = None,
        right: Optional[str] = None,
        bottom: Optional[str] = None,
        left: Optional[str] = None,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        base = Style(
            position="absolute",
            top=top,
            right=right,
            bottom=bottom,
            left=left,
        )
        merged = base.merge(style)
        super().__init__(style=merged, css_class=css_class, children=list(children))

    def to_html(self) -> str:
        attrs = self._build_attrs()
        inner = self._render_children()
        return f"<div{attrs}>{inner}</div>"
