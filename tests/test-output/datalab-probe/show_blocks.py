import json
from pathlib import Path
from collections import Counter

d = json.loads(Path("test-output/datalab-probe/citizenship.convert.json").read_text(encoding="utf-8"))


def walk(node, depth=0, out=None):
    out = out if out is not None else []
    out.append((depth, node))
    for child in (node.get("children") or []):
        walk(child, depth + 1, out)
    return out


print("ROOT keys:", list(d.keys()))
print("metadata:", json.dumps(d.get("metadata"), ensure_ascii=False)[:400])
page = d["children"][0]
print("PAGE keys:", list(page.keys()))
print("PAGE block_type:", page.get("block_type"), "bbox:", page.get("bbox"))
print()

rows = walk(page)
print("total nodes:", len(rows))
print("block types:", Counter(n.get("block_type") for _, n in rows))
print()

indent = "  "
for depth, n in rows[:40]:
    bbox = n.get("bbox")
    bb = [round(v, 1) for v in bbox] if bbox else None
    html = (n.get("html") or "").replace("\n", " ")[:70]
    print(f"{indent*depth}{n.get('block_type','?'):12} id={n.get('id')} bbox={bb} poly={'Y' if n.get('polygon') else 'N'} {html!r}")
