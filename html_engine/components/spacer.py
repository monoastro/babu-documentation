"""
Spacer and divider components.
"""

from __future__ import annotations

from typing import Optional

from html_engine.components.base import Component
from html_engine.styles import Style


class Spacer(Component):
    """
    Empty space of a fixed size.

    Vertical by default. A ``width`` makes it a horizontal gutter instead,
    which is what a flex row needs to push two groups apart::

        FlexRow(left, Spacer(width="40px"), right)

    Parameters:
        height: CSS height (e.g. "20px", "1em"). Defaults to "20px".
        width: CSS width. Omitted when not given, so the spacer stays a
            full-width block.
        style: Additional inline styles, merged over the size.
    """

    def __init__(
        self,
        height: str = "20px",
        *,
        width: Optional[str] = None,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        base = Style(height=height, width=width)
        # ``flex-shrink:0`` keeps a horizontal spacer from being squeezed to
        # nothing by a tight flex row — a gutter that collapses under pressure
        # is not a gutter.
        if width:
            base = base.clone(flex_shrink="0")
        super().__init__(style=base.merge(style), css_class=css_class)
        self.height = height
        self.width = width

    def to_html(self) -> str:
        return f"<div{self._build_attrs()}></div>"


class HorizontalRule(Component):
    """
    Horizontal rule (``<hr>``) divider.

    Parameters:
        style: Override styles (color, margin, border, etc.).
    """

    _default_style = Style(
        border="none",
        border_top="1px solid #000000",
        margin="10px 0",
    )

    def __init__(self, *, style: Optional[Style] = None, css_class: Optional[str] = None):
        merged = self._default_style.merge(style)
        super().__init__(style=merged, css_class=css_class)

    def to_html(self) -> str:
        attrs = self._build_attrs()
        return f"<hr{attrs}>"


class PageBreak(Component):
    """
    Renders a page break for print media.
    """

    def __init__(self, *, style: Optional[Style] = None, css_class: Optional[str] = None):
        super().__init__(style=style, css_class=css_class)

    def to_html(self) -> str:
        # Avoid overriding the page-break style but merge others
        base_style = Style(raw="page-break-after:always;break-after:page;")
        merged_style = base_style.merge(self.style)
        attrs = self._build_attrs(extra_style=merged_style)
        return f"<div{attrs}></div>"

