"""
Layout components: FlexRow, FlexCol, AbsoluteBox, Div.

These are generic container components for composing document layouts
using CSS Flexbox and absolute positioning.
"""

from __future__ import annotations

from typing import Optional, Union

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


class Grid(Component):
    """
    CSS Grid container.

    Parameters:
        columns: Grid template columns (e.g. 12 or "repeat(12, 1fr)" or "1fr 2fr").
                 If an int is provided, it automatically translates to "repeat(X, 1fr)".
        rows: Optional grid template rows (e.g. "auto").
        gap: Gap between grid items.
    """

    def __init__(
        self,
        *children: Component,
        columns: Union[int, str] = 12,
        rows: Optional[str] = None,
        gap: Optional[str] = None,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        col_str = f"repeat({columns}, 1fr)" if isinstance(columns, int) else columns
        base = Style(display="grid", grid_template_columns=col_str)
        if rows:
            base = base.clone(grid_template_rows=rows)
        if gap:
            base = base.clone(gap=gap)
        merged = base.merge(style)
        super().__init__(style=merged, css_class=css_class, children=list(children))

    def to_html(self) -> str:
        attrs = self._build_attrs()
        inner = self._render_children()
        return f"<div{attrs}>{inner}</div>"


class GridItem(Component):
    """
    CSS Grid item.

    Parameters:
        column_span: Number of columns this item spans (e.g. 4 or "span 4").
                     If an int is provided, it automatically translates to "span X".
        row_span: Optional number of rows this item spans.
    """

    def __init__(
        self,
        *children: Component,
        column_span: Optional[Union[int, str]] = None,
        row_span: Optional[Union[int, str]] = None,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        base = Style()
        if column_span is not None:
            col_val = f"span {column_span}" if isinstance(column_span, int) else column_span
            base = base.clone(grid_column=col_val)
        if row_span is not None:
            row_val = f"span {row_span}" if isinstance(row_span, int) else row_span
            base = base.clone(grid_row=row_val)
        merged = base.merge(style)
        super().__init__(style=merged, css_class=css_class, children=list(children))

    def to_html(self) -> str:
        attrs = self._build_attrs()
        inner = self._render_children()
        return f"<div{attrs}>{inner}</div>"


class Card(Component):
    """
    A styled container mimicking a paper card.

    Includes preset styles: background color, border, padding, border-radius, and shadow.
    """

    _default_style = Style(
        background="#ffffff",
        border="1px solid #e0e0e0",
        border_radius="8px",
        padding="20px",
        box_shadow="0 4px 6px rgba(0, 0, 0, 0.05)",
        margin_bottom="20px",
    )

    def __init__(
        self,
        *children: Component,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        merged = self._default_style.merge(style)
        super().__init__(style=merged, css_class=css_class, children=list(children))

    def to_html(self) -> str:
        attrs = self._build_attrs()
        inner = self._render_children()
        return f"<div{attrs}>{inner}</div>"
