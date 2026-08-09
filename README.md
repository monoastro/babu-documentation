# Babu Document Digitization

Babu digitizes Nepali government documents into structured data and printable
HTML. It provides a reusable Python HTML document engine, document-specific
layouts, an OCR extraction pipeline, and an agentic controller that verifies
rendered output against the source scan and repairs it under human supervision.

```text
source image
  → OCR extraction (Datalab)
  → structured JSON
  → layout builder
  → html_engine
  → HTML + PNG
  → verify (vision model)
  → human checkpoint → Architect Agent repair loop
```

## What is included

- `html_engine/` — component-based Python HTML renderer with an open `Style`
  API (any CSS property, not a closed allowlist). Output is enforced monochrome
  (see below). Includes placeholders for document furniture that cannot be
  rendered: `PlaceholderBox`, `Watermark`, `SignatureBlock`, `corner_box`.
- `document_builder/` — layouts for `citizenship`, `laalpurja` (land ownership),
  and `letter`. All rendered value fields carry `contenteditable="true"` and
  `data-field` attributes for direct browser editing.
- `information_extraction/` — extraction helpers, JSON schemas, and the
  digitization entry point powered by Datalab OCR.
- `agentic_controller/` — the autonomous pipeline: RAG index over the codebase,
  a vision verifier, and an Architect Agent that writes layout and schema fixes.
- `tests/` — 65 tests across 5 suites covering the open `Style`, the monochrome
  guarantee, placeholder components, the layout validation gate, and `main.py`.
- `output/` — generated HTML, PNG, and verification reports.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env`:

| Variable | Required | Purpose |
|---|---|---|
| `DATALAB_API_KEY` | yes | OCR extraction |
| `OPENAI_API_KEY` | yes | Vision verifier |
| `OPENAI_MODEL` | no | Verifier model (default `gpt-4.1-mini`) |
| `ANTHROPIC_API_KEY` | no | Architect Agent — preferred backend when set |
| `ARCHITECT_BACKEND` | no | Force `anthropic` or `openai` |
| `ARCHITECT_MODEL` | no | Override the agent model |
| `CHROME_EXECUTABLE` | no | Path to Chrome/Chromium if not auto-detected |

The Architect Agent needs `ANTHROPIC_API_KEY` **or** `OPENAI_API_KEY`. It
prefers Anthropic when both are present.

> **Note on `DATALAB_API_KEY`:** the loader uses `load_dotenv()`, which does
> **not** override variables already exported in your shell. If you have a stale
> `DATALAB_API_KEY` in `~/.bashrc` or similar, it silently wins over `.env` and
> you get a `401 Unauthorized` from datalab.to. Unset the shell export rather
> than editing `.env` again.

PNG rendering needs Chrome or Chromium on `PATH` (via `html2image`).

## Run the full pipeline

```bash
python -m agentic_controller.run path/to/document.png --document-type laalpurja
```

| Flag | Default | Description |
|---|---|---|
| `image` | *(required)* | Path to source document image (PNG or JPEG) |
| `-t`, `--document-type` | `laalpurja` | `laalpurja`, `citizenship`, `letter`, or a new type |
| `--max-iterations` | `3` | Maximum repair cycles before only *approve* is offered |
| `--output-dir` | `output/` | Where HTML, PNG, and reports are written |
| `--auto-approve` | off | Unattended: auto-fix while blocking issues remain, then accept |
| `--result-json` | — | Write the run result, including full history, as JSON |

The run extracts, builds, renders, verifies, then pauses at a **single human
checkpoint** per iteration:

| Input | Effect |
|---|---|
| `a` / `approve` | Accept the current output and finish |
| `r` / `retry` | Architect Agent diagnoses the report and repairs autonomously |
| `e` / `edit` | Prompts for free-text concerns, then repairs using that guidance |

If the document type has no registered layout and schema, the run generates
both from the source image before the first build.

## Build one document by hand

`main.py` is the manual counterpart to the pipeline above — same builders, same
engine, no vision verifier and no repair loop. Use it while iterating on a
layout, when you want to see the render rather than pay for a critique of it.

```bash
# OCR a scan, then build
python main.py test-data/demo.png --type letter

# Save the extracted JSON so later runs skip OCR entirely
python main.py test-data/demo.png --type letter --save-data output/letter.json

# Re-render from data already extracted — no API call
python main.py --type letter --data output/letter.json

# Build with every field empty, to check layout and spacing alone
python main.py --type laalpurja --blank --png
```

| Flag | Default | Description |
|---|---|---|
| `image` | — | Source scan to OCR. Omit when using `--data` or `--blank` |
| `-t`, `--type` | `laalpurja` | `citizenship`, `laalpurja`, or `letter` |
| `-o`, `--output` | `output/<type>.html` | Output HTML path |
| `--data` | — | Build from this JSON instead of running OCR |
| `--save-data` | — | Write the extracted JSON for later `--data` runs |
| `--blank` | off | Every field empty — layout check, no OCR |
| `--png` | off | Also render a PNG (needs Chrome/Chromium) |
| `--strict` | off | Turn unrecognized-CSS-property warnings into errors |

Exactly one data source is required: an image, `--data`, or `--blank`. Both
`--data` and `--blank` skip the extractor entirely, so neither costs an API
call.

## Output is strictly black and white

Every rendered document is pure monochrome — `#000000` ink on `#ffffff`
surfaces. This is enforced structurally in `html_engine/monochrome.py`, not by
convention: `Style.to_css()`, `Style.raw`, raw `style="..."` attributes, and the
final HTML are all normalized. There is no escape hatch. Source scans are
frequently colourful; a colour difference is never a verification discrepancy.

## Tests

```bash
python tests/run_all.py          # all 5 suites, 65 tests, no pytest needed
python tests/test_styles.py      # or run one suite directly
```

| Suite | Covers |
|---|---|
| `test_styles.py` | Open `Style`: any CSS property renders, typos warn, shorthand orders before longhand |
| `test_monochrome.py` | Every route CSS can take to the page, plus all registered layouts |
| `test_components.py` | Placeholders, watermark, signature block, the `field=` contract |
| `test_layout_gate.py` | `validate_layout` catches errors inside a builder body, not just at import |
| `test_main_cli.py` | `--blank` / `--data` never reach OCR; argument validation |

## Generate example documents

```bash
python document_builder/citizenship/test-generate-citzenship.py
python document_builder/laalpurja/test-generate-laalpurja.py
```

## Standalone tools

```bash
# Verify a render pair
python -m agentic_controller.verifier source.jpg rendered.png --output report.json

# Repair from a report (or omit --report to verify first)
python -m agentic_controller.architect repair laalpurja source.png rendered.png

# Generate layout + schema for a brand-new document type
python -m agentic_controller.architect generate <type> source.png --notes "..."

# Search the codebase index
python -m agentic_controller.rag_engine query "how do I center a heading"
python -m agentic_controller.rag_engine stats
```

The RAG index rebuilds itself when the code it covers changes — no manual step
is needed before an agent run.

## Full technical documentation

See [documentation/DOCUMENTATION.md](documentation/DOCUMENTATION.md) for the
engine architecture, component reference, builder design, extraction pipeline,
monochrome enforcement, and agentic controller internals.
