import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
from datalab_sdk import DatalabClient
from datalab_sdk.models import OCROptions

out = Path("test-output/datalab-probe")
client = DatalabClient()

# The big Text block's HTML, to see what structure survives inside one block.
d = json.loads((out / "citizenship.accurate.json").read_text(encoding="utf-8"))
page = d["children"][0]
for child in page.get("children") or []:
    if child.get("block_type") == "Text" and len(child.get("html") or "") > 200:
        print("=== Text block html ===")
        print(child["html"][:1500])
        print()

# Line-level bboxes from the deprecated /ocr endpoint.
try:
    r = client.ocr("test-data/citizenship.png", options=OCROptions())
    print("ocr success:", r.success, "error:", r.error)
    (out / "citizenship.ocr.json").write_text(
        json.dumps(r.pages, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    page0 = r.pages[0]
    print("page keys:", list(page0.keys()))
    lines = page0.get("text_lines", [])
    print("text_lines:", len(lines))
    for line in lines[:12]:
        print(" ", {k: line[k] for k in line if k != "polygon"})
except Exception as exc:
    print("ocr endpoint failed:", type(exc).__name__, exc)
