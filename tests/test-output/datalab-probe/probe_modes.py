import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
from datalab_sdk import DatalabClient
from datalab_sdk.models import ConvertOptions

out = Path("test-output/datalab-probe")
out.mkdir(parents=True, exist_ok=True)
client = DatalabClient()


def count(node, acc=None):
    acc = acc if acc is not None else []
    acc.append(node.get("block_type"))
    for child in (node.get("children") or []):
        count(child, acc)
    return acc


for mode in ("accurate",):
    result = client.convert(
        "test-data/citizenship.png",
        options=ConvertOptions(output_format="json", mode=mode, add_block_ids=True),
    )
    path = out / f"citizenship.{mode}.json"
    path.write_text(json.dumps(result.json, ensure_ascii=False, indent=2), encoding="utf-8")
    page = result.json["children"][0]
    from collections import Counter

    print(mode, "->", Counter(count(page)), "cost:", result.cost_breakdown)
