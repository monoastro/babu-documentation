# Babu Document Digitization

Babu digitizes Nepali documents into structured data and printable HTML. It
provides a reusable Python HTML document engine, document-specific layouts for
citizenship and land-ownership certificates, an OCR extraction pipeline, and a
LangGraph controller that verifies, repairs, and finalizes rendered documents
under human supervision.

```text
source image
  → OCR extraction (Datalab)
  → structured JSON
  → layout builder
  → html_engine
  → HTML + PNG
  → LangGraph controller (verify → human review → repair loop)
```

## What is included

- `html_engine/` — component-based Python HTML renderer with optional PDF
  export via WeasyPrint.
- `document_builder/` — citizenship and Laal Purja (land-ownership) layouts.
  All rendered value fields carry `contenteditable="true"` and `data-field`
  attributes for direct browser editing.
- `information_extraction/` — extraction helpers, JSON schemas, and
  digitization entry point powered by Datalab OCR.
- `controller/` — LangGraph StateGraph that orchestrates the full pipeline:
  extraction → build → verify → human-in-the-loop review → bounded repair.
- `output/` — sample generated HTML and PNG outputs.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp controller/.env.example controller/.env
# Set OPENAI_API_KEY and DATALAB_API_KEY in controller/.env
```

PDF export additionally requires WeasyPrint:

```bash
pip install weasyprint
```

## Run the full pipeline

```bash
python -m controller.run path/to/document.png --document-type laalpurja
```

Options:

| Flag | Default | Description |
|---|---|---|
| `image` | *(required)* | Path to source document image |
| `--document-type` | `laalpurja` | `laalpurja` or `citizenship` |
| `--max-iterations` | `3` | Maximum repair/edit cycles before forced stop |

The controller will extract, build, verify, and then pause for your review.
At each iteration you can approve the output, trigger an automatic LLM repair,
or manually edit specific field values. See [controller/README.md](controller/README.md)
for the full architecture and human-review flow.

## Generate example documents

```bash
python document_builder/citizenship/test-generate-citzenship.py
python document_builder/laalpurja/test-generate-laalpurja.py
```

## Verify a render (standalone)

```bash
python -m controller.document_verifier source.png rendered.png --output report.json
```

## Full technical documentation

See [documentation/DOCUMENTATION.md](documentation/DOCUMENTATION.md) for the
engine architecture, component reference, builder design, extraction pipeline,
and controller internals.
