"""
Tax Clearance Certificate Layout — document_builder/tax_clearance/layout_1.py
Faithful digital replica of the tax clearance certificate as structured digital document. All fields are mapped to their English-label equivalents, values in original script. Placeholder boxes are used for emblem, QR, and officer's signature/seal.
"""

from __future__ import annotations
from typing import Any
from html_engine import (
    Document, Heading, Text, LabelValue, FlexRow, FlexCol, Div, Spacer, Style, PlaceholderBox, SignatureBlock
)

_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

def build_tax_clearance(data: dict) -> Document:
    # Replace None with empty string for every value except for lists
    def safe_get(key, default=""):
        v = data.get(key, default)
        return v if v is not None else default
    def safe_items(key):
        v = data.get(key, [])
        return v if v is not None else []
    _ea = lambda fld: {"contenteditable": "true", "data-field": fld}

    doc = Document(
        "Tax Clearance Certificate",
        page_width="900px", page_height="auto", background="#ffffff",
        font_family='"Times New Roman", serif', border="1.3px solid #000000",
        page_style=Style(padding="22px 34px", box_sizing="border-box"),
        extra_css=_EDITABLE_CSS,
    )

    # --- HEADER ---
    doc.add(
        FlexRow(
            FlexCol(
                PlaceholderBox("Coat of Arms of Nepal", size="62px", shape="circle", style=Style(margin_bottom="10px")),
                style=Style(margin_right="18px") if safe_get("emblem_present") else Style(display="none"),
            ),
            FlexCol(
                Text(safe_get("office_name"), style=Style(font_weight="bold", font_size="15px", text_align="center", line_height="1.55", letter_spacing="0.01em"), attrs=_ea("office_name")),
                style=Style(min_width="357px", margin_top="3px", margin_right="20px", align_items="center", justify_content="center")
            ),
            FlexCol(
                # Info header block: letter, reg, notice numbers and dates
                LabelValue("Letter No.:", safe_get("letter_no"), value_attrs=_ea("letter_no"), label_style=Style(width="87px")),
                LabelValue("Reg. No.:", safe_get("registration_no"), value_attrs=_ea("registration_no"), label_style=Style(width="87px")),
                LabelValue("Tax Notice No.:", safe_get("tax_notice_no"), value_attrs=_ea("tax_notice_no"), label_style=Style(width="87px")),
                LabelValue("Issue Date (BS):", safe_get("issue_date_nepali"), value_attrs=_ea("issue_date_nepali"), label_style=Style(width="110px")),
                LabelValue("Print Date (BS):", safe_get("print_date_nepali"), value_attrs=_ea("print_date_nepali"), label_style=Style(width="110px")),
                PlaceholderBox("QR Code", shape="rect", size="54px", style=Style(margin_top="9px")) if safe_get("qr_present") else Spacer(height="0px"),
                style=Style(gap="3px", align_items="flex-end", margin_left="12px")
            ),
            style=Style(justify_content="space-between", align_items="flex-start", width="100%")
        )
    )
    doc.add(Spacer(height="10px"))

    # --- SUBJECT ---
    doc.add(
        Heading(f"Subject: {safe_get('subject')}", level=2, style=Style(font_size="17px", text_align="center", font_weight="bold", text_decoration="underline", margin_top="5px", margin_bottom="10px"))
    )

    # --- RECIPIENT BLOCK ---
    doc.add(
        FlexCol(
            LabelValue("Recipient Name:", safe_get("recipient_name"), value_attrs=_ea("recipient_name")),
            LabelValue("Address:", safe_get("recipient_address"), value_attrs=_ea("recipient_address")),
            LabelValue("PAN No.:", safe_get("recipient_pan"), value_attrs=_ea("recipient_pan")),
            style=Style(margin_bottom="15px", margin_left="12px", gap="2px")
        )
    )

    # --- MAIN TEXT ---
    doc.add(Text(safe_get("main_text"), style=Style(font_size="15px", line_height="1.6", margin_bottom="15px"), attrs=_ea("main_text")))

    # --- INCOME ITEMS TABLE ---
    doc.add(
        Div(
            Heading("Income Items", level=3, style=Style(font_size="14px", font_weight="bold", margin_bottom="6px")),
            FlexRow(
                Div(Text("Title", style=Style(font_weight="bold", font_size="13px")), style=Style(width="310px", border_bottom="1.1px solid #000")),
                Div(Text("Amount (NPR)", style=Style(font_weight="bold", font_size="13px")), style=Style(width="170px", border_bottom="1.1px solid #000")),
                style=Style(gap="12px", margin_bottom="2px")
            ),
            *[
                FlexRow(
                    Div(Text(row.get("item", ""), attrs=_ea(f"income_items.{i}.item")), style=Style(width="310px", border_bottom="0.85px solid #000")),
                    Div(Text(row.get("amount", ""), attrs=_ea(f"income_items.{i}.amount")), style=Style(width="170px", text_align="right", border_bottom="0.85px solid #000")),
                    style=Style(gap="12px")
                )
                for i, row in enumerate(safe_items("income_items"))
            ],
            # Total income row
            FlexRow(
                Div(Text("Total Income", style=Style(font_weight="bold")), style=Style(width="310px")),
                Div(Text(safe_get("total_income"), attrs=_ea("total_income")), style=Style(width="170px", text_align="right")),
                style=Style(gap="12px", margin_top="2px", border_top="1px solid #000")
            ),
            style=Style(border="1.1px solid #000000", padding="14px 16px", margin_top="10px", margin_bottom="18px", border_radius="5px", background="#ffffff")
        )
    )

    # --- SIGNATURE + FOOTER ---
    doc.add(
        FlexRow(
            Spacer(width="40px"),
            SignatureBlock(
                name=safe_get("certifying_officer_name"),
                name_field="certifying_officer_name",
                title=safe_get("certifying_officer_title"),
                title_field="certifying_officer_title",
                signature_label=safe_get("signature_label"),
                align="left",
                style=Style(margin_top="12px", min_width="242px"),
            ),
            Spacer(width="25px"),
            PlaceholderBox("Office Seal", shape="circle", size="67px", style=Style(margin_left="28px", margin_top="7px")),
            style=Style(justify_content="flex-end", align_items="flex-end", margin_top="8px", margin_bottom="0px")
        )
    )

    # --- FOOTER REMARKS/NOTES ---
    doc.add(
        Div(
            Text(safe_get("remarks"), attrs=_ea("remarks"), style=Style(font_size="12px", line_height="1.55")),
            style=Style(margin_top="15px", padding="7px 0 3px 0")
        )
    )

    return doc
