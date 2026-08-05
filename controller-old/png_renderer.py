"""
Render html to a PNG via headless Chrome/Chromium.
Chrome/Chromium executable is resolved in this order:
  1. CHROME_EXECUTABLE env var (e.g. export CHROME_EXECUTABLE=/usr/bin/chromium)
  2. Auto-detection by html2image (searches common system paths)

If no browser is found, rendering is skipped

html_path:  Absolute path to the HTML file.
output_dir: Directory where the PNG will be written.
save_as:    PNG filename (e.g. ``"laalpurja.png"``).
size:       Viewport (width, height) in CSS pixels.
"""

from __future__ import annotations
import os
from pathlib import Path


def render_png(html_path: Path, output_dir: Path, save_as: str, size: tuple[int, int] = (1300, 1100)) -> bool:
    try:
        from html2image import Html2Image

        chrome_exe = os.getenv("CHROME_EXECUTABLE") or None
        kwargs = {
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
        return True
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

def test():
    render_png(html_path=Path("output/laalpurja.html"), output_dir=Path("output"), save_as="laalpurja-output.png", size=(1500, 1500) )

if __name__ == "__main__":
    test()

