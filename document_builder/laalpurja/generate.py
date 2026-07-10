#!/usr/bin/env python3
"""
Generate the Land Ownership Registration Certificate (Laal Purja) HTML and PDF.

Fills in sample data (representing realistic land plot details) and
writes the rendered outputs to the output directory.

Usage::

    python document_builder/laalpurja/generate.py
"""

from __future__ import annotations

import os
from pathlib import Path
import sys

# Ensure project root is on the import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from document_builder.laalpurja.layout import build_laalpurja


def main() -> None:
    # ── Sample data matching the reference image / realistic details ──
    data = {
        "certificate_no": "4915149",
        "district": "Lalitpur",
        "vdc_muc": "Lagankhel",
        "ward_no": "7",
        "owner_name": "", # Left blank as in reference image or we can set it
        "owner_address": "District: Gorkha, M.C. /V.D.C: Makaising, Ward No. 7",
        "husband_name": "Santosh Shrestha",
        "father_in_law_name": "Jit Bahadur Shrestha",
        "citizenship_no": "443015/343",
        "photo_src": "owner_photo.png",
        "emblem_src": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Emblem_of_Nepal.svg/1200px-Emblem_of_Nepal.svg.png",
        "issue_date": "2007/02/16 A.D.",
        "issue_office": "District Administration Office: Gorkha",
        "signatory_name": "(Signed)",
        "signatory_title": "Land Revenue Officer",
        "plots": [
            {
                "plot_id": "1433",
                "transaction_no": "3933",
                "transaction_date": "2013/06/10",
                "transaction_type": "Resignation",
                "district": "Lalitpur",
                "vdc_muc": "Sanagaun",
                "ward_no": "8",
                "sheet_no": "8",
                "plot_no": "1447",
                "description_1": "Residential land",
                "description_2": "Private land",
                "owner_share": "Sole ownership",
                "tenant_name": "Landowner herself",
                "class_english": "dry agricultural land",
                "grade_english": "First class",
                "ropani": 0,
                "aana": 2,
                "paisa": 2,
                "daam": 2,
                "metric_area": "83.47",
                "register_page_no": "2069",
                "register_serial_no": "3933",
                "remarks": "",
                "signature": "(Signed)",
            },
            {
                "plot_id": "1423",
                "transaction_no": "3933",
                "transaction_date": "2013/06/10",
                "transaction_type": "Resignation",
                "district": "Lalitpur",
                "vdc_muc": "Sanagaun",
                "ward_no": "8",
                "sheet_no": "8 ka",
                "plot_no": "1445",
                "description_1": "Residential land",
                "description_2": "Private land",
                "owner_share": "Full ownership",
                "tenant_name": "Landowner herself",
                "class_english": "irrigated agricultural land",
                "grade_english": "First class",
                "ropani": 0,
                "aana": 0,
                "paisa": 0,
                "daam": 2,
                "metric_area": "3.97",
                "register_page_no": "2069",
                "register_serial_no": "3933",
                "remarks": "",
                "signature": "(Signed)",
            },
            {
                "plot_id": "1431",
                "transaction_no": "3933",
                "transaction_date": "2013/06/10",
                "transaction_type": "Resignation",
                "district": "Lalitpur",
                "vdc_muc": "Sanagaun",
                "ward_no": "8",
                "sheet_no": "8 ka",
                "plot_no": "1431",
                "description_1": "Residential land",
                "description_2": "Private land",
                "owner_share": "Sole ownership",
                "tenant_name": "Landowner herself",
                "class_english": "dry agricultural land",
                "grade_english": "First class",
                "ropani": 0,
                "aana": 0,
                "paisa": 2,
                "daam": 0,
                "metric_area": "15.90",
                "register_page_no": "2069",
                "register_serial_no": "3933",
                "remarks": "",
                "signature": "(Signed)",
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
