from __future__ import annotations

from typing import Any

from html_engine import (
    Document,
    Style,
    Text,
    LabelValue,
    FieldGroup,
    MultiFieldRow,
    AbsoluteBox,
    FlexRow,
    FlexCol,
    PlaceholderBox,
)


EN_FONT = '"Times New Roman"'

LABEL_STYLE = Style(
    font_weight="bold",
    font_size="20px",
    width="270px",
    flex_shrink="0",
)

VALUE_STYLE = Style(
    font_size="20px",
    flex="1",
)

LINE_STYLE = Style(font_size="20px")

RIGHT_LABEL = Style(
    font_weight="bold",
    font_size="20px",
    width="130px",
    flex_shrink="0",
    text_align="right",
    padding_right="10px",
)

RIGHT_VALUE = Style(
    font_size="20px",
    width="110px",
    flex_shrink="0",
)

OFFICER_LABEL = Style(
    font_weight="bold",
    font_size="19px",
    width="125px",
    flex_shrink="0",
)

OFFICER_VALUE = Style(
    font_size="19px",
    flex="1",
)

NOTE_STYLE = Style(
    font_size="19px",
    line_height="1.35",
)

# The Act statement runs past its column and across the thumb boxes on the
# original, so it is given the full page width rather than the column's.
ACT_STYLE = NOTE_STYLE.clone(width="1000px")

GROW = Style(flex="1")


_EDITABLE_CSS = """
[contenteditable]:hover {
    outline: 2px dashed #000000;
    cursor: text;
}

[contenteditable]:focus {
    outline: 2px solid #000000;
    background: #ffffff;
}
"""


def _ea(field_name: str) -> dict[str, str]:
    return {
        "contenteditable": "true",
        "data-field": field_name,
    }


def field_row(
    label: str,
    value: str,
    label_style: Style = LABEL_STYLE,
    value_style: Style = VALUE_STYLE,
    field_name: str = "",
    style: Style | None = None,
) -> LabelValue:
    value_attrs = _ea(field_name) if field_name else {}

    return LabelValue(
        label,
        value,
        label_style=label_style,
        value_style=value_style,
        value_attrs=value_attrs,
        style=style,
    )


def multi_row(
    *parts: LabelValue,
    style: Style | None = None,
) -> MultiFieldRow:
    return MultiFieldRow(*parts, style=style)


def _place_block(
    district: str,
    unit_label: str,
    unit: str,
    district_field: str,
    unit_field: str,
) -> FlexCol:
    return FlexCol(
        Text(
            f"District: {district}",
            style=LINE_STYLE,
            attrs=_ea(district_field),
        ),
        Text(
            f"{unit_label}: {unit}",
            style=LINE_STYLE,
            attrs=_ea(unit_field),
        ),
    )


def _thumb_box(
    label: str,
    impression: str,
    label_field: str,
) -> FlexCol:
    """One captioned thumb-impression box.

    The extracted value says whether the scan carried an impression; the box
    itself is always drawn dashed, because the reproduction never contains the
    impression image, only a note that one was taken.
    """
    present = str(impression).strip().lower() == "present"

    return FlexCol(
        Text(
            label,
            style=Style(
                font_weight="bold",
                font_size="19px",
                margin_bottom="6px",
            ),
            attrs=_ea(label_field),
        ),
        PlaceholderBox(
            "Provided" if present else "Not Provided",
            size="165px",
            dashed=True,
        ),
    )


def _officer_row(
    label: str,
    value: str,
    field_name: str,
) -> LabelValue:
    return LabelValue(
        label,
        value,
        label_style=OFFICER_LABEL,
        value_style=OFFICER_VALUE,
        value_attrs=_ea(field_name),
    )


def _officer_block(
    heading: str,
    heading_field: str,
    signature: str,
    name: str,
    designation: str,
    signature_field: str,
    name_field: str,
    designation_field: str,
    date_value: str | None = None,
    date_field: str | None = None,
    signature_last: bool = False,
) -> FlexCol:
    """One officer's block: a heading, then their identifying rows.

    The two officers on this certificate do not print their rows in the same
    order — the issuing officer signs first, the officer providing the copy
    signs last — so ``signature_last`` moves that one row without duplicating
    the whole block.
    """
    signature_row = _officer_row("Signature:", signature, signature_field)
    identity_rows = [
        _officer_row("Name:", name, name_field),
        _officer_row("Designation:", designation, designation_field),
    ]

    rows: list[Any] = [
        Text(
            heading,
            style=Style(
                font_weight="bold",
                font_size="19px",
                margin_bottom="5px",
            ),
            attrs=_ea(heading_field),
        ),
    ]

    if signature_last:
        rows.extend(identity_rows)
        rows.append(signature_row)
    else:
        rows.append(signature_row)
        rows.extend(identity_rows)

    if date_value is not None and date_field is not None:
        rows.append(
            _officer_row(
                "Issue Date:",
                date_value,
                date_field,
            )
        )

    return FlexCol(*rows, gap="6px")


def build_citizenship_back(data: dict[str, Any]) -> Document:
    d = {
        # Top English section
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

        # Lower English section
        "nepal_citizenship_act_sentence": "",
        "citizenship_type": "",

        "right_thumb_impression": "",
        "left_thumb_impression": "",

        # Officer providing/certifying the copy
        "copy_issue_date_bs": "",
        "copy_officer_signature": "",
        "copy_officer_name": "",
        "copy_officer_designation": "",

        # Original issuing officer
        "issuing_officer_signature": "",
        "issuing_officer_name": "",
        "issuing_officer_designation": "",
        "issue_date_bs": "",

        # Footer
        "remarks": "",
    }

    d.update({k: v for k, v in data.items() if k in d})

    doc = Document(
        "Nepali Citizenship Certificate (Back)",
        page_width="1200px",
        page_height="750px",
        background="#ffffff",
        font_family=EN_FONT,
        border="2px solid #000000",
        extra_css=_EDITABLE_CSS,
    )

    # =======================================================================
    # TOP ENGLISH INFORMATION BOX
    # =======================================================================

    details = FieldGroup(
        multi_row(
            field_row(
                "Citizenship Certificate No.:",
                d["citizenship_no"],
                field_name="citizenship_no",
                style=GROW,
            ),
            field_row(
                "Sex:",
                d["sex"],
                RIGHT_LABEL,
                RIGHT_VALUE,
                "sex",
            ),
        ),

        multi_row(
            field_row(
                "Full Name:",
                d["full_name"],
                field_name="full_name",
            )
        ),

        multi_row(
            LabelValue(
                "Date of Birth (AD):",
                FlexRow(
                    Text(
                        f"Year: {d['dob_year']}",
                        style=LINE_STYLE,
                        attrs=_ea("dob_year"),
                    ),
                    Text(
                        f"Month: {d['dob_month']}",
                        style=LINE_STYLE,
                        attrs=_ea("dob_month"),
                    ),
                    Text(
                        f"Day: {d['dob_day']}",
                        style=LINE_STYLE,
                        attrs=_ea("dob_day"),
                    ),
                    gap="40px",
                ),
                label_style=LABEL_STYLE,
                value_style=VALUE_STYLE,
            )
        ),

        multi_row(
            LabelValue(
                "Birth Place:",
                _place_block(
                    d["birth_district"],
                    "VDC",
                    d["birth_rm_mn"],
                    "birth_district",
                    "birth_rm_mn",
                ),
                label_style=LABEL_STYLE,
                value_style=VALUE_STYLE,
                style=GROW,
            ),
            field_row(
                "Ward No.:",
                d["birth_ward_no"],
                RIGHT_LABEL,
                RIGHT_VALUE,
                "birth_ward_no",
            ),
        ),

        multi_row(
            LabelValue(
                "Permanent Address:",
                _place_block(
                    d["perm_district"],
                    "Municipality",
                    d["perm_municipality"],
                    "perm_district",
                    "perm_municipality",
                ),
                label_style=LABEL_STYLE,
                value_style=VALUE_STYLE,
                style=GROW,
            ),
            field_row(
                "Ward No.:",
                d["perm_ward_no"],
                RIGHT_LABEL,
                RIGHT_VALUE,
                "perm_ward_no",
            ),
        ),

        spacing="14px",
        style=Style(font_size="20px"),
    )

    doc.add(
        AbsoluteBox(
            FlexCol(
                Text(
                    "Government of Nepal has issued this Citizenship Certificate "
                    "with following details.",
                    style=Style(
                        font_weight="bold",
                        font_size="20px",
                        margin_bottom="14px",
                    ),
                ),
                details,
            ),
            top="28px",
            left="30px",
            style=Style(
                width="1138px",
                border="2px solid #000000",
                padding="18px 20px",
                box_sizing="border-box",
            ),
        )
    )

    # =======================================================================
    # LOWER LEFT: LEGAL STATEMENT / CITIZENSHIP TYPE / THUMBS
    # =======================================================================

    left_lower = FlexCol(
        Text(
            d["nepal_citizenship_act_sentence"],
            style=ACT_STYLE,
            attrs=_ea("nepal_citizenship_act_sentence"),
        ),

        field_row(
            "Citizenship Type:",
            d["citizenship_type"],
            Style(
                font_weight="bold",
                font_size="20px",
                width="200px",
                flex_shrink="0",
            ),
            VALUE_STYLE,
            "citizenship_type",
        ),

        Text(
            "Certificate Holder's Signature:",
            style=Style(
                font_weight="bold",
                font_size="19px",
                margin_top="2px",
            ),
        ),

        # The original leaves the space under this heading blank for a wet
        # signature — the thumb boxes follow immediately.
        FlexRow(
            _thumb_box(
                "(Right)   Thumb Impression",
                d["right_thumb_impression"],
                "right_thumb_impression",
            ),
            _thumb_box(
                "(Left)",
                d["left_thumb_impression"],
                "left_thumb_impression",
            ),
            gap="34px",
        ),
        gap="9px",
    )

    doc.add(
        AbsoluteBox(
            left_lower,
            top="365px",
            left="34px",
            style=Style(width="610px"),
        )
    )

    # =======================================================================
    # LOWER RIGHT: OFFICER PROVIDING / CERTIFYING THE COPY
    # =======================================================================

    copy_officer = FlexCol(
        Text(
            "Date: " + d["copy_issue_date_bs"],
            style=Style(
                font_weight="bold",
                font_size="19px",
            ),
            attrs=_ea("copy_issue_date_bs"),
        ),

        _officer_block(
            heading="Officer Providing the Copy:",
            heading_field="copy_officer_heading",
            signature=d["copy_officer_signature"],
            name=d["copy_officer_name"],
            designation=d["copy_officer_designation"],
            signature_field="copy_officer_signature",
            name_field="copy_officer_name",
            designation_field="copy_officer_designation",
            signature_last=True,
        ),
    )

    # copy_officer_heading is intentionally fixed English text. It is not an
    # extraction field, but leaving it in the editable layout is useful.
    doc.add(
        AbsoluteBox(
            copy_officer,
            top="365px",
            left="650px",
            style=Style(width="510px"),
        )
    )

    # =======================================================================
    # LOWER RIGHT: ORIGINAL ISSUING OFFICER
    # =======================================================================

    issuing_officer = _officer_block(
        heading="Officer Issuing this Certificate:",
        heading_field="issuing_officer_heading",
        signature=d["issuing_officer_signature"],
        name=d["issuing_officer_name"],
        designation=d["issuing_officer_designation"],
        signature_field="issuing_officer_signature",
        name_field="issuing_officer_name",
        designation_field="issuing_officer_designation",
        date_value=d["issue_date_bs"],
        date_field="issue_date_bs",
    )

    doc.add(
        AbsoluteBox(
            issuing_officer,
            top="545px",
            left="650px",
            style=Style(width="510px"),
        )
    )

    # =======================================================================
    # FOOTER
    # =======================================================================

    doc.add(
        AbsoluteBox(
            Text(
                d["remarks"],
                style=NOTE_STYLE,
                attrs=_ea("remarks"),
            ),
            left="34px",
            bottom="28px",
            style=Style(width="1128px"),
        )
    )

    return doc

