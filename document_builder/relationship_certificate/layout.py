"""
Relationship Certificate Layout — document_builder/relationship_certificate/layout_1.py
Faithful digital replica of the relationship certificate issued by a Nepal municipality ward office.
Imports html_engine and builds all fields declared in the extraction schema. Placeholder boxes render seals, emblems, photos, and signatures.
Editable fields are annotated with contenteditable="true" and the correct data-field attribute.
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

def _ea(field_name: str):
    return {"contenteditable": "true", "data-field": field_name}

def build_relationship_certificate(data: dict[str, Any]) -> Document:
    d = {k: (v if v is not None else "") for k, v in data.items()}
    doc = Document(
        "Relationship Certificate",
        page_width="930px", page_height="auto", background="#ffffff",
        font_family='"Times New Roman", serif', border="1.4px solid #000000",
        page_style=Style(padding="24px 36px", box_sizing="border-box"),
        extra_css=_EDITABLE_CSS,
    )

    ###### Header block: emblems, QR, office data
    doc.add(
        FlexRow(
            FlexCol(
                PlaceholderBox("Coat of Arms of Nepal", size="68px", shape="circle", style=Style(margin_bottom="7px")),
                LabelValue("Letter No.:", d.get("letter_no", ""), value_attrs=_ea("letter_no"), label_style=Style(width="104px", font_weight="bold", font_size="13px")),
                LabelValue("Ref No.:", d.get("ref_no", ""), value_attrs=_ea("ref_no"), label_style=Style(width="104px", font_weight="bold", font_size="13px")),
                style=Style(gap="3px", margin_right="18px")
            ),
            FlexCol(
                Heading(d.get("office_name", "Nagarjun Municipality 10 No. Ward Office"), level=1, style=Style(text_align="center", font_size="22px", font_weight="bold", margin_bottom="2px")),
                Text(d.get("municipality", ""), style=Style(text_align="center", font_size="15px", font_weight="bold"), attrs=_ea("municipality")),
                Text(f"Ward No.: {d.get('ward_no','')}", style=Style(text_align="center", font_size="13px"), attrs=_ea("ward_no")),
                Text(f"District: {d.get('district','')} | Province: {d.get('province','')}", style=Style(text_align="center", font_size="13px")),
                style=Style(align_items="center", gap="0px")
            ),
            FlexCol(
                PlaceholderBox("Round Office Seal", shape="circle", size="64px", style=Style(margin_bottom="5px")),
                PlaceholderBox("QR Code", shape="rect", size="54px", style=Style(margin_bottom="9px")),
                LabelValue("Date:", d.get("date", ""), value_attrs=_ea("date"), label_style=Style(width="65px", font_weight="bold", font_size="13px")),
                style=Style(align_items="flex-end", gap="3px", margin_left="18px")
            ),
            style=Style(justify_content="space-between", align_items="flex-start", width="100%")
        )
    )
    doc.add(Spacer(height="9px"))

    ###### Subject heading
    doc.add(
        Heading(d.get("subject", "RELATIONSHIP VERIFICATION"), level=2,
            style=Style(font_size="17px", text_align="center", font_weight="bold", text_decoration="underline", margin_top="2px", margin_bottom="6px"))
    )
    doc.add(Text("To Whom It May Concern", style=Style(font_size="15px", text_align="center", font_weight="bold", margin_bottom="10px")))

    ###### Certificate main text
    doc.add(Text(d.get("main_text", ""), style=Style(font_size="15px", line_height="1.6", margin_bottom="16px"), attrs=_ea("main_text")))

    ###### Family members as horizontal image-and-label row
    members = d.get("family_members", [])
    member_blocks = []
    for i, member in enumerate(members):
        block = FlexCol(
            PlaceholderBox("Photograph", shape="rect", size="99px", style=Style(margin_bottom="7px")),
            Text(member.get("name", ""), style=Style(font_size="14px", font_weight="bold", text_align="center"), attrs=_ea(f"family_members.{i}.name")),
            Text(member.get("relation", ""), style=Style(font_size="13px", text_align="center", font_style="italic"), attrs=_ea(f"family_members.{i}.relation")),
            style=Style(width="152px", align_items="center", margin_left="11px", margin_right="11px")
        )
        member_blocks.append(block)
    doc.add(
        FlexRow(
            *member_blocks,
            style=Style(justify_content="center", align_items="flex-start", margin_top="8px", margin_bottom="22px")
        )
    )

    ###### Footer: signature and office stamp
    doc.add(
        FlexRow(
            Spacer(width="24px"),
            SignatureBlock(
                name=d.get("ward_chairperson_name", ""),
                name_field="ward_chairperson_name",
                title=d.get("ward_chairperson_title", ""),
                title_field="ward_chairperson_title",
                signature_label="(Signed)",
                align="left",
                style=Style(margin_top="12px", min_width="302px"),
            ),
            Spacer(width="25px"),
            PlaceholderBox("Office Seal", shape="circle", size="78px", style=Style(margin_left="20px")),
            style=Style(justify_content="flex-end", align_items="flex-end", margin_top="4px", margin_bottom="0px")
        )
    )

    return doc
