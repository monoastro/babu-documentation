from __future__ import annotations
from typing import Any
from html_engine import (
    Document, Style, Heading, Text, LabelValue, FieldGroup, MultiFieldRow, FlexRow, FlexCol, AbsoluteBox, Spacer, RawHTML, Div, HorizontalRule
)

_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

LABEL_STYLE = Style(font_weight="bold", font_size="18px", width="185px", flex_shrink="0")
VALUE_STYLE = Style(font_size="18px", flex="1")

def _ea(field_name: str) -> dict[str, str]:
    return {"contenteditable": "true", "data-field": field_name}

def build_letter(data: dict[str, Any]) -> Document:
    d = {
        "ref_no": "",
        "date": "",
        "recipient": "",
        "recipient_department": "",
        "recipient_campus": "",
        "subject": "",
        "body": "",
        "signed_name": "",
        "position": "",
        "signature_placeholder": "(Signed)",
        "seal_placeholder": "Round Office Seal",
        "logo_placeholder": "Tribhuvan University Crest",
        "qr_placeholder": "QR Code",
        "watermark_placeholder": "Clock Tower Watermark",
        "bodharth_list": [],
        "email_address": "",
        "website_url": "",
        "footer_line": "---",
        "signature_seal_placeholder": "Office Stamp/Seal"
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

    # LOGO (top left)
    doc.add(
        AbsoluteBox(
            Text(d["logo_placeholder"], attrs=_ea("logo_placeholder"), style=Style(font_size="13.5px", border="2px solid #000000", border_radius="7px", padding="8px 5px", text_align="center")),
            top="22px", left="17px", style=Style(width="62px", height="62px", display="flex", align_items="center", justify_content="center")
        )
    )
    # QR CODE (top right)
    doc.add(
        AbsoluteBox(
            Text(d["qr_placeholder"], attrs=_ea("qr_placeholder"), style=Style(font_size="13.5px", border="2px solid #000000", border_radius="6px", padding="9px 7px", text_align="center")),
            top="18px", right="18px", style=Style(width="69px", height="69px", display="flex", align_items="center", justify_content="center")
        )
    )
    # Central watermark (faint background, not selectable)
    doc.add(
        AbsoluteBox(
            Text(d["watermark_placeholder"], style=Style(font_size="86px", font_weight="bold", opacity="0.12", text_align="center")),
            left="200px", top="310px", style=Style(width="500px", height="400px", pointer_events="none", user_select="none")
        )
    )

    # Header (centered)
    doc.add(
        FlexCol(
            Heading("त्रिभुवन विश्वविद्यालय", level=2, style=Style(color="#000000", font_size="19px", margin_bottom="0")),
            Heading("Tribhuvan University", level=5, style=Style(font_size="13px", color="#000000",margin="-2px 0 0 0")),
            Heading("त्रि–चन्द्र बहुमुखी क्याम्पस", level=1, style=Style(font_size="30px", color="#000000", margin_bottom="0", font_weight="bold")),
            Heading("Tri-Chandra Multiple Campus", level=2, style=Style(font_size="20px", color="#000000", font_weight="bold", margin="-2px 0 2px 0")),
            Heading("स्थापित १९७५ बि.सं./Estd. 1918 A.D.", level=5, style=Style(font_size="12px", margin_top="-6px")),
            style=Style(text_align="center", margin_top="0px", margin_bottom="1px"),
        )
    )
    # Seal placeholder (below header, above office row)
    doc.add(
        AbsoluteBox(
            Text(d["seal_placeholder"], attrs=_ea("seal_placeholder")),
            style=Style(
                width="98px", height="98px", border="2px solid #000000",
                display="flex", align_items="center", justify_content="center", font_size="15px", text_align="center", border_radius="70px"
            ),
            left="397px",
            top="124px"
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
    # Recipient 3-line block
    doc.add(
        FlexCol(
            Div(Text(d["recipient"], attrs=_ea("recipient")), style=Style(font_size="17px", margin_top="9px", margin_bottom="0")),
            Div(Text(d["recipient_department"], attrs=_ea("recipient_department")), style=Style(font_size="16.5px", margin_top="2.5px", margin_bottom="0")),
            Div(Text(d["recipient_campus"], attrs=_ea("recipient_campus")), style=Style(font_size="16.5px", margin_top="2px", margin_bottom="0")),
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
    # Signature and office stamp
    doc.add(
        FlexRow(
            Div(style=Style(width="55%")),
            FlexCol(
                Spacer(height="58px"),
                Text(d["signature_placeholder"], attrs=_ea("signature_placeholder"), style=Style(font_size="15px", border="1.8px dashed #000000", padding="6px 13px", margin_bottom="5.2px")),
                Text(d["signed_name"], attrs=_ea("signed_name"), style=Style(font_weight="bold", font_size="18px", margin_bottom="2.5px")),
                Text(d["position"], attrs=_ea("position"), style=Style(font_size="16px", color="#000000", margin_bottom="8px")),
                # Stamp/seal placeholder under signatory
                Text(d["signature_seal_placeholder"], attrs=_ea("signature_seal_placeholder"), style=Style(border="2px solid #000000", border_radius="49px", font_size="13.6px", width="110px", margin="5px auto 2px auto", padding="7px 0", text_align="center")),
                style=Style(text_align="center", width="278px"),
            ),
            style=Style(margin_top="13px", margin_bottom="7px")
        )
    )
    # बोधार्थ:/CC list
    doc.add(
        Heading("बोधार्थ:", level=4, style=Style(font_size="18px", color="#000000", margin_top="7px")),
    )
    bodh = d["bodharth_list"] if d["bodharth_list"] else []
    doc.add(
        FlexCol(*[
            Text(f"{row}", attrs=_ea(f"bodharth_list.{i}"), style=Style(font_size="16.5px")) for i, row in enumerate(bodh)
        ],
        style=Style(gap="2.5px", margin_left="18px", margin_top="3px", margin_bottom="4px")
        )
    )
    # Horizontal Rule and Footer: email (left) | website (right)
    doc.add(
        FlexCol(
            HorizontalRule(style=Style(margin_top="14px", margin_bottom="2px", border_top="1.8px solid #000000")),
            FlexRow(
                Text("Email: " + d["email_address"], attrs=_ea("email_address"), style=Style(font_size="14px", color="#000000", text_align="left", flex="1", padding_left="7px")),
                Text("Website: " + d["website_url"], attrs=_ea("website_url"), style=Style(font_size="14px", color="#000000", text_align="right", flex="1", padding_right="7px")),
                style=Style(justify_content="space-between", width="100%", align_items="center")
            ),
            style=Style(width="99.5%", margin_bottom="2.5px", margin_top="-7px")
        )
    )
    return doc
