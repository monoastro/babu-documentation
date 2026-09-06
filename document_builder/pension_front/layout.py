from html_engine import Document, Style, Text, FlexCol, Spacer, PlaceholderBox

_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

def _ea(field_name: str):
    return {"contenteditable": "true", "data-field": field_name}

def build_pension_front(data: dict) -> Document:
    d = {k: (v if v is not None else "") for k, v in data.items()}
    doc = Document(
        "Pension Rights Certificate - Front Cover",
        page_width="900px", page_height="1200px", background="#ffffff",
        font_family='"Times New Roman", Times, serif', border="1px solid #000000",
        page_style=Style(padding="30px 40px", box_sizing="border-box"),
        extra_css=_EDITABLE_CSS,
    )
    doc.add(Spacer(height="120px"))
    doc.add(
        FlexCol(
            Text(d.get("main_title", ""), style=Style(font_size="30px", font_weight="bold", text_align="center"), attrs=_ea("main_title")),
            Spacer(height="60px"),
            PlaceholderBox(label="Coat of Arms of Nepal", width="170px", height="140px", font_size="16px"),
            Spacer(height="250px"),
            Text(d.get("authority_line_1", ""), style=Style(font_size="18px", font_weight="bold", text_align="center"), attrs=_ea("authority_line_1")),
            Spacer(height="12px"),
            Text(d.get("authority_line_2", ""), style=Style(font_size="18px", text_align="center"), attrs=_ea("authority_line_2")),
            gap="0px", style=Style(width="100%", align_items="center"),
        )
    )
    return doc
