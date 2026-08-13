#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from document_builder.pan.layout import build_pan

def main() -> None:
    data = {
        "pan_no": "611061579",
        "registration_date_day": "26",
        "registration_date_month": "05",
        "registration_date_year": "2019",
        "tax_type": "Income Tax",
        "office_name": "Inland Revenue Office Nepalgunj",
        "taxpayer_name": "Rima Chand",
        "business_name": "Jharna Fancy",
        "taxpayer_type": "Individual",
        "address": "Ward No. 4, Buspark, Sub-Metropolitan City: Nepalgunj, Banke",
        "business_activities": "Retail trade of readymade garments, retail trade of shoes and slippers",
        "taxpayer_signature": "Riya",
        "officer_name": "Bishnu Bahadur Rawat",
        "officer_designation": "Tax Officer",
    }

    doc = build_pan(data)
    html = doc.render()
    output_dir = Path(__file__).parent
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "test-pan.html"
    output_file.write_text(html, encoding="utf-8")
    print(f"Generated: {output_file.resolve()}")

if __name__ == "__main__":
    main()
