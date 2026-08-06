from __future__ import annotations
from typing import Any
from html_engine import (
    Document, Style, Heading, Text, LabelValue, FieldGroup, MultiFieldRow, FlexRow, FlexCol, AbsoluteBox, Spacer, RawHTML, Div
)

_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

LABEL_STYLE = Style(font_weight="bold", font_size="18px", width="185px", flex_shrink="0")
VALUE_STYLE = Style(font_size="18px", flex="1")

# Helper for editable attribute
def _ea(field_name: str) -> dict[str, str]:
    return {"contenteditable": "true", "data-field": field_name}

def build_letter(data: dict[str, Any]) -> Document:
    d = {
        "ref_no": "",
        "date": "",
        "recipient": "",
        "subject": "",
        "body": "",
        "signed_name": "",
        "position": "",
        "signature_placeholder": "(Signed)",
        "seal_placeholder": "Round Office Seal",
        "bodharth_list": [],
    }
    d.update(data or {})

    doc = Document(
        "Tri-Chandra Letter",
        page_width="900px",
        page_height="1320px",
        background="#ffffff",
        font_family='"Times New Roman", "Noto Sans Devanagari", serif',
        extra_css=_EDITABLE_CSS,
        border="1px solid #000000"
    )

    # Header: Tri-Chandra and Tribhuvan U.
    doc.add(
        FlexRow(
            Div(
                Heading("त्रिभुवन विश्वविद्यालय", level=2, style=Style(color="#000000", font_size="19px", margin_bottom="0")),
                Heading("Tribhuvan University", level=5, style=Style(font_size="13px", color="#000000",margin="-2px 0 0 0")),
                style=Style(text_align="left", flex="1", padding_left="14px"),
            ),
            Div(
                Heading("Ph. No. +977-014244047", level=5, style=Style(font_weight="normal", font_size="13px", color="#000000", text_align="right")),
                style=Style(flex="1", text_align="right", padding_right="18px"),
            ),
            style=Style(width="100%", align_items="flex-start", gap="20px", margin_top="12px"),
        )
    )
    doc.add(
        FlexCol(
            Heading("त्रि–चन्द्र बहुमुखी क्याम्पस", level=1, style=Style(font_size="30px", color="#000000", margin_bottom="0", font_weight="bold")),
            Heading("Tri-Chandra Multiple Campus", level=2, style=Style(font_size="20px", color="#000000", font_weight="bold", margin="-2px 0 2px 0")),
            Heading("स्थापना १९७५ ई.स./Estd. 1918 A.D.", level=5, style=Style(font_size="12px", margin_top="-6px")),
            style=Style(text_align="center", margin_top="0px", margin_bottom="4px"),
        )
    )
    # Seal placeholder (top near QR/stamp)
    doc.add(
        AbsoluteBox(
            Text(d["seal_placeholder"], attrs=_ea("seal_placeholder")),
            style=Style(
                width="110px", height="110px", border="2px solid #000000",
                display="flex", align_items="center", justify_content="center", font_size="15px", text_align="center", border_radius="70px"
            ),
            left="520px",
            top="55px"
        )
    )

    # Office/contact row
    doc.add(
        FlexRow(
            Div(
                Text("क्याम्पस प्रमुखको कार्यालय", style=Style(color="#000000", font_weight="bold", font_size="12.5px")),
                RawHTML("<br>"),
                Text("Office of the Campus Chief", style=Style(color="#000000", font_size="12px")),
                RawHTML("<br>"),
                LabelValue("Ref. No.:", d["ref_no"], label_style=LABEL_STYLE, value_style=VALUE_STYLE, value_attrs=_ea("ref_no")),
                style=Style(padding_left="17px", width="55%"),
            ),
            Div(
                Text("सरस्वती सदन, घण्टाघर, काठमाडौं, नेपाल\nSaraswati Sadan, Ghantaghar, Kathmandu, Nepal", style=Style(font_size="13px")),
                RawHTML("<br>"),
                LabelValue("Date:", d["date"], label_style=LABEL_STYLE, value_style=VALUE_STYLE, value_attrs=_ea("date")),
                style=Style(text_align="right", padding_right="18px", width="45%"),
            ),
            style=Style(width="98%", margin_top="5px")
        )
    )
    # Body – recipient block
    doc.add(
        FlexCol(
            Div(Text(d["recipient"], attrs=_ea("recipient")), style=Style(font_size="17px", margin_top="25px", margin_bottom="0")),
            style=Style(margin_top="18px", margin_bottom="0")
        )
    )
    doc.add(Spacer(height="3px"))
    # Subject
    doc.add(
        Heading("Subject:", level=4, style=Style(font_size="18px", margin="5px 0 0 0", color="#000000")),
    )
    doc.add(
        Div(Text(d["subject"], attrs=_ea("subject")), style=Style(font_size="17px", margin_bottom="6px"))
    )
    # Body letter text
    doc.add(
        Div(Text(d["body"], attrs=_ea("body")), style=Style(font_size="17.7px", white_space="pre-wrap", margin="9px 0"))
    )
    # Signature and name
    doc.add(
        FlexRow(
            Div(style=Style(width="55%")),
            FlexCol(
                Spacer(height="70px"),
                Text(d["signature_placeholder"], attrs=_ea("signature_placeholder"), style=Style(font_size="15px", border="1.8px dashed #000000", padding="6px 13px", margin_bottom="6px")),
                Text(d["signed_name"], attrs=_ea("signed_name"), style=Style(font_weight="bold", font_size="18px", margin_bottom="2px")),
                Text(d["position"], attrs=_ea("position"), style=Style(font_size="16px", color="#000000")),
                style=Style(text_align="center", width="270px"),
            ),
            style=Style(margin_top="12px", margin_bottom="6px")
        )
    )
    # बोधार्थ:/CC list
    doc.add(
        Heading("बोधार्थ:", level=4, style=Style(font_size="18px", color="#000000", margin_top="7px")),
    )
    bodh = d["bodharth_list"] if d["bodharth_list"] else []
    doc.add(
        FlexCol(*[
            Text(f"{i+1}) {row}", attrs=_ea(f"bodharth_list.{i}"), style=Style(font_size="16.5px")) for i, row in enumerate(bodh)
        ],
        style=Style(gap="2.5px", margin_left="18px", margin_top="3px", margin_bottom="4px")
        )
    )
    return doc
