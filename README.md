# Babu Document Digitization

Babu digitizes Nepali government documents into structured data and printable
HTML. It provides a reusable Python HTML document engine, document-specific
layouts, an OCR extraction pipeline, and an agentic controller that verifies
rendered output against the source scan and repairs it under human supervision.

```text
source image
  → OCR extraction (Datalab)
  → structured JSON
  → translation (LLM: Nepali → target language)
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
- `document_builder/` — layouts for `citizenship`, `citizenship_back`,
  `laalpurja` (land ownership), `letter`, and five agent-generated types
  (`income_certificate`, `relationship_certificate`, `see_certificate`,
  `tax_clearance`, `transfer_certificate`), plus the registry that discovers
  them. Document types are found on disk, not listed in code; an `ACTIVE` file
  in each layout directory names the live layout (see below). All rendered value
  fields carry `contenteditable="true"` and `data-field` attributes for direct
  browser editing.
- `information_extraction/` — extraction helpers, JSON schemas, the LLM
  translation stage (`translator.py`), and the digitization entry point powered
  by Datalab OCR.
- `agentic_controller/` — the autonomous pipeline: RAG index over the codebase,
  a vision verifier, and an Architect Agent that writes layout and schema fixes.
- `tests/` — 183 tests across 10 suites covering the open `Style`, the monochrome
  guarantee, placeholder components, the layout validation gate, the A4
  autolayout geometry, `main.py`, the Architect Agent's command sandbox,
  layout/schema resolution, and translation.
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
| `OPENAI_API_KEY` | yes | Vision verifier and the translation stage |
| `OPENAI_MODEL` | no | Verifier model (default `gpt-4.1-mini`) |
| `TRANSLATOR_MODEL` | no | Translation model (defaults to `OPENAI_MODEL`) |
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
python -m agentic_controller.run path/to/document.png -t laalpurja --lang ja
```

| Flag | Default | Description |
|---|---|---|
| `image` | *(required)* | Path to source document image (PNG or JPEG) |
| `-t`, `--document-type` | `laalpurja` | Any discovered type, or a new one to generate |
| `--max-iterations` | `3` | Maximum repair cycles before only *approve* is offered |
| `--output-dir` | `output/` | Where HTML, PNG, and reports are written |
| `--auto-approve` | off | Unattended: auto-fix while blocking issues remain, then accept |
| `--no-translate` | off | Keep extracted values in their original script |
| `-l`, `--lang` | `en` | Language to translate into (`en`, `ja`); verification judges against the same one |
| `--result-json` | — | Write the run result, including full history, as JSON |

The run extracts, translates, builds, renders, verifies, then pauses at a
**single human checkpoint** per iteration:

| Input | Effect |
|---|---|
| `a` / `approve` | Accept the current output and finish |
| `r` / `retry` | Architect Agent diagnoses the report and repairs autonomously |
| `e` / `edit` | Prompts for free-text concerns, then repairs using that guidance |

If the document type has no registered layout and schema, the run generates
both from the source image before the first build.

### Which layout is live

Layouts are never edited in place. A repair writes `layout_1.py`, `layout_2.py`,
… beside the original `layout.py`, and a one-line `ACTIVE` file in the same
directory names the one that actually builds:

```
document_builder/citizenship_back/
    layout.py       # the original, never written to — roll back to it any time
    layout_1.py     # a repair
    ACTIVE          # contains: layout_1.py
```

No `ACTIVE` file means `layout.py`, so a directory that has never been patched
needs no bookkeeping. The Architect Agent writes `ACTIVE` itself, but only after
`validate_layout` builds the new layout on blank data — a layout that raises
cannot become live, and the previous good one stays up. Rolling back is editing
one line, and `git log` on `ACTIVE` is the promotion history.

Document types themselves are discovered the same way: any directory under
`document_builder/` with a resolvable layout and a matching schema in
`information_extraction/schemas/` is a usable `--type`. Adding one takes no code
edit, which is what lets a generation run use the type it just wrote.

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

# Keep the extracted values in their original script
python main.py test-data/demo.png --type letter --no-translate

# Translate into Japanese instead of English
python main.py test-data/demo.png --type letter --lang ja

# Build with every field empty, to check layout and spacing alone
python main.py --type laalpurja --blank --png
```

| Flag | Default | Description |
|---|---|---|
| `image` | — | Source scan to OCR. Omit when using `--data` or `--blank` |
| `-t`, `--type` | `laalpurja` | Any discovered type; `python main.py --help` lists what is currently installed |
| `-o`, `--output` | `output/<type>.html` | Output HTML path |
| `--data` | — | Build from this JSON instead of running OCR |
| `--save-data` | — | Write the extracted JSON for later `--data` runs |
| `--blank` | off | Every field empty — layout check, no OCR |
| `--no-translate` | off | Keep extracted values in their original script |
| `-l`, `--lang` | `en` | Language to translate into (`en`, `ja`) |
| `--png` | off | Also render a PNG (needs Chrome/Chromium) |
| `--strict` | off | Turn unrecognized-CSS-property warnings into errors |

Exactly one data source is required: an image, `--data`, or `--blank`. Both
`--data` and `--blank` skip the extractor entirely, so neither costs an API
call.

## Output is in the target language

Extraction returns values in the script they were printed in, usually
Devanagari. `information_extraction/translator.py` translates them before they
reach a layout, so the rendered document is readable in the target language
throughout — English by default, Japanese with `--lang ja`:

| | Source | English | Japanese |
|---|---|---|---|
| Phrases | `वंशज` | `By descent` | `子孫によって` |
| Names, places | `उमा देवी चौलागाई` | `Uma Devi Chaulagai` | `ウマ・デヴィ・チャウラガイ` |
| Numerals | `८` | `8` | `8` |
| BS dates | `२०४९/०३/०९` | `1992-06-23` | `1992-06-23` |

A new language is a new row in the `LanguageSpec` registry in
`information_extraction/languages.py` — the prompt templates are shared, only
the worked examples change.

Three things are deliberately left alone. Values that are already in the target
script cost nothing and are skipped. Bikram Sambat dates are converted locally
by `nepali_datetime`, never by the model — date arithmetic is exactly what an
LLM gets subtly wrong. And `present` / `absent` are an OCR contract rather than
content: a layout reads them to decide whether to draw a thumb-impression box
at all, so rewording one would silently remove an element from the page.

Bilingual field pairs get the same treatment. A `certificate_title_np` printed
above its `certificate_title_en`, or a `date_of_birth_bs` beside its `_ad`
twin, is deliberately scripted — translating the first line would make the
document say "Certificate" twice. Only the presence of the sibling triggers
this; a lone `foo_np` is the only value there is, and is translated normally.

Everything translatable in a document goes out in one request. Batching is
cheaper than a call per field and also more accurate — the model sees
`district` and `municipality` together and can tell that a word is a place
name. Results are cached on disk by `(model, kind, language, text)`, so the
repair loop's second and third iterations re-translate nothing, and a Japanese
run is never served an English cache hit.

A failed translation is reported, not raised: a document rendered in Devanagari
is more useful than no document. `--no-translate` skips the stage in both
pipelines.

Verification follows the same language. `agentic_controller/verifier.py` builds
its system prompt per language, so a Japanese render is judged against Japanese;
judged against the wrong one, every correctly translated value would be reported
as a data-accuracy defect and the repair loop would chase them forever.

## Output is strictly black and white

Every rendered document is pure monochrome — `#000000` ink on `#ffffff`
surfaces. This is enforced structurally in `html_engine/monochrome.py`, not by
convention: `Style.to_css()`, `Style.raw`, raw `style="..."` attributes, and the
final HTML are all normalized. There is no escape hatch. Source scans are
frequently colourful; a colour difference is never a verification discrepancy.

## Tests

```bash
python tests/run_all.py          # all 10 suites, 183 tests, no pytest needed
python tests/test_styles.py      # or run one suite directly
```

| Suite | Covers |
|---|---|
| `test_styles.py` | Open `Style`: any CSS property renders, typos warn, shorthand orders before longhand |
| `test_monochrome.py` | Every route CSS can take to the page, plus all registered layouts |
| `test_components.py` | Placeholders, watermark, signature block, the `field=` contract, child coercion |
| `test_layout_gate.py` | `validate_layout` catches errors inside a builder body, not just at import |
| `test_autolayout.py` | `/convert` block geometry becomes an exact A4 layout: one uniform scale, ink-extent fit, relative order preserved, generated source passes the gate, every field survives extraction |
| `test_main_cli.py` | `--blank` / `--data` never reach OCR; argument validation |
| `test_command_sandbox.py` | `execute_command` refuses `python -c`, redirection, chaining, substitution; originals are restored if a command touches them; an *existing* `layout.py` or base schema is never a write target, but a brand-new type may create its own |
| `test_registry_resolution.py` | `ACTIVE` selects the live layout and degrades safely; traversal in `ACTIVE` is rejected; discovery finds new types; promotion takes effect mid-process |
| `test_translator.py` | Sentinels, values already in the target script, and a bilingual pair's Nepali half never reach the model; BS dates convert locally; nested `plots` rows and extractor metadata survive; a failed call degrades to the original data; the cache spares the second run and is keyed on model and language; `--lang` changes what counts as already-translated |
| `test_verifier_prompt.py` | The verification prompt names its target language and carries that language's worked examples, while the other four rules stay shared and numbered as `verification-rules.md` mirrors them |

## Generate example documents

```bash
python document_builder/citizenship/test-generate-citzenship.py
python document_builder/laalpurja/test-generate-laalpurja.py
```

## Standalone tools

```bash
# Verify a render pair (--lang must match the language the render was built in)
python -m agentic_controller.verifier source.jpg rendered.png --output report.json
python -m agentic_controller.verifier source.jpg rendered.png --lang ja

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

See [documentation/FRONTEND-PLAN.md](documentation/FRONTEND-PLAN.md) for the
staged plan to put a Next.js visual editor in front of this engine over a
FastAPI layer, with a shared Document JSON schema as the contract between them.
