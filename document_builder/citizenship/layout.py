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

LABEL_STYLE = Style(font_weight="bold", font_size="20px", width="240px", flex_shrink="0")
VALUE_STYLE = Style(font_size="20px", flex="1")
SMALL_LABEL = Style(font_weight="bold", font_size="20px", width="180px", flex_shrink="0")
RIGHT_LABEL = Style(font_weight="bold", font_size="20px", width="220px", flex_shrink="0", text_align="right", padding_right="10px")
ROW_STYLE = Style(margin_bottom="18px")

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

def multi_row(*parts: LabelValue, style: Style | None = None) -> MultiFieldRow:
    return MultiFieldRow(*parts, style=style)

def _address_block(district: str, municipality: str) -> FlexCol:
    return FlexCol( Text(f"District: {district}", style=Style(font_size="20px")), Text(f"Municipality/VDC: {municipality}", style=Style(font_size="20px")),)

def build_citizenship(data: dict[str, Any]) -> Document:
    d = {
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
        "father_citizenship_no": "",
        "father_address": "",
        "father_na_ki": "",
        "mother_name": "",
        "mother_citizenship_no": "",
        "mother_address": "",
        "mother_na_ki": "",
        "spouse_name": "",
        "spouse_citizenship_no": "",
        "spouse_na_ki": "",
        "district_admin_location": "",
    }
    d.update(data)

    doc = Document(
        "Nepali Citizenship Certificate",
        page_width="1200px",
        page_height="780px",
        background="#ffffff",
        font_family='"Times New Roman"',
        border="2px solid #000000",
    )

    doc.add(
        AbsoluteBox(
            Text("Coat of Arms of Nepal"),
            style=Style(
                width="120px",
                height="120px",
                border="2px solid #000000",
                display="flex",
                align_items="center",
                justify_content="center",
                font_size="14px",
                text_align="center",
                ),
            left="100px",
            top="40px",
        )
    )

    doc.add(
        AbsoluteBox(
            FlexCol(
                Heading( "Government of Nepal", level=1, style=Style(margin="0", font_size="28px"),),
                Heading( "Ministry of Home Affairs", level=2, style=Style(margin="0", font_size="28px"),),
                Heading( f"District Administration Office, {d['district_admin_location']}", level=3, style=Style(margin="0", font_size="28px"),),
                Heading( "Certificate of Nepali Citizenship", level=4, style=Style(margin="0", font_size="28px"),),
                style=Style(text_align="center", line_height="1.5"),
            ),
            top="25px",
            left="0",
            style=Style(width="100%"),
        )
    )

    doc.add(
        AbsoluteBox(
            Text("Round Office Seal"),
            style=Style(
                width="120px",
                height="120px",
                border="2px solid #000000",
                display="flex",
                align_items="center",
                justify_content="center",
                font_size="14px",
                text_align="center",
            ),
            right="150px",
            top="20px",
        )
    )


    doc.add( 
        AbsoluteBox(
            Text(f"Citizenship No.: {d['citizenship_no']}"), 
            style=Style(font_size="22px", font_weight="bold"),
            top="185px",
            left="55px",
    ))

    doc.add(
        AbsoluteBox(
            Text("Photograph Sd."),
            style=Style(
                width="260px",
                height="260px",
                border="2px solid #000000",
                display="flex",
                align_items="center",
                justify_content="center",
                font_size="14px",
                text_align="center",
            ),
            left="55px",
            top="300px",
        )
    )

    data_section = FieldGroup(
        multi_row(
            field_row("Full Name:", d["full_name"]),
            field_row("Gender:", d["gender"], label_style=RIGHT_LABEL),
        ),
        multi_row(
            LabelValue(
                "Birth Place:",
                _address_block(d["birth_district"], d["birth_municipality"]),
                label_style=LABEL_STYLE,
                value_style=VALUE_STYLE,
            ),
            field_row("Ward No.:", d["birth_ward"], label_style=RIGHT_LABEL),
        ),
        multi_row(
            LabelValue(
                "Permanent Address:",
                _address_block(d["perm_district"], d["perm_municipality"]),
                label_style=LABEL_STYLE,
                value_style=VALUE_STYLE,
            ),
            field_row("Ward No.:", d["perm_ward"], label_style=RIGHT_LABEL),
        ),
        multi_row(
            LabelValue(
                "Date of Birth:",
                FlexRow(
                    Text(f"Year: {d['dob_year']}", style=Style(font_size="20px")),
                    Text(f"Month: {d['dob_month']}", style=Style(font_size="20px")),
                    Text(f"Day: {d['dob_day']}", style=Style(font_size="20px")),
                    gap="20px",
                ),
                label_style=LABEL_STYLE,
                value_style=VALUE_STYLE,
            ),
        ),
        multi_row(
            field_row("Father's Name:", d["father_name"]),
            field_row("Citizenship No.:", d["father_citizenship_no"], label_style=RIGHT_LABEL),
        ),
        multi_row(
            field_row("Address:", d["father_address"]),
            field_row("Citizenship Type:", d["father_na_ki"], label_style=RIGHT_LABEL),
        ),
        multi_row(
            field_row("Mother's Name:", d["mother_name"]),
            field_row("Citizenship No.:", d["mother_citizenship_no"], label_style=RIGHT_LABEL),
        ),
        multi_row(
            field_row("Address:", d["mother_address"]),
            field_row("Citizenship Type:", d["mother_na_ki"], label_style=RIGHT_LABEL),
        ),
        multi_row(
            field_row("Spouse's Name:", d["spouse_name"]),
            field_row("Citizenship No.:", d["spouse_citizenship_no"], label_style=RIGHT_LABEL),
        ),
        multi_row(
            field_row("Address:", ""),
            field_row("Citizenship Type:", d["spouse_na_ki"], label_style=RIGHT_LABEL),
        ),
        spacing="18px",
        style=Style(font_size="20px"),
    )

    doc.add(
        AbsoluteBox( data_section, left="350px", top="240px", style=Style(width="870px"),
        )
    )
    return doc
