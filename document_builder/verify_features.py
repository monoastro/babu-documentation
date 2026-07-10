#!/usr/bin/env python3
"""
Verification script for HTML Engine updates and enhancements.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure project root is on the import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from html_engine import (
    Document,
    Style,
    px,
    pct,
    em,
    rem,
    pt,
    Text,
    Heading,
    Paragraph,
    Link,
    LabelValue,
    TableCell,
    TableRow,
    Table,
    Div,
    FlexRow,
    FlexCol,
    AbsoluteBox,
    Grid,
    GridItem,
    Card,
    PageBreak,
    ListItem,
    UnorderedList,
    OrderedList,
)


def run_tests() -> None:
    print("=== RUNNING HTML ENGINE TESTS ===")

    # 1. Test Unit Helpers
    print("Testing Unit Helpers...")
    assert px(10) == "10px", f"Expected 10px, got {px(10)}"
    assert pct(50.5) == "50.5%", f"Expected 50.5%, got {pct(50.5)}"
    assert em(1.5) == "1.5em", f"Expected 1.5em, got {em(1.5)}"
    assert rem(2) == "2rem", f"Expected 2rem, got {rem(2)}"
    assert pt(12) == "12pt", f"Expected 12pt, got {pt(12)}"
    print("✓ Unit Helpers OK")

    # 2. Test HTML Escaping
    print("Testing HTML Auto-Escaping...")
    malicious_str = "Dangerous <script> & ' \""
    
    # Text component
    txt_escaped = Text(malicious_str).to_html()
    assert "&lt;script&gt;" in txt_escaped, "Text failed to escape <script>"
    assert "&amp;" in txt_escaped, "Text failed to escape &"
    assert "&apos;" in txt_escaped or "&#x27;" in txt_escaped, "Text failed to escape '"
    
    txt_unescaped = Text(malicious_str, escape=False).to_html()
    assert "<script>" in txt_unescaped, "Text unescaped mode failed to keep raw string"

    # Heading component
    h_escaped = Heading(malicious_str).to_html()
    assert "&lt;script&gt;" in h_escaped

    # Paragraph component
    p_escaped = Paragraph(malicious_str).to_html()
    assert "&lt;script&gt;" in p_escaped

    # LabelValue component
    lv_escaped = LabelValue(malicious_str, malicious_str).to_html()
    assert "&lt;script&gt;" in lv_escaped

    # TableCell component
    cell_escaped = TableCell(malicious_str).to_html()
    assert "&lt;script&gt;" in cell_escaped
    
    print("✓ HTML Auto-Escaping OK")

    # 3. Test Link Component
    print("Testing Link component...")
    link = Link("Google", "https://google.com", target="_blank")
    link_html = link.to_html()
    assert 'href="https://google.com"' in link_html
    assert 'target="_blank"' in link_html
    assert "Google" in link_html
    print("✓ Link Component OK")

    # 4. Test Grid, GridItem, and Card Components
    print("Testing Layout Components (Grid, GridItem, Card)...")
    grid = Grid(
        GridItem(Text("Col 1"), column_span=4),
        GridItem(Text("Col 2"), column_span=8),
        columns=12,
        gap="10px",
    )
    grid_html = grid.to_html()
    assert "display:grid" in grid_html
    assert "grid-template-columns:repeat(12, 1fr)" in grid_html
    assert "gap:10px" in grid_html
    assert "grid-column:span 4" in grid_html
    assert "grid-column:span 8" in grid_html

    card = Card(Text("Card Content"))
    card_html = card.to_html()
    assert "box-shadow:0 4px 6px rgba(0, 0, 0, 0.05)" in card_html
    assert "border-radius:8px" in card_html
    print("✓ Grid, GridItem, Card Components OK")

    # 5. Test List Components
    print("Testing List Components (UnorderedList, OrderedList, ListItem)...")
    ul = UnorderedList("Item 1", "Item 2", ListItem("Item 3", style=Style(color="red")))
    ul_html = ul.to_html()
    assert "<ul>" in ul_html
    assert "<li>Item 1</li>" in ul_html
    assert '<li style="color:red">Item 3</li>' in ul_html

    ol = OrderedList("First", "Second")
    ol_html = ol.to_html()
    assert "<ol>" in ol_html
    assert "<li>First</li>" in ol_html
    print("✓ List Components OK")

    # 6. Test PageBreak and Document Page Numbers
    print("Testing PageBreak and Pagination...")
    pb = PageBreak()
    pb_html = pb.to_html()
    assert "page-break-after:always" in pb_html
    assert "break-after:page" in pb_html

    doc = Document("Test Page Numbering", show_page_numbers=True)
    doc_html = doc.render()
    assert "@page" in doc_html
    assert "counter(page)" in doc_html
    print("✓ PageBreak & Page Numbering OK")

    print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")


if __name__ == "__main__":
    run_tests()
