"""
html_engine — Programmatic HTML Document Generation Engine.

Build pixel-perfect, printable HTML documents by composing typed
building blocks in Python. No templates, no dependencies.

Usage::

    from html_engine import Document, Style, Text, Heading, LabelValue, Image

    doc = Document("My Certificate", page_width="1200px", page_height="820px")
    doc.add(
        Heading("Certificate of Completion", level=1, style=Style(text_align="center")),
        LabelValue("Name:", "Jane Doe"),
        LabelValue("Date:", "2026-01-01"),
    )
    html = doc.render()

    with open("output.html", "w") as f:
        f.write(html)
"""

# Core
from html_engine.styles import Style
from html_engine.document import Document

# Components
from html_engine.components.base import Component
from html_engine.components.text import Text, Heading, Paragraph, RawHTML
from html_engine.components.field import LabelValue, FieldGroup, MultiFieldRow
from html_engine.components.image import Image
from html_engine.components.table import Table, TableRow, TableCell
from html_engine.components.grid import Div, FlexRow, FlexCol, AbsoluteBox
from html_engine.components.spacer import Spacer, HorizontalRule

# Renderer and PDF
from html_engine.renderer import render
from html_engine.pdf import html_to_pdf

__all__ = [
    # Core
    "Style",
    "Document",
    "Component",
    "render",
    "html_to_pdf",
    # Text
    "Text",
    "Heading",
    "Paragraph",
    "RawHTML",
    # Fields
    "LabelValue",
    "FieldGroup",
    "MultiFieldRow",
    # Media
    "Image",
    # Table
    "Table",
    "TableRow",
    "TableCell",
    # Layout
    "Div",
    "FlexRow",
    "FlexCol",
    "AbsoluteBox",
    # Spacer
    "Spacer",
    "HorizontalRule",
]
