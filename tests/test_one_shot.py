import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from one_shot import client, generate

PASS = 0
TOTAL = 0


def check(name: str, condition: bool) -> None:
    global PASS, TOTAL
    TOTAL += 1
    if condition:
        PASS += 1
    else:
        print(f"FAIL {name}")


prompt = generate.PROMPT_PATH.read_text(encoding="utf-8")
example = generate.EXAMPLE_PATH.read_text(encoding="utf-8")

check("prompt forbids devanagari numerals", "०–९" in prompt)
check("prompt requires single font stack", '"Times New Roman", Times, serif' in prompt)
check("prompt forbids page border", "No border on the page div" in prompt)
check("prompt has print rules", "@page { size: A4 portrait; margin: 0; }" in prompt)
check("prompt has editable hover styles", "[contenteditable" in prompt)
check("prompt forbids external requests", "no external requests" in prompt)
check("prompt says output html only", "Output only\nthe HTML" in prompt)

check("example has page scaffold", "class=\"page\"" in example)
check("example has circle", "border-radius: 50%" in example)
check("example has box", ".header-container" in example)
check("example has dotted-underline text field", "field-item" in example)
check("example has table", "<table>" in example)
check("example has totals row", "total-row" in example)
check("example has signature", "signature-block" in example)
check("example has photograph box", "Photograph Sd." in example)
check("example has thumb impression dashed", "Thumb Impression" in example)
check("example has photo-box", "photo-box" in example)
check("example has row/colspan land table", 'rowspan="2"' in example)
check("example cites sources", "5. pragya" in example and "4. sabin" in example and "3. sabitri" in example)
check("example snippets are html/css not prose-only", example.count("```html") >= 5)

no_devanagari = not re.search(r"[\u0900-\u097F]", example)
check("example contains no devanagari", no_devanagari)

p = generate.build_prompt(None)
check("prompt without example is prompt alone", p == prompt)

p = generate.build_prompt("<div>x</div>")
check("build_prompt appends example after rules", p.startswith(prompt) and p.endswith("<div>x</div>"))
check("build_prompt labels the example section", "# Reference snippets" in p)

check("fenced html extracted", generate.extract_html("```html\n<div>a</div>\n```") == "<div>a</div>")
check("plain html passes through", generate.extract_html("<div>a</div>") == "<div>a</div>")
check("whitespace stripped", generate.extract_html("  <div>a</div>  ") == "<div>a</div>")

saved_call = client.call
calls = []


def fake_call(prompt_text, *, images=None, temperature=0.2):
    calls.append((prompt_text, images))
    return "```html\n<!DOCTYPE html>\n<html lang=\"en\"><title>t</title></html>\n```"


client.call = fake_call
try:
    rc = generate.main(["--image", "master-data/laalpurja.png", "--out", "/tmp/opencode/test_draft.html"])
    check("main returns 0", rc == 0)
    check("main sent one png image", calls and calls[0][1] == [("image/png", Path("master-data/laalpurja.png").read_bytes())])
    check("main prompt includes rules and example", "Digitization Rules" in calls[0][0] and "Reference snippets" in calls[0][0])
    written = Path("/tmp/opencode/test_draft.html").read_text(encoding="utf-8")
    check("draft file written with fences stripped", written.startswith("<!DOCTYPE html>"))

    rc = generate.main(["--image", "missing.png"])
    check("missing image fails", rc == 1)
    rc = generate.main(["--image", "README.md"])
    check("bad suffix fails", rc == 1)
    check("no call made on failures", len(calls) == 1)
finally:
    client.call = saved_call

print(f"{PASS}/{TOTAL} passed")
sys.exit(0 if PASS == TOTAL else 1)
