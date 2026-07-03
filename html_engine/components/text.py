"""
Text components: Text, Heading, Paragraph.
"""

from __future__ import annotations

from typing import Optional

from html_engine.components.base import Component
from html_engine.styles import Style


class Text(Component):
    """
    Inline text element rendered as a ``<span>``.

    Parameters:
        content: The text string to display.
        style: Optional inline styles.
        css_class: Optional CSS class name(s).
    """

    def __init__(
        self,
        content: str = "",
        *,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class)
        self.content = content

    def to_html(self) -> str:
        attrs = self._build_attrs()
        return f"<span{attrs}>{self.content}</span>"


class Heading(Component):
    """
    Block heading element rendered as ``<h1>`` through ``<h6>``.

    Parameters:
        content: The heading text.
        level: Heading level (1–6). Defaults to 1.
        style: Optional inline styles.
        css_class: Optional CSS class name(s).
    """

    def __init__(
        self,
        content: str = "",
        *,
        level: int = 1,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class)
        self.content = content
        self.level = max(1, min(6, level))

    def to_html(self) -> str:
        tag = f"h{self.level}"
        attrs = self._build_attrs()
        return f"<{tag}{attrs}>{self.content}</{tag}>"


class Paragraph(Component):
    """
    Block paragraph element rendered as ``<p>``.

    Parameters:
        content: The paragraph text.
        style: Optional inline styles.
        css_class: Optional CSS class name(s).
    """

    def __init__(
        self,
        content: str = "",
        *,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class)
        self.content = content

    def to_html(self) -> str:
        attrs = self._build_attrs()
        return f"<p{attrs}>{self.content}</p>"


class RawHTML(Component):
    """
    Escape hatch: renders arbitrary HTML verbatim.

    Use sparingly — this bypasses all engine abstractions.
    """

    def __init__(self, html: str):
        super().__init__()
        self.html = html

    def to_html(self) -> str:
        return self.html
