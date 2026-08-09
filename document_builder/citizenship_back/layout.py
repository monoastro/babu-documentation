from __future__ import annotations
from typing import Any
from html_engine import (
    Document, Style, Text, AbsoluteBox, FlexRow, FlexCol, Spacer,
    PlaceholderBox, SignatureBlock,
)

LABEL_STYLE = Style(font_weight="bold", font_size="20px", width="280px", flex_shrink="0")
VALUE_STYLE = Style(font_size="20px", flex="1")
_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

def build_citizenship_back(data: dict[str, Any]) -> Document:
    d = {
        "citizenship_type": "",
        "right_thumb_impression": "",
        "left_thumb_impression": "",
        "issuing_officer_signature": "",
        "issuing_officer_name": "",
        "issuing_officer_designation": "",
        "issue_date_bs": ""
    }
    d.update(data or {})
    # OCR returns absent fields as None; a literal "None" on the page is a defect.
    d = {k: ("" if v is None else v) for k, v in d.items()}

    doc = Document(
        "Nepali Citizenship Certificate (Back)",
        page_width="1200px",
        page_height="800px",
        background="#ffffff",
        font_family='"Times New Roman"',
        border="2px solid #000000",
        extra_css=_EDITABLE_CSS,
    )

    # Info rows (citizenship type and thumb remarks)
    doc.add(
        AbsoluteBox(
            FlexCol(
                Text("Citizenship Type:", style=LABEL_STYLE),
                Text(d["citizenship_type"], style=VALUE_STYLE, field="citizenship_type"),
                Spacer(height="10px"),
                Text("Thumb Impression of Certificate Holder:", style=LABEL_STYLE),
            ),
            left="30px", top="10px", style=Style(width="1100px")
        )
    )

    # Thumb impressions — the inked print itself cannot be reproduced, so each
    # side gets an outline at the right size and the extracted remark below it.
    doc.add(
        AbsoluteBox(
            FlexRow(
                FlexCol(Text("Right Thumb", style=LABEL_STYLE),
                        PlaceholderBox("Right Thumb Impression", size="200px"),
                        Text(d["right_thumb_impression"], style=VALUE_STYLE, field="right_thumb_impression")),
                Spacer(width="50px"),
                FlexCol(Text("Left Thumb", style=LABEL_STYLE),
                        PlaceholderBox("Left Thumb Impression", size="200px"),
                        Text(d["left_thumb_impression"], style=VALUE_STYLE, field="left_thumb_impression"))
            ),
            left="30px", top="110px", style=Style(width="700px", height="220px")
        )
    )

    # Issuing authority and date section (bottom-right)
    doc.add(
        AbsoluteBox(
            FlexCol(
                Text("Issuing Officer Signature:", style=LABEL_STYLE),
                Div("(Signed)", style=Style(width="160px", height="55px", border="2px solid #000000", display="flex", align_items="center", justify_content="center", font_size="18px", text_align="center")),
                Text(d["issuing_officer_signature"], style=VALUE_STYLE, attrs=_ea("issuing_officer_signature")),
                Spacer(height="10px"),
                Text("Issuing Officer Name:", style=LABEL_STYLE),
                Text(d["issuing_officer_name"], style=VALUE_STYLE, attrs=_ea("issuing_officer_name")),
                Text("Designation:", style=LABEL_STYLE),
                Text(d["issuing_officer_designation"], style=VALUE_STYLE, attrs=_ea("issuing_officer_designation")),
                Text("Issue Date (BS):", style=LABEL_STYLE),
                Text(d["issue_date_bs"], style=VALUE_STYLE, attrs=_ea("issue_date_bs")),
            ),
            left="820px", top="350px", style=Style(width="350px")
        )
    )
    return doc
