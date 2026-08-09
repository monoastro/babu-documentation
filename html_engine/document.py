"""
Document — the root of a renderable page.

A ``Document`` holds page geometry plus a flat list of top-level components,
and hands both to ``html_engine.renderer.render``::

    doc = Document("My Certificate", page_width="1200px")
    doc.add(Heading("Title", level=1), LabelValue("Name:", "John Doe"))
    html = doc.render()
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from html_engine.components.base import Component
from html_engine.styles import Style


class Document:
    """
    A single page of output.

    Parameters:
        title: ``<title>`` text.
        page_width: Width of the ``.page`` sheet. Fixed widths keep the render
            reproducible across viewports.
        page_height: Fixed height, or ``"auto"`` to grow with the content.
        min_height: Floor for an ``auto`` page.
        background: Page surface. Normalized to white by the monochrome rule.
        font_family: Base family. Include a Devanagari fallback for Nepali
            documents.
        border: Page border, which is also what the PNG renderer crops to.
        clip: Whether a fixed-height page hides overflowing content. ``True``
            (the default) matches print, where content past the page edge is
            simply gone. ``False`` lets it spill visibly — set it while
            debugging a page that seems to be losing its footer, because a
            clipped overflow and a genuinely missing section look identical in
            the rendered PNG, and the vision verifier reports both as lost
            content. Ignored when *page_height* is ``"auto"``.
        page_style: Extra styles for the ``.page`` wrapper.
        body_style: Extra styles for ``<body>``.
        extra_css: Raw CSS appended to the ``<style>`` block. Colour-normalized
            like everything else.
        lang: ``<html lang>``. Use ``"ne"`` for Nepali documents so screen
            readers pick the right pronunciation.
        show_page_numbers: Emit an ``@page`` counter rule for print.
    """

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
        clip: bool = True,
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
        self.clip = clip
        self.page_style = page_style
        self.body_style = body_style
        self.extra_css = extra_css
        self.lang = lang
        self.show_page_numbers = show_page_numbers
        self.children: list[Component] = []

    def add(self, *components: Any) -> Document:
        """Append top-level components. Returns self for chaining.

        Accepts components, strings, numbers, or ``None`` — the same coercion
        every container applies, so a page-level child cannot slip through
        unchecked and fail later during rendering.
        """
        from html_engine.components.base import coerce_children

        self.children.extend(coerce_children(components, owner="Document"))
        return self

    def render(self) -> str:
        """Render to a complete, self-contained HTML string."""
        from html_engine.renderer import render

        return render(self)

    def save(self, path: str | Path) -> Path:
        """
        Write the rendered HTML to *path*, creating parent directories.

        Returns the path written, so a caller can chain straight into
        rendering a PNG from it.
        """
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.render(), encoding="utf-8")
        return target
