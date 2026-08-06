"""
Land Ownership Registration Certificate (Laal Purja) — Layout Definition, patched for top-right double identifier and checked-by date in footer.

- Renders both the main certificate number and the upper supplementary/preprinted identifier in the header (top-right).
- Outputs checked-by date (if present) in the lower-right footer below Checked by signature, field-anchored.
- Table certifier signature field marked editable, expects either text or a placeholder for scanned/handwritten marker per schema.
"""

from __future__ import annotations
from typing import Any
from html_engine import (
    Document, Style, Heading, Text, LabelValue, FieldGroup, MultiFieldRow, FlexRow, FlexCol, Div, Spacer, Table, TableRow, TableCell
)

_FS   = "13px"
_FONT = '"Times New Roman", Times, serif'
_BORDER = "1px solid #000000"
_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

_TH = Style(
    border=_BORDER, padding="4px 3px", font_size="12px", font_weight="bold",
    text_align="center", vertical_align="middle", background="#ffffff", white_space="pre-line",
)
_TD = Style(
    border=_BORDER, padding="4px 3px", font_size="12px", text_align="center",
    vertical_align="middle", white_space="pre-line",
)
_LBL = Style(font_weight="bold", font_size=_FS, flex_shrink="0")
_VAL = Style(font_size=_FS, flex="1")

_DEVA = str.maketrans("०१२३४५६७८९", "0123456789")
def _to_float(s) -> float:
    try: return float(str(s or "").translate(_DEVA))
    except ValueError: return 0.0

def _ea(field_name: str):
    return {"contenteditable": "true", "data-field": field_name}

def _lv(label, value, lw="160px", field_name=""):
    va = _ea(field_name) if field_name else {}
    la = _ea(f"label.{field_name}") if field_name else {}
    return LabelValue(label, value, label_style=_LBL.clone(width=lw), value_style=_VAL, value_attrs=va, label_attrs=la)

def _th(*args, **kwargs):
    s = _TH.merge(kwargs.pop("style", None))
    return TableCell(*args, is_header=True, style=s, **kwargs)

def _td(*args, field_name: str = "", **kwargs):
    s = _TD.merge(kwargs.pop("style", None))
    a = _ea(field_name) if field_name else {}
    return TableCell(*args, style=s, attrs=a, **kwargs)

def build_laalpurja(data: dict[str, Any]) -> Document:
    d = {k: (v if v is not None else "") for k, v in data.items()}
    doc = Document(
        "Land Ownership Registration Certificate",
        page_width="1200px", page_height="auto", background="#ffffff", border=_BORDER,
        font_family=_FONT, page_style=Style(padding="30px 40px", box_sizing="border-box"), extra_css=_EDITABLE_CSS,
    )

    # Header: Double identifier (top-right stacked)
    cert_no_block = FlexCol(
        Text("Land Ownership Certificate No.:", style=Style(font_size="12px")),
        Text(d.get("certificate_no", ""), style=Style(font_size="13px", font_weight="bold", margin_top="2px"), attrs=_ea("certificate_no")),
        Spacer(height="5px"),
        Text("Preprinted Identifier:", style=Style(font_size="11px", color="#000000")),
        Text(d.get("supplementary_id", ""), style=Style(font_size="12px", font_weight="bold", margin_top="1px", color="#000000"), attrs=_ea("supplementary_id")),
        style=Style(text_align="left", min_width="170px", align_self="flex-start")
    )
    coat_box = Div(
        FlexCol(
            Text("Coat of Arms", style=Style(font_size="12px")),
            Text("of Nepal",     style=Style(font_size="12px")),
            style=Style(align_items="center"),
        ),
        style=Style(width="110px", height="90px", border=_BORDER, display="flex", align_items="center", justify_content="center", text_align="center"),
    )
    gov_titles = FlexCol(
        Heading("Government of Nepal", level=1, style=Style(margin="0", font_size="22px", font_weight="bold", text_align="center")),
        Heading("Ministry of Land Reform and Management", level=2, style=Style(margin="2px 0 0 0", font_size="15px", font_weight="bold", text_align="center")),
        Heading("Department of Land Reform and Management", level=3, style=Style(margin="2px 0 0 0", font_size="15px", font_weight="bold", text_align="center")),
        Heading(f"Land Revenue Office,{d.get('office_vdc','')},{d.get('office_district','')}", level=4, style=Style(margin="2px 0 0 0", font_size="14px", font_weight="bold", text_align="center")),
        Text("(Official Stamp)", style=Style(font_size="12px", text_align="center", margin_top="2px")),
        style=Style(flex="1"),
    )
    doc.add(FlexRow(coat_box, gov_titles, cert_no_block, style=Style(width="100%", align_items="center")))
    doc.add(Spacer(height="16px"))

    doc.add(Heading(
        "Land Ownership Registration Certificate", level=1,
        style=Style(font_size="24px", font_weight="bold", text_align="center", text_decoration="underline", margin="0"),
    ))
    doc.add(Spacer(height="18px"))
    _box = Style(border=_BORDER, background="#ffffff", box_sizing="border-box")
    photo_box = Div(
        FlexCol(
            Text("Photograph", style=Style(font_size=_FS, font_weight="bold")),
            Div(style=Style(flex="1")),
            Text("(Signed)", style=Style(font_size="12px")),
            style=Style(height="100%", align_items="flex-start", justify_content="space-between"),),
        style=_box.clone(width="110px",height="155px",padding="8px 10px",display="flex",flex_direction="column"),)
    _thumb_col = Style(flex="1", display="flex", flex_direction="column", align_items="center", padding_top="6px",)
    thumb_box = Div(
        FlexCol(
            Text("Thumb Impression",style=Style(font_size=_FS, font_weight="bold", text_align="center",border_bottom=_BORDER, padding_bottom="4px", width="100%")),
            FlexRow(
                Div(FlexCol(Text("Right", style=Style(font_size=_FS, font_weight="bold")),Text("Impressed", style=Style(font_size="11px", margin_top="4px")),style=Style(align_items="center"),),style=_thumb_col.clone(border_right=_BORDER),),
                Div(FlexCol(Text("Left", style=Style(font_size=_FS, font_weight="bold")),Text("Impressed", style=Style(font_size="11px", margin_top="4px")),style=Style(align_items="center"),),style=_thumb_col,),style=Style(flex="1", width="100%")),style=Style(height="100%", align_items="stretch"),),style=_box.clone(width="230px",height="155px",padding="6px",display="flex",flex_direction="column"),)
    addr_row = MultiFieldRow(
        LabelValue("Address:", f"District: {d.get('owner_district','')},", label_style=_LBL.clone(width="130px"), value_style=_VAL),
        LabelValue(f"M.C. /V.D.C.: {d.get('owner_vdc','')}, Ward No. {d.get('owner_ward','')}", "", label_style=Style(font_size=_FS, flex_shrink="0"), value_style=_VAL))
    cit_date_row = MultiFieldRow(
        LabelValue("Citizenship No.:", d.get("citizenship_no", ""), label_style=_LBL.clone(width="130px"), value_style=Style(font_size=_FS, min_width="100px")),
        LabelValue("Issued Date:", f"  {d.get('issue_date','')}", label_style=_LBL.clone(width="100px"), value_style=_VAL),)
    details_panel = Div(
        FieldGroup(
            _lv("Name of landowner:", d.get("owner_name",""), lw="160px", field_name="owner_name"),
            addr_row,
            _lv("Husband's Name:", d.get("husband_name",""), lw="160px", field_name="husband_name"),
            _lv("Father in Law name:", d.get("father_in_law",""), lw="160px", field_name="father_in_law"),
            cit_date_row,
            _lv("Issued Office:", d.get("issue_office",""), lw="130px", field_name="issue_office"),
            spacing="5px", style=Style(font_size=_FS)),
        style=_box.clone(flex="1",height="155px",padding="8px 14px",display="flex",flex_direction="column",justify_content="center"),)
    photo_wrap = Div(photo_box, style=Style(margin_right="10px"))
    thumb_wrap = Div(thumb_box, style=Style(margin_right="10px"))
    doc.add(FlexRow(photo_wrap, thumb_wrap, details_panel, style=Style(width="100%", align_items="stretch")))
    doc.add(Spacer(height="18px"))

    # LAND RECORDS TABLE — signature is editable/textual or placeholder for scanned mark
    thead = [
        TableRow(
            _th("Evd. Symbol", colspan=3),
            _th("District/\nV.D.C./M.C.", rowspan=2),
            _th("Ward No./\nMap Sheet No.", rowspan=2),
            _th("Plot No./\nSect ion No.", rowspan=2),
            _th("Description\n(house,\nCultivated etc)", rowspan=2),
            _th("Land\nOwner\nShare on\nTitle", rowspan=2),
            _th("Tenant's\nName", rowspan=2),
            _th("Kind of\nLand or\nClass", rowspan=2),
            _th("Area\nSq. Mt.", rowspan=2),
            _th("Register\nPage No.", rowspan=2),
            _th("Remark", rowspan=2),
            _th("Signature\nof the\ncertifier", rowspan=2),
        ),
        TableRow(_th("Prior\nPlot\nNo."), _th("Description of transaction", colspan=2)),
    ]
    body_rows = []
    total_sqm = 0.0
    def _v(plot, key): return str(plot.get(key) or "")
    for i, plot in enumerate(d.get("plots", [])):
        total_sqm += _to_float(plot.get("area_sqm"))
        pf = f"plots.{i}."
        body_rows.append(TableRow(
            _td(_v(plot,"plot_no"), rowspan=2, field_name=f"{pf}plot_no"),
            _td(_v(plot,"evd_no"), field_name=f"{pf}evd_no"),
            _td(_v(plot,"evd_date"), field_name=f"{pf}evd_date"),
            _td(_v(plot,"vdc"), rowspan=2, field_name=f"{pf}vdc"),
            _td(_v(plot,"ward_top"), field_name=f"{pf}ward_top"),
            _td(_v(plot,"plot_section"), rowspan=2, field_name=f"{pf}plot_section"),
            _td(_v(plot,"desc_top"), field_name=f"{pf}desc_top"),
            _td(_v(plot,"owner_share"), rowspan=2, field_name=f"{pf}owner_share"),
            _td(_v(plot,"tenant"), rowspan=2, field_name=f"{pf}tenant"),
            _td(_v(plot,"kind_top"), rowspan=2, field_name=f"{pf}kind_top"),
            _td(_v(plot,"area_local"), field_name=f"{pf}area_local"),
            _td(_v(plot,"register_page"), field_name=f"{pf}register_page"),
            _td(_v(plot,"remark"), rowspan=2, field_name=f"{pf}remark"),
            # Signature field: editable, expects either (Signed) or text about visual marks
            _td(_v(plot,"signature") if _v(plot,"signature") else "(Signed/Certified)", rowspan=2, field_name=f"{pf}signature"),
        ))
        body_rows.append(TableRow(
            _td(_v(plot,"transaction_type"), colspan=2, field_name=f"{pf}transaction_type"),
            _td(_v(plot,"ward_bottom"), field_name=f"{pf}ward_bottom"),
            _td(_v(plot,"desc_bottom"), field_name=f"{pf}desc_bottom"),
            _td(_v(plot,"area_sqm"), field_name=f"{pf}area_sqm"),
            _td(_v(plot,"register_serial"), field_name=f"{pf}register_serial"),
        ))
    doc.add(Table(thead_rows=thead, children=body_rows))
    doc.add(FlexRow(Text(f"Total Area (Sq.m.)  {total_sqm:.2f}",style=Style(font_size=_FS, font_weight="bold")),style=Style(justify_content="flex-end", width="100%", margin_top="6px")))
    if d.get("doc_id"): doc.add(Spacer(height="4px")); doc.add(Text(d["doc_id"], style=Style(font_size="10px", color="#000000")))
    doc.add(Spacer(height="10px"))
    # Footer: checked-by date
    def _footer_item(bold_label: str, value: str) -> FlexRow:
        return FlexRow(Text(bold_label, style=Style(font_size=_FS, font_weight="bold")), Text(value, style=Style(font_size=_FS)), gap="2px")
    # Footer row proper
    footer_row = FlexRow(
        _footer_item("Printing done by:", " (Signed)."),
        _footer_item("Print Date:", f" {d.get('print_date','')}"),
        _footer_item("Checked by:", " (Signed)"),
        style=Style(justify_content="space-between", width="100%")
    )
    doc.add(footer_row)
    checked_by_date = d.get("checked_by_date", "")
    if checked_by_date:
        doc.add(FlexRow(Text("Checked by date:", style=Style(font_size="12px", font_weight="bold")),
                        Text(checked_by_date, style=Style(font_size="12px", margin_left="4px"), attrs=_ea("checked_by_date")),
                        style=Style(justify_content="flex-end", margin_top="2px", width="100%")))
    return doc
