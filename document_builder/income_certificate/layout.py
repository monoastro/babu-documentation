"""
Income Certificate Layout — document_builder/income_certificate/layout_1.py
Faithful digital replica of the source income certificate issued by a Nepal municipality ward office.
Imports html_engine and builds all fields declared in the extraction schema. Placeholder boxes render seals and signatures.
Editable fields are annotated with `contenteditable="true"` and the correct `data-field` attribute.
"""

from __future__ import annotations
from typing import Any
from html_engine import (
    Document, Heading, Text, LabelValue, FlexRow, FlexCol, Div, Spacer, Table, TableRow, TableCell, Style, PlaceholderBox, SignatureBlock
)

_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

def _ea(field_name: str):
    return {"contenteditable": "true", "data-field": field_name}

def _lv(label, value, lw="160px", field_name=""):
    va = _ea(field_name) if field_name else {}
    la = _ea(f"label.{field_name}") if field_name else {}
    return LabelValue(label, value, label_style=Style(font_weight="bold", font_size="14px", width=lw), value_style=Style(font_size="13px"), value_attrs=va, label_attrs=la)

def build_income_certificate(data: dict[str, Any]) -> Document:
    d = {k: (v if v is not None else "") for k, v in data.items()}
    doc = Document(
        "Annual Income Certificate",
        page_width="900px", page_height="auto", background="#ffffff",
        font_family='"Times New Roman", serif', border="1.4px solid #000000",
        page_style=Style(padding="24px 32px", box_sizing="border-box"),
        extra_css=_EDITABLE_CSS,
    )

    ###### Header
    doc.add(
        FlexRow(
            FlexCol(
                LabelValue("Letter No.:", d.get("letter_no", ""), value_attrs=_ea("letter_no"), label_style=Style(width="100px", font_weight="bold", font_size="13px")),
                LabelValue("Ref No.:", d.get("ref_no", ""), value_attrs=_ea("ref_no"), label_style=Style(width="100px", font_weight="bold", font_size="13px")),
                style=Style(gap="3px", margin_right="18px")
            ),
            FlexCol(
                Heading(d.get("office_name", "Nagarjun Municipality 10 No. Ward Office"), level=1, style=Style(text_align="center", font_size="21px", font_weight="bold", margin_bottom="2px")),
                Text(d.get("municipality", ""), style=Style(text_align="center", font_size="15px", font_weight="bold"), attrs=_ea("municipality")),
                Text(f"Ward No.: {d.get('ward_no','')}", style=Style(text_align="center", font_size="13px"), attrs=_ea("ward_no")),
                Text(f"District: {d.get('district','')} | Province: {d.get('province','')}", style=Style(text_align="center", font_size="13px")),
                style=Style(align_items="center", gap="0px")
            ),
            FlexCol(
                LabelValue("Date:", d.get("date", ""), value_attrs=_ea("date"), label_style=Style(width="75px", font_weight="bold", font_size="13px")),
                PlaceholderBox("Office Seal", shape="circle", size="64px", style=Style(margin_top="10px")),
                style=Style(align_items="flex-end", gap="3px", margin_left="18px")
            ),
            style=Style(justify_content="space-between", align_items="flex-start", width="100%")
        )
    )
    doc.add(Spacer(height="6px"))

    ###### Subject heading
    doc.add(
        Heading(d.get("subject", "Annual Income Certificate"), level=2,
            style=Style(font_size="18px", text_align="center", font_weight="bold", text_decoration="underline", margin_top="3px", margin_bottom="14px"))
    )

    ###### Certificate body (To Whom & paragraph)
    doc.add(Text("To Whom It May Concern", style=Style(font_size="14px", text_align="center", font_weight="bold", margin_bottom="8px")))
    cert_holder = d.get("certificate_holder", "")
    father = d.get("certificate_holder_father", "")
    mother = d.get("certificate_holder_mother", "")
    grandfather = d.get("certificate_holder_grandfather", "")
    holder_addr = d.get("holder_local_address", "")
    para = f"This is to certify that {cert_holder}, son of {father} and {mother}, grandson of {grandfather}, a permanent resident of {holder_addr}, has following sources of income from the following sources. The details have been verified out according to the evidence and records that are provided to office."
    doc.add(Text(para, style=Style(font_size="14px", margin_bottom="14px")))

    ###### Table of sources of income
    # Table header
    table_head = TableRow(*[
        TableCell("S.N.", is_header=True, style=Style(font_weight="bold", border_bottom="1.4px solid #000000")),
        TableCell("Owner's Name", is_header=True, style=Style(font_weight="bold", border_bottom="1.4px solid #000000")),
        TableCell("Relation", is_header=True, style=Style(font_weight="bold", border_bottom="1.4px solid #000000")),
        TableCell("Sources of Income", is_header=True, style=Style(font_weight="bold", border_bottom="1.4px solid #000000")),
        TableCell("Annual Income", is_header=True, style=Style(font_weight="bold", border_bottom="1.4px solid #000000")),
        TableCell("Remarks", is_header=True, style=Style(font_weight="bold", border_bottom="1.4px solid #000000")),
    ])

    # Table rows
    body_rows = []
    for i, row in enumerate(d.get("income_sources", [])):
        rf = f"income_sources.{i}."
        body_rows.append(
            TableRow(
                TableCell(row.get("sn", ""), attrs=_ea(f"{rf}sn")),
                TableCell(row.get("owner_name", ""), attrs=_ea(f"{rf}owner_name")),
                TableCell(row.get("relation", ""), attrs=_ea(f"{rf}relation")),
                TableCell(row.get("source_of_income", ""), attrs=_ea(f"{rf}source_of_income")),
                TableCell(row.get("annual_income", ""), attrs=_ea(f"{rf}annual_income")),
                TableCell(row.get("remarks", ""), attrs=_ea(f"{rf}remarks")),
            )
        )
    table = Table(
        thead_rows=[table_head],
        children=body_rows,
        style=Style(font_size="13px", width="100%", border="1.2px solid #000000", margin_bottom="3px")
    )
    doc.add(table)

    # Table totals under table
    doc.add(
        FlexRow(
            Text("Total Income in NRs:", style=Style(font_weight="bold", font_size="14px")),
            Text(d.get("total_income_nrs", ""), style=Style(font_size="14px", font_weight="bold"), attrs=_ea("total_income_nrs")),
            style=Style(gap="18px", margin_right="16px")
        )
    )
    doc.add(
        FlexRow(
            Text("Total Income in AUD:", style=Style(font_weight="bold", font_size="14px")),
            Text(d.get("total_income_aud", ""), style=Style(font_size="14px", font_weight="bold"), attrs=_ea("total_income_aud")),
            style=Style(gap="18px", margin_right="16px")
        )
    )

    ###### Summary/Words
    doc.add(Text(
        f"Total Annual Income in NRs. {d.get('total_income_nrs','')} (In words: {d.get('total_income_nrs_words','')})",
        style=Style(font_size="13px", margin_top="8px"),
        attrs=_ea("total_income_nrs_words")
    ))
    doc.add(Text(
        f"Today's Buying Rate 1 AUD = NRs. {d.get('todays_aud_rate','')}",
        style=Style(font_size="13px", margin_top="0px"),
        attrs=_ea("todays_aud_rate")
    ))
    doc.add(Text(
        f"Equivalent in AUD = {d.get('total_income_aud','')} (In words: {d.get('total_income_aud_words','')})",
        style=Style(font_size="13px", margin_top="0px"),
        attrs=_ea("total_income_aud_words")
    ))

    doc.add(Spacer(height="38px"))

    ###### Footer: Signature and seal
    doc.add(
        FlexRow(
            Spacer(width="42px"),
            # Signature block
            SignatureBlock(
                name=d.get("ward_chairperson_name", ""),
                name_field="ward_chairperson_name",
                title=d.get("ward_chairperson_title", ""),
                title_field="ward_chairperson_title",
                signature_label="(Signed)",
                align="left",
                style=Style(margin_top="1px", min_width="280px"),
            ),
            Spacer(width="20px"),
            PlaceholderBox("Office Seal", shape="circle", size="82px", style=Style(margin_left="32px")),
            style=Style(justify_content="flex-start", align_items="flex-end", margin_top="0px")
        )
    )

    return doc
