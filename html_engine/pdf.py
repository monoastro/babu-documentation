from __future__ import annotations
from typing import Optional


def html_to_pdf(html_string: str, output_path: str, base_url: Optional[str] = None) -> None:
    try:
        import weasyprint
    except ImportError:
        raise ImportError(
            "The 'weasyprint' package is required for PDF export. "
            "Please install it using: 'pip install weasyprint'. "
        ) from None
    weasyprint.HTML(string=html_string, base_url=base_url).write_pdf(output_path)
