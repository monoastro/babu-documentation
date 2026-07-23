"""
Laalpurja generator — builds the Land Ownership Registration Certificate.
Run from the project root:
    python document_builder/laalpurja/generate.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from document_builder.laalpurja.layout import build_laalpurja


def main() -> None:
    data = {
        "certificate_no": "4915149",
        "office_vdc": "Lagankhel",
        "office_district": "Lalitpur",
        "owner_name": "",
        "owner_district": "Gorkha",
        "owner_vdc": "Makaising",
        "owner_ward": "7",
        "husband_name": "Santosh Shrestha",
        "father_in_law": "Jit Bahadur Shrestha",
        "citizenship_no": "443015/343",
        "issue_date": "2007/02/16 A.D.",
        "issue_office": "District Administration Office: Gorkha",
        "doc_id": "103mm002",
        "print_date": "2013/06/10",
        "plots": [
            {
                "plot_no":          "1433",
                "evd_no":           "3933",
                "evd_date":         "2013/06/10",
                "transaction_type": "Resignation",
                "vdc":              "Sanagaun",
                "ward_top":         "8",
                "ward_bottom":      "8",
                "plot_section":     "1447",
                "desc_top":         "Residential land",
                "desc_bottom":      "Private land",
                "owner_share":      "Sole\nownership",
                "tenant":           "Landowner\nherself",
                "kind_top":         "First class\ndry\nagricultural\nland",
                "area_local":       "0-2-2-2",
                "area_sqm":         "83.47",
                "register_page":    "2069",
                "register_serial":  "3933",
                "remark":           "",
                "signature":        "(Signed)",
            },
            {
                "plot_no":          "1423",
                "evd_no":           "3933",
                "evd_date":         "2013/06/10",
                "transaction_type": "Resignation",
                "vdc":              "Sanagun",
                "ward_top":         "8",
                "ward_bottom":      "8 ka",
                "plot_section":     "1445",
                "desc_top":         "Residential land",
                "desc_bottom":      "Private land",
                "owner_share":      "Full\nownership",
                "tenant":           "Landowner\nherself",
                "kind_top":         "First class\nirrigated\nagricultural\nland",
                "area_local":       "0-0-0-2",
                "area_sqm":         "3.97",
                "register_page":    "2069",
                "register_serial":  "3933",
                "remark":           "",
                "signature":        "(Signed)",
            },
            {
                "plot_no":          "1431",
                "evd_no":           "3933",
                "evd_date":         "2013/06/10",
                "transaction_type": "Resignation",
                "vdc":              "Sanagaun",
                "ward_top":         "8",
                "ward_bottom":      "8 ka",
                "plot_section":     "1431",
                "desc_top":         "Residential land",
                "desc_bottom":      "Private land",
                "owner_share":      "Sole\nownership",
                "tenant":           "Landowner\nherself",
                "kind_top":         "First class\ndry\nagricultural\nland",
                "area_local":       "0-0-2-0",
                "area_sqm":         "15.90",
                "register_page":    "2069",
                "register_serial":  "3933",
                "remark":           "",
                "signature":        "(Signed)",
            },

        ],
    }

    doc = build_laalpurja(data)

    output_dir = Path(__file__).parent
    output_dir.mkdir(exist_ok=True)

    html_path = "laalpurja.html"
    pdf_path  = "laalpurja.pdf"

    doc.save(str(html_path))
    print(f"Generated HTML: {html_path.resolve()}")

    try:
        doc.to_pdf(str(pdf_path))
        print(f"Generated PDF:  {pdf_path.resolve()}")
    except ImportError as e:
        print(f"PDF skipped: {e}")
    except Exception as e:
        print(f"PDF failed: {e}")


if __name__ == "__main__":
    main()
