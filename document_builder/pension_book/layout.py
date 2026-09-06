"""Translated layout for the Police Kitabkhana pension book spread."""

from __future__ import annotations

from typing import Any

from html_engine import AbsoluteBox, Div, Document, FlexCol, FlexRow, PlaceholderBox, Style, Text


PAGE_WIDTH = "1352px"
PAGE_HEIGHT = "897px"

_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

FIELDS = (
    "identity_book_no",
    "left_office_or_holder_name",
    "right_office_or_holder_name",
    "photo_description",
    "record_keeper_signature",
    "right_thumbprint",
    "left_thumbprint",
    "issuing_officer_signature",
    "issuing_officer_name",
    "issuing_officer_rank",
    "issuing_office",
    "pension_payment_order_no",
    "pension_payment_branch",
    "payment_order_text",
    "payment_order_officer_name",
    "payment_order_officer_rank",
    "payment_order_office",
    "payment_order_date_bs",
    "authority_serial_no",
    "deceased_employee_name",
    "deceased_employee_symbol_no",
    "deceased_employee_permanent_address_district",
    "deceased_employee_permanent_address_municipality",
    "deceased_employee_permanent_address_ward",
    "deceased_employee_birth_date_bs",
    "deceased_employee_post",
    "deceased_employee_class",
    "deceased_employee_office",
    "deceased_employee_death_date_bs",
    "service_period_years",
    "service_period_months",
    "service_period_days",
    "deceased_employee_last_salary",
    "family_pension_recipient_name",
    "family_pension_recipient_birth_date_bs",
    "family_pension_recipient_permanent_address_district",
    "family_pension_recipient_permanent_address_municipality",
    "family_pension_recipient_permanent_address_ward",
    "family_pension_recipient_relationship",
    "family_pension_start_date_bs",
    "family_pension_end_date_bs",
    "family_pension_monthly_amount",
    "other_required_information",
)


def _safe_data(data: dict[str, Any] | None) -> dict[str, str]:
    values = {field: "" for field in FIELDS}
    values.update(data or {})
    return {field: "" if values[field] is None else str(values[field]) for field in FIELDS}


def _line_value(value: str, field: str, *, width: str = "180px", size: str = "18px") -> Div:
    return Div(
        Text(value, field=field, style=Style(font_size=size, line_height="1.18")),
        style=Style(
            width=width,
            min_height="22px",
            border_bottom="1px solid #000000",
            display="inline-block",
            vertical_align="bottom",
            padding_left="4px",
            box_sizing="border-box",
            overflow_wrap="anywhere",
        ),
    )


def _label_line(label: str, value: str, field: str, *, label_width: str = "132px", value_width: str = "245px") -> FlexRow:
    return FlexRow(
        Text(label, style=Style(font_size="19px", font_weight="bold", width=label_width, flex_shrink="0")),
        _line_value(value, field, width=value_width),
        style=Style(align_items="flex-end"),
    )


def _section_title(text: str) -> Text:
    return Text(text, style=Style(font_size="23px", font_weight="bold", text_decoration="underline"))


def _right_detail_row(label: str, value: str, field: str, *, indent: str = "0px") -> FlexRow:
    return FlexRow(
        Text(label, style=Style(font_size="20px", width="252px", padding_left=indent, box_sizing="border-box")),
        _line_value(value, field, width="250px", size="18px"),
        style=Style(align_items="flex-end"),
    )


def _address_row(
    prefix: str,
    district: str,
    district_field: str,
    municipality: str,
    municipality_field: str,
    ward: str,
    ward_field: str,
    *,
    y_gap: str = "0px",
) -> FlexCol:
    return FlexCol(
        FlexRow(
            Text(prefix, style=Style(font_size="20px", width="255px")),
            Text("District", style=Style(font_size="20px", width="88px")),
            _line_value(district, district_field, width="158px", size="18px"),
            style=Style(align_items="flex-end"),
        ),
        FlexRow(
            Text("Municipality/VDC", style=Style(font_size="20px", width="255px")),
            _line_value(municipality, municipality_field, width="158px", size="18px"),
            Text("Ward No.", style=Style(font_size="20px", width="102px", padding_left="26px", box_sizing="border-box")),
            _line_value(ward, ward_field, width="64px", size="18px"),
            style=Style(align_items="flex-end"),
        ),
        gap=y_gap,
    )


def _page_frame(left: str) -> AbsoluteBox:
    return AbsoluteBox(
        Div(
            style=Style(
                width="560px",
                height="788px",
                border="2px solid #000000",
                box_sizing="border-box",
            )
        ),
        left=left,
        top="38px",
    )


def _left_page(d: dict[str, str]) -> list[AbsoluteBox]:
    return [
        _page_frame("42px"),
        AbsoluteBox(
            FlexCol(
                Text("Election Registration Book", style=Style(font_size="26px", font_weight="bold", text_align="center")),
                Text("Police Kitabkhana", style=Style(font_size="17px", text_align="center")),
                gap="4px",
                style=Style(align_items="center", line_height="1.05"),
            ),
            left="172px",
            top="54px",
            style=Style(width="315px"),
        ),
        AbsoluteBox(_label_line("Verified by", d["left_office_or_holder_name"], "left_office_or_holder_name", label_width="118px", value_width="238px"), left="228px", top="106px"),
        AbsoluteBox(_label_line("Record keeper", d["right_office_or_holder_name"], "right_office_or_holder_name", label_width="142px", value_width="170px"), left="270px", top="135px"),
        AbsoluteBox(Text("Photo", style=Style(font_size="21px", font_weight="bold")), left="70px", top="138px"),
        AbsoluteBox(
            PlaceholderBox(d["photo_description"] or "Photograph", width="176px", height="233px", font_size="18px"),
            left="55px",
            top="184px",
        ),
        AbsoluteBox(Text("Right", style=Style(font_size="18px", font_weight="bold")), left="393px", top="158px"),
        AbsoluteBox(Text("Left", style=Style(font_size="18px", font_weight="bold")), left="517px", top="158px"),
        AbsoluteBox(
            PlaceholderBox(d["right_thumbprint"] or "Right\nthumbprint", width="114px", height="146px", font_size="15px"),
            left="352px",
            top="183px",
        ),
        AbsoluteBox(
            PlaceholderBox(d["left_thumbprint"] or "Left\nthumbprint", width="114px", height="146px", font_size="15px"),
            left="472px",
            top="183px",
        ),
        AbsoluteBox(_line_value(d["record_keeper_signature"], "record_keeper_signature", width="206px", size="17px"), left="244px", top="342px"),
        AbsoluteBox(Text("Record keeper", style=Style(font_size="18px", font_weight="bold")), left="236px", top="327px"),
        AbsoluteBox(
            FlexCol(
                Text("Authority letter issuing officer", style=Style(font_size="18px", font_weight="bold")),
                _label_line("Signature", d["issuing_officer_signature"], "issuing_officer_signature", label_width="84px", value_width="210px"),
                _label_line("Name", d["issuing_officer_name"], "issuing_officer_name", label_width="84px", value_width="210px"),
                _label_line("Rank", d["issuing_officer_rank"], "issuing_officer_rank", label_width="84px", value_width="210px"),
                gap="4px",
            ),
            left="314px",
            top="421px",
            style=Style(width="300px"),
        ),
        AbsoluteBox(Text("Police Kitabkhana", style=Style(font_size="20px", font_weight="bold")), left="437px", top="548px"),
        AbsoluteBox(
            Text("This authority letter entitles pension payment at the rate approved for the retired/deceased employee.", style=Style(font_size="18px", font_weight="bold", line_height="1.28")),
            left="63px",
            top="581px",
            style=Style(width="520px"),
        ),
        AbsoluteBox(_label_line("Branch", d["pension_payment_branch"], "pension_payment_branch", label_width="72px", value_width="240px"), left="142px", top="633px"),
        AbsoluteBox(_label_line("P.P.O. No.", d["pension_payment_order_no"], "pension_payment_order_no", label_width="98px", value_width="158px"), left="64px", top="605px"),
        AbsoluteBox(
            FlexCol(
                Text("Payment order issuing officer:", style=Style(font_size="19px", font_weight="bold")),
                _label_line("Name", d["payment_order_officer_name"], "payment_order_officer_name", label_width="84px", value_width="235px"),
                _label_line("Rank", d["payment_order_officer_rank"], "payment_order_officer_rank", label_width="84px", value_width="235px"),
                _label_line("Office", d["payment_order_office"], "payment_order_office", label_width="84px", value_width="235px"),
                _label_line("Date", d["payment_order_date_bs"], "payment_order_date_bs", label_width="84px", value_width="235px"),
                gap="5px",
            ),
            left="203px",
            top="676px",
            style=Style(width="365px"),
        ),
    ]


def _right_page(d: dict[str, str]) -> list[AbsoluteBox]:
    return [
        _page_frame("769px"),
        AbsoluteBox(
            FlexCol(
                Text("Family Pension Authority Letter", style=Style(font_size="26px", font_weight="bold", text_align="center")),
                Text("Authority letter serial number", style=Style(font_size="20px", font_weight="bold", text_align="center")),
                _line_value(d["authority_serial_no"], "authority_serial_no", width="255px", size="18px"),
                gap="3px",
                style=Style(align_items="center", line_height="1.05"),
            ),
            left="855px",
            top="57px",
            style=Style(width="370px"),
        ),
        AbsoluteBox(_section_title("(a) Details of deceased employee"), left="782px", top="130px"),
        AbsoluteBox(_right_detail_row("1. Name", d["deceased_employee_name"], "deceased_employee_name"), left="783px", top="165px"),
        AbsoluteBox(_right_detail_row("Symbol No.", d["deceased_employee_symbol_no"], "deceased_employee_symbol_no"), left="1098px", top="165px"),
        AbsoluteBox(_address_row("2. Permanent address", d["deceased_employee_permanent_address_district"], "deceased_employee_permanent_address_district", d["deceased_employee_permanent_address_municipality"], "deceased_employee_permanent_address_municipality", d["deceased_employee_permanent_address_ward"], "deceased_employee_permanent_address_ward"), left="783px", top="198px"),
        AbsoluteBox(_right_detail_row("3. Birth date", d["deceased_employee_birth_date_bs"], "deceased_employee_birth_date_bs"), left="783px", top="262px"),
        AbsoluteBox(_right_detail_row("4. Post", d["deceased_employee_post"], "deceased_employee_post"), left="783px", top="296px"),
        AbsoluteBox(_right_detail_row("5. Class", d["deceased_employee_class"], "deceased_employee_class"), left="783px", top="330px"),
        AbsoluteBox(_right_detail_row("6. Office", d["deceased_employee_office"], "deceased_employee_office"), left="783px", top="364px"),
        AbsoluteBox(_right_detail_row("7. Death date", d["deceased_employee_death_date_bs"], "deceased_employee_death_date_bs"), left="783px", top="399px"),
        AbsoluteBox(
            FlexRow(
                Text("8. Service period", style=Style(font_size="20px", width="196px")),
                Text("Years", style=Style(font_size="19px", width="56px")),
                _line_value(d["service_period_years"], "service_period_years", width="65px", size="18px"),
                Text("Months", style=Style(font_size="19px", width="75px", padding_left="16px", box_sizing="border-box")),
                _line_value(d["service_period_months"], "service_period_months", width="65px", size="18px"),
                Text("Days", style=Style(font_size="19px", width="58px", padding_left="16px", box_sizing="border-box")),
                _line_value(d["service_period_days"], "service_period_days", width="58px", size="18px"),
                style=Style(align_items="flex-end"),
            ),
            left="783px",
            top="433px",
        ),
        AbsoluteBox(_right_detail_row("9. Last salary", d["deceased_employee_last_salary"], "deceased_employee_last_salary"), left="783px", top="468px"),
        AbsoluteBox(_section_title("(b) Details of family pension recipient"), left="782px", top="499px"),
        AbsoluteBox(_right_detail_row("1. Name", d["family_pension_recipient_name"], "family_pension_recipient_name"), left="783px", top="533px"),
        AbsoluteBox(_right_detail_row("2. Birth date", d["family_pension_recipient_birth_date_bs"], "family_pension_recipient_birth_date_bs"), left="783px", top="568px"),
        AbsoluteBox(_address_row("3. Permanent address", d["family_pension_recipient_permanent_address_district"], "family_pension_recipient_permanent_address_district", d["family_pension_recipient_permanent_address_municipality"], "family_pension_recipient_permanent_address_municipality", d["family_pension_recipient_permanent_address_ward"], "family_pension_recipient_permanent_address_ward"), left="783px", top="603px"),
        AbsoluteBox(_right_detail_row("4. Relationship", d["family_pension_recipient_relationship"], "family_pension_recipient_relationship"), left="783px", top="668px"),
        AbsoluteBox(_section_title("(c) Pension period and amount"), left="782px", top="704px"),
        AbsoluteBox(
            FlexRow(
                Text("1. From", style=Style(font_size="20px", width="90px")),
                _line_value(d["family_pension_start_date_bs"], "family_pension_start_date_bs", width="160px", size="18px"),
                Text("To", style=Style(font_size="20px", width="55px", padding_left="20px", box_sizing="border-box")),
                _line_value(d["family_pension_end_date_bs"], "family_pension_end_date_bs", width="160px", size="18px"),
                style=Style(align_items="flex-end"),
            ),
            left="783px",
            top="738px",
        ),
        AbsoluteBox(_right_detail_row("2. Monthly pension amount", d["family_pension_monthly_amount"], "family_pension_monthly_amount"), left="783px", top="772px"),
        AbsoluteBox(_section_title("(d) Other required information"), left="782px", top="807px"),
        AbsoluteBox(_line_value(d["other_required_information"], "other_required_information", width="405px", size="18px"), left="942px", top="807px"),
    ]


def build_pension_book(data: dict[str, Any]) -> Document:
    d = _safe_data(data)

    doc = Document(
        "Pension Book",
        page_width=PAGE_WIDTH,
        page_height=PAGE_HEIGHT,
        background="#ffffff",
        font_family='"Noto Sans Devanagari", "Times New Roman", serif',
        border="1px solid #000000",
        page_style=Style(
            width=PAGE_WIDTH,
            height=PAGE_HEIGHT,
            padding="0px",
            margin="0px",
            position="relative",
            overflow="hidden",
            box_sizing="border-box",
        ),
        extra_css=_EDITABLE_CSS,
        lang="en",
    )

    doc.add(
        AbsoluteBox(
            Div(style=Style(width="2px", height="897px", background="#000000")),
            left="675px",
            top="0px",
        ),
        AbsoluteBox(
            Text("Police Kitabkhana", style=Style(font_size="14px", color="#000000", opacity="0.16")),
            left="12px",
            top="8px",
        ),
        AbsoluteBox(
            Text("Police Kitabkhana", style=Style(font_size="14px", color="#000000", opacity="0.16")),
            left="742px",
            top="8px",
        ),
    )

    for box in _left_page(d):
        doc.add(box)
    for box in _right_page(d):
        doc.add(box)

    doc.add(
        AbsoluteBox(Text("2", style=Style(font_size="18px", font_weight="bold")), left="352px", bottom="42px"),
        AbsoluteBox(Text("3", style=Style(font_size="18px", font_weight="bold")), left="1034px", bottom="42px"),
    )

    return doc
