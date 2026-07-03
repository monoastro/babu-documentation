#!/usr/bin/env python3
"""
Generate the Nepali Citizenship Certificate HTML.

Fills in sample data from the reference citizenship document and
writes the rendered HTML to ``output/citizenship.html``.

Usage::

    python documents/citizenship/generate.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from documents.citizenship.layout import build_citizenship


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
        "dob_day": "11 (B.S.)",
        "father_name": "Punalal Jaisi",
        "father_citizenship_no": "332",
        "father_address": "Soru Rural Municipality-10, Mugu",
        "father_na_ki": "Baisakh",
        "mother_name": "Bhimadi Tulasi Jaisi",
        "mother_citizenship_no": "03115757",
        "mother_address": "Soru Rural Municipality-10, Mugu",
        "mother_na_ki": "Baisakh",
        "spouse_name": "XXX",
        "spouse_citizenship_no": "—",
        "spouse_na_ki": "",
        "photo_src": "your-photo.jpg",
        "emblem_src": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Emblem_of_Nepal.svg/1200px-Emblem_of_Nepal.svg.png",
        "district_name": "Mugu",
        "signatory_name": "K.M. Dhakal",
        "signatory_title": "Chief District Officer",
    }

    doc = build_citizenship(data)
    html = doc.render()

    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "citizenship.html"
    output_file.write_text(html, encoding="utf-8")
    print(f"Generated: {output_file.resolve()}")


if __name__ == "__main__":
    main()
