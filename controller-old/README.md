# Controller — Document Verification, Repair & LangGraph Pipeline

Compares a source document image with its digitally rendered replica, produces
a structured discrepancy report, and repairs the extraction schema / layout
through a bounded human-in-the-loop loop.

## Setup

Python 3.10+ and an OpenAI API key.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # add your OPENAI_API_KEY + DATALAB_API_KEY
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     controller/graph.py                             │
│                                                                     │
│   check_resources → extract_data → build_document → verify          │
│                                         ▲                           │
│                                         │           ┌─ approve → END│
│   apply_edits ──────────────────────────┤           │               │
│                                         │  human    ├─ retry → ─┐   │
│   apply_repair ─────────────────────────┘  review ──┤           │   │
│        ▲                                            └─ edit → ──┤   │
│        │                                                        │   │
│   analyze_repair ◄──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

Each iteration is recorded in `state["history"]` for full traceability.

## Modules

| File | Purpose |
|---|---|
| `graph.py` | LangGraph StateGraph — nodes, edges, routing, state definition |
| `run.py` | CLI runner — drives the graph interactively with terminal I/O |
| `document_verifier.py` | Compares source PNG ↔ rendered PNG → `VerificationReport` |
| `layout_repairer.py` | Reads a report → proposes patches → re-extracts → re-renders |
| `schema_patcher.py` | Applies `SchemaPatch` operations to a JSON extraction schema |
| `models.py` | Pydantic models: `SchemaPatch`, `LayoutPatch`, `RepairPlan` |

## Quick start — full pipeline

```bash
python -m controller.run controller/data/input.png --document-type laalpurja
```

The pipeline will:
1. **Check** if a layout builder and extraction schema exist for the document type
2. **Extract** structured data from the image via Datalab OCR
3. **Build** HTML + PNG from the extracted data
4. **Verify** the rendered output against the source image
5. **Pause** for your review — you see the verification report and choose:
   - `a` (approve) — finalize the output
   - `r` (retry) — let the LLM analyze and repair automatically
   - `e` (edit) — manually edit specific field values

### Options

| Flag | Default | Description |
|---|---|---|
| `image` | *(required)* | Path to source document image |
| `--document-type` | `laalpurja` | Document type (`laalpurja`, `citizenship`) |
| `--max-iterations` | `3` | Maximum repair/edit iterations before forced stop |

## Individual commands

### 1. Verify a document

```bash
python -m controller.document_verifier [source.png] [rendered.png]
python -m controller.document_verifier --output report.json
```

### 2. Repair a document (standalone)

```bash
# Dry run — inspect the plan before applying
python -m controller.layout_repairer --dry-run

# Full repair
python -m controller.layout_repairer
```

## Contenteditable HTML output

The rendered HTML includes `contenteditable="true"` and `data-field="field_name"`
attributes on every extracted value element. This means:

- **Open the HTML in a browser** and click any value to edit it directly
- Each editable element has a `data-field` attribute identifying which schema
  field it corresponds to (e.g. `data-field="owner_name"`,
  `data-field="plots.0.plot_no"`)
- Hover shows a dashed blue outline; focus shows a solid outline with yellow
  background

This is the foundation for the planned visual editor (drag-and-drop fields,
resize boxes, section management).

## Design choices

- **Constrained patches only** — the LLM proposes changes from a fixed
  vocabulary (`add_field`, `modify_field`, `add_header_field`, etc.).
  It cannot generate raw HTML, CSS, or Python code.
- **Original files untouched** — schema patches write to `_patched.json`
  alongside the original. The existing layout builder is reused as-is.
- **LangGraph `interrupt()`** — human review uses LangGraph's interrupt
  mechanism with a `MemorySaver` checkpointer, so the same graph can be
  driven by a CLI, web API, or any other frontend without code changes.
- **Bounded iterations** — `max_iterations` prevents infinite loops.
  After that many cycles, only "approve" is available.
- **Full history** — every iteration's verification result and decision is
  recorded in `state["history"]` (append-only via LangGraph's `add` reducer).

## Future: visual editor

The `contenteditable` + `data-field` attrs lay the groundwork for:

- Drag-and-drop field reordering
- Resize handles on boxes/sections
- Add/remove fields from the document
- Direct text editing with live data sync back to the extraction schema
- All edits feed back through the same `apply_edits` node in the graph
