from __future__ import annotations

from typing import Any

from html_engine import (
    Document,
    Style,
    Text,
    LabelValue,
    FlexCol,
    Spacer,
    PlaceholderBox,
    Table,
    TableRow,
    TableCell,
    AbsoluteBox,
)

_EDITABLE_CSS = """
[contenteditable]:hover {
    outline: 2px dashed #000000;
    cursor: text;
}

[contenteditable]:focus {
    outline: 2px solid #000000;
    background: #ffffff;
}

.tax-table-cell {
    border: 1px solid #000000;
}
"""


def _ea(field_name: str) -> dict[str, str]:
    return {
        "contenteditable": "true",
        "data-field": field_name,
    }


def build_tax_clearance(data: dict[str, Any]) -> Document:
    def safe_get(key: str, default: Any = "") -> Any:
        value = data.get(key, default)
        return default if value is None else value

    def safe_items(key: str) -> list:
        value = data.get(key, [])
        return value if isinstance(value, list) else []

    # A4 portrait: 210 x 297 mm at ~96 CSS DPI.
    # This is deliberately a fixed canvas because the source is a fixed-layout
    # government form rather than a responsive web page.
    doc = Document(
        "Tax Clearance Certificate",
        page_width="794px",
        page_height="1123px",
        background="#ffffff",
        font_family='"Times New Roman", serif',
        page_style=Style(
            padding="0px",
            margin="0px",
            width="794px",
            height="1123px",
            box_sizing="border-box",
            overflow="hidden",
        ),
        extra_css=_EDITABLE_CSS,
    )

    # -----------------------------------------------------------------------
    # 1. MASTHEAD
    # -----------------------------------------------------------------------

    if safe_get("emblem_present"):
        doc.add(
            AbsoluteBox(
                PlaceholderBox(
                    "Coat of Arms of Nepal",
                    size="82px",
                    shape="circle",
                ),
                top="57px",
                left="55px",
            )
        )

    # Keep each source heading as its own line. Do NOT put the complete office
    # hierarchy into one long flowing line.
    office_lines = [
        ("Government of Nepal", "office_government"),
        ("Ministry of Finance", "office_ministry"),
        ("Inland Revenue Department", "office_department"),
        ("Inland Revenue Office Lahan", "office_main"),
        ("Treasury and Accounts Controller Office, Udayapur", "office_suboffice"),
        ("Related to Rule 26 of Income Tax Rules, 2079", "rule_reference"),
    ]

    office_nodes = []
    for text, field in office_lines:
        office_nodes.append(
            Text(
                safe_get(field, text),
                style=Style(
                    font_weight="bold" if field != "rule_reference" else "normal",
                    font_size="15px" if field != "rule_reference" else "13px",
                    line_height="1.42",
                    text_align="center",
                    width="430px",
                ),
                attrs=_ea(field),
            )
        )

    doc.add(
        AbsoluteBox(
            FlexCol(
                *office_nodes,
                gap="0px",
                style=Style(align_items="center"),
            ),
            top="49px",
            left="182px",
            style=Style(
                width="430px",
                align_items="center",
            ),
        )
    )

    # -----------------------------------------------------------------------
    # 2. LEFT REFERENCE BLOCK
    # -----------------------------------------------------------------------

    left_header = FlexCol(
        LabelValue(
            "Letter No.:",
            safe_get("letter_no"),
            label_style=Style(
                font_size="13px",
                font_weight="bold",
                width="78px",
                flex_shrink="0",
            ),
            value_style=Style(font_size="13px", flex="1"),
            value_attrs=_ea("letter_no"),
        ),
        LabelValue(
            "Reg. No.:",
            safe_get("registration_no"),
            label_style=Style(
                font_size="13px",
                font_weight="bold",
                width="78px",
                flex_shrink="0",
            ),
            value_style=Style(font_size="13px", flex="1"),
            value_attrs=_ea("registration_no"),
        ),
        LabelValue(
            "Tax Clearance No.:",
            safe_get("tax_clearance_no"),
            label_style=Style(
                font_size="13px",
                font_weight="bold",
                width="78px",
                flex_shrink="0",
            ),
            value_style=Style(font_size="13px", flex="1"),
            value_attrs=_ea("tax_clearance_no"),
        ),
        gap="6px",
    )

    doc.add(
        AbsoluteBox(
            left_header,
            top="252px",
            left="55px",
            style=Style(width="220px"),
        )
    )

    # -----------------------------------------------------------------------
    # 3. RIGHT DATE SENTENCES
    # -----------------------------------------------------------------------

    # The source does not use a short "Issue Date:" label. It contains a full
    # sentence. Keep the sentence intact in the English rendering.
    issue_sentence = safe_get("issue_date_sentence")
    if not issue_sentence:
        issue_sentence = (
            f"This letter has been prepared on "
            f"{safe_get('issue_date_gregorian') or safe_get('issue_date_nepali')}."
        )

    print_sentence = safe_get("print_date_sentence")
    if not print_sentence:
        print_sentence = (
            f"Print Date: "
            f"{safe_get('print_date_gregorian') or safe_get('print_date_nepali')}"
        )

    doc.add(
        AbsoluteBox(
            FlexCol(
                Text(
                    issue_sentence,
                    style=Style(
                        font_size="12px",
                        line_height="1.3",
                        width="265px",
                        text_align="left",
                    ),
                    attrs=_ea("issue_date_sentence"),
                ),
                Text(
                    print_sentence,
                    style=Style(
                        font_size="12px",
                        line_height="1.3",
                        width="265px",
                        text_align="left",
                        margin_top="5px",
                    ),
                    attrs=_ea("print_date_sentence"),
                ),
                gap="0px",
            ),
            top="245px",
            left="485px",
            style=Style(width="265px"),
        )
    )

    # -----------------------------------------------------------------------
    # 4. QR CODE
    # -----------------------------------------------------------------------

    if safe_get("qr_present"):
        doc.add(
            AbsoluteBox(
                PlaceholderBox(
                    "QR Code",
                    size="62px",
                ),
                top="286px",
                left="613px",
            )
        )

    # -----------------------------------------------------------------------
    # 5. SEAL
    # -----------------------------------------------------------------------

    if safe_get("seal_present"):
        doc.add(
            AbsoluteBox(
                PlaceholderBox(
                    "Round Office Seal",
                    shape="circle",
                    size="66px",
                    style=Style(opacity="0.45"),
                ),
                top="147px",
                left="338px",
                style=Style(z_index="3"),
            )
        )

    # -----------------------------------------------------------------------
    # 6. SUBJECT
    # -----------------------------------------------------------------------

    doc.add(
        AbsoluteBox(
            Text(
                f"Subject: {safe_get('subject')}",
                style=Style(
                    font_size="17px",
                    font_weight="bold",
                    text_align="center",
                    text_decoration="underline",
                    width="500px",
                ),
                attrs=_ea("subject"),
            ),
            top="359px",
            left="147px",
            style=Style(width="500px"),
        )
    )

    # -----------------------------------------------------------------------
    # 7. RECIPIENT LETTER BLOCK
    # -----------------------------------------------------------------------

    recipient = FlexCol(
        Text(
            safe_get("recipient_salutation"),
            style=Style(
                font_size="14px",
                line_height="1.35",
            ),
            attrs=_ea("recipient_salutation"),
        ),
        Text(
            safe_get("recipient_name"),
            style=Style(
                font_size="14px",
                line_height="1.35",
            ),
            attrs=_ea("recipient_name"),
        ),
        Text(
            safe_get("recipient_address"),
            multiline=True,
            style=Style(
                font_size="14px",
                line_height="1.35",
            ),
            attrs=_ea("recipient_address"),
        ),
        Text(
            f"PAN No.: {safe_get('recipient_pan')}",
            style=Style(
                font_size="14px",
                line_height="1.35",
                font_weight="normal",
            ),
            attrs=_ea("recipient_pan"),
        ),
        gap="2px",
    )

    doc.add(
        AbsoluteBox(
            recipient,
            top="422px",
            left="55px",
            style=Style(width="680px"),
        )
    )

    # -----------------------------------------------------------------------
    # 8. MAIN CERTIFICATE TEXT
    # -----------------------------------------------------------------------

    doc.add(
        AbsoluteBox(
            Text(
                safe_get("main_text"),
                multiline=True,
                style=Style(
                    font_size="14px",
                    line_height="1.45",
                    width="680px",
                    text_align="left",
                ),
                attrs=_ea("main_text"),
            ),
            top="493px",
            left="55px",
            style=Style(width="680px"),
        )
    )

    # -----------------------------------------------------------------------
    # 9. INCOME TABLE WITH INNER BORDERS
    # -----------------------------------------------------------------------

    income_items = safe_items("income_items")

    if income_items:
        cell_style = Style(
            padding="5px 7px",
            box_sizing="border-box",
            border="1px solid #000000",
        )

        header_style = Style(
            font_weight="bold",
            font_size="12px",
            text_align="center",
            border="1px solid #000000",
        )

        body_style = Style(
            font_size="12px",
            text_align="center",
            border="1px solid #000000",
        )

        headers = [
            "Income Statement Date",
            "Total Income / Turnover (NPR)",
            "Taxable Income (NPR)",
            "Tax Deposited (NPR)",
        ]

        header_row = TableRow(
            *(
                TableCell(
                    header,
                    is_header=True,
                    style=header_style.merge(cell_style),
                )
                for header in headers
            )
        )

        rows = []
        for index, row in enumerate(income_items):
            if not isinstance(row, dict):
                continue

            rows.append(
                TableRow(
                    TableCell(
                        row.get("submission_date", ""),
                        style=body_style.merge(cell_style),
                        field=f"income_items.{index}.submission_date",
                    ),
                    TableCell(
                        row.get("total_income", ""),
                        style=body_style.merge(cell_style),
                        field=f"income_items.{index}.total_income",
                    ),
                    TableCell(
                        row.get("taxable_income", ""),
                        style=body_style.merge(cell_style),
                        field=f"income_items.{index}.taxable_income",
                    ),
                    TableCell(
                        row.get("tax_deposited", ""),
                        style=body_style.merge(cell_style),
                        field=f"income_items.{index}.tax_deposited",
                    ),
                )
            )

        doc.add(
            AbsoluteBox(
                Table(
                    thead_rows=[header_row],
                    children=rows,
                    style=Style(
                        width="680px",
                        border="1px solid #000000",
                        border_collapse="collapse",
                    ),
                ),
                top="574px",
                left="55px",
                style=Style(width="680px"),
            )
        )

    # -----------------------------------------------------------------------
    # 10. CERTIFYING OFFICER
    # -----------------------------------------------------------------------

    officer_name = str(safe_get("certifying_officer_name")).strip()
    officer_title = str(safe_get("certifying_officer_title")).strip()
    signature_label = str(safe_get("signature_label")).strip()

    if officer_name or officer_title or signature_label:
        doc.add(
            AbsoluteBox(
                FlexCol(
                    Text(
                        signature_label or "Signature:",
                        style=Style(
                            font_size="13px",
                            font_weight="bold",
                        ),
                        attrs=_ea("signature_label"),
                    ),
                    Text(
                        officer_name,
                        style=Style(font_size="13px"),
                        attrs=_ea("certifying_officer_name"),
                    ),
                    Text(
                        officer_title,
                        style=Style(font_size="13px"),
                        attrs=_ea("certifying_officer_title"),
                    ),
                    gap="3px",
                ),
                top="665px",
                left="55px",
                style=Style(width="250px"),
            )
        )

    # -----------------------------------------------------------------------
    # 11. NOTES
    # -----------------------------------------------------------------------

    doc.add(
        AbsoluteBox(
            FlexCol(
                Text(
                    "Notes:",
                    style=Style(
                        font_weight="bold",
                        font_size="13px",
                        margin_bottom="8px",
                    ),
                ),
                Text(
                    safe_get("remarks"),
                    multiline=True,
                    style=Style(
                        font_size="12px",
                        line_height="1.45",
                        width="680px",
                        text_align="left",
                    ),
                    attrs=_ea("remarks"),
                ),
                gap="0px",
            ),
            top="753px",
            left="55px",
            style=Style(
                width="680px",
            ),
        )
    )

    return doc

