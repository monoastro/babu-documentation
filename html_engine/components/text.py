"""
Text components: Text, Heading, Paragraph, Link.
"""

from __future__ import annotations

import html
from typing import Optional, Union

from html_engine.components.base import Component
from html_engine.styles import Style


class Text(Component):
    """
    Inline text element rendered as a ``<span>``.

    Parameters:
        content: The text string to display.
        escape: If True, content will be HTML-escaped. Defaults to True.
        style: Optional inline styles.
        css_class: Optional CSS class name(s).
    """

    def __init__(
        self,
        content: str = "",
        *,
        escape: bool = True,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class)
        self.content = content
        self.escape = escape

    def to_html(self) -> str:
        attrs = self._build_attrs()
        content_html = html.escape(str(self.content)) if self.escape else str(self.content)
        return f"<span{attrs}>{content_html}</span>"


class Heading(Component):
    """
    Block heading element rendered as ``<h1>`` through ``<h6>``.

    Parameters:
        content: The heading text.
        level: Heading level (1–6). Defaults to 1.
        escape: If True, content will be HTML-escaped. Defaults to True.
        style: Optional inline styles.
        css_class: Optional CSS class name(s).
    """

    def __init__(
        self,
        content: str = "",
        *,
        level: int = 1,
        escape: bool = True,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class)
        self.content = content
        self.level = max(1, min(6, level))
        self.escape = escape

    def to_html(self) -> str:
        tag = f"h{self.level}"
        attrs = self._build_attrs()
        content_html = html.escape(str(self.content)) if self.escape else str(self.content)
        return f"<{tag}{attrs}>{content_html}</{tag}>"


class Paragraph(Component):
    """
    Block paragraph element rendered as ``<p>``.

    Parameters:
        content: The paragraph text.
        escape: If True, content will be HTML-escaped. Defaults to True.
        style: Optional inline styles.
        css_class: Optional CSS class name(s).
    """

    def __init__(
        self,
        content: str = "",
        *,
        escape: bool = True,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class)
        self.content = content
        self.escape = escape

    def to_html(self) -> str:
        attrs = self._build_attrs()
        content_html = html.escape(str(self.content)) if self.escape else str(self.content)
        return f"<p{attrs}>{content_html}</p>"


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


class Link(Component):
    """
    Renders an anchor element ``<a>``.

    Parameters:
        content: The text content or nested component inside the link.
        href: Link URL.
        target: Optional target (e.g. "_blank").
        escape: If True, string content will be HTML-escaped. Defaults to True.
        style: Optional inline styles.
        css_class: Optional CSS class name(s).
    """

    def __init__(
        self,
        content: Union[str, Component],
        href: str,
        *,
        target: Optional[str] = None,
        escape: bool = True,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class)
        self.content = content
        self.href = href
        self.target = target
        self.escape = escape

    def to_html(self) -> str:
        attrs = self._build_attrs()
        target_attr = f' target="{self.target}"' if self.target else ""

        if isinstance(self.content, Component):
            inner = self.content.to_html()
        else:
            inner = html.escape(str(self.content)) if self.escape else str(self.content)

        return f'<a href="{self.href}"{target_attr}{attrs}>{inner}</a>'
