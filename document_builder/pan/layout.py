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
)

LABEL_STYLE = Style(font_weight="bold", font_size="16px", width="220px", flex_shrink="0")
VALUE_STYLE = Style(font_size="16px", flex="1")
ROW_STYLE = Style(margin_bottom="15px")

def field_row(
    label: str,
    value: str,
    label_style: Style = LABEL_STYLE,
    value_style: Style = VALUE_STYLE,
) -> LabelValue:
    return LabelValue(
        label,
        value,
        label_style=label_style,
        value_style=value_style,
    )

def build_pan(data: dict[str, Any]) -> Document:
    d = {
        "pan_no": "",
        "registration_date_day": "",
        "registration_date_month": "",
        "registration_date_year": "",
        "tax_type": "",
        "office_name": "",
        "taxpayer_name": "",
        "business_name": "",
        "taxpayer_type": "",
        "address": "",
        "business_activities": "",
        "taxpayer_signature": "",
        "officer_name": "",
        "officer_designation": "",
    }
    d.update(data)

    doc = Document(
        "Permanent Account Number (PAN) Certificate",
        page_width="850px",
        page_height="1150px",
        background="#ffffff",
        font_family='"Times New Roman", serif',
        border="3px double #000000",
    )

    # Coat of Arms (Top Left)
    doc.add(
        AbsoluteBox(
            FlexCol(
                Text("Coat of Arms", style=Style(font_size="11px", color="#888")),
                style=Style(align_items="center", justify_content="center")
            ),
            style=Style(
                width="110px",
                height="110px",
                border="1px solid #d3d3d3",
                display="flex",
                align_items="center",
                justify_content="center",
                text_align="center",
            ),
            left="50px",
            top="40px",
        )
    )

    # Header Texts (Centre)
    doc.add(
        AbsoluteBox(
            FlexCol(
                Heading("Government of Nepal", level=1, style=Style(margin="0 0 2px 0", font_size="20px", font_weight="bold", text_align="center")),
                Heading("Ministry of Finance", level=2, style=Style(margin="0 0 2px 0", font_size="18px", font_weight="bold", text_align="center")),
                Heading("Inland Revenue Department", level=3, style=Style(margin="0 0 5px 0", font_size="22px", font_weight="bold", text_align="center")),
                style=Style(align_items="center", justify_content="center")
            ),
            left="180px",
            right="180px",
            top="45px",
        )
    )

    # Photo Box (Top Right)
    doc.add(
        AbsoluteBox(
            FlexCol(
                Text("Photo", style=Style(font_size="11px", color="#888")),
                style=Style(align_items="center", justify_content="center")
            ),
            style=Style(
                width="110px",
                height="130px",
                border="1px solid #d3d3d3",
                display="flex",
                align_items="center",
                justify_content="center",
                text_align="center",
            ),
            right="50px",
            top="40px",
        )
    )

    # Document Title
    doc.add(
        AbsoluteBox(
            FlexCol(
                Heading("Permanent Account Number (PAN) Registration Certificate", level=1, style=Style(font_size="22px", font_weight="bold", text_align="center")),
                style=Style(border_bottom="2px solid #000000", padding_bottom="5px", align_items="center")
            ),
            left="50px",
            right="50px",
            top="215px",
        )
    )

    # PAN and Registration Date Section
    pan_cleaned = str(d.get("pan_no") or "").replace("-", "").replace(" ", "")
    # A standard PAN has 9 digits; ensure we render exactly 9 boxes
    pan_padded = pan_cleaned.ljust(9)[:9]
    pan_boxes = []
    for digit in pan_padded:
        pan_boxes.append(
            Div(
                Text(digit if digit != " " else "", style=Style(font_size="18px", font_weight="bold")),
                style=Style(
                    width="26px",
                    height="30px",
                    border="1px solid #000000",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    margin_right="2px",
                )
            )
        )

    # Date table component on the right
    date_table = Div(
        # Headers Row
        FlexRow(
            FlexCol(
                Text("Regd. Date", style=Style(font_size="12px", font_weight="bold", text_align="right")),
                style=Style(margin_right="10px")
            ),
            FlexCol(
                # Date values row
                FlexRow(
                    Div(Text(d["registration_date_day"], style=Style(font_size="12px", font_weight="bold")), style=Style(width="28px", height="22px", border="1px solid #000", display="flex", align_items="center", justify_content="center")),
                    Div(Text(d["registration_date_month"], style=Style(font_size="12px", font_weight="bold")), style=Style(width="28px", height="22px", border="1px solid #000", display="flex", align_items="center", justify_content="center", margin_left="2px")),
                    Div(Text(d["registration_date_year"], style=Style(font_size="12px", font_weight="bold")), style=Style(width="48px", height="22px", border="1px solid #000", display="flex", align_items="center", justify_content="center", margin_left="2px")),
                ),
                # Sub labels row
                FlexRow(
                    Text("Day", style=Style(font_size="9px", width="28px", text_align="center")),
                    Text("Month", style=Style(font_size="9px", width="28px", text_align="center", margin_left="2px")),
                    Text("Year", style=Style(font_size="9px", width="48px", text_align="center", margin_left="2px")),
                ),
                gap="1px"
            ),
            style=Style(align_items="center")
        )
    )

    doc.add(
        AbsoluteBox(
            FlexRow(
                # Left side: PAN number label & boxes
                FlexRow(
                    FlexCol(
                        Text("Permanent Account Number:", style=Style(font_size="14px", font_weight="bold")),
                    ),
                    Div(style=Style(width="10px")),
                    FlexRow(*pan_boxes),
                    style=Style(align_items="center")
                ),
                # Right side: आयकर + दर्ता मिति
                FlexRow(
                    FlexCol(
                        Text(d["tax_type"] or "Income Tax", style=Style(font_size="13px", font_weight="bold")),
                        style=Style(margin_right="15px", border="1px solid #000", padding="2px 6px")
                    ),
                    date_table,
                    style=Style(align_items="center")
                ),
                style=Style(width="100%", justify_content="space-between")
            ),
            left="50px",
            right="50px",
            top="295px",
        )
    )

    # Details Block
    details = FieldGroup(
        field_row("Office:", d["office_name"]),
        field_row("Taxpayer's Name:", d["taxpayer_name"]),
        field_row("Business Name:", d["business_name"]),
        field_row("Taxpayer Type:", d["taxpayer_type"]),
        field_row("Address:", d["address"]),
        field_row("Business Activities:", d["business_activities"]),
        spacing="16px",
        style=Style(font_size="16px"),
    )

    doc.add(
        AbsoluteBox(
            details,
            left="50px",
            right="50px",
            top="375px",
            style=Style(width="750px")
        )
    )

    # Signature/Seal Section
    doc.add(
        AbsoluteBox(
            FlexRow(
                # Taxpayer Signature (Left)
                FlexCol(
                    Text(d["taxpayer_signature"], style=Style(font_family="'Brush Script MT', cursive", font_size="28px", text_align="center", height="40px")),
                    Div(style=Style(width="180px", border_top="1px dashed #000000", margin="5px 0")),
                    Text("Taxpayer's Signature", style=Style(font_size="13px", font_weight="bold", text_align="center")),
                    style=Style(align_items="center")
                ),
                # Officer Signature & Stamp (Right)
                FlexCol(
                    # Stamp representation
                    AbsoluteBox(
                        Div(
                            Text("Tax Officer", style=Style(color="rgba(0, 150, 255, 0.8)", font_weight="bold", font_size="13px")),
                            style=Style(
                                border="2px solid rgba(0, 150, 255, 0.8)",
                                padding="2px 10px",
                                border_radius="5px",
                                transform="rotate(-5deg)",
                                display="flex",
                                flex_direction="column",
                                align_items="center"
                            )
                        ),
                        right="10px",
                        bottom="80px",
                    ),
                    Text(d["officer_name"], style=Style(font_size="15px", font_weight="bold", text_align="center", height="40px", line_height="40px")),
                    Div(style=Style(width="180px", border_top="1px dashed #000000", margin="5px 0")),
                    Text(d["officer_designation"] or "Tax Officer", style=Style(font_size="13px", font_weight="bold", text_align="center")),
                    style=Style(position="relative", align_items="center")
                ),
                style=Style(width="750px", justify_content="space-between")
            ),
            left="50px",
            right="50px",
            top="680px",
        )
    )

    # Bottom Instructions Box
    instructions = FlexCol(
        Text("Duties to be followed by the taxpayer:", style=Style(font_weight="bold", font_size="14px", margin_bottom="10px")),
        Text("1. Invoice/bill must be mandatorily issued while conducting transactions.", style=Style(font_size="11px", color="#444", margin_bottom="6px")),
        Text("2. Those registered in VAT must submit VAT returns and tax amount within 25 days of the end of each tax period (monthly, bi-monthly, or quadrimesterly).", style=Style(font_size="11px", color="#444", margin_bottom="6px")),
        Text("3. Those dealing with excise-taxable transactions must submit monthly records and excise duty within 25 days of the end of each month, except as otherwise provided.", style=Style(font_size="11px", color="#444", margin_bottom="6px")),
        Text("4. Income details of each fiscal year must be submitted within three months of the end of the fiscal year.", style=Style(font_size="11px", color="#444", margin_bottom="6px")),
        Text("5. Failure to submit details and tax amount within the specified time will attract interest, fees, and penalties.", style=Style(font_size="11px", color="#444", margin_bottom="6px")),
        Text("6. This certificate must be kept in a visible place at the place of transaction / main office.", style=Style(font_size="11px", color="#444", margin_bottom="6px")),
        Text("7. In case of any confusion, please contact the office.", style=Style(font_size="11px", color="#444")),
        style=Style(
            border="1px solid #000000",
            padding="15px",
            background="#fafafa",
        )
    )

    doc.add(
        AbsoluteBox(
            instructions,
            left="50px",
            right="50px",
            bottom="50px",
        )
    )

    return doc
