"""
Land Ownership Registration Certificate (Laal Purja) — Layout Definition.

Uses the generalized html_engine components to build a landscape A4
printable document matching the landOwnership.png layout exactly.
"""

from __future__ import annotations

from typing import Any

from html_engine import (
    Document,
    Style,
    Heading,
    Text,
    Image,
    LabelValue,
    FieldGroup,
    MultiFieldRow,
    AbsoluteBox,
    FlexRow,
    FlexCol,
    Div,
    Spacer,
    RawHTML,
    Table,
    TableRow,
    TableCell,
)

_TABLE_HEADER_CELL_STYLE = Style(
    background="#ffffff",
    border="1px solid #000000",
    padding="8px 4px",
    font_size="13px",
    font_weight="bold",
    text_align="center",
)

_TABLE_BODY_CELL_STYLE = Style(
    border="1px solid #000000",
    padding="6px 4px",
    font_size="13px",
    text_align="center",
)


def build_laalpurja(data: dict[str, Any]) -> Document:
    d = {
        "certificate_no": "",
        "district": "",
        "vdc_muc": "",
        "ward_no": "",
        "owner_name": "",
        "owner_address": "",
        "husband_name": "",
        "father_in_law_name": "",
        "citizenship_no": "",
        "photo_src": "owner_photo.png",
        "emblem_src": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Emblem_of_Nepal.svg/1200px-Emblem_of_Nepal.svg.png",
        "issue_date": "",
        "issue_office": "",
        "signatory_name": "",
        "signatory_title": "",
        "plots": [],
    }
    d.update(data)

    doc = Document(
        "Land Ownership Registration Certificate",
        page_width="1200px",
        page_height="auto",
        min_height="840px",
        background="#ffffff",
        border="1px solid #000000",
        font_family="'Times New Roman'",
        page_style=Style(
            padding="30px 40px",
            box_sizing="border-box",
        ),
    )

    # ── 1. Header Section ──────────────────────────────────────────
    header_col = FlexRow(
        # Emblem Placeholder Box (top-left)
        Div(
            FlexCol(
                Text("Coat of Arms", style=Style(font_size="12px", font_weight="bold")),
                Text("of Nepal", style=Style(font_size="12px", font_weight="bold", margin_top="2px")),
                style=Style(align_items="center")
            ),
            style=Style(
                width="130px",
                height="100px",
                border="1px solid #000000",
                display="flex",
                align_items="center",
                justify_content="center",
                text_align="center",
                background="#ffffff"
            )
        ),
        # Center title stack
        FlexCol(
            Heading("Government of Nepal", level=2, style=Style(text_align="center", font_size="20px", font_weight="bold", margin="0")),
            Heading("Ministry of Land Reform and Management", level=3, style=Style(text_align="center", font_size="16px", font_weight="bold", margin="4px 0 0 0")),
            Heading("Department of Land Reform and Management", level=4, style=Style(text_align="center", font_size="14px", font_weight="bold", margin="2px 0 0 0")),
            Heading(f"Land Revenue Office, {d['vdc_muc'] or '[Office Name]'}, {d['district'] or '[District]'}", level=4, style=Style(text_align="center", font_size="14px", font_weight="bold", margin="2px 0 0 0")),
            Text("(Official Stamp)", style=Style(text_align="center", font_size="12px", margin_top="4px", font_style="italic")),
            Spacer(height="15px"),
            Heading("Land Ownership Registration Certificate", level=1, style=Style(text_align="center", font_size="24px", font_weight="bold", margin="0")),
            style=Style(flex="1")
        ),
        # Serial Number (top-right)
        FlexCol(
            Text("Land Ownership Certificate No.:", style=Style(font_size="13px")),
            Text(d["certificate_no"], style=Style(font_size="16px", font_weight="bold", margin_top="2px")),
            style=Style(text_align="left", min_width="180px", align_self="flex-start")
        ),
        style=Style(width="100%", align_items="center", padding_bottom="15px")
    )
    doc.add(header_col)
    doc.add(Spacer(height="15px"))

    # ── 2. Photographic and Details Panels ───────────────────────
    # Left Box: Photograph Box
    photo_box = Div(
        FlexCol(
            Text("Photograph", style=Style(font_size="13px", font_weight="bold")),
            Spacer(height="10px"),
            Text("(Signed)", style=Style(font_size="12px", font_style="italic")),
            style=Style(align_items="center")
        ),
        style=Style(
            width="120px",
            height="160px",
            border="1px solid #000000",
            display="flex",
            align_items="center",
            justify_content="center",
            box_sizing="border-box",
            background="#ffffff"
        )
    )

    # Middle Box: Thumb Impression Box
    thumb_box = Div(
        FlexCol(
            Text("Thumb Impression", style=Style(font_weight="bold", font_size="13px", text_align="center", border_bottom="1px solid #000000", padding_bottom="4px", width="100%")),
            Spacer(height="8px"),
            FlexRow(
                # Right
                Div(
                    Text("Right", style=Style(font_size="12px", font_weight="bold")),
                    Spacer(height="25px"),
                    Text("Impressed", style=Style(font_size="11px", color="#666")),
                    style=Style(flex="1", display="flex", flex_direction="column", align_items="center", border_right="1px dashed #000000", height="100%")
                ),
                # Left
                Div(
                    Text("Left", style=Style(font_size="12px", font_weight="bold")),
                    Spacer(height="25px"),
                    Text("Impressed", style=Style(font_size="11px", color="#666")),
                    style=Style(flex="1", display="flex", flex_direction="column", align_items="center", height="100%")
                ),
                style=Style(flex="1", width="100%")
            ),
            style=Style(height="100%", align_items="center")
        ),
        style=Style(
            width="240px",
            height="160px",
            border="1px solid #000000",
            padding="6px",
            box_sizing="border-box",
            background="#ffffff"
        )
    )

    # Right Box: Details Box
    details_box = Div(
        FlexCol(
            LabelValue("Name of landowner:", d.get("owner_name") or "—", label_width="160px", label_style=Style(font_weight="bold", font_size="13px"), value_style=Style(font_size="13px")),
            LabelValue("Address:", d.get("owner_address") or "—", label_width="160px", label_style=Style(font_weight="bold", font_size="13px"), value_style=Style(font_size="13px")),
            
            # Dynamic spouse/father-in-law mapping or father/grandfather
            LabelValue("Husband's Name:" if d.get("husband_name") else "Father's Name:", 
                       d.get("husband_name") or d.get("father_name") or "—", 
                       label_width="160px", label_style=Style(font_weight="bold", font_size="13px"), value_style=Style(font_size="13px")),
            LabelValue("Father in Law name:" if d.get("father_in_law_name") else "Grandfather's Name:", 
                       d.get("father_in_law_name") or d.get("grandfather_name") or "—", 
                       label_width="160px", label_style=Style(font_weight="bold", font_size="13px"), value_style=Style(font_size="13px")),
            
            MultiFieldRow(
                LabelValue("Citizenship No.:", d.get("citizenship_no") or "—", label_width="160px", label_style=Style(font_weight="bold", font_size="13px"), value_style=Style(font_size="13px")),
                LabelValue("Issued Date:", d.get("issue_date") or "—", label_width="90px", label_style=Style(font_weight="bold", font_size="13px"), value_style=Style(font_size="13px")),
                style=Style(width="100%")
            ),
            LabelValue("Issued Office:", d.get("issue_office") or "—", label_width="160px", label_style=Style(font_weight="bold", font_size="13px"), value_style=Style(font_size="13px")),
            gap="5px",
            style=Style(width="100%")
        ),
        style=Style(
            border="1px solid #000000",
            background="#ffffff",
            padding="10px 15px",
            flex="1",
            height="160px",
            box_sizing="border-box"
        )
    )

    info_section = FlexRow(
        photo_box,
        thumb_box,
        details_box,
        gap="20px",
        style=Style(width="100%", align_items="stretch")
    )
    doc.add(info_section)
    doc.add(Spacer(height="20px"))

    # ── 3. Land Records Table ──────────────────────────────────────
    header_row_1 = TableRow(
        TableCell("Prior Plot No.", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Evd. Symbol", colspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("District/ V.D.C./ M.C.", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Ward No./ Map Sheet No.", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Plot No./ Section No.", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Description (house, Cultivated etc)", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Land Owner Share on Title", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Tenant's Name", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Kind of Land or Class", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Area Sq. Mt.", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Register Page No.", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Remark", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Signature of the certifier", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        style=Style(background="#ffffff")
    )

    header_row_2 = TableRow(
        TableCell("Description of transaction", colspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        style=Style(background="#ffffff")
    )

    body_rows: list[TableRow] = []
    total_metric = 0.0

    for plot in d["plots"]:
        # Subtotals
        try:
            total_metric += float(plot.get("metric_area") or 0.0)
        except ValueError:
            pass

        # Formatting local area unit representation
        r = plot.get("ropani", 0)
        a = plot.get("aana", 0)
        p = plot.get("paisa", 0)
        dm = plot.get("daam", 0)
        area_str = f"{r}-{a}-{p}-{dm}"

        # Evd Symbol columns split
        evd_sym = plot.get("transaction_no", "")
        evd_date = plot.get("transaction_date", "")

        # Row 1 (Top sub-row)
        row_1 = TableRow(
            TableCell(plot.get("plot_id") or "—", rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(evd_sym, style=_TABLE_BODY_CELL_STYLE),
            TableCell(evd_date, style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("vdc_muc") or "—", rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(str(plot.get("ward_no") or ""), style=_TABLE_BODY_CELL_STYLE),
            TableCell(str(plot.get("plot_no") or ""), rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("description_1") or "—", style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("owner_share") or "—", rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("tenant_name") or "—", rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("grade_english") or "—", style=_TABLE_BODY_CELL_STYLE),
            TableCell(area_str, style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("register_page_no") or "—", style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("remarks") or "", rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("signature") or "", rowspan=2, style=_TABLE_BODY_CELL_STYLE),
        )

        # Row 2 (Bottom sub-row)
        row_2 = TableRow(
            TableCell(plot.get("transaction_type") or "—", colspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("sheet_no") or "—", style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("description_2") or "—", style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("class_english") or "—", style=_TABLE_BODY_CELL_STYLE),
            TableCell(str(plot.get("metric_area") or "0"), style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("register_serial_no") or "—", style=_TABLE_BODY_CELL_STYLE),
        )

        body_rows.append(row_1)
        body_rows.append(row_2)

    land_table = Table(
        thead_rows=[header_row_1, header_row_2],
        children=body_rows,
        style=Style(width="100%", margin_top="10px")
    )
    doc.add(land_table)

    # ── 4. Total Area Footer ───────────────────────────────────────
    total_area_row = FlexRow(
        Text(f"Total Area (Sq.m.) {total_metric:.2f}", style=Style(font_weight="bold", font_size="14px")),
        style=Style(justify_content="flex-end", width="100%", padding_right="80px", margin_top="8px")
    )
    doc.add(total_area_row)
    doc.add(Spacer(height="30px"))

    # ── 5. Signatures and Date Footer ──────────────────────────────
    footer_signatures = FlexRow(
        Text("Printing done by: (Signed)", style=Style(font_size="13px", font_weight="bold")),
        Text(f"Print Date: {d.get('issue_date') or '2013/06/10 A.D.'}", style=Style(font_size="13px", font_weight="bold")),
        Text("Checked by: (Signed)", style=Style(font_size="13px", font_weight="bold")),
        style=Style(justify_content="space-between", width="100%", padding="0 40px", box_sizing="border-box")
    )
    doc.add(footer_signatures)

    return doc
