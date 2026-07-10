"""
Document container — the top-level object that holds all components
and renders to a complete, standalone HTML page.
"""

from __future__ import annotations

from typing import Optional

from html_engine.components.base import Component
from html_engine.styles import Style


class Document:
    """
    Represents a single printable document page.

    Assembles components into a full HTML page with proper DOCTYPE,
    meta tags, embedded styles, and a page wrapper div.

    Parameters:
        title: HTML ``<title>`` content.
        page_width: CSS width of the page. Defaults to "1200px".
        page_height: CSS height of the page. Defaults to "820px".
        background: Page background color. Defaults to "#f5f5f5".
        font_family: Global font family. Defaults to Times New Roman.
        border: Page border. Defaults to "2px solid #444".
        page_style: Additional Style overrides for the page wrapper.
        body_style: Additional Style overrides for the ``<body>``.
        extra_css: Raw CSS string appended to the ``<style>`` block.
        lang: HTML lang attribute. Defaults to "en".

    Usage::

        doc = Document("My Certificate", page_width="1200px")
        doc.add(
            Heading("Title", level=1),
            LabelValue("Name:", "John Doe"),
        )
        html = doc.render()
    """

    def __init__(
        self,
        title: str = "Document",
        *,
        page_width: str = "1200px",
        page_height: str = "auto",
        min_height: Optional[str] = None,
        background: str = "#f5f5f5",
        font_family: str = '"Times New Roman", serif',
        border: str = "2px solid #444",
        page_style: Optional[Style] = None,
        body_style: Optional[Style] = None,
        extra_css: str = "",
        lang: str = "en",
        show_page_numbers: bool = False,
    ):
        self.title = title
        self.page_width = page_width
        self.page_height = page_height
        self.min_height = min_height
        self.background = background
        self.font_family = font_family
        self.border = border
        self.page_style = page_style
        self.body_style = body_style
        self.extra_css = extra_css
        self.lang = lang
        self.show_page_numbers = show_page_numbers
        self.children: list[Component] = []

    def add(self, *components: Component) -> Document:
        """Append one or more components to the document. Returns self for chaining."""
        self.children.extend(components)
        return self

    def render(self) -> str:
        """
        Render the full document to a standalone HTML string.

        Returns:
            Complete HTML page as a string.
        """
        from html_engine.renderer import render
        return render(self)

    def save(self, path: str) -> None:
        """
        Render the document to HTML and save it to the specified file path.
        """
        html = self.render()
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    def to_pdf(self, path: str, base_url: Optional[str] = None) -> None:
        """
        Render the document and convert it to a PDF file.
        Requires weasyprint.
        """
        from html_engine.pdf import html_to_pdf
        html = self.render()
        html_to_pdf(html, path, base_url=base_url)
