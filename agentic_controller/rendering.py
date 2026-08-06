#HTML to PNG rendering via headless Chrome/Chromium.

from __future__ import annotations

import os
import re
from pathlib import Path

#: Fallback viewport, used only when the page geometry cannot be determined.
DEFAULT_SIZE: tuple[int, int] = (1300, 1100)

#: ``renderer.render()`` lays the page out with ``margin:30px auto``.
PAGE_MARGIN = 30

#: Tall probe viewport for ``height:auto`` pages, whose real height is known
#: only after the browser has laid the content out. The image is cropped back
#: to the page afterwards, so an oversized probe costs a little memory, never
#: correctness.
PROBE_HEIGHT = 4000

_PAGE_RULE = re.compile(r"\.page\s*\{([^}]*)\}", re.IGNORECASE)
_PX = re.compile(r"^\s*(\d+(?:\.\d+)?)px\s*$", re.IGNORECASE)


def _page_metrics(html: str) -> tuple[int | None, int | None]:
    """
    Read the declared ``.page`` width and height out of rendered HTML.

    Returns ``(width, height)`` in pixels, either of which may be ``None``
    when the value is ``auto`` or otherwise not a plain px length.
    """
    match = _PAGE_RULE.search(html)
    if not match:
        return None, None

    declared: dict[str, str] = {}
    for part in match.group(1).split(";"):
        if ":" in part:
            key, _, value = part.partition(":")
            declared[key.strip().lower()] = value.strip()

    def as_px(value: str | None) -> int | None:
        if not value:
            return None
        found = _PX.match(value)
        return int(float(found.group(1))) if found else None

    return as_px(declared.get("width")), as_px(declared.get("height"))


def _crop_to_page(path: Path, pad: int = PAGE_MARGIN) -> tuple[int, int] | None:
    """
    Crop a rendered PNG down to the page itself.

    The ``.page`` wrapper carries a border, so the ink bounding box is exactly
    the page rectangle. Cropping to it gives every document the same framing
    regardless of viewport, which matters because the verifier compares the
    source scan against this image — inconsistent margins read as layout
    discrepancies that no layout change can fix.

    Returns the cropped size, or ``None`` if Pillow is unavailable or the page
    is blank (in which case the file is left untouched).
    """
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return None

    with Image.open(path) as img:
        rgb = img.convert("RGB")
        # Ink bbox = everything that differs from the white surface.
        white = Image.new("RGB", rgb.size, (255, 255, 255))
        bbox = ImageChops.difference(rgb, white).getbbox()
        if not bbox:
            return None

        left = max(bbox[0] - pad, 0)
        top = max(bbox[1] - pad, 0)
        right = min(bbox[2] + pad, rgb.width)
        bottom = min(bbox[3] + pad, rgb.height)
        cropped = rgb.crop((left, top, right, bottom))
        cropped.save(path)
        return cropped.size


def render_png(
    html_path: Path,
    output_dir: Path,
    save_as: str,
    size: tuple[int, int] | None = None,
) -> bool:
    """
    Render *html_path* to ``output_dir/save_as``.

    Parameters:
        size: Explicit viewport. Left as ``None`` (the default) the viewport is
            derived from the page's own geometry, which is what keeps tall
            documents from being silently cut off — a fixed viewport shorter
            than the page crops it, and the verifier then reports the missing
            content as a layout defect.

    Returns:
        ``True`` when the PNG landed on disk.
    """
    try:
        from html2image import Html2Image

        output_dir.mkdir(parents=True, exist_ok=True)

        page_w = page_h = None
        if size is None:
            try:
                page_w, page_h = _page_metrics(
                    html_path.read_text(encoding="utf-8", errors="ignore")
                )
            except OSError:
                page_w = page_h = None

            width = (page_w + PAGE_MARGIN * 2) if page_w else DEFAULT_SIZE[0]
            # An auto-height page needs a probe tall enough to hold whatever
            # the content turns out to be; the crop restores the real size.
            height = (page_h + PAGE_MARGIN * 2) if page_h else PROBE_HEIGHT
            size = (width, height)

        chrome_exe = os.getenv("CHROME_EXECUTABLE") or None
        kwargs: dict[str, object] = {
            "output_path": str(output_dir),
            "disable_logging": True,
        }
        if chrome_exe:
            kwargs["browser_executable"] = chrome_exe

        hti = Html2Image(**kwargs)
        hti.screenshot(
            url=str(html_path.absolute()),
            save_as=save_as,
            size=size,
        )

        out_path = output_dir / save_as
        if not out_path.is_file():
            return False

        cropped = _crop_to_page(out_path)
        if cropped and page_h and cropped[1] < page_h:
            # The page rendered shorter than declared: content is missing, not
            # merely cropped. Worth saying out loud — it looks identical to a
            # layout bug in the verification report.
            print(
                f"  ⚠ Rendered page is {cropped[1]}px tall but the layout "
                f"declares {page_h}px."
            )
        return True
    except ImportError:
        print(
            "PNG render skipped — html2image is not installed.\n"
            "pip install html2image"
        )
        return False
    except FileNotFoundError as exc:
        print(
            f"PNG render skipped — Chrome/Chromium not found.\n"
            f"Install chromium or set CHROME_EXECUTABLE=/path/to/chrome\n"
            f"({exc})"
        )
        return False
    except Exception as exc:
        print(f"PNG render skipped: {exc}")
        return False
