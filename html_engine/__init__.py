"""
html_engine — Programmatic HTML Document Generation Engine.

Build pixel-perfect, printable HTML documents by composing typed
building blocks in Python. No templates, no dependencies.
"""

# Core
from html_engine.styles import Style, px, pct, em, rem, pt
from html_engine.document import Document

# Components
from html_engine.components.base import Component
from html_engine.components.text import Text, Heading, Paragraph, RawHTML, Link
from html_engine.components.field import LabelValue, FieldGroup, MultiFieldRow
from html_engine.components.image import Image
from html_engine.components.table import Table, TableRow, TableCell
from html_engine.components.grid import Div, FlexRow, FlexCol, AbsoluteBox, Grid, GridItem, Card
from html_engine.components.spacer import Spacer, HorizontalRule, PageBreak
from html_engine.components.list import ListItem, UnorderedList, OrderedList

# Renderer and PDF
from html_engine.renderer import render
from html_engine.pdf import html_to_pdf

__all__ = [
    # Core & Styling
    "Style",
    "px",
    "pct",
    "em",
    "rem",
    "pt",
    "Document",
    "Component",
    "render",
    "html_to_pdf",
    # Text
    "Text",
    "Heading",
    "Paragraph",
    "RawHTML",
    "Link",
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
    "Grid",
    "GridItem",
    "Card",
    # Spacer
    "Spacer",
    "HorizontalRule",
    "PageBreak",
    # Lists
    "ListItem",
    "UnorderedList",
    "OrderedList",
]
