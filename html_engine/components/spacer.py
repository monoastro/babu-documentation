"""
Spacer and divider components.
"""

from __future__ import annotations

from typing import Optional

from html_engine.components.base import Component
from html_engine.styles import Style


class Spacer(Component):
    """
    Empty vertical space with a fixed height.

    Parameters:
        height: CSS height value (e.g. "20px", "1em").
    """

    def __init__(self, height: str = "20px"):
        super().__init__()
        self.height = height

    def to_html(self) -> str:
        return f'<div style="height:{self.height}"></div>'


class HorizontalRule(Component):
    """
    Horizontal rule (``<hr>``) divider.

    Parameters:
        style: Override styles (color, margin, border, etc.).
    """

    _default_style = Style(
        border="none",
        border_top="1px solid #999",
        margin="10px 0",
    )

    def __init__(self, *, style: Optional[Style] = None, css_class: Optional[str] = None):
        merged = self._default_style.merge(style)
        super().__init__(style=merged, css_class=css_class)

    def to_html(self) -> str:
        attrs = self._build_attrs()
        return f"<hr{attrs}>"
