"""
Image component for the HTML Document Engine.
"""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path
from typing import Optional

from html_engine.components.base import Component
from html_engine.styles import Style


class Image(Component):
    """
    Renders an ``<img>`` element.

    Parameters:
        src: Image source — a URL, file path, or pre-encoded data URI.
        alt: Alt text for accessibility.
        style: Inline styles (width, height, border, etc.).
        grayscale: If True, applies ``filter: grayscale(100%)``.
        embed: If True and *src* is a local file path, embeds the image
               as a base64 data URI for fully self-contained HTML.
        css_class: Optional CSS class name(s).
    """

    def __init__(
        self,
        src: str,
        *,
        alt: str = "",
        style: Optional[Style] = None,
        grayscale: bool = False,
        embed: bool = False,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class)
        self.src = src
        self.alt = alt
        self.grayscale = grayscale
        self.embed = embed

    def _resolve_src(self) -> str:
        """Resolve the image source, optionally embedding as base64."""
        if not self.embed:
            return self.src

        path = Path(self.src)
        if not path.is_file():
            # Can't embed — fall back to the original src
            return self.src

        mime, _ = mimetypes.guess_type(str(path))
        mime = mime or "application/octet-stream"
        data = path.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:{mime};base64,{b64}"

    def to_html(self) -> str:
        # Build the style, adding grayscale filter if requested
        extra = None
        if self.grayscale:
            current_filter = self.style.filter if self.style else None
            if current_filter:
                extra = Style(filter=f"grayscale(100%) {current_filter}")
            else:
                extra = Style(filter="grayscale(100%)")

        attrs = self._build_attrs(extra_style=extra)
        src = self._resolve_src()
        return f'<img src="{src}" alt="{self.alt}"{attrs}>'
