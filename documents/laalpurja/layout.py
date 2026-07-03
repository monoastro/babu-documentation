"""
Land Ownership Registration Certificate (Laal Purja) — Layout Definition.

Uses the generalized html_engine components to dynamically build a printable,
flow-based document representing a Nepali land ownership certificate.
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

# ═══════════════════════════════════════════════════════════════════
#  REUSABLE STYLE TOKENS
# ═══════════════════════════════════════════════════════════════════

_HEADER_TITLE_STYLE = Style(
    color="#8B0000",
    text_align="center",
    font_weight="bold",
    margin="0",
)

_BOX_BORDER_STYLE = Style(
    border="1.5px solid #555",
    border_radius="4px",
    background="#ffffff",
    padding="12px",
)

_THUMB_COL_STYLE = Style(
    flex="1",
    display="flex",
    flex_direction="column",
    justify_content="space-between",
    align_items="center",
    height="100%",
)

_TABLE_HEADER_CELL_STYLE = Style(
    background="#f8f4f4",
    border="1.5px solid #444",
    padding="6px",
    font_size="14px",
    font_weight="bold",
    text_align="center",
)

_TABLE_BODY_CELL_STYLE = Style(
    border="1.5px solid #444",
    padding="6px",
    font_size="14px",
    text_align="center",
)

# ═══════════════════════════════════════════════════════════════════
#  DOCUMENT BUILDER
# ═══════════════════════════════════════════════════════════════════

def build_laalpurja(data: dict[str, Any]) -> Document:
    """
    Build a Land Ownership Registration Certificate (Laal Purja) document.

    Parameters:
        data: Dictionary with the following keys:
            - ``certificate_no``: Registration/Serial No (e.g. "LP-5912A")
            - ``district``: District name (e.g. "Lalitpur")
            - ``vdc_muc``: Municipality/VDC name (e.g. "Godawari")
            - ``ward_no``: Ward number (e.g. "5")
            - ``owner_name``: Name of the land owner
            - ``owner_address``: Address of the land owner
            - ``grandfather_name``: Owner's grandfather's name
            - ``father_name``: Owner's father's name
            - ``spouse_name``: Owner's spouse's name
            - ``citizenship_no``: Owner's citizenship number
            - ``photo_src``: Path or URL to owner's photo
            - ``emblem_src``: Path or URL to the government emblem
            - ``issue_date``: Certificate issuing date (e.g. "2080-04-12")
            - ``issue_office``: Issuing office (e.g. "Lalitpur Land Revenue Office")
            - ``signatory_name``: Name of the issuing officer
            - ``signatory_title``: Title of the officer (e.g. "Land Revenue Officer")
            - ``plots``: List of dicts representing land plots, each containing:
                - ``plot_id``: Serial number in table
                - ``district``: Plot district
                - ``vdc_muc``: Plot municipality
                - ``ward_no``: Plot ward
                - ``sheet_no``: Map sheet number
                - ``plot_no``: Plot number
                - ``ropani``, ``aana``, ``paisa``, ``daam``: Local area units
                - ``metric_area``: Area in square meters (float/str)
                - ``class_nepali``: Land classification in Nepali (e.g. "Khet")
                - ``class_english``: Land classification in English (e.g. "Wet Land")
                - ``grade_nepali``: Land grade in Nepali (e.g. "Abal")
                - ``grade_english``: Land grade in English (e.g. "Grade A")
                - ``remarks``: Remarks or conditions

    Returns:
        A :class:`Document` representing the certificate.
    """
    # ── Defaults ──────────────────────────────────────────────────
    d = {
        "certificate_no": "LP-000000",
        "district": "",
        "vdc_muc": "",
        "ward_no": "",
        "owner_name": "",
        "owner_address": "",
        "grandfather_name": "",
        "father_name": "",
        "spouse_name": "N/A",
        "citizenship_no": "",
        "photo_src": "owner_photo.png",
        "emblem_src": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Emblem_of_Nepal.svg/1200px-Emblem_of_Nepal.svg.png",
        "issue_date": "",
        "issue_office": "Land Revenue Office",
        "signatory_name": "",
        "signatory_title": "Land Revenue Officer",
        "plots": [],
    }
    d.update(data)

    # ── Document Setup ────────────────────────────────────────────
    # Laal Purja is a content-driven document that wraps content flow-wise
    doc = Document(
        "Land Ownership Registration Certificate",
        page_width="1200px",
        page_height="auto",
        min_height="840px",
        background="#faf6f0",  # Slight parchment tint
        border="3px double #8B0000",
        page_style=Style(
            padding="40px",
            box_sizing="border-box",
        ),
        extra_css="""
            @media print {
                .page {
                    border: 3px double #8B0000 !important;
                    background: #faf6f0 !important;
                }
            }
        """
    )

    # ── 1. Header Section ──────────────────────────────────────────
    # Left: Emblem, Center: Text, Right: Serial
    header_col = FlexRow(
        # Emblem
        Div(
            Image(d["emblem_src"], style=Style(width="100px", height="100px", object_fit="contain")),
            style=Style(width="150px")
        ),
        # Title Stack
        FlexCol(
            Heading("Government of Nepal", level=2, style=_HEADER_TITLE_STYLE.clone(font_size="22px")),
            Heading("Ministry of Land Reform and Management", level=3, style=_HEADER_TITLE_STYLE.clone(font_size="18px", margin_top="4px")),
            Heading("Department of Land Reform and Management", level=4, style=_HEADER_TITLE_STYLE.clone(font_size="16px", margin_top="2px")),
            Heading(f"Land Revenue Office, {d['district'] or '[District]'}", level=4, style=_HEADER_TITLE_STYLE.clone(font_size="16px", margin_top="2px")),
            Spacer(height="12px"),
            Heading("Land Ownership Registration Certificate", level=1, style=_HEADER_TITLE_STYLE.clone(font_size="26px", color="#A30000")),
            style=Style(flex="1")
        ),
        # Certificate Number
        Div(
            FlexCol(
                Text("Certificate No:", style=Style(font_weight="bold", font_size="14px")),
                Text(d["certificate_no"], style=Style(font_size="18px", font_weight="bold", color="#A30000", margin_top="4px")),
                style=Style(
                    border="1px solid #8B0000",
                    padding="10px",
                    border_radius="4px",
                    text_align="center",
                    min_width="140px",
                )
            ),
            style=Style(width="150px", display="flex", justify_content="flex-end")
        ),
        style=Style(width="100%", align_items="center", border_bottom="2px solid #8B0000", padding_bottom="18px")
    )
    doc.add(header_col)
    doc.add(Spacer(height="20px"))

    # ── 2. Three Bordered Information Boxes ────────────────────────
    # Box 1: Photo
    photo_box = Div(
        FlexCol(
            # Photo frame
            Div(
                Image(d["photo_src"], style=Style(width="100%", height="100%", object_fit="cover")),
                style=Style(width="120px", height="140px", border="1px solid #777", background="#e8e8e8", overflow="hidden")
            ),
            Spacer(height="8px"),
            Text("(Signature of Owner)", style=Style(font_size="12px", font_style="italic")),
            style=Style(align_items="center")
        ),
        style=_BOX_BORDER_STYLE.clone(width="160px", height="190px", display="flex", align_items="center", justify_content="center")
    )

    # Box 2: Thumb Impression
    thumb_box = Div(
        FlexCol(
            Text("Thumb Impression", style=Style(font_weight="bold", font_size="13px", text_align="center", border_bottom="1px solid #777", padding_bottom="4px", width="100%")),
            Spacer(height="8px"),
            FlexRow(
                # Left
                Div(
                    Text("Left", style=Style(font_size="11px", color="#666")),
                    style=_THUMB_COL_STYLE.clone(border_right="1px dashed #999")
                ),
                # Right
                Div(
                    Text("Right", style=Style(font_size="11px", color="#666")),
                    style=_THUMB_COL_STYLE
                ),
                style=Style(flex="1", width="100%")
            ),
            style=Style(height="100%", align_items="center")
        ),
        style=_BOX_BORDER_STYLE.clone(width="180px", height="190px")
    )

    # Box 3: Details Box
    details_box = Div(
        FlexCol(
            LabelValue("Owner's Full Name:", d["owner_name"], label_style=Style(font_weight="bold", width="180px"), value_style=Style(color="#222")),
            LabelValue("Owner's Address:", d["owner_address"], label_style=Style(font_weight="bold", width="180px")),
            LabelValue("Grandfather's Name:", d["grandfather_name"], label_style=Style(font_weight="bold", width="180px")),
            LabelValue("Father's Name:", d["father_name"], label_style=Style(font_weight="bold", width="180px")),
            LabelValue("Spouse's Name:", d["spouse_name"], label_style=Style(font_weight="bold", width="180px")),
            LabelValue("Citizenship/ID No:", d["citizenship_no"], label_style=Style(font_weight="bold", width="180px")),
            LabelValue("Issue Date / Office:", f"{d['issue_date']} / {d['issue_office']}", label_style=Style(font_weight="bold", width="180px")),
            gap="8px",
            style=Style(width="100%")
        ),
        style=_BOX_BORDER_STYLE.clone(flex="1", height="190px", box_sizing="border-box")
    )

    info_section = FlexRow(
        photo_box,
        thumb_box,
        details_box,
        gap="20px",
        style=Style(width="100%", align_items="stretch")
    )
    doc.add(info_section)
    doc.add(Spacer(height="25px"))

    # ── 3. Land Records Table ──────────────────────────────────────
    # Table headers setup (2 levels)
    header_row_1 = TableRow(
        TableCell("S.N.", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Location Details", colspan=3, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Map Details", colspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Land Area (Local Units)", colspan=4, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Land Classification", colspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Remarks", rowspan=2, is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        style=Style(background="#f8f4f4")
    )

    header_row_2 = TableRow(
        TableCell("District", is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("VDC / Mun.", is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Ward", is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Sheet No", is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Plot No", is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Ropani", is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Aana", is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Paisa", is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Daam", is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Class/Type", is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        TableCell("Grade", is_header=True, style=_TABLE_HEADER_CELL_STYLE),
        style=Style(background="#f8f4f4")
    )

    # Build body rows dynamically
    body_rows: list[TableRow] = []
    total_daams = 0
    total_metric = 0.0

    for idx, plot in enumerate(d["plots"], 1):
        # Calculate local area in total daams
        r = int(plot.get("ropani") or 0)
        a = int(plot.get("aana") or 0)
        p = int(plot.get("paisa") or 0)
        dm = int(plot.get("daam") or 0)
        total_daams += r * 16 * 4 * 4 + a * 4 * 4 + p * 4 + dm

        # Calculate metric area sum
        try:
            total_metric += float(plot.get("metric_area") or 0.0)
        except ValueError:
            pass

        sn_str = str(plot.get("plot_id") or idx)

        # Row A: main row (local units)
        row_a = TableRow(
            TableCell(sn_str, rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("district", ""), rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("vdc_muc", ""), rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(str(plot.get("ward_no", "")), rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(str(plot.get("sheet_no", "")), rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(str(plot.get("plot_no", "")), rowspan=2, style=_TABLE_BODY_CELL_STYLE),
            TableCell(str(r), style=_TABLE_BODY_CELL_STYLE),
            TableCell(str(a), style=_TABLE_BODY_CELL_STYLE),
            TableCell(str(p), style=_TABLE_BODY_CELL_STYLE),
            TableCell(str(dm), style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("class_nepali", ""), style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("grade_nepali", ""), style=_TABLE_BODY_CELL_STYLE),
            TableCell(plot.get("remarks", ""), rowspan=2, style=_TABLE_BODY_CELL_STYLE),
        )

        # Row B: sub-row (metric area and English classification)
        row_b = TableRow(
            TableCell(f"Metric: {plot.get('metric_area', '0')} m²", colspan=4, style=_TABLE_BODY_CELL_STYLE.clone(text_align="left", font_style="italic", color="#555")),
            TableCell(plot.get("class_english", ""), style=_TABLE_BODY_CELL_STYLE.clone(color="#555")),
            TableCell(plot.get("grade_english", ""), style=_TABLE_BODY_CELL_STYLE.clone(color="#555")),
        )

        body_rows.append(row_a)
        body_rows.append(row_b)

    # Convert total daams back to ropani/aana/paisa/daam
    daam_rem = total_daams % 4
    paisa_total = total_daams // 4
    paisa_rem = paisa_total % 4
    aana_total = paisa_total // 4
    aana_rem = aana_total % 16
    ropani_total = aana_total // 16

    # Create footer totals row
    tfoot_rows = [
        TableRow(
            TableCell("Total Area:", colspan=6, style=_TABLE_HEADER_CELL_STYLE.clone(text_align="right")),
            TableCell(str(ropani_total), style=_TABLE_HEADER_CELL_STYLE),
            TableCell(str(aana_rem), style=_TABLE_HEADER_CELL_STYLE),
            TableCell(str(paisa_rem), style=_TABLE_HEADER_CELL_STYLE),
            TableCell(str(daam_rem), style=_TABLE_HEADER_CELL_STYLE),
            TableCell(f"Total Metric: {total_metric:.2f} m²", colspan=3, style=_TABLE_HEADER_CELL_STYLE.clone(text_align="center")),
        )
    ]

    land_table = Table(
        thead_rows=[header_row_1, header_row_2],
        tfoot_rows=tfoot_rows,
        children=body_rows,
        style=Style(width="100%", margin_top="10px")
    )
    doc.add(land_table)
    doc.add(Spacer(height="35px"))

    # ── 4. Signatures / Certificate Issuing Info ───────────────────
    # Left: Office Seal / Stamp space, Right: Authorized Signatory
    footer_section = FlexRow(
        # Office Stamp
        Div(
            FlexCol(
                Text("Land Revenue Office", style=Style(font_size="12px", font_weight="bold", color="#666")),
                Text("Official Seal", style=Style(font_size="11px", color="#999")),
                style=Style(
                    width="120px",
                    height="120px",
                    border="1.5px dashed #8B0000",
                    border_radius="50%",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    text_align="center",
                )
            ),
            style=Style(flex="1", display="flex", justify_content="flex-start", padding_left="30px")
        ),
        # Signatory block
        Div(
            FlexCol(
                Spacer(height="40px"),  # Space for physical/image signature
                Text(d["signatory_name"], style=Style(font_weight="bold", font_size="16px", border_top="1px solid #444", padding_top="4px", width="220px", text_align="center")),
                Text(d["signatory_title"], style=Style(font_size="14px", color="#444", text_align="center")),
                Text(f"Date: {d['issue_date']}", style=Style(font_size="12px", color="#666", text_align="center", margin_top="4px")),
                style=Style(align_items="center")
            ),
            style=Style(flex="1", display="flex", justify_content="flex-end", padding_right="30px")
        ),
        style=Style(width="100%", align_items="flex-end")
    )
    doc.add(footer_section)

    return doc
