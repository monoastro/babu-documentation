import json
from pathlib import Path

pages = json.loads(
    Path("test-output/datalab-probe/citizenship.ocr.json").read_text(encoding="utf-8")
)
page = pages[0]
lines = page["text_lines"]
print("page keys:", list(page.keys()))
print("image_bbox:", page.get("image_bbox"))
print("line keys:", list(lines[0].keys()))
print("total lines:", len(lines))
print()
for i, line in enumerate(lines):
    bbox = [round(v, 1) for v in line.get("bbox", [])]
    conf = line.get("confidence", 0)
    print(f"[{i:2}] conf={conf:.3f} bbox={bbox} {line['text']!r}")
