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
    AbsoluteBox,
    FlexRow,
    FlexCol,
)


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

LABEL_STYLE = Style(
    font_weight="bold",
    font_size="20px",
    width="245px",
    flex_shrink="0",
)

VALUE_STYLE = Style(
    font_size="20px",
    flex="1",
)

RIGHT_LABEL = Style(
    font_weight="bold",
    font_size="20px",
    width="180px",
    flex_shrink="0",
    text_align="right",
    padding_right="10px",
)

SMALL_LABEL = Style(
    font_weight="bold",
    font_size="20px",
    width="180px",
    flex_shrink="0",
)

ROW_STYLE = Style(
    margin_bottom="7px",
)

# The permanent-address district is printed as one continuous line on the
# original: label and value must not wrap, whatever the value's length.
NOWRAP_LABEL = LABEL_STYLE.clone(white_space="nowrap")
NOWRAP_VALUE = VALUE_STYLE.clone(white_space="nowrap")

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
    """Attributes used by the visual editor to identify editable fields."""
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
) -> LabelValue:
    attrs = _ea(field_name) if field_name else {}

    return LabelValue(
        label,
        value,
        label_style=label_style,
        value_style=value_style,
        value_attrs=attrs,
    )


def multi_row(
    *parts: LabelValue,
    style: Style | None = None,
) -> MultiFieldRow:
    return MultiFieldRow(*parts, style=style)


def build_citizenship_old(data: dict[str, Any]) -> Document:
    d: dict[str, Any] = {
        "citizenship_no": "",
        "full_name": "",
        "gender": "",
        "birth_district": "",
        "birth_municipality": "",
        "birth_ward": "",
        "perm_district": "",
        "perm_municipality": "",
        "perm_ward": "",
        "dob_year": "",
        "dob_month": "",
        "dob_day": "",
        "father_name": "",
        "father_address": "",
        "father_na_ki": "",
        "mother_name": "",
        "mother_address": "",
        "mother_na_ki": "",
        "district_admin_location": "",
    }

    d.update({k: v for k, v in data.items() if k in d})

    # Old citizenship certificate is approximately 1158 x 759 px.
    # Keep the same aspect ratio used by the newer citizenship layout.
    doc = Document(
        "Nepali Citizenship Certificate - Old Layout",
        page_width="1200px",
        page_height="780px",
        background="#ffffff",
        font_family='"Noto Sans Devanagari", "Noto Sans", "Arial"',
        border="2px solid #000000",
        extra_css=_EDITABLE_CSS,
    )

    # -----------------------------------------------------------------------
    # Government emblem
    # -----------------------------------------------------------------------
    doc.add(
        AbsoluteBox(
            Text(
                "Coat of Arms\nof Nepal",
                style=Style(
                    font_size="13px",
                    text_align="center",
                    line_height="1.2",
                ),
            ),
            style=Style(
                width="135px",
                height="135px",
                border="2px solid #000000",
                display="flex",
                align_items="center",
                justify_content="center",
                text_align="center",
            ),
            left="70px",
            top="48px",
        )
    )

    # -----------------------------------------------------------------------
    # Header
    # -----------------------------------------------------------------------
    doc.add(
        AbsoluteBox(
            FlexCol(
                Heading(
                    "Government of Nepal",
                    level=1,
                    style=Style(
                        margin="0",
                        font_size="28px",
                        font_weight="bold",
                    ),
                ),
                Heading(
                    "Ministry of Home Affairs",
                    level=2,
                    style=Style(
                        margin="0",
                        font_size="28px",
                        font_weight="bold",
                    ),
                ),
                Heading(
                    f"District Administration Office, {d['district_admin_location']}",
                    level=3,
                    style=Style(
                        margin="0",
                        font_size="28px",
                        font_weight="bold",
                    ),
                    attrs=_ea("district_admin_location"),
                ),
                Heading(
                    "Certificate of Nepali Citizenship",
                    level=4,
                    style=Style(
                        margin="3px 0 0 0",
                        font_size="27px",
                        font_weight="bold",
                    ),
                ),
                gap="1px",
                style=Style(
                    text_align="center",
                    line_height="1.35",
                ),
            ),
            top="25px",
            left="285px",
            style=Style(width="700px"),
        )
    )

    # -----------------------------------------------------------------------
    # Round office seal
    # -----------------------------------------------------------------------
    doc.add(
        AbsoluteBox(
            Text(
                "Office\nSeal",
                style=Style(
                    font_size="13px",
                    text_align="center",
                    line_height="1.2",
                ),
            ),
            style=Style(
                width="125px",
                height="125px",
                border="2px solid #000000",
                border_radius="50%",
                display="flex",
                align_items="center",
                justify_content="center",
                text_align="center",
            ),
            right="55px",
            top="35px",
        )
    )

    # -----------------------------------------------------------------------
    # Citizenship number / document number
    # -----------------------------------------------------------------------
    doc.add(
        AbsoluteBox(
            FlexCol(
                Text(
                    f"{d['citizenship_no']}",
                    style=Style(
                        font_size="21px",
                        font_weight="bold",
                    ),
                    attrs=_ea("citizenship_no"),
                ),
                Text(
                    "Citizenship No.",
                    style=Style(
                        font_size="18px",
                        font_weight="bold",
                    ),
                ),
                gap="0px",
            ),
            left="42px",
            top="205px",
            style=Style(width="240px"),
        )
    )

    # -----------------------------------------------------------------------
    # Photograph
    # -----------------------------------------------------------------------
    doc.add(
        AbsoluteBox(
            Text(
                # The original is signed across the photograph, so the caption
                # carries the "(Sd.)" marker the scan shows.
                "Photograph(Sd.)",
                style=Style(
                    font_size="16px",
                    font_weight="bold",
                    text_align="center",
                ),
            ),
            style=Style(
                width="255px",
                height="300px",
                border="2px solid #000000",
                display="flex",
                align_items="center",
                justify_content="center",
                text_align="center",
            ),
            left="52px",
            top="310px",
        )
    )

    # -----------------------------------------------------------------------
    # Main information section
    #
    # The old certificate is much more compact than the newer format.
    # The information begins immediately below the certificate title and
    # occupies the right-hand ~70% of the page.
    # -----------------------------------------------------------------------
    data_section = FieldGroup(
        # Full Name / Gender
        multi_row(
            field_row(
                "Full Name:",
                d["full_name"],
                field_name="full_name",
            ),
            field_row(
                "Gender:",
                d["gender"],
                label_style=RIGHT_LABEL,
                field_name="gender",
            ),
            style=ROW_STYLE,
        ),

        # Birth Place - District
        multi_row(
            LabelValue(
                "Birth Place, District:",
                d["birth_district"],
                label_style=LABEL_STYLE,
                value_style=VALUE_STYLE,
                value_attrs=_ea("birth_district"),
            ),
            style=ROW_STYLE,
        ),

        # Birth Place - Local Administrative Unit + Ward
        multi_row(
            LabelValue(
                "VDC/Municipality:",
                d["birth_municipality"],
                label_style=LABEL_STYLE,
                value_style=VALUE_STYLE,
                value_attrs=_ea("birth_municipality"),
            ),
            field_row(
                "Ward No.:",
                d["birth_ward"],
                label_style=RIGHT_LABEL,
                field_name="birth_ward",
            ),
            style=ROW_STYLE,
        ),

        # Permanent Address - District.
        #
        # Unlike every other row this one is a bare label-value pair rather
        # than a MultiFieldRow: the original prints "Permanent Address:
        # District:" as a single unbroken caption, so the row has nothing to
        # sit beside it and the extra flex wrapper would only add nesting.
        LabelValue(
            "Permanent Address: District:",
            d["perm_district"],
            label_style=NOWRAP_LABEL,
            value_style=NOWRAP_VALUE,
            value_attrs=_ea("perm_district"),
            style=ROW_STYLE,
        ),

        # Permanent Address - Local Administrative Unit + Ward
        multi_row(
            LabelValue(
                "VDC/Municipality:",
                d["perm_municipality"],
                label_style=LABEL_STYLE,
                value_style=VALUE_STYLE,
                value_attrs=_ea("perm_municipality"),
            ),
            field_row(
                "Ward No.:",
                d["perm_ward"],
                label_style=RIGHT_LABEL,
                field_name="perm_ward",
            ),
            style=ROW_STYLE,
        ),

        # Date of Birth
        multi_row(
            LabelValue(
                "Date of Birth:",
                FlexRow(
                    Text(
                        f"{d['dob_year']}",
                        style=Style(font_size="20px", flex="1"),
                        attrs=_ea("dob_year"),
                    ),
                    Text(
                        "Year",
                        style=Style(font_size="20px", width="45px"),
                    ),
                    Text(
                        f"{d['dob_month']}",
                        style=Style(font_size="20px", width="55px"),
                        attrs=_ea("dob_month"),
                    ),
                    Text(
                        "Month",
                        style=Style(font_size="20px", width="65px"),
                    ),
                    Text(
                        f"{d['dob_day']}",
                        style=Style(font_size="20px", width="55px"),
                        attrs=_ea("dob_day"),
                    ),
                    Text(
                        "Day",
                        style=Style(font_size="20px", width="45px"),
                    ),
                    gap="7px",
                ),
                label_style=LABEL_STYLE,
                value_style=VALUE_STYLE,
            ),
            style=ROW_STYLE,
        ),

        # Father's Full Name
        multi_row(
            field_row(
                "Father's Full Name:",
                d["father_name"],
                field_name="father_name",
            ),
            style=ROW_STYLE,
        ),

        # Father's Address + Citizenship
        multi_row(
            field_row(
                "Address:",
                d["father_address"],
                field_name="father_address",
            ),
            field_row(
                "Citizenship:",
                d["father_na_ki"],
                label_style=RIGHT_LABEL,
                field_name="father_na_ki",
            ),
            style=ROW_STYLE,
        ),

        # Mother's Full Name
        multi_row(
            field_row(
                "Mother's Full Name:",
                d["mother_name"],
                field_name="mother_name",
            ),
            style=ROW_STYLE,
        ),

        # Mother's Address + Citizenship
        multi_row(
            field_row(
                "Address:",
                d["mother_address"],
                field_name="mother_address",
            ),
            field_row(
                "Citizenship:",
                d["mother_na_ki"],
                label_style=RIGHT_LABEL,
                field_name="mother_na_ki",
            ),
            style=ROW_STYLE,
        ),

        style=Style(
            font_size="20px",
            width="100%",
        ),
    )

    doc.add(
        AbsoluteBox(
            data_section,
            left="350px",
            top="205px",
            style=Style(width="810px"),
        )
    )

    return doc


