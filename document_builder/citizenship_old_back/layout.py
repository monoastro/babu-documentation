from __future__ import annotations

from typing import Any

from html_engine import (
    Document,
    Style,
    Text,
    LabelValue,
    AbsoluteBox,
    MultiFieldRow,
    Div,
)


# ---------------------------------------------------------------------------
# Styles
#
# The reverse of the old certificate is a plain two-column sheet: spouse and
# holder details across the top, thumb impressions bottom-left, the issuing
# officer bottom-right. Every row is a fixed-width label beside a fixed-width
# value, so the label never reflows when a value runs long.
# ---------------------------------------------------------------------------

LABEL_STYLE = Style(
    font_size="20px",
    font_weight="bold",
    line_height="1.2",
    flex_shrink="0",
)

# `flex: 0 1 auto` is CSS's own default. It is spelled out because LabelValue
# gives its value `flex: 1`, and a flex-basis of 0 would override the explicit
# width every row on this page depends on.
VALUE_STYLE = Style(
    font_size="20px",
    line_height="1.2",
    flex="0 1 auto",
)

BOLD_LINE = Style(
    font_size="20px",
    font_weight="bold",
    line_height="1.2",
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
"""


def _value(width: str, **extra: str) -> Style:
    """The shared value style at a specific column width."""
    return VALUE_STYLE.clone(width=width, **extra)


def _row(
    label: str,
    value: str,
    field: str,
    label_width: str,
    value_width: str,
    margin_bottom: str | None = None,
    min_height: str | None = None,
) -> LabelValue:
    """One label–value row of the reverse sheet."""
    value_style = (
        _value(value_width, min_height=min_height)
        if min_height
        else _value(value_width)
    )

    return LabelValue(
        label,
        value,
        label_style=LABEL_STYLE,
        label_width=label_width,
        value_style=value_style,
        field=field,
        style=Style(margin_bottom=margin_bottom) if margin_bottom else None,
    )


def _thumb_box(
    impression: str,
    field: str,
    shared_border: bool = False,
) -> Div:
    """One thumb-impression box, captioned along its bottom edge.

    The two boxes butt against each other on the original and share the middle
    rule, so the right-hand one drops its own left border.
    """
    box_style = Style(
        width="235px",
        height="270px",
        border="2px solid #000000",
        box_sizing="border-box",
        position="relative",
    )
    if shared_border:
        box_style = box_style.clone(border_left="0")

    return Div(
        Div(
            impression,
            style=Style(
                width="100%",
                text_align="center",
                font_size="18px",
                position="absolute",
                bottom="18px",
                left="0",
            ),
            field=field,
        ),
        style=box_style,
    )


def build_citizenship_old_back(data: dict[str, Any]) -> Document:
    """
    Build the English reproduction of the back of the old-format Nepali
    Citizenship Certificate.

    The reverse carries only what the front had no room for: the spouse's
    details, the holder's name and citizenship type, the two thumb
    impressions, and the officer who issued the certificate. Everything about
    the holder themself — name, birth, addresses, parents — is on the front,
    so none of it is repeated here.
    """

    d: dict[str, Any] = {
        # Spouse
        "spouse_full_name": "",
        "spouse_address": "",
        "spouse_citizenship": "",

        # Holder
        "nepal_citizenship_act_sentence": "",
        "certificate_holder_name": "",
        "citizenship_type": "",
        "certificate_holder_signature": "",

        "right_thumb_impression": "",
        "left_thumb_impression": "",

        # Issuing officer
        "citizenship_no": "",
        "issuing_officer_signature": "",
        "issuing_officer_name": "",
        "issuing_officer_designation": "",
        "issuing_issue_date_bs": "",
    }

    d.update({k: v for k, v in data.items() if k in d})

    doc = Document(
        "Nepali Citizenship Certificate - Old Back Layout",
        page_width="1200px",
        page_height="680px",
        background="#ffffff",
        font_family='"Noto Sans Devanagari", "Noto Sans", "Arial", sans-serif',
        border="2px solid #000000",
        page_style=Style(box_sizing="border-box"),
        extra_css=_EDITABLE_CSS,
    )

    # -----------------------------------------------------------------------
    # TOP: spouse and certificate holder
    # -----------------------------------------------------------------------

    doc.add(
        AbsoluteBox(
            _row(
                "Spouse's Full Name:",
                d["spouse_full_name"],
                "spouse_full_name",
                label_width="245px",
                value_width="420px",
                margin_bottom="9px",
            ),

            # Address and citizenship share a line on the original.
            MultiFieldRow(
                _row(
                    "Address:",
                    d["spouse_address"],
                    "spouse_address",
                    label_width="245px",
                    value_width="420px",
                ),
                _row(
                    "Citizenship:",
                    d["spouse_citizenship"],
                    "spouse_citizenship",
                    label_width="150px",
                    value_width="160px",
                ),
                style=Style(margin_bottom="10px"),
            ),

            # A block element, not a span: the statement earns its own line and
            # the gap below it comes from that margin.
            Div(
                d["nepal_citizenship_act_sentence"],
                style=BOLD_LINE.clone(margin_bottom="9px"),
                field="nepal_citizenship_act_sentence",
            ),

            _row(
                "Certificate Holder's Name:",
                d["certificate_holder_name"],
                "certificate_holder_name",
                label_width="390px",
                value_width="600px",
                margin_bottom="8px",
            ),
            _row(
                "Type of Citizenship:",
                d["citizenship_type"],
                "citizenship_type",
                label_width="390px",
                value_width="600px",
                margin_bottom="8px",
            ),
            _row(
                "Certificate Holder's Signature:",
                d["certificate_holder_signature"],
                "certificate_holder_signature",
                label_width="390px",
                value_width="600px",
                min_height="24px",
            ),

            top="38px",
            left="62px",
            style=Style(
                width="1080px",
                font_size="20px",
                line_height="1.2",
            ),
        )
    )

    # -----------------------------------------------------------------------
    # LOWER LEFT: thumb impressions
    # -----------------------------------------------------------------------

    doc.add(
        AbsoluteBox(
            Text("Thumb impressions"),
            top="245px",
            left="62px",
            style=Style(
                width="470px",
                font_size="20px",
                font_weight="bold",
                line_height="1.2",
                text_align="center",
            ),
        )
    )

    doc.add(
        AbsoluteBox(
            Div("Right", style=Style(width="235px")),
            Div("Left", style=Style(width="235px")),
            top="268px",
            left="62px",
            style=Style(
                width="470px",
                height="24px",
                font_size="20px",
                font_weight="bold",
                line_height="1.2",
                text_align="center",
                display="flex",
            ),
        )
    )

    doc.add(
        AbsoluteBox(
            _thumb_box(d["right_thumb_impression"], "right_thumb_impression"),
            _thumb_box(
                d["left_thumb_impression"],
                "left_thumb_impression",
                shared_border=True,
            ),
            top="292px",
            left="62px",
            style=Style(
                width="470px",
                height="270px",
                display="flex",
            ),
        )
    )

    # -----------------------------------------------------------------------
    # LOWER RIGHT: certificate number and issuing officer
    # -----------------------------------------------------------------------

    doc.add(
        AbsoluteBox(
            _row(
                "Certificate No.:",
                d["citizenship_no"],
                "citizenship_no",
                label_width="185px",
                value_width="300px",
                margin_bottom="12px",
            ),

            Div(
                "Officer Issuing this Certificate:",
                style=BOLD_LINE.clone(line_height=None, margin_bottom="10px"),
            ),

            _row(
                "Signature:",
                d["issuing_officer_signature"],
                "issuing_officer_signature",
                label_width="220px",
                value_width="290px",
                margin_bottom="10px",
                min_height="24px",
            ),
            _row(
                "Full Name:",
                d["issuing_officer_name"],
                "issuing_officer_name",
                label_width="220px",
                value_width="290px",
                margin_bottom="10px",
            ),
            _row(
                "Designation:",
                d["issuing_officer_designation"],
                "issuing_officer_designation",
                label_width="220px",
                value_width="290px",
                margin_bottom="10px",
            ),
            _row(
                "Issue Date (BS):",
                d["issuing_issue_date_bs"],
                "issuing_issue_date_bs",
                label_width="220px",
                value_width="290px",
            ),

            top="245px",
            left="610px",
            style=Style(
                width="525px",
                font_size="20px",
                line_height="1.25",
            ),
        )
    )

    return doc
