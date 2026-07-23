from __future__ import annotations

from typing import Optional

from html_engine.components.base import Component
from html_engine.styles import Style


"""
    doc = Document("My Certificate", page_width="1200px")
    doc.add(
        Heading("Title", level=1),
        LabelValue("Name:", "John Doe"),
    )
    html = doc.render()
"""
class Document:
    def __init__(
        self,
        title: str = "Document",
        *,
        page_width: str = "1200px",
        page_height: str = "auto",
        min_height: Optional[str] = None,
        background: str = "#ffffff",
        font_family: str = '"Times New Roman", serif',
        border: str = "2px solid #000000",
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
        self.children.extend(components)
        return self

    def render(self) -> str:
        from html_engine.renderer import render
        return render(self)

    def save(self, path: str) -> None:
        html = self.render()
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    def to_pdf(self, path: str, base_url: Optional[str] = None) -> None:
        from html_engine.pdf import html_to_pdf
        html = self.render()
        html_to_pdf(html, path, base_url=base_url)
