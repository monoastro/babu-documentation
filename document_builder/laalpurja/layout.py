"""
Land Ownership Registration Certificate (Laal Purja) — Layout Definition.

Pixel-faithful recreation of the official document:
- Black-and-white, A4 landscape, Times New Roman font
- Header: Coat of Arms box (top-left), Gov titles (centre), Cert No. (top-right)
- Bold underlined title beneath the header
- Info section: Photo box | Thumb Impression box | Owner details panel (with visible gaps)
- 14-column dual-row-per-plot table:
    "Evd. Symbol" colspan=3 → sub-headers: "Prior Plot No." (1 col) +
    "Description of transaction" colspan=2 (evd_no col + evd_date/transaction col)
- Total area row, doc-id label, footer print/check line
"""

from __future__ import annotations

from typing import Any

from html_engine import (
    Document,
    Style,
    Heading,
    Text,
    LabelValue,
    FieldGroup,
    MultiFieldRow,
    FlexRow,
    FlexCol,
    Div,
    Spacer,
    Table,
    TableRow,
    TableCell,
)

# ─── Shared style tokens ───────────────────────────────────────────────────

_FS   = "13px"
_FONT = '"Times New Roman", Times, serif'
_BORDER = "1px solid #000000"

# Table cell styles — pre-line so \n inside data renders as a line break
_TH = Style(
    border=_BORDER,
    padding="4px 3px",
    font_size="12px",
    font_weight="bold",
    text_align="center",
    vertical_align="middle",
    background="#ffffff",
    white_space="pre-line",
)

_TD = Style(
    border=_BORDER,
    padding="4px 3px",
    font_size="12px",
    text_align="center",
    vertical_align="middle",
    white_space="pre-line",
)

# Label/value shared styles for the details panel
_LBL = Style(font_weight="bold", font_size=_FS, flex_shrink="0")
_VAL = Style(font_size=_FS, flex="1")


# ─── Helpers ───────────────────────────────────────────────────────────────

def _lv(label: str, value: str, lw: str = "160px") -> LabelValue:
    return LabelValue(label, value, label_style=_LBL.clone(width=lw), value_style=_VAL)


def _th(*args, **kwargs) -> TableCell:
    s = _TH.merge(kwargs.pop("style", None))
    return TableCell(*args, is_header=True, style=s, **kwargs)


def _td(*args, **kwargs) -> TableCell:
    s = _TD.merge(kwargs.pop("style", None))
    return TableCell(*args, style=s, **kwargs)


# ─── Main builder ──────────────────────────────────────────────────────────

def build_laalpurja(data: dict[str, Any]) -> Document:
    """
    Build a Land Ownership Registration Certificate (Laal Purja) document.

    ``data`` keys
    -------------
    certificate_no     e.g. "4915149"
    office_vdc         Office VDC/Municipality, e.g. "Lagankhel"
    office_district    Office district, e.g. "Lalitpur"
    owner_name         Full name (may be blank)
    owner_district     Address district
    owner_vdc          Address M.C./V.D.C.
    owner_ward         Address ward number
    husband_name       Husband's name
    father_in_law      Father-in-law's name
    citizenship_no     Citizenship number
    issue_date         e.g. "2007/02/16 A.D."
    issue_office       Issuing office full name
    doc_id             Bottom-left doc identifier, e.g. "103mm002"
    print_date         Footer print date, e.g. "2013/06/10"
    plots              List of plot dicts (see below)

    Each plot dict
    --------------
    plot_no            Prior Plot No. (rowspan=2 in left-most Evd col)
    evd_no             Evidence number (top sub-row of "Description of transaction")
    evd_date           Evidence date   (top sub-row of "Description of transaction")
    transaction_type   e.g. "Resignation" (bottom sub-row, colspan=2 under "Description of transaction")
    vdc                District/V.D.C./M.C. (rowspan=2)
    ward_top           Ward/map sheet — top sub-row
    ward_bottom        Ward/map sheet — bottom sub-row
    plot_section       Plot No./Section No. (rowspan=2)
    desc_top           Description top line, e.g. "Residential land"
    desc_bottom        Description bottom line, e.g. "Private land"
    owner_share        Land owner share on title (rowspan=2)
    tenant             Tenant's name (rowspan=2)
    kind_top           Kind of land / class (rowspan=2)
    area_local         Local area string, e.g. "0-2-2-2" (top sub-row)
    area_sqm           Metric area in sq.m. (bottom sub-row)
    register_page      Register page no (top sub-row)
    register_serial    Register serial no (bottom sub-row)
    remark             Remark text (rowspan=2, usually blank)
    signature          Certifier signature (rowspan=2, e.g. "(Signed)")
    """

    d: dict[str, Any] = {
        "certificate_no": "",
        "office_vdc": "",
        "office_district": "",
        "owner_name": "",
        "owner_district": "",
        "owner_vdc": "",
        "owner_ward": "",
        "husband_name": "",
        "father_in_law": "",
        "citizenship_no": "",
        "issue_date": "",
        "issue_office": "",
        "doc_id": "",
        "print_date": "",
        "plots": [],
    }
    d.update(data)

    # ── Document ──────────────────────────────────────────────────────────
    doc = Document(
        "Land Ownership Registration Certificate",
        page_width="1200px",
        page_height="auto",
        background="#ffffff",
        border=_BORDER,
        font_family=_FONT,
        page_style=Style(padding="30px 40px", box_sizing="border-box"),
    )

    # ══════════════════════════════════════════════════════════════════════
    # 1. HEADER
    # ══════════════════════════════════════════════════════════════════════

    coat_box = Div(
        FlexCol(
            Text("Coat of Arms", style=Style(font_size="12px")),
            Text("of Nepal",     style=Style(font_size="12px")),
            style=Style(align_items="center"),
        ),
        style=Style(
            width="110px", height="90px",
            border=_BORDER,
            display="flex", align_items="center", justify_content="center",
            text_align="center",
        ),
    )

    gov_titles = FlexCol(
        Heading("Government of Nepal",
                level=1, style=Style(margin="0", font_size="22px", font_weight="bold", text_align="center")),
        Heading("Ministry of Land Reform and Management",
                level=2, style=Style(margin="2px 0 0 0", font_size="15px", font_weight="bold", text_align="center")),
        Heading("Department of Land Reform and Management",
                level=3, style=Style(margin="2px 0 0 0", font_size="15px", font_weight="bold", text_align="center")),
        Heading(f"Land Revenue Office,{d['office_vdc']},{d['office_district']}",
                level=4, style=Style(margin="2px 0 0 0", font_size="14px", font_weight="bold", text_align="center")),
        Text("(Official Stamp)", style=Style(font_size="12px", text_align="center", margin_top="2px")),
        style=Style(flex="1"),
    )

    cert_no_block = FlexCol(
        Text("Land Ownership Certificate No.:", style=Style(font_size="12px")),
        Text(d["certificate_no"], style=Style(font_size="13px", font_weight="bold", margin_top="2px")),
        style=Style(text_align="left", min_width="160px", align_self="flex-start"),
    )

    doc.add(FlexRow(
        coat_box,
        gov_titles,
        cert_no_block,
        style=Style(width="100%", align_items="center"),
    ))
    doc.add(Spacer(height="16px"))

    doc.add(Heading(
        "Land Ownership Registration Certificate",
        level=1,
        style=Style(
            font_size="24px", font_weight="bold", text_align="center",
            text_decoration="underline", margin="0",
        ),
    ))
    doc.add(Spacer(height="18px"))

    # ══════════════════════════════════════════════════════════════════════
    # 2. INFO SECTION  — Photo | Thumb | Details
    #    Boxes have visible 1px borders and a gap between them.
    # ══════════════════════════════════════════════════════════════════════

    _box = Style(border=_BORDER, background="#ffffff", box_sizing="border-box")

    # ── Photo box: text top-left, (Signed) bottom-left ─────────────────
    photo_box = Div(
        FlexCol(
            Text("Photograph", style=Style(font_size=_FS, font_weight="bold")),
            Div(style=Style(flex="1")),
            Text("(Signed)", style=Style(font_size="12px")),
            style=Style(
                height="100%",
                align_items="flex-start",
                justify_content="space-between",
            ),
        ),
        style=_box.clone(
            width="110px",
            height="155px",
            padding="8px 10px",
            display="flex",
            flex_direction="column",
        ),
    )

    # ── Thumb Impression: header | Right col / Left col ─────────────────
    _thumb_col = Style(
        flex="1", display="flex", flex_direction="column",
        align_items="center", padding_top="6px",
    )
    thumb_box = Div(
        FlexCol(
            Text("Thumb Impression",
                 style=Style(font_size=_FS, font_weight="bold", text_align="center",
                             border_bottom=_BORDER, padding_bottom="4px", width="100%")),
            FlexRow(
                Div(
                    FlexCol(
                        Text("Right",     style=Style(font_size=_FS, font_weight="bold")),
                        Text("Impressed", style=Style(font_size="11px", margin_top="4px")),
                        style=Style(align_items="center"),
                    ),
                    style=_thumb_col.clone(border_right=_BORDER),
                ),
                Div(
                    FlexCol(
                        Text("Left",      style=Style(font_size=_FS, font_weight="bold")),
                        Text("Impressed", style=Style(font_size="11px", margin_top="4px")),
                        style=Style(align_items="center"),
                    ),
                    style=_thumb_col,
                ),
                style=Style(flex="1", width="100%"),
            ),
            style=Style(height="100%", align_items="stretch"),
        ),
        style=_box.clone(
            width="230px",
            height="155px",
            padding="6px",
            display="flex",
            flex_direction="column",
        ),
    )

    # ── Details panel ────────────────────────────────────────────────────
    # Address: split across one line — district left, VDC/ward right
    addr_row = MultiFieldRow(
        LabelValue(
            "Address:",
            f"District: {d['owner_district']},",
            label_style=_LBL.clone(width="130px"),
            value_style=_VAL,
        ),
        LabelValue(
            f"M.C. /V.D.C.: {d['owner_vdc']}, Ward No. {d['owner_ward']}",
            "",
            label_style=Style(font_size=_FS, flex_shrink="0"),
            value_style=_VAL,
        ),
    )

    # Citizenship No. + Issued Date on same line with clear separation
    cit_date_row = MultiFieldRow(
        LabelValue("Citizenship No.:", d["citizenship_no"],
                   label_style=_LBL.clone(width="130px"), value_style=Style(font_size=_FS, min_width="100px")),
        LabelValue("Issued Date:", f"  {d['issue_date']}",
                   label_style=_LBL.clone(width="100px"), value_style=_VAL),
    )

    details_panel = Div(
        FieldGroup(
            _lv("Name of landowner:", d["owner_name"], lw="160px"),
            addr_row,
            _lv("Husband's Name:", d["husband_name"], lw="160px"),
            _lv("Father in Law name:", d["father_in_law"], lw="160px"),
            cit_date_row,
            _lv("Issued Office:", d["issue_office"], lw="130px"),
            spacing="5px",
            style=Style(font_size=_FS),
        ),
        style=_box.clone(
            flex="1",
            height="155px",
            padding="8px 14px",
            display="flex",
            flex_direction="column",
            justify_content="center",
        ),
    )

    # Gap between boxes via margin-right on photo and thumb
    photo_wrap = Div(photo_box, style=Style(margin_right="10px"))
    thumb_wrap = Div(thumb_box, style=Style(margin_right="10px"))

    doc.add(FlexRow(
        photo_wrap,
        thumb_wrap,
        details_panel,
        style=Style(width="100%", align_items="stretch"),
    ))
    doc.add(Spacer(height="18px"))

    # ══════════════════════════════════════════════════════════════════════
    # 3. LAND RECORDS TABLE
    #
    # Column layout (14 physical columns):
    #
    #  ┌──────────────────────────┬───────────────┬──────────────────────────────────────────────────────────────────────────────────────┐
    #  │      Evd. Symbol (cs=3)  │               │                                                                                      │
    #  ├────────────┬─────────────┤               │   ...all others with rowspan=2...                                                    │
    #  │ Prior      │ Descr. of   │ District/     │                                                                                      │
    #  │ Plot No.   │ transaction │ V.D.C./M.C.   │                                                                                      │
    #  │            │  (cs=2)     │               │                                                                                      │
    #  └────────────┴─────────────┴───────────────┴──────────────────────────────────────────────────────────────────────────────────────┘
    #
    # Top data row:  plot_no(rs=2) | evd_no | evd_date | vdc(rs=2) | ward_top | plot_sec(rs=2) | desc_top | share(rs=2) | tenant(rs=2) | kind(rs=2) | area_local | reg_page | remark(rs=2) | sig(rs=2)
    # Bottom row:    [skip]        | Resignation (cs=2)  | [skip]   | ward_bot | [skip]         | desc_bot | [skip]      | [skip]       | [skip]     | area_sqm   | reg_ser  | [skip]       | [skip]
    # ══════════════════════════════════════════════════════════════════════

    thead = [
        TableRow(
            _th("Evd. Symbol",                        colspan=3),
            _th("District/\nV.D.C./M.C.",             rowspan=2),
            _th("Ward No./\nMap Sheet No.",            rowspan=2),
            _th("Plot No./\nSect ion No.",             rowspan=2),
            _th("Description\n(house,\nCultivated etc)", rowspan=2),
            _th("Land\nOwner\nShare on\nTitle",        rowspan=2),
            _th("Tenant's\nName",                      rowspan=2),
            _th("Kind of\nLand or\nClass",             rowspan=2),
            _th("Area\nSq. Mt.",                       rowspan=2),
            _th("Register\nPage No.",                  rowspan=2),
            _th("Remark",                              rowspan=2),
            _th("Signature\nof the\ncertifier",        rowspan=2),
        ),
        TableRow(
            _th("Prior\nPlot\nNo."),
            _th("Description of transaction",          colspan=2),
        ),
    ]

    body_rows: list[TableRow] = []
    total_sqm = 0.0

    for plot in d["plots"]:
        try:
            total_sqm += float(plot.get("area_sqm") or 0)
        except ValueError:
            pass

        # Top sub-row
        body_rows.append(TableRow(
            _td(str(plot.get("plot_no",           "")), rowspan=2),
            _td(str(plot.get("evd_no",            ""))),
            _td(str(plot.get("evd_date",          ""))),
            _td(str(plot.get("vdc",               "")), rowspan=2),
            _td(str(plot.get("ward_top",          ""))),
            _td(str(plot.get("plot_section",      "")), rowspan=2),
            _td(str(plot.get("desc_top",          ""))),
            _td(str(plot.get("owner_share",       "")), rowspan=2),
            _td(str(plot.get("tenant",            "")), rowspan=2),
            _td(str(plot.get("kind_top",          "")), rowspan=2),
            _td(str(plot.get("area_local",        ""))),
            _td(str(plot.get("register_page",     ""))),
            _td(str(plot.get("remark",            "")), rowspan=2),
            _td(str(plot.get("signature",         "")), rowspan=2),
        ))

        # Bottom sub-row — transaction_type spans the 2 "Description of transaction" cols
        body_rows.append(TableRow(
            _td(str(plot.get("transaction_type",  "")), colspan=2),
            _td(str(plot.get("ward_bottom",       ""))),
            _td(str(plot.get("desc_bottom",       ""))),
            _td(str(plot.get("area_sqm",          ""))),
            _td(str(plot.get("register_serial",   ""))),
        ))

    doc.add(Table(thead_rows=thead, children=body_rows))

    # ── Total area (right-aligned) ──────────────────────────────────────
    doc.add(FlexRow(
        Text(f"Total Area (Sq.m.)  {total_sqm:.2f}",
             style=Style(font_size=_FS, font_weight="bold")),
        style=Style(justify_content="flex-end", width="100%", margin_top="6px"),
    ))

    # ── Document ID label ───────────────────────────────────────────────
    if d["doc_id"]:
        doc.add(Spacer(height="4px"))
        doc.add(Text(d["doc_id"], style=Style(font_size="10px", color="#555")))

    doc.add(Spacer(height="10px"))

    # ══════════════════════════════════════════════════════════════════════
    # 4. FOOTER
    # ══════════════════════════════════════════════════════════════════════

    def _footer_item(bold_label: str, value: str) -> FlexRow:
        return FlexRow(
            Text(bold_label, style=Style(font_size=_FS, font_weight="bold")),
            Text(value,      style=Style(font_size=_FS)),
            gap="2px",
        )

    doc.add(FlexRow(
        _footer_item("Printing done by:", " (Signed)."),
        _footer_item("Print Date:", f" {d['print_date']} A.D."),
        _footer_item("Checked by:", " (Signed)"),
        style=Style(justify_content="space-between", width="100%"),
    ))

    return doc
