"""
  Digitally faithful layout for Nepal PAN Certificate (layout_1.py)
  """

from __future__ import annotations
from typing import Any
from html_engine import (
        Document, Text, LabelValue, FlexRow, FlexCol, Div, Spacer, Style, PlaceholderBox, SignatureBlock, UnorderedList,
        AbsoluteBox
        )

_EDITABLE_CSS = """
[contenteditable]:hover { outline: 2px dashed #000000; cursor: text; }
[contenteditable]:focus { outline: 2px solid #000000; background: #ffffff; }
"""

PAGE_WIDTH = "794px"
PAGE_HEIGHT = "1123px"

FIELDS = (
        'pan_no',
        'inland_revenue_office',
        'taxpayer_service_office',
        'vat_no',
        'excise_no',
        'registration_date_bs',
        'registration_date',
        'business_name',
        'taxpayer_type',
        'address',
        'business_nature',
        'taxpayer_signature',
        'tax_officer_signature',
        'duties',
        )

def build_pan(data: dict[str, Any]) -> Document:
    d = {key: "" for key in FIELDS}
    d.update(data or {})

    doc = Document(
            'Pan',
            page_width=PAGE_WIDTH,
            page_height=PAGE_HEIGHT,
            background="#ffffff",
            font_family='"Times New Roman", serif',
            border="2px solid #000000",
            extra_css=_EDITABLE_CSS,
            )

    # Top Emblem/Logos
    doc.add(
            AbsoluteBox(
                PlaceholderBox(
                    'Government of Nepal logo', width='90px', height='90px', shape='rect', font_size='13px'),
                left='50px', top='45px',
                )
            )
    doc.add(
            AbsoluteBox(
                PlaceholderBox(
                    'Round Office Seal', size='85px', shape='circle', font_size='12px'),
                left='655px', top='45px',
                )
            )

    # Ministry header
    doc.add(
            AbsoluteBox(
                Text(
                    'Government of Nepal\nMinistry of Finance\nInland Revenue Department',
                    style=Style(font_size='17px', font_weight='bold', line_height='1.15', text_align='center'),
                    ),
                left='180px',
                top='49px',
                style=Style(width='380px'),
                )
            )

    # Title
    doc.add(
            AbsoluteBox(
                Text(
                    'Permanent Account Number (PAN) Registration Certificate',
                    style=Style(font_size='19px', font_weight='bold', line_height='1.15', text_align='center'),
                    ),
                left='90px',
                top='140px',
                style=Style(width='614px'),
                )
            )

    # PAN Number Boxed Row
    doc.add(
            AbsoluteBox(
                FlexRow(
                    Text('PAN No.', style=Style(font_size='18px', font_weight='bold', margin_top='10px')),
                    Spacer(width='20px'),
                    Div(
                        FlexRow(*[
                            Div(Text(
                                (d['pan_no'][i] if len(d['pan_no']) > i else ''),
                                style=Style(font_size='24px', font_weight='bold', text_align='center'),
                                ), style=Style(border='2px solid #000', border_radius='2px', width='34px', height='40px',
                                               margin_right='4px', display='inline-flex', align_items='center', justify_content='center', background='#fff'))
                                for i in range(9)
                                ]),
                        )
                    ),
                left='280px',
                top='185px',
                )
            )

    # Upper form section (split into 2 columns for better spacing)
    doc.add(
            AbsoluteBox(
                FlexRow(
                    # Left fields
                    FlexCol(
                        LabelValue(label='Inland Revenue Office', value=d['inland_revenue_office'],
                                   field='inland_revenue_office', label_style=Style(font_size='13px', font_weight='bold', width='160px'),
                                   value_style=Style(font_size='16px')),
                        Spacer(height='7px'),
                        LabelValue(label='Taxpayer Service Office', value=d['taxpayer_service_office'],
                                   field='taxpayer_service_office', label_style=Style(font_size='13px', font_weight='bold', width='160px'),
                                   value_style=Style(font_size='16px')),
                        Spacer(height='7px'),
                        LabelValue(label='VAT No.', value=d['vat_no'], field='vat_no',
                                   label_style=Style(font_size='13px', font_weight='bold', width='160px'), value_style=Style(font_size='14.5px')),
                        Spacer(height='7px'),
                        LabelValue(label='Excise Duty No.', value=d['excise_no'], field='excise_no',
                                   label_style=Style(font_size='13px', font_weight='bold', width='160px'), value_style=Style(font_size='14.5px')),
                        style=Style(gap='0', flex='1'),
                        ),
                    Spacer(width='40px'),
                    # Right fields (Dates)
                    FlexCol(
                        LabelValue(label='Reg. Date (BS)', value=d['registration_date_bs'], field='registration_date_bs',
                                   label_style=Style(font_size='12px', font_weight='bold', width='110px'), value_style=Style(font_size='15px')),
                        Spacer(height='10px'),
                        LabelValue(label='Reg. Date (AD)', value=d['registration_date'], field='registration_date',
                                   label_style=Style(font_size='12px', font_weight='bold', width='110px'), value_style=Style(font_size='15px')),
                        style=Style(gap='0', width='280px'),
                        )
                    ),
                left='50px',
                top='250px',
                style=Style(width='694px'),
                )
            )

    # Business Info Center Block
    doc.add(
            AbsoluteBox(
                Text(d['business_name'], field='business_name', style=Style(font_size='19px', font_weight='bold',
                                                                            margin_bottom='4px')),
                left='75px',
                top='370px',
                style=Style(width='650px'),
                )
            )
    doc.add(
            AbsoluteBox(
                LabelValue(label='Type', value=d['taxpayer_type'], field='taxpayer_type',
                           label_style=Style(font_size='15px', font_weight='bold', width='150px'), value_style=Style(font_size='15px')),
                left='75px',
                top='405px',
                style=Style(width='500px'),
                )
            )
    doc.add(
            AbsoluteBox(
                LabelValue(label='Address', value=d['address'], field='address', label_style=Style(font_size='14px',
                                                                                                   width='150px'), value_style=Style(font_size='15px')),
                left='75px',
                top='435px',
                style=Style(width='500px'),
                )
            )
    doc.add(
            AbsoluteBox(
                LabelValue(label='Nature of Business', value=d['business_nature'], field='business_nature',
                           label_style=Style(font_size='14px', width='150px'), value_style=Style(font_size='15px')),
                left='75px',
                top='465px',
                style=Style(width='500px'),
                )
            )

    # Signature and Seal Blocks (spacing tightened relative to duties list)
    doc.add(
            AbsoluteBox(
                FlexRow(
                    # Left: Taxpayer signature + stamp
                    SignatureBlock(
                        name=d['taxpayer_signature'],
                        signature_label="(Signed)",
                        stamp_label="School Stamp",
                        name_field='taxpayer_signature',
                        align='center',
                        ),
                    # Right: Tax Officer signature + seal
                    SignatureBlock(
                        name=d['tax_officer_signature'],
                        title="Tax Officer",
                        signature_label="(Signed)",
                        stamp_label="Round Office Seal",
                        name_field='tax_officer_signature',
                        title_field=None,
                        align='center',
                        ),
                    style=Style(justify_content='space-between', width='680px')
                    ),
                left='45px',
                top='560px',
                )
            )

    # Duties (moved up from the deep bottom gap)
    doc.add(
            AbsoluteBox(
                Text('Duties to Be Followed by the Taxpayer:', style=Style(font_size='15px', font_weight='bold')),
                left='54px',
                top='730px',
                )
            )
    doc.add(
            AbsoluteBox(
                UnorderedList(*(d['duties'] or []), style=Style(font_size='13.5px', margin_left='20px', margin_top='5px', max_width='670px')),
                left='54px',
                top='760px',
                )
            )

    return doc

