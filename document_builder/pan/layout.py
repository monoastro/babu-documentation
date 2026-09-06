"""Translated, source-faithful layout for the Rajendra Rai PAN certificate."""

from __future__ import annotations

import re
from typing import Any

from html_engine import AbsoluteBox, Div, Document, FlexCol, FlexRow, LabelValue, PlaceholderBox, Style, Text


# Rajendra's source is 637 x 895 portrait.  These A4-sized dimensions retain
# that proportion and all coordinates below scale from its visible form.
PAGE_WIDTH = "794px"
PAGE_HEIGHT = "1123px"

_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

FIELDS = (
    "pan_no",
    "inland_revenue_office",
    "taxpayer_service_office",
    "income_tax_registration_date_bs",
    "vat_registration_date_bs",
    "excise_registration_date_bs",
    "taxpayer_name",
    "business_name",
    "taxpayer_type",
    "address",
    "business_activities",
)

_LABEL_STYLE = Style(font_size="16px", font_weight="bold", flex_shrink="0")
_VALUE_STYLE = Style(font_size="17px", min_width="0", overflow_wrap="anywhere")


def _row(label: str, value: str, field: str, *, label_width: str = "172px") -> LabelValue:
    return LabelValue(
        label,
        value,
        field=field,
        label_width=label_width,
        label_style=_LABEL_STYLE,
        value_style=_VALUE_STYLE,
    )


def _digits(value: str, count: int) -> list[str]:
    """Fit a PAN serial into its individual printed cells."""
    compact = re.sub(r"[\s-]", "", value)
    return list(compact[:count].ljust(count))


def _pan_cells(value: str) -> FlexRow:
    return FlexRow(
        *(
            Div(
                Text(digit.strip(), style=Style(font_size="19px", font_weight="bold")),
                style=Style(
                    width="21px",
                    height="29px",
                    border="1px solid #000000",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    box_sizing="border-box",
                ),
            )
            for digit in _digits(value, 10)
        ),
        gap="1px",
        field="pan_no",
    )


def _date_parts(value: str) -> list[str]:
    """Make one editable BS date look like source's day/month/year cells."""
    parts = [part for part in re.split(r"[\s/.-]+", value.strip()) if part]
    if len(parts) == 3:
        return parts
    return ["", "", value]


def _date_cells(value: str, field: str) -> FlexRow:
    day, month, year = _date_parts(value)
    widths = ("30px", "30px", "54px")
    return FlexRow(
        *(
            Div(
                Text(part, style=Style(font_size="13px", font_weight="bold")),
                style=Style(
                    width=width,
                    height="25px",
                    border="1px solid #000000",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    box_sizing="border-box",
                    overflow="hidden",
                ),
            )
            for part, width in zip((day, month, year), widths)
        ),
        gap="1px",
        field=field,
    )


def _signature_line(label: str) -> FlexCol:
    """The scan has handwritten signatures over a single horizontal rule."""
    return FlexCol(
        Div(style=Style(width="210px", height="62px", border_bottom="1px solid #000000")),
        Text(label, style=Style(font_size="14px", font_weight="bold", text_align="center")),
        gap="7px",
        style=Style(align_items="center"),
    )


def build_pan(data: dict[str, Any]) -> Document:
    d = {field: "" for field in FIELDS}
    d.update(data or {})
    d = {field: value if value is not None else "" for field, value in d.items()}

    doc = Document(
        "Permanent Account Number (PAN) Registration Certificate",
        page_width=PAGE_WIDTH,
        page_height=PAGE_HEIGHT,
        background="#ffffff",
        font_family='"Noto Sans Devanagari", "Times New Roman", serif',
        border="1px solid #000000",
        extra_css=_EDITABLE_CSS,
        lang="en",
    )

    # Government crest, translated central header, and passport photo retain
    # the source scan's three-part top band.
    doc.add(
        AbsoluteBox(
            PlaceholderBox("Government\nemblem", width="115px", height="115px", font_size="13px"),
            left="42px",
            top="40px",
        ),
        AbsoluteBox(
            FlexCol(
                Text("Government of Nepal", style=Style(font_size="22px", font_weight="bold")),
                Text("Ministry of Finance", style=Style(font_size="20px", font_weight="bold")),
                Text("Inland Revenue Department", style=Style(font_size="22px", font_weight="bold")),
                gap="2px",
                style=Style(align_items="center", line_height="1.1", text_align="center"),
            ),
            left="183px",
            top="42px",
            style=Style(width="380px"),
        ),
        AbsoluteBox(
            PlaceholderBox("Photograph", width="134px", height="165px", font_size="14px"),
            right="30px",
            top="34px",
        ),
        AbsoluteBox(
            Text(
                "Permanent Account Number (PAN) Registration Certificate",
                style=Style(font_size="20px", font_weight="bold", text_align="center"),
            ),
            left="72px",
            top="180px",
            style=Style(width="650px"),
        ),
    )

    # Compact upper form: offices left, 10-cell PAN serial centre, and tax
    # registration dates right, exactly as this certificate format presents it.
    doc.add(
        AbsoluteBox(
            FlexCol(
                Text("Permanent account number:", style=Style(font_size="16px", font_weight="bold")),
                _row("Inland Revenue Office:", d["inland_revenue_office"], "inland_revenue_office", label_width="176px"),
                _row("Taxpayer Service Office:", d["taxpayer_service_office"], "taxpayer_service_office", label_width="176px"),
                gap="6px",
            ),
            left="40px",
            top="253px",
            style=Style(width="375px"),
        ),
        AbsoluteBox(
            _pan_cells(str(d["pan_no"])),
            left="258px",
            top="254px",
        ),
        AbsoluteBox(
            FlexCol(
                Text("Registration date", style=Style(font_size="15px", font_weight="bold", text_align="center")),
                FlexRow(Text("Income tax:", style=Style(font_size="14px", font_weight="bold", width="73px")), _date_cells(str(d["income_tax_registration_date_bs"]), "income_tax_registration_date_bs")),
                FlexRow(Text("VAT:", style=Style(font_size="14px", font_weight="bold", width="73px")), _date_cells(str(d["vat_registration_date_bs"]), "vat_registration_date_bs")),
                FlexRow(Text("Excise:", style=Style(font_size="14px", font_weight="bold", width="73px")), _date_cells(str(d["excise_registration_date_bs"]), "excise_registration_date_bs")),
                FlexRow(
                    Div(style=Style(width="73px")),
                    Text("Day", style=Style(font_size="10px", width="31px", text_align="center")),
                    Text("Month", style=Style(font_size="10px", width="31px", text_align="center")),
                    Text("Year", style=Style(font_size="10px", width="54px", text_align="center")),
                ),
                gap="3px",
            ),
            right="39px",
            top="235px",
            style=Style(width="192px"),
        ),
    )

    # Central taxpayer block follows source row order and leaves its large
    # blank lower half intact.
    doc.add(
        AbsoluteBox(
            FlexCol(
                _row("Taxpayer name:", d["taxpayer_name"], "taxpayer_name"),
                _row("Business name:", d["business_name"], "business_name"),
                _row("Taxpayer type:", d["taxpayer_type"], "taxpayer_type"),
                _row("Address:", d["address"], "address"),
                gap="18px",
            ),
            left="40px",
            top="353px",
            style=Style(width="590px"),
        ),
        AbsoluteBox(
            FlexRow(
                Text("Business activities:", style=Style(font_size="16px", font_weight="bold", width="172px", flex_shrink="0")),
                Div(
                    Text(str(d["business_activities"]), field="business_activities", multiline=True, style=Style(font_size="16px")),
                    style=Style(
                        width="495px",
                        min_height="29px",
                        border="1px solid #000000",
                        padding="3px 6px",
                        box_sizing="border-box",
                    ),
                ),
            ),
            left="40px",
            top="547px",
        ),
        AbsoluteBox(_signature_line("Taxpayer's signature"), left="96px", top="594px"),
        AbsoluteBox(_signature_line("Tax officer's signature"), right="82px", top="594px"),
    )

    # Fixed instructions sit at source scan's bottom, not inside a framed card.
    doc.add(
        AbsoluteBox(
            FlexCol(
                Text("Duties to be followed by taxpayer:", style=Style(font_size="14px", font_weight="bold")),
                Text("• Issue an invoice or bill for every transaction.", style=Style(font_size="11px")),
                Text("• Submit VAT and excise returns and tax within the statutory deadline.", style=Style(font_size="11px")),
                Text("• Submit annual income details within three months after each fiscal year ends.", style=Style(font_size="11px")),
                Text("• Late filing or payment may result in interest, fees, and penalties.", style=Style(font_size="11px")),
                Text("• Keep this certificate visibly displayed at the place of business.", style=Style(font_size="11px")),
                Text("• Contact the Inland Revenue Office if clarification is needed.", style=Style(font_size="11px")),
                gap="4px",
            ),
            left="39px",
            top="950px",
            style=Style(width="710px"),
        ),
    )

    return doc
