"""
Renderer — walks the Document's component tree and emits a complete,
standalone HTML page string.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from html_engine.document import Document


def render(doc: Document) -> str:
    """
    Render a :class:`Document` to a full HTML string.

    The output is a self-contained page with:
    - DOCTYPE, charset, viewport meta tags
    - A ``<style>`` block with body and page-wrapper rules
    - A ``.page`` wrapper div containing all rendered components
    - An optional print button

    Parameters:
        doc: The Document to render.

    Returns:
        Complete HTML page as a string.
    """
    # ── Build body CSS ──────────────────────────────────────────
    body_css_parts = [
        "margin:0",
        "background:#d9d9d9",
        f"font-family:{doc.font_family}",
    ]
    if doc.body_style:
        extra = doc.body_style.to_css()
        if extra:
            body_css_parts.append(extra)
    body_css = ";".join(body_css_parts)

    # ── Build page wrapper CSS ──────────────────────────────────
    page_css_parts = [
        f"width:{doc.page_width}",
        f"height:{doc.page_height}",
        "margin:30px auto",
        f"background:{doc.background}",
        "position:relative",
        f"border:{doc.border}",
        "box-shadow:0 0 20px rgba(0,0,0,0.2)",
    ]
    if doc.page_height != "auto":
        page_css_parts.append("overflow:hidden")
    if doc.min_height:
        page_css_parts.append(f"min-height:{doc.min_height}")

    if doc.page_style:
        extra = doc.page_style.to_css()
        if extra:
            page_css_parts.append(extra)
    page_css = ";".join(page_css_parts)

    # ── Render all child components ─────────────────────────────
    children_html = "".join(child.to_html() for child in doc.children)

    # ── Print styles ────────────────────────────────────────────
    page_numbers_css = ""
    if doc.show_page_numbers:
        page_numbers_css = """
        @page {
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-family: inherit;
                font-size: 12px;
                color: #666;
            }
        }
        """

    print_css = f"""
    @media print {{
        body {{ background: white !important; margin: 0 !important; }}
        .page {{
            margin: 0 !important;
            box-shadow: none !important;
            border: 2px solid #444 !important;
            page-break-after: always;
        }}
        .no-print {{ display: none !important; }}
    }}
    {page_numbers_css}
    """

    # ── Assemble ────────────────────────────────────────────────
    return f"""<!DOCTYPE html>
<html lang="{doc.lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{doc.title}</title>
<style>
    body {{ {body_css} }}
    .page {{ {page_css} }}
    {print_css}
    {doc.extra_css}
</style>
</head>
<body>
<div class="page">
{children_html}
</div>
</body>
</html>"""
