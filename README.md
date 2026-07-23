# Babu Document Digitization

Babu digitizes Nepali documents into structured data and printable HTML. The
repository provides a reusable Python HTML document engine, layouts for Nepali
citizenship and land-ownership documents, extraction schemas, and a controller
for visually checking a rendered layout against its source scan.

```text
document image -> extraction data -> layout builder -> HTML -> rendered PNG
                                                        |
                                              visual verification
```

## What is included

- `html_engine/` — reusable, component-based HTML and optional PDF renderer.
- `document_builder/` — citizenship and Laal Purja (land ownership) layouts.
- `information_extraction/` — extraction helpers, schemas, and digitization
  entry point.
- `controller/` — LangChain-based, read-only visual verifier and the foundation
  for a future LangGraph repair loop.
- `output/` — sample generated HTML and image outputs.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The visual verifier also needs an OpenAI API key:

```bash
cd controller
cp .env.example .env
# Set OPENAI_API_KEY in .env
```

## Generate example documents

```bash
python document_builder/citizenship/test-generate-citzenship.py
python document_builder/laalpurja/test-generate-laalpurja.py
```

## Verify a render

Place a reference scan at `controller/input.png` and its rendered counterpart
at `controller/output.png`, then run:

```bash
cd controller
python document_verifier.py --output report.json
```

The verifier compares both images using a vision model and emits a validated
JSON report. It does not alter either image or the layout. Images are sent to
the configured model, so only use documents whose handling has been approved.

## Direction of the controller

The next controller stage will use LangGraph to coordinate a bounded loop:
render, inspect, request a constrained patch to known layout blocks, validate,
render again, and escalate low-confidence or unresolved cases to a human. The
model will not be allowed to freely generate or replace HTML.

For the engine, builders, extraction path, and controller design, see
[technical documentation](documentation/DOCUMENTATION.md). The controller's
own quick start is in [controller/README.md](controller/README.md).
