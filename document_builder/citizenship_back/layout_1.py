from __future__ import annotations
from typing import Any
from html_engine import (
    Document, Style, Heading, Text, LabelValue, AbsoluteBox,
    FlexRow, FlexCol, Div, Spacer, PlaceholderBox, SignatureBlock
)

_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

def _ea(field_name: str) -> dict[str, str]:
    return {"contenteditable": "true", "data-field": field_name}

def build_citizenship_back(data: dict[str, Any]) -> Document:
    d = {
        "citizenship_no": "",
        "full_name": "",
        "sex": "",
        "dob_year": "",
        "dob_month": "",
        "dob_day": "",
        "birth_district": "",
        "birth_rm_mn": "",
        "birth_ward_no": "",
        "perm_district": "",
        "perm_municipality": "",
        "perm_ward_no": "",
        "nepal_citizenship_act_sentence": "",
        "citizenship_type": "",
        "certificate_holder_signature_label": "",
        "right_thumb_label": "",
        "left_thumb_label": "",
        "authority_name": "",
        "authority_title": "",
        "issue_date_bs": "",
        "remarks": ""
    }
    d.update({k: v for k, v in data.items() if k in d})

    doc = Document(
        "Nepali Citizenship Certificate (Back)",
        page_width="1086px",
        page_height="768px",
        background="#ffffff",
        font_family='"Times New Roman"',
        border="2px solid #000000",
        extra_css=_EDITABLE_CSS,
    )

    # Header box
    doc.add(
        AbsoluteBox(
            FlexCol(
                Text("Government of Nepal has issued this Citizenship Certificate with following details.", style=Style(font_weight="bold", font_size="16px", margin_bottom="4px")),
                FlexRow(
                    LabelValue("Citizenship Certificate No.:", d["citizenship_no"], value_attrs=_ea("citizenship_no")),
                    LabelValue("Sex:", d["sex"], value_attrs=_ea("sex"), label_style=Style(font_weight="bold")),
                    gap="40px"
                ),
                FlexRow(
                    LabelValue("Full Name:", d["full_name"], value_attrs=_ea("full_name")),
                    gap="40px"
                ),
                FlexRow(
                    LabelValue("Date of Birth (AD):", f"Year: {d['dob_year']}  Month: {d['dob_month']}  Day: {d['dob_day']}", value_attrs=_ea("dob_year")),
                    gap="40px"
                ),
                FlexRow(
                    LabelValue("Birth Place:", f"District: {d['birth_district']}   R. M.: {d['birth_rm_mn']}   Ward No.: {d['birth_ward_no']}", value_attrs=_ea("birth_district")),
                    gap="40px"
                ),
                FlexRow(
                    LabelValue("Permanent Address:", f"District: {d['perm_district']}   Municipality: {d['perm_municipality']}   Ward No.: {d['perm_ward_no']}", value_attrs=_ea("perm_district")),
                    gap="40px"
                ),
            ),
            top="22px",
            left="20px",
            style=Style(width="1035px", border="1.5px solid #000000", padding="12px"),
        )
    )

    # Act compliance sentence (below header)
    doc.add(
        AbsoluteBox(
            Text(d["nepal_citizenship_act_sentence"], attrs=_ea("nepal_citizenship_act_sentence"), style=Style(font_size="15px", margin_top="7px", margin_bottom="3px")),
            top="148px",
            left="30px",
            style=Style(width="1005px")
        )
    )

    # Citizenship type (below act sentence)
    doc.add(
        AbsoluteBox(
            FlexRow(
                Text("Citizenship Type:", style=Style(font_weight="bold", font_size="16px", margin_right="4px")),
                Text(d["citizenship_type"], attrs=_ea("citizenship_type"), style=Style(font_size="16px")),
                gap="10px"
            ),
            top="176px",
            left="30px",
        )
    )

    # Signature & thumb impressions section (left/middle)
    doc.add(
        AbsoluteBox(
            FlexCol(
                Text(d["certificate_holder_signature_label"], attrs=_ea("certificate_holder_signature_label"), style=Style(font_weight="bold", font_size="15px", margin_bottom="6px")),
                FlexRow(
                    # Right thumb
                    FlexCol(
                        Text("Right Thumb", style=Style(font_weight="bold", font_size="15px", margin_bottom="2px")),
                        PlaceholderBox(label="Right Thumb Impression", size="150px", shape="rect"),
                        Text(d["right_thumb_label"], attrs=_ea("right_thumb_label"), style=Style(font_size="15px")),
                    ),
                    Spacer(width="40px"),
                    # Left thumb
                    FlexCol(
                        Text("Left Thumb", style=Style(font_weight="bold", font_size="15px", margin_bottom="2px")),
                        PlaceholderBox(label="Left Thumb Impression", size="150px", shape="rect"),
                        Text(d["left_thumb_label"], attrs=_ea("left_thumb_label"), style=Style(font_size="15px")),
                    ),
                ),
            ),
            top="212px",
            left="40px",
            style=Style(width="400px", gap="14px")
        )
    )

    # Signature and Official section (right side)
    doc.add(
        AbsoluteBox(
            FlexCol(
                Text("Authorized Official issuing this Certificate:", style=Style(font_weight="bold", font_size="16px", margin_bottom="5px")),
                SignatureBlock(
                    name=d["authority_name"],
                    title=d["authority_title"],
                    signature_label="(Signed)",
                    name_field="authority_name",
                    title_field="authority_title",
                    rule_gap="18px",
                    align="left",
                ),
                FlexRow(
                    LabelValue("Issue Date (BS):", d["issue_date_bs"], value_attrs=_ea("issue_date_bs")),
                    gap="10px"
                ),
            ),
            top="210px",
            left="600px",
            style=Style(width="440px", border="1px solid #000000", padding="18px")
        )
    )

    # Remarks / legal note
    doc.add(
        AbsoluteBox(
            Text(d["remarks"], attrs=_ea("remarks"), style=Style(font_size="15px", margin_top="8px")),
            left="24px",
            bottom="44px",
            style=Style(width="1000px")
        )
    )

    return doc
