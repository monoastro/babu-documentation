"""
SEE Certificate Layout — document_builder/see_certificate/layout_1.py
Structured digital replica of the Secondary Education Examination Certificate.
Follows schema see_certificate_patched.json. Placeholder boxes for emblems, signature, and seal.
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

def build_see_certificate(data: dict) -> Document:
    def safe_get(key, default=""):
        v = data.get(key, default)
        return v if v is not None else default
    _ea = lambda fld: {"contenteditable": "true", "data-field": fld}

    doc = Document(
        "Secondary Education Examination Certificate",
        page_width="850px", page_height="auto", background="#ffffff",
        font_family='"Times New Roman", serif', border="1.3px solid #000000",
        page_style=Style(padding="30px 40px", box_sizing="border-box"),
        extra_css=_EDITABLE_CSS,
    )

    # --- HEADER ---
    doc.add(
        FlexRow(
            FlexCol(
                PlaceholderBox(
                    safe_get("emblem_placeholder", "Coat of Arms of Nepal"),
                    size="64px", shape="circle", field="emblem_placeholder",
                    style=Style(margin_right="8px", margin_bottom="6px")
                ),
                style=Style(min_width="70px", align_items="flex-start")
            ),
            FlexCol(
                Text("GOVERNMENT OF NEPAL", style=Style(font_weight="bold", font_size="13px", letter_spacing="0.5px", text_align="center")),
                Text("NATIONAL EXAMINATIONS BOARD", style=Style(font_weight="bold", font_size="15px", text_align="center")),
                Text("SECONDARY EDUCATION EXAMINATION, GRADE-10", style=Style(font_weight="bold", font_size="14px", text_align="center", margin_bottom="6px")),
                Spacer(height="5px"),
                FlexRow(
                    Text(safe_get("certificate_title_np"), style=Style(font_weight="bold", font_size="22px", text_align="center", letter_spacing="0.5px"), attrs=_ea("certificate_title_np")),
                    style=Style(width="100%", justify_content="center")
                ),
                FlexRow(
                    Text(safe_get("certificate_title_en"), style=Style(font_weight="bold", font_size="22px", text_align="center", font_style="italic", margin_top="2px", letter_spacing="0.5px"), attrs=_ea("certificate_title_en")),
                    style=Style(width="100%", justify_content="center", margin_bottom="8px")
                ),
                style=Style(align_items="center", justify_content="center", width="460px")
            ),
            FlexCol(
                FlexRow(
                    Text("SR NO:", style=Style(font_weight="bold", font_size="13px")),
                    Text(safe_get("sr_no"), attrs=_ea("sr_no"), style=Style(font_size="13.5px", margin_left="4px", letter_spacing="0.2px")),
                    style=Style(align_items="center")
                ),
                PlaceholderBox(
                    safe_get("board_logo_placeholder", "NEB Board Logo"),
                    size="58px", shape="circle", field="board_logo_placeholder",
                    style=Style(margin_left="10px", margin_top="5px")
                ),
                style=Style(min_width="90px", align_items="flex-end")
            ),
            style=Style(width="100%", justify_content="space-between", align_items="flex-start")
        )
    )
    doc.add(Spacer(height="24px"))

    # --- BODY ---
    doc.add(
        Text(
            "This is to certify that ",
            style=Style(font_size="15px", display="inline", font_family='"Times New Roman", serif')
        )
    )
    doc.add(
        Text(
            safe_get("student_name"),
            style=Style(font_size="16px", font_weight="bold", display="inline", margin_left="3px"), attrs=_ea("student_name")
        )
    )
    doc.add(Text(", a student of ", style=Style(font_size="15px", display="inline")))
    doc.add(
        Text(
            safe_get("school_name"),
            style=Style(font_size="15.5px", font_weight="bold", display="inline", margin_left="3px"), attrs=_ea("school_name")
        )
    )
    doc.add(Text(",", style=Style(font_size="15px", display="inline")))
    doc.add(Spacer(height="4px"))
    doc.add(
        FlexRow(
            Text("Roll", style=Style(font_size="14px", font_weight="bold", margin_right="6px", margin_left="0px")),
            Text(safe_get("roll_no"), attrs=_ea("roll_no"), style=Style(font_size="14px", margin_right="4px")),
            Text(", has duly completed the Secondary Education Examination, Grade-10 in the year ", style=Style(font_size="14px", margin_right="0px")),
            Text(safe_get("examination_year_bs"), attrs=_ea("examination_year_bs"), style=Style(font_size="14px", font_weight="bold", margin_right="2px")),
            Text(" BS (", style=Style(font_size="14px")),
            Text(safe_get("examination_year_ad"), attrs=_ea("examination_year_ad"), style=Style(font_size="14px", font_weight="bold")),
            Text(" AD)", style=Style(font_size="14px")),
            style=Style(flex_wrap="wrap")
        )
    )
    doc.add(Spacer(height="4px"))
    doc.add(
        FlexRow(
            Text("with Grade Point Average (GPA) ", style=Style(font_size="14px")),
            Text(safe_get("gpa"), attrs=_ea("gpa"), style=Style(font_size="14px", font_weight="bold", margin_right="6px")),
            Text(". According to the record of this office, his/her date of birth is ", style=Style(font_size="14px")),
            Text(safe_get("date_of_birth_bs"), attrs=_ea("date_of_birth_bs"), style=Style(font_size="14px", font_weight="bold")),
            Text(" BS (", style=Style(font_size="14px")),
            Text(safe_get("date_of_birth_ad"), attrs=_ea("date_of_birth_ad"), style=Style(font_size="14px", font_weight="bold")),
            Text(" AD)", style=Style(font_size="14px")),
            style=Style(flex_wrap="wrap")
        )
    )
    doc.add(Spacer(height="16px"))
    # --- CERTIFICATE DETAIL BLOCK ---
    doc.add(
        FlexRow(
            FlexCol(
                LabelValue("Symbol No.:", safe_get("symbol_no"), value_attrs=_ea("symbol_no"), label_style=Style(width="99px", font_weight="bold")),
                LabelValue("Date of Issue:", safe_get("date_of_issue"), value_attrs=_ea("date_of_issue"), label_style=Style(width="99px", font_weight="bold")),
                Spacer(height="12px"),
                LabelValue("CHECKED BY:", safe_get("checked_by"), value_attrs=_ea("checked_by"), label_style=Style(width="99px", font_weight="bold")),
                style=Style(min_width="270px", justify_content="flex-start")
            ),
            FlexCol(
                Spacer(height="42px"),
                SignatureBlock(
                    name=safe_get("signature_name"),
                    name_field="signature_name",
                    title=safe_get("signature_title"),
                    title_field="signature_title",
                    signature_label=safe_get("signature_placeholder", "(Signed)"),
                    stamp_label=safe_get("seal_placeholder", "Round Office Seal"),
                    align="left",
                    style=Style(margin_top="8px", min_width="248px")
                ),
                style=Style(justify_content="flex-end", align_items="flex-end", min_width="270px")
            ),
            style=Style(width="100%", justify_content="space-between", align_items="flex-end", margin_bottom="3px")
        )
    )
    doc.add(Spacer(height="17px"))
    # --- FOOTER ---
    doc.add(Div(style=Style(width="100%", border_bottom="1.1px solid #000000", height="1px", margin_bottom="3px")))
    doc.add(
        FlexRow(
            Text(safe_get("footer_line"), style=Style(font_size="11px")),
            Text(safe_get("controller_label", "CONTROLLER OF EXAMINATIONS"), attrs=_ea("controller_label"), style=Style(font_size="11px", text_align="right", font_weight="bold")),
            style=Style(width="100%", justify_content="space-between", align_items="center", margin_top="2px")
        )
    )
    return doc
