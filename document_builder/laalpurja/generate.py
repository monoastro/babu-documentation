#!/usr/bin/env python3
"""
Generate the Land Ownership Registration Certificate (Laal Purja) HTML and PDF.

Fills in sample data (representing realistic land plot details) and
writes the rendered outputs to the output directory.

Usage::

    python documents/laalpurja/generate.py
"""

from __future__ import annotations

import os
from pathlib import Path
import sys

# Ensure project root is on the import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from documents.laalpurja.layout import build_laalpurja


def main() -> None:
    # ── Sample data matching the reference image / realistic details ──
    data = {
        "certificate_no": "LP-884920B",
        "district": "Lalitpur",
        "vdc_muc": "Godawari Municipality",
        "ward_no": "5",
        "owner_name": "Ram Bahadur Thapa",
        "owner_address": "Godawari Ward No. 5, Lalitpur, Nepal",
        "grandfather_name": "Hari Bahadur Thapa",
        "father_name": "Krishna Bahadur Thapa",
        "spouse_name": "Sita Devi Thapa",
        "citizenship_no": "27-01-72-03941",
        "photo_src": "owner_photo.png",
        "emblem_src": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Emblem_of_Nepal.svg/1200px-Emblem_of_Nepal.svg.png",
        "issue_date": "2080-04-12",
        "issue_office": "Lalitpur Land Revenue Office",
        "signatory_name": "Madhav Prasad Bhattarai",
        "signatory_title": "Land Revenue Officer",
        "plots": [
            {
                "plot_id": "1",
                "district": "Lalitpur",
                "vdc_muc": "Godawari",
                "ward_no": "5",
                "sheet_no": "2-Kha",
                "plot_no": "1042",
                "ropani": 1,
                "aana": 4,
                "paisa": 2,
                "daam": 1,
                "metric_area": "642.50",
                "class_nepali": "खेत (Khet)",
                "class_english": "Wet Land",
                "grade_nepali": "अब्बल (Abal)",
                "grade_english": "Grade A",
                "remarks": "Registered",
            },
            {
                "plot_id": "2",
                "district": "Lalitpur",
                "vdc_muc": "Godawari",
                "ward_no": "5",
                "sheet_no": "2-Kha",
                "plot_no": "1043",
                "ropani": 0,
                "aana": 8,
                "paisa": 1,
                "daam": 3,
                "metric_area": "260.40",
                "class_nepali": "पाखो (Pakho)",
                "class_english": "Dry Land",
                "grade_nepali": "दोयम (Doyam)",
                "grade_english": "Grade B",
                "remarks": "Registered",
            },
            {
                "plot_id": "3",
                "district": "Lalitpur",
                "vdc_muc": "Godawari",
                "ward_no": "5",
                "sheet_no": "3-Ga",
                "plot_no": "412",
                "ropani": 2,
                "aana": 0,
                "paisa": 0,
                "daam": 0,
                "metric_area": "1017.44",
                "class_nepali": "खेत (Khet)",
                "class_english": "Wet Land",
                "grade_nepali": "अब्बल (Abal)",
                "grade_english": "Grade A",
                "remarks": "Registered",
            },

            {
                "plot_id": "4",
                "district": "Lalitpur",
                "vdc_muc": "Godawari",
                "ward_no": "5",
                "sheet_no": "3-Ga",
                "plot_no": "412",
                "ropani": 2,
                "aana": 0,
                "paisa": 0,
                "daam": 0,
                "metric_area": "1017.44",
                "class_nepali": "खेत (Khet)",
                "class_english": "Wet Land",
                "grade_nepali": "अब्बल (Abal)",
                "grade_english": "Grade A",
                "remarks": "Registered",
            },
        ],
    }

    # Create layout definition Document
    doc = build_laalpurja(data)

    # Establish output directory
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    html_output_path = output_dir / "laalpurja.html"
    pdf_output_path = output_dir / "laalpurja.pdf"

    # Save to HTML
    doc.save(str(html_output_path))
    print(f"Generated HTML: {html_output_path.resolve()}")

    # Try saving to PDF (weasyprint is optional)
    try:
        doc.to_pdf(str(pdf_output_path))
        print(f"Generated PDF: {pdf_output_path.resolve()}")
    except ImportError as e:
        print(f"PDF generation skipped: {e}")
    except Exception as e:
        print(f"PDF generation failed due to unexpected error: {e}")


if __name__ == "__main__":
    main()
