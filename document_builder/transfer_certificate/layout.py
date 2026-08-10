"""
Transfer Certificate Layout — document_builder/transfer_certificate/layout_1.py
Faithful digital replica of the transfer certificate issued by a Nepali school.
Imports html_engine and builds all fields declared in the extraction schema. Placeholder boxes render seals, logos, and signatures.
Editable fields are annotated with contenteditable="true" and the correct data-field attribute.
"""

from __future__ import annotations
from typing import Any
from html_engine import (
    Document, Heading, Text, LabelValue, FlexRow, FlexCol, Div, Spacer, Style, PlaceholderBox
)

_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

def _ea(field_name: str):
    return {"contenteditable": "true", "data-field": field_name}

def build_transfer_certificate(data: dict[str, Any]) -> Document:
    d = {k: (v if v is not None else "") for k, v in data.items()}
    doc = Document(
        "Transfer Certificate",
        page_width="850px", page_height="auto", background="#ffffff",
        font_family='"Times New Roman", serif', border="1.4px solid #000000",
        page_style=Style(padding="34px 38px", box_sizing="border-box"),
        extra_css=_EDITABLE_CSS,
    )

    ###### Header section: School logo, School Name, School Address/Contact
    doc.add(FlexCol(
        PlaceholderBox(
            label=d.get("school_logo_label", "School Logo"),
            size="84px",
            shape="circle",
            style=Style(margin="0 auto 15px auto")
        ),
        Heading(d.get("school_name", ""), level=1, style=Style(text_align="center", font_weight="bold", font_size="26px", letter_spacing="1.3px", margin_bottom="1px"), attrs=_ea("school_name")),
        Text(d.get("school_address", ""), style=Style(text_align="center", font_size="14px", margin_bottom="1px"), attrs=_ea("school_address")),
        Text(d.get("school_contact", ""), style=Style(text_align="center", font_size="13px", margin_bottom="12px"), attrs=_ea("school_contact")),
    ))
    doc.add(Spacer(height="4px"))
    doc.add(
        Heading(d.get("certificate_title", ""), level=2,
            style=Style(font_size="18px", text_align="center", font_weight="bold", text_decoration="underline", margin="7px 0 15px 0"),
            attrs=_ea("certificate_title")
        )
    )
    doc.add(Spacer(height="8px"))

    ###### Main Certificate Body
    doc.add(Div(
        Text(
            f"This is to certify that {d.get('student_full_name', '')}, son of {d.get('father_name', '')}, was a student of {d.get('grade', '')} in this School during the academic session {d.get('academic_session', '')}. He has passed the {d.get('exam_name', '')} held in the year {d.get('exam_year', '')} with Grade Point Average (GPA) {d.get('gpa', '')} under Symbol No. {d.get('symbol_no', '')} (Registration No. {d.get('registration_no', '')}).",
            style=Style(font_size="15px", line_height="1.8", margin_bottom="10px"),
            attrs=_ea("student_full_name")
        ),
        Text(
            f"As per our records, the date of birth of {d.get('student_full_name', '')} is {d.get('dob_bs', '')} ({d.get('dob_ad', '')}). {d.get('character_statement', '')}",
            style=Style(font_size="15px", line_height="1.8", margin_bottom="8px"),
            attrs=_ea("dob_bs")
        ),
        Text(
            f"{d.get('co_curricular_statement', '')}",
            style=Style(font_size="15px", line_height="1.8", margin_bottom="15px"),
            attrs=_ea("co_curricular_statement")
        ),
    ))

    ###### Footer: date, seal, principal signature
    doc.add(FlexRow(
        FlexCol(
            LabelValue("Dated:", d.get("date_of_issue", ""), value_attrs=_ea("date_of_issue"), label_style=Style(width="62px", font_weight="bold", font_size="14px")),
            style=Style(justify_content="flex-start", min_width="150px", margin_top="16px")
        ),
        Spacer(width="50px"),
        FlexCol(
            PlaceholderBox(
                label=d.get("school_seal_label", "School Seal"),
                size="73px",
                shape="circle",
                style=Style(margin="0 auto 2px auto")
            ),
            style=Style(align_items="center")
        ),
        Spacer(width="60px"),
        FlexCol(
            PlaceholderBox(
                label=d.get("principal_signature_label", "(Signed)"),
                size="64px",
                shape="rect",
                dashed=True,
                style=Style(margin_bottom="2px")
            ),
            Text(
                d.get("principal_name", ""),
                style=Style(text_align="center", font_weight="bold", font_size="15px"),
                attrs=_ea("principal_name")
            ),
            Text(
                d.get("principal_title", ""),
                style=Style(text_align="center", font_size="13px"),
                attrs=_ea("principal_title")
            ),
            style=Style(align_items="center", min_width="180px")
        ),
        style=Style(justify_content="space-between", align_items="flex-end", margin_top="28px", margin_bottom="11px", width="100%")
    ))

    doc.add(Spacer(height="30px"))

    return doc
