#HTML to PNG rendering via headless Chrome/Chromium.

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_SIZE: tuple[int, int] = (1300, 1100)


def render_png(
    html_path: Path,
    output_dir: Path,
    save_as: str,
    size: tuple[int, int] = DEFAULT_SIZE,
) -> bool:
    try:
        from html2image import Html2Image

        output_dir.mkdir(parents=True, exist_ok=True)

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
        return (output_dir / save_as).is_file()
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
