#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from document_builder.citizenship.layout import build_citizenship


def main() -> None:
    data = {
        "citizenship_no": "58-02-79-00253",
        "full_name": "Kamal Jaisi",
        "gender": "Male",
        "birth_district": "Mugu",
        "birth_municipality": "Soru",
        "birth_ward": "20",
        "perm_district": "Mugu",
        "perm_municipality": "Soru",
        "perm_ward": "20",
        "dob_year": "2060",
        "dob_month": "02",
        "dob_day": "11",
        "father_name": "Punalal Jaisi",
        "father_citizenship_no": "332",
        "father_address": "Soru Rural Municipality-10, Mugu",
        "father_na_ki": "Lineage",
        "mother_name": "Bhimadi Tulasi Jaisi",
        "mother_citizenship_no": "03115757",
        "mother_address": "Soru Rural Municipality-10, Mugu",
        "mother_na_ki": "Lineage",
        "spouse_name": "XXX",
        "spouse_citizenship_no": "",
        "spouse_na_ki": "",
        "district_admin_location": "Mugu",
    }

    doc = build_citizenship(data)
    html = doc.render()
    output_dir = Path(__file__).parent
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "test-citizenship.html"
    output_file.write_text(html, encoding="utf-8")
    print(f"Generated: {output_file.resolve()}")

if __name__ == "__main__":
    main()
