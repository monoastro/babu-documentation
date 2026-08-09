# this walks the Document's component tree and gives a complete, standalone HTML page string

from __future__ import annotations
from typing import TYPE_CHECKING

from html_engine.monochrome import normalize_html

if TYPE_CHECKING:
    from html_engine.document import Document

def render(doc: Document) -> str:
    """
    Render a Document class to a full HTML string.

    The output is a self-contained page with:
    - DOCTYPE, charset, viewport meta tags
    - A ``<style>`` block with body and page-wrapper rules
    - A ``.page`` wrapper div containing all rendered components

    Colours are normalized to black-and-white as the last step, which covers
    ``extra_css``, ``Document(background=...)``, the print rules, and any
    style a component hardcoded into its own ``to_html()``. Text content is
    never touched.
    """
    body_css_parts = [ "margin:0", "background:#ffffff", f"font-family:{doc.font_family}", ]
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
        #"box-shadow:0 0 20px #000000",
    ]
    if doc.page_height != "auto" and doc.clip:
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
                color: #000000;
            }
        }
        """

    print_css = f"""
    @media print {{
        body {{ background: white !important; margin: 0 !important; }}
        .page {{
            margin: 0 !important;
            box-shadow: none !important;
            border: 2px solid #000000 !important;
            page-break-after: always;
        }}
        .no-print {{ display: none !important; }}
    }}
    {page_numbers_css}
    """

    return normalize_html(
        f"""<!DOCTYPE html>
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
    )
