# Frontend integration plan

A staged plan for putting a Next.js visual editor in front of the existing
Python document engine, and for reshaping the engine where it needs to change to
support that.

## Why this project exists

The goal is a workflow that automates and assists digitizing and translating
official Nepali documents into English — and later into other languages such as
Japanese — for foreign applications that require them: university admissions,
visa applications, and similar processes where the receiving institution cannot
read Nepali and needs a translated legal document.

That framing decides several arguments in this plan. The output is a legal
document, not a design artifact, so fidelity to the source scan outranks
authoring freedom. The person operating the editor is correcting a machine's
reading of a scan, not composing a page from scratch. And the same document will
be produced in more than one target language, so nothing may hardcode English.

## How to read the two source documents

`documentation/prd.md` is the frontend specification. It was written without
knowing that the OCR, translation, layout, and HTML generation are already built
in Python, so it is a guidance system for the direction of the project rather
than law. Where it assumes the frontend owns document processing, it is wrong
about this codebase.

`documentation/prd-update.txt` is the corrective overlay and governs wherever the
two conflict. Its central claim is the one this plan is built on:

> Next.js owns interaction and visualization. Python owns document intelligence.
> Document JSON becomes the contract between Python and Next.js.

The PRD's editor requirements — element types, selection, drag, resize, snapping,
undo/redo, properties panel, acceptance criteria AC-01 to AC-20, and the phased
build order in its §46 — all still stand. Only the question of *where the
intelligence lives* changes.

## Decisions settled up front

These are the choices every later stage depends on. They are recorded here so
they are not re-argued mid-build.

| Question | Decision | Reason |
|---|---|---|
| Element geometry shape | Nested `geometry: {x, y, width, height}` (prd-update §4), not the PRD's flat `x/y/width/height` | Elements also carry `style` and `metadata` objects; keeping geometry a sibling of those makes the whole element uniformly grouped, and lets a geometry-only patch be sent as one field |
| Canonical document representation | Document JSON is canonical. Python layouts become *generators of* and *renderers for* JSON, not the source of truth | Two clients must read the same document; a Python function body is not a format the browser can consume |
| Existing Python layouts | Kept, not deleted. They become the initial-layout generators invoked once per document type, emitting JSON | They encode real knowledge about each document's structure, and the Architect Agent already knows how to write them |
| Page geometry | A4 at 96 DPI, 794 × 1123 px, replacing the current 1200 px default | The deliverable is printed and submitted to an institution; A4 is the paper it lands on |
| MVP persistence | Filesystem JSON under a per-document directory, with a storage interface thin enough to swap for PostgreSQL JSONB | The engine already writes files per run; a database is not on the critical path to a working editor |
| Request model | Synchronous FastAPI endpoints, with every long operation returning a job-shaped response from day one | prd-update §11: keep it synchronous while it is quick, but design so async can be introduced without changing the client |
| Database ownership | Only FastAPI writes storage. Next.js never touches it directly | prd-update §10 |
| Monochrome rule | Scoped to document output only. Editor chrome, overlays, warnings, and selection handles are free to use colour | The rule exists to keep the printed document print-safe and faithful; it was never about the tool |
| First layout for an unseen type | Derived deterministically from OCR line boxes before the first model call, then critiqued by the Architect Agent in iteration 1 (Stage 4b) | The scan already knows where everything was. Clustering boxes costs nothing and repeats exactly, and the agent is better at judging a rendered page than at guessing positions blind |
| Source of geometry | `/ocr` line and character boxes — not `/extract`, which has none, and not `/convert` block boxes alone, which are too coarse (a whole table is one block) | Confirmed by probe against `test-data/citizenship.png`; see Stage 4 |
| Target language | A `LanguageSpec` in the `LANGUAGES` registry, selected by code (`en`, `ja`) and threaded through the pipeline. Engine side implemented | Adding a language must be adding one table entry, not editing prompts and cache keys across several files |

## Target architecture

```
            ┌──────────────────────────────────┐
            │ Next.js visual editor            │
            │ React · TypeScript · Zustand     │
            └───────────────┬──────────────────┘
                            │ HTTP, Document JSON
            ┌───────────────▼──────────────────┐
            │ FastAPI application layer        │
            │ documents · jobs · commands      │
            └───────────────┬──────────────────┘
                            │
    ┌───────────┬───────────┼───────────┬──────────────┐
    ▼           ▼           ▼           ▼              ▼
  OCR      Translation   Layout     Document JSON   HTML
extractor  translator   builders     model/store   renderer
    (all existing Python, unchanged where possible)
```

The four layers are presentation, application, document engine, and storage,
exactly as prd-update §12 lays them out.

## The central engineering problem

The PRD assumes documents are declarative JSON. This engine's documents are
Python source files: `build_citizenship(data)` places `AbsoluteBox` components at
literal pixel offsets and returns a `Document`. Those layout files are versioned
by an `ACTIVE` pointer and written by the Architect Agent.

Neither representation can simply replace the other. JSON cannot express what a
builder does with `data` — seeding defaults, branching on sentinel values like
`present` / `absent`, looping over a laalpurja's `plots` list. And a Python
function body is not something the browser can render or edit.

The resolution is to give each representation the job it is good at:

```
schema + OCR data ──▶ build_<type>(data) ──▶ Document (components)
                                                   │
                                        serialize  │
                                                   ▼
                                          Document JSON  ◀──── editor edits
                                                   │
                             ┌─────────────────────┴──────────────┐
                             ▼                                    ▼
                    Python HTML renderer                   React renderer
                       (export path)                       (canvas path)
```

The builder runs once, to produce the *first draft* of a document. From that
moment the JSON is the document, and the builder is not consulted again. This
keeps every piece of existing layout knowledge while making the artifact
editable.

Full structural fidelity on the first pass is not achievable — the component tree
mixes absolutely positioned boxes with flow layout, and some geometry only exists
after the browser lays it out. Stage 2 therefore defines a `fragment` element
type that carries a sanitized HTML fragment with a measured bounding box. A
fragment can be moved, resized, and deleted in the editor but not restyled from
the inside. Each document type's fragments are then promoted to first-class
elements over time, and a document that is all fragments still round-trips
byte-identically, which is what makes the migration safe to do incrementally.

---

# Stages

Each stage ends in a working system. Nothing here requires a later stage to be
useful, and each states what must be true before it counts as done.

## Stage 0 — Groundwork

**Goal.** Clear the obstacles that would otherwise be hit repeatedly later.

- ~~Retire `web/app.py`.~~ **Done.** It was a Flask prototype that shelled out to
  `controller.run`, a module path that no longer exists — the package was renamed
  to `agentic_controller`. It also hardcoded two document types and piped
  `"approve\n"` into the loop's stdin. The directory is gone; the Next.js editor
  is its replacement, written fresh rather than ported.
- Add `fastapi`, `uvicorn[standard]`, `python-multipart`, and `playwright` to
  `requirements.txt`. Playwright earns its place in Stage 4 for geometry
  measurement; `html2image` stays for the verifier's PNG path.
- Scope the monochrome rule. `html_engine/monochrome.py` currently normalizes
  every colour token at every output route with no opt-out, which is right for
  document output and wrong for an application UI. Nothing in the module changes;
  what changes is that the FastAPI layer's own responses, the editor's chrome,
  and any overlay the editor draws are outside its reach by construction —
  they never pass through `normalize_html`. Record this boundary in
  `documentation/DOCUMENTATION.md` beside the existing monochrome section so it
  is not mistaken for a regression.
- Fix the `## Future work → ### Visual editor` section of
  `documentation/DOCUMENTATION.md` to point at this plan instead of describing
  the editor as speculative.

**Done when.** `git ls-files web/` is empty, `pip install -r requirements.txt`
succeeds from a clean venv, and `python tests/run_all.py` still reports 9 suites
and 156 tests passing.

## Stage 1 — The Document JSON schema

**Goal.** One schema, in one place, that both languages implement against. This
is the contract; everything downstream is a consumer of it.

New directory `document-schema/`:

```
document-schema/
├── document.schema.json
├── page.schema.json
├── element.schema.json
├── text.schema.json
├── image.schema.json
├── field.schema.json
├── fragment.schema.json
├── style.schema.json
├── metadata.schema.json
└── README.md
```

The document envelope:

```json
{
  "schemaVersion": "1.0",
  "id": "doc-7f3a",
  "name": "Citizenship certificate — Uma Devi Chaulagai",
  "documentType": "citizenship",
  "sourceLanguage": "ne",
  "targetLanguage": "en",
  "pages": [
    {
      "id": "page-001",
      "width": 794,
      "height": 1123,
      "unit": "px",
      "elements": []
    }
  ]
}
```

Every element:

```json
{
  "id": "text_001",
  "type": "text",
  "geometry": { "x": 120, "y": 100, "width": 160, "height": 30 },
  "rotation": 0,
  "zIndex": 4,
  "locked": false,
  "hidden": false,
  "content": "Certificate No.",
  "style": {
    "fontFamily": "Noto Sans",
    "fontSize": 16,
    "fontWeight": 400,
    "textAlign": "left"
  },
  "metadata": {
    "source": "ocr",
    "ocrConfidence": 0.97,
    "originalText": "प्रमाणपत्र नं.",
    "language": "en",
    "translatedFrom": "ne",
    "field": "certificate_no"
  }
}
```

Three points about this shape, each load-bearing:

`metadata.field` is the bridge to everything that already exists. The engine
already emits `contenteditable="true" data-field="<dotted.path>"` through
`editable_attrs`, and those paths are extraction-schema keys. An element whose
`metadata.field` is `plots[0].plot_no` is the same thing the extractor filled and
the translator walked. No new identifier space is invented.

`metadata.originalText` and `translatedFrom` are the provenance the translator
already computes. `Translation.original` returns a flat `path → original value`
map, and `main.py` already persists it under `_translation_original`. Stage 8
routes that existing data into element metadata instead of a sidecar key.

The `field` element type from the PRD stays distinct from `text`. A `text`
element is literal content; a `field` element is a named slot that renders as
`<span data-field="owner_name">{{owner_name}}</span>` in a template and as its
resolved value in a filled document. Templates need this distinction; the PRD is
right to keep it.

`README.md` in that directory states the invariants prose cannot be derived from
the schema files: coordinates are page-relative pixels with the origin at the
page's top-left; `zIndex` ordering is stable for equal values by array position;
an element's `geometry` is its unrotated bounding box, with `rotation` applied
about the box's centre.

**Done when.** All nine schema files validate as JSON Schema, the README states
the invariants, and a hand-written example document validates against
`document.schema.json`.

## Stage 2 — Python side of the contract

**Goal.** Python can produce and consume Document JSON, and the round trip is
lossless.

New package `document_model/`:

| File | Responsibility |
|---|---|
| `model.py` | Dataclasses mirroring the schema: `DocumentModel`, `Page`, `Element` subclasses, `Geometry`, `ElementStyle`, `ElementMetadata` |
| `load.py` | `from_json(payload) -> DocumentModel`, validating against `document-schema/` |
| `dump.py` | `to_json(model) -> dict` |
| `serialize.py` | `document_to_model(doc: Document, *, measurements) -> DocumentModel` — the builder-output bridge |
| `render.py` | `render_model(model) -> str` — Document JSON to HTML, the export path |

`render.py` reuses `html_engine` rather than emitting HTML by hand: each element
becomes an `AbsoluteBox` carrying its geometry, and the result goes through the
same `renderer.render` and `monochrome.normalize_html` as any other document. The
export path therefore inherits the monochrome guarantee and the print rules for
free, and there is exactly one HTML emitter in the codebase.

`serialize.py` walks a built `Document`'s component tree. A subtree rooted at an
`AbsoluteBox` with a resolvable `left`/`top` and a text-bearing leaf becomes a
`text` element directly. Anything else becomes a `fragment` element holding its
rendered HTML and the bounding box supplied by the measurement pass. The
`measurements` argument is a `{element_id: geometry}` map produced by Stage 4;
until that stage exists, `serialize.py` accepts `None` and falls back to a single
page-sized fragment, which is enough to prove the round trip.

**Verification.** A new `tests/test_document_model.py`:

- For each of the nine registered document types: build with `--blank` data,
  serialize to JSON, render the JSON back to HTML, and assert the result is
  byte-identical to the builder's own `doc.render()`. This is the round-trip
  guarantee, and it is the test that makes every later stage safe.
- `from_json(to_json(m)) == m` for a hand-built model.
- Every element the serializer produces validates against the schema.
- `find_violations` reports nothing on any rendered model.

**Done when.** Round-trip is byte-identical for all nine types, and
`tests/run_all.py` reports 9 suites with the new one passing.

## Stage 3 — FastAPI application layer

**Goal.** Every capability the engine has, reachable over HTTP, with the
Document JSON as the payload.

New package `api/`:

```
api/
├── main.py          FastAPI app, CORS for the editor's dev origin
├── routes/
│   ├── documents.py upload, get, update, delete, list
│   ├── commands.py  the command endpoint
│   └── jobs.py      job status
├── storage.py       the storage interface and its filesystem implementation
├── jobs.py          in-process job registry
└── schemas.py       Pydantic request and response models
```

Endpoints:

| Method and path | Does |
|---|---|
| `POST /api/documents` | Upload a scan plus a document type. Runs extraction, translation, the builder, and serialization. Returns the Document JSON |
| `GET /api/documents` | List stored documents |
| `GET /api/documents/{id}` | Fetch one Document JSON |
| `PUT /api/documents/{id}` | Replace the Document JSON. The editor's save |
| `DELETE /api/documents/{id}` | Remove it |
| `POST /api/documents/{id}/commands` | Run a named command. See below |
| `GET /api/documents/{id}/render` | Rendered HTML for preview |
| `POST /api/documents/{id}/export` | Export HTML, later PDF |
| `GET /api/jobs/{id}` | Job status and result |
| `GET /api/document-types` | The registry's types and their schemas, for the editor's type picker |

The command endpoint is prd-update §15, and it is worth taking seriously. A
request names an operation; a response reports what changed:

```json
{ "command": "TRANSLATE_DOCUMENT", "targetLanguage": "ja" }
```

```json
{
  "command": "TRANSLATE_DOCUMENT",
  "status": "completed",
  "changes": [
    { "elementId": "text_001", "property": "content",
      "oldValue": "Certificate", "newValue": "証明書" }
  ]
}
```

Commands for the MVP: `TRANSLATE_DOCUMENT`, `REEXTRACT_FIELD`,
`VALIDATE_LAYOUT`, `REGENERATE_LAYOUT`. The changes array is what the editor
feeds into its undo history, so a backend operation is undoable by the same
mechanism as a drag — which is why this is worth building before the history
store rather than after.

Every long-running endpoint returns `{"jobId": ..., "status": ..., "result": ...}`
even when it completed inline. The client polls `GET /api/jobs/{id}` only while
status is pending. Moving to a real queue later then changes no client code.

`storage.py` defines the interface — `save(id, model)`, `load(id)`, `list()`,
`delete(id)`, `put_asset(id, name, bytes)` — with a filesystem implementation
writing `storage/documents/{id}/document.json` alongside the source scan and any
images. A PostgreSQL JSONB implementation is a later drop-in.

Uploads are the one place untrusted bytes enter. Enforce a content-type
allowlist, a size ceiling, and a generated document id; never derive a path from
a client-supplied name.

**Verification.** `tests/test_api.py` using FastAPI's `TestClient`: upload with a
stubbed extractor returns valid Document JSON; `PUT` then `GET` returns exactly
what was stored; a malformed document is rejected with 422 and does not
overwrite; path traversal in any id is rejected; the render endpoint's output has
no monochrome violations.

**Done when.** `uvicorn api.main:app` serves every endpoint above, and the tests
pass without a network call or an API key.

## Stage 4 — Geometry measurement and initial layout

**Goal.** Elements arrive in the editor with real positions, not one page-sized
fragment.

Add `document_model/measure.py`. It loads the builder's rendered HTML in headless
Chromium via Playwright, tags each candidate node, reads `getBoundingClientRect`
relative to the `.page` element, and returns the `{element_id: geometry}` map
that `serialize.py` takes. `rendering.py`'s existing `_page_metrics` already
parses the declared `.page` width and height, and that stays the reference frame.

This is also where the engine's real OCR shape has to be faced honestly, and a
probe against Datalab on `test-data/citizenship.png` settled what is actually
available. The PRD's §41 describes OCR returning bounding boxes that drive
automatic layout. That is half true, and the half that is true is not on the
endpoint the pipeline uses:

| Endpoint | What it returns | Geometry |
| --- | --- | --- |
| `/extract` (what `extractor.py` calls) | values keyed by the JSON schema, with citations | **none** |
| `/convert` (`output_format="json"`, `add_block_ids=True`) | a block tree — `Page` → `Picture`/`Text`/`SectionHeader` | block `bbox` + `polygon`, page space 2296×1540 |
| `/ocr` (deprecated, still live) | 34 `text_lines`, each with `text`, `confidence`, `chars`, `words` | **line-level and char-level** `bbox` + `polygon`, image space 1352×910 |

Three things follow, and each is a trap if missed.

- **Values and geometry come from different calls.** `/extract` gives clean,
  schema-keyed values and no coordinates; `/ocr` gives coordinates attached to
  noisy raw text (`"लिङ्ग :प्रुष"`, `"जिल्ला : ग्ल्मी"`, a stray emoji, confidences
  from 0.434 to 0.998, one line containing a literal `<br>`). Neither is a
  substitute for the other. The bridge matches an extracted value to the line
  that most likely printed it, and treats a failed match as "no geometry for
  this field" rather than guessing.
- **The two geometry spaces do not agree.** `/convert` reports the page as
  2296×1540, `/ocr` reports the image as 1352×910 — a factor of about 1.698.
  Whichever is adopted, every box is normalized to fractions of the page before
  anything else touches it, so the renderer's own page size in `_page_metrics`
  stays the single reference frame.
- **Block-level geometry is too coarse alone.** The citizenship scan's largest
  `Text` block contains an entire `<table>` of label/value rows in its HTML, with
  no per-cell coordinates. `/ocr` line boxes are what make individual fields
  addressable. `ConvertOptions(extras="table_row_bboxes")` is worth one probe
  before committing to the `/ocr` path, since it may give row geometry on the
  supported endpoint.

So there are two distinct capabilities, and both are now in scope — the second
in Stage 4b:

1. **Layout from the builder, values from OCR.** The builder decides where things
   go; OCR fills them in. This is what the engine does today and what this stage
   measures. It works, and it covers every registered document type.
2. **Layout from the scan.** Deriving a first layout from OCR box positions, for
   a document type nobody has written a layout for. Stage 4b.

Fail soft: when Playwright or a browser is unavailable, `measure` returns `None`
and serialization falls back to the whole-page fragment, exactly as
`render_png` already degrades. A machine without Chromium must still be able to
run the pipeline.

**Done when.** Serializing a built citizenship document yields distinct elements
with plausible geometry, the round-trip test from Stage 2 still passes
byte-identically, and the pipeline still runs with Playwright uninstalled.

## Stage 4b — A first layout from the scan's own geometry

**Goal.** When a document type has no layout, the agent's first iteration
reviews a real page instead of drafting one blind.

Today `generate_resources()` writes both schema and layout from the source image
alone, with nothing rendered yet to look at. The agent is guessing at positions
it cannot see the consequences of, and the repair loop then spends iterations
undoing that guess. The scan already knows where everything was; that knowledge
should arrive before the first model call, not after it.

**The decision** (this was left open, and this is the answer): the bbox-to-layout
step is a **deterministic pre-agent generator**, not a new agent mode — but its
output feeds the agent's existing first iteration, so from the outside it looks
exactly like the "auto-layout runs first, agent refines" flow that was asked for.

Two reasons for deterministic rather than model-driven:

- It costs nothing and repeats exactly. Positions come from arithmetic on boxes,
  so the same scan gives the same layout every time, and a bad layout is
  debuggable rather than resampled.
- The agent's tooling is already the right shape for the second half. It reads a
  rendered PNG, compares it against the source, and edits a layout file through
  `write_file` under the `validate_layout` gate. Handing it a rendered first
  draft plays to that. Handing it a JSON geometry blob would not — nothing in
  its toolset writes JSON.

New `document_builder/autolayout.py`:

- `boxes_from_ocr(image_path) -> list[TextBox]` — one call to `/ocr`, each line
  normalized to page fractions, low-confidence lines flagged rather than dropped.
- `group_boxes(boxes) -> list[Region]` — lines merged into rows and columns by
  vertical overlap and horizontal gaps. This is the whole algorithm: no model,
  no learning, just clustering on coordinates.
- `layout_source(regions, schema) -> str` — emits a `layout_1.py` in exactly the
  form the agent writes and `validate_layout` accepts, positioning a `Text` or
  `Field` per region and binding it to the schema key whose extracted value best
  matches that region's OCR text.
- Unmatched regions become placeholder text elements with the raw OCR string, so
  nothing on the page silently disappears; the agent can see them and decide.

Wiring in `agentic_controller/run.py`, at the `if not exists:` branch:

1. `autolayout` writes `layout_1.py` and, if no schema exists, `generate_resources()`
   still writes the schema — the schema is a semantic question, not a geometric
   one, and stays the agent's job.
2. The pipeline runs and renders as normal, so iteration 1 produces a real PNG.
3. `analyze_and_repair()` gets that PNG *plus* the region map, and its first pass
   is a critique of a concrete page.

Fail soft everywhere: if the `/ocr` call fails, if the boxes cluster into
nonsense, or if the emitted source does not pass `validate_layout`, the run falls
back to today's behaviour — `generate_resources()` drafts the layout — and says
so in the console. A worse first draft is not worth a failed run.

**Done when.** A document type with its layout deleted rebuilds to a recognisable
page in iteration 1 without the agent having written a layout, the repair loop
then converges in fewer iterations than from a blind draft, and deleting the
`DATALAB_API_KEY` or breaking the `/ocr` call still produces a document by the
old path.

## Stage 5 — Editor skeleton

**Goal.** A Next.js application that loads a document from the API and draws it.

`frontend/` at the repository root, `npm` as the package manager — node v26 and
npm are present on this machine, pnpm is not.

The directory layout follows PRD §34, and the store separation in PRD §14 is
followed as written — `documentStore`, `selectionStore`, `historyStore`,
`uiStore`, kept apart rather than merged into one:

```
frontend/
├── app/
│   ├── page.tsx                    document list
│   └── editor/[documentId]/page.tsx
├── components/
│   ├── editor/                     Toolbar, Canvas, Sidebar, PropertiesPanel
│   └── elements/                   TextElement, ImageElement, FieldElement, FragmentElement
├── store/                          documentStore, selectionStore, historyStore, uiStore
├── models/                         TypeScript types generated from document-schema/
├── renderer/                       JSON to React
├── commands/                       one file per undoable operation
├── lib/api.ts                      the FastAPI client
└── types/
```

The TypeScript types in `models/` are generated from `document-schema/` by
`json-schema-to-typescript`, wired to an `npm run schema` script. Hand-written
types drift from the schema; generated ones cannot.

The renderer maps element type to component through a registry —
`ElementRegistry.register({type, renderer, inspector, serializer})` per PRD §33 —
not a `switch`. Adding the `fragment` type, and later each promoted element type,
must not mean editing a chain of conditionals.

Scope for this stage is deliberately narrow: three-panel shell, canvas at A4
dimensions with zoom, elements rendered read-only, no interaction yet. PRD §46's
phases 1 through 4.

**Done when.** `/editor/{id}` for a document created through the API renders it
recognizably, and the canvas matches the Python HTML render closely enough to
compare side by side.

## Stage 6 — Editing

**Goal.** The PRD's editor, made real. Its §46 phases 5 through 9, and its
acceptance criteria AC-01 through AC-20.

Selection with marquee and shift-click; drag to move; eight resize handles with
aspect-ratio lock on shift; rotation; inline text editing; the properties panel
bound to the selected element's `style`; alignment and distribution; snapping to
page edges, element edges, and centres with visible guides; grid and rulers;
z-order controls; duplicate and delete; lock and hide.

Undo and redo go through `commands/`, one file per operation, matching the PRD's
operation list: `CREATE_ELEMENT`, `DELETE_ELEMENT`, `MOVE_ELEMENT`,
`RESIZE_ELEMENT`, `UPDATE_STYLE`, `UPDATE_CONTENT`, `CHANGE_Z_INDEX`. Every
command is invertible. Backend commands from Stage 3 enter the same history as a
compound command built from their `changes` array, so undoing a translation is
the same operation as undoing a drag.

Two things this editor needs that a general design tool would not, both following
from the product being a legal translation:

- **Confidence surfacing.** An element with a low `metadata.ocrConfidence` is
  visibly marked. The operator's job is to find what the machine misread, and the
  machine already knows where it was unsure.
- **Original-value inspection.** Selecting an element shows
  `metadata.originalText` beside the current content. Verifying a translation
  against the source is the core review action, and it should not require opening
  the scan.

**Done when.** AC-01 through AC-20 all pass by hand, and reloading after a save
reproduces the document exactly.

## Stage 7 — Persistence and the round trip

**Goal.** Edits survive, and what the editor shows is what gets exported.

Autosave on a debounce through `PUT /api/documents/{id}`, with an explicit save
control and a dirty indicator. Optimistic concurrency by a version integer on the
document; a stale `PUT` is rejected rather than silently overwriting.

The renderer-parity test is the important part of this stage, and prd-update §9
is right to flag it. Two renderers reading one document must agree. Add
`tests/test_renderer_parity.py`: for a fixture set of documents, render through
Python, screenshot the editor canvas through Playwright, and compare bounding
boxes of corresponding elements within a small tolerance. Divergence here is the
failure mode that would otherwise be discovered by a user receiving a wrong
document, so it gets a test rather than a convention.

Fonts are the likely source of divergence. Both renderers must load the same
Devanagari-capable family from the same files; the document's `style.fontFamily`
names a family that both sides resolve identically, and the export embeds or
references it explicitly.

**Done when.** Edit, reload, and export produce the same document three times
over, and the parity test passes for all nine types.

## Stage 8 — Translation as a document operation

**Goal.** Translation stops being a pipeline stage and becomes something the
operator invokes, reviews, and can undo.

`TRANSLATE_DOCUMENT` collects every translatable element, calls the existing
`translate_data`, and writes results back **keyed by element id**. The ids do not
change, so geometry and z-order survive — this is prd-update §6's point, and it
is why translation must operate on the model rather than on HTML.

The translator's existing rules all still apply and none of them move: sentinel
values like `present` and `absent` are never translated because layouts branch on
them; bilingual pairs such as `certificate_title_np` beside
`certificate_title_en` keep their Devanagari half; Bikram Sambat dates convert
locally through `nepali_datetime` rather than through the model; Devanagari
digits normalize to ASCII; values are batched, deduplicated, and disk-cached.

What changes is where the output goes. `Translation.original` already returns a
flat `path → original value` map, and `main.py` already saves it under
`_translation_original`. That data now populates `metadata.originalText` and
`metadata.translatedFrom` on each element, which is what makes review, undo, and
the side-by-side view all possible from one source.

Side-by-side (prd-update §17) then falls out: two panes, elements matched by id,
the original on the left and the translation on the right. Because the ids are
shared, scroll and selection sync between them without any alignment heuristic.

**Done when.** Translating in the editor updates content in place, every changed
element carries its original, the operation undoes cleanly, and the side-by-side
view lines up.

## Stage 9 — Layout warnings

**Goal.** Catch the failure this product is most exposed to: translated text that
no longer fits.

English and Japanese renderings of a Devanagari string are frequently wider or
narrower than the original, and a legal document with a clipped field is not
usable. The `VALIDATE_LAYOUT` command measures every element's rendered text
against its geometry and returns prd-update §7's warning shape:

```json
{
  "layoutWarnings": [
    { "elementId": "text_123", "type": "overflow", "severity": "warning" }
  ]
}
```

Types to detect: `overflow` when content exceeds the box, `collision` when two
elements' boxes intersect unintentionally, `offPage` when an element leaves the
page, and `empty` when a required field resolved to nothing. The editor marks
each warned element and lists them in a panel.

Validation runs automatically after any translation, and on demand otherwise.
Warnings never block — the operator decides. The point is that nothing ships
clipped without someone having seen it.

**Done when.** Translating a document into a language with longer strings raises
overflow warnings on exactly the elements that overflow, and the editor shows
them.

## Stage 10 — Export

**Goal.** Produce the file that gets submitted.

HTML export goes through `document_model/render.py`, so it is the same emitter
and inherits the monochrome guarantee. Per PRD §36, exported HTML must not carry
executable content: sanitize `fragment` HTML on the way in, escape all text on
the way out, and emit no script or event-handler attributes.

PDF is what an institution actually accepts, so it is not deferred past this
stage. Headless Chromium's print-to-PDF via Playwright reuses the page geometry
and the `@media print` rules the renderer already emits, and the A4 page size
chosen in the decisions table means print output needs no scaling.

Also export the Document JSON itself. It is the archival format, the thing that
allows a document to be re-opened, re-translated into a second language, or
diffed against a later revision.

**Done when.** HTML, PDF, and JSON all export; the PDF is A4 with no scaling
artifacts; and the exported HTML contains no script.

## Stage 11 — The agentic loop, made reviewable

**Goal.** Bring the existing verify-and-repair loop into the web workflow.

`agentic_controller/run.py` blocks on `input()` in `_collect_decision` and
`_collect_user_concerns`. That is correct for a terminal and impossible over
HTTP. The seam already exists: `auto_approve=True` skips the prompts, and
`digitize` returns a `history` list.

Refactor `digitize` to take a *checkpoint handler* rather than calling `input()`
directly. The CLI passes the existing stdin prompt; the API passes a handler that
records the checkpoint as a job awaiting review and returns. The editor then
shows the verifier's report — `VerificationReport` and `Discrepancy` are already
Pydantic models with `severity`, `confidence`, and `.blocking()`, so they
serialize into the UI with no adaptation — beside the source scan and the render,
and the operator's decision resumes the loop.

This is where the product's promise of automation is realized: the machine
extracts, translates, lays out, renders, and critiques its own output; the person
reviews flagged discrepancies rather than transcribing a document by hand.

**Done when.** A document can be taken from upload through a repair iteration to
approval entirely in the browser, and the CLI path still works unchanged.

## Stage 12 — More than one target language

**Goal.** Make Japanese a configuration change rather than a rewrite.

**The engine half is done.** Target language is now a parameter end to end:

- New `information_extraction/languages.py` holds a frozen `LanguageSpec` per
  language in a `LANGUAGES` registry — `code`, `name`, `script_is_ascii`, and the
  three worked-example blocks (`transliteration`, `meaning`, `office`) that a
  prompt needs in the target script. Adding a language is adding one entry; no
  logic elsewhere changes. The module imports nothing, so a CLI can read
  `LANGUAGES` to build its `--lang` choices without pulling in the OpenAI client.
- `translator.py` builds its prompt from `_PROMPT_TEMPLATE`/`_PROSE_TEMPLATE` and
  the spec, rather than a hardcoded English `_SYSTEM_PROMPT`.
- The cache key is `(model, kind, target_language, value)`, so a Japanese run is
  never served the English hits an earlier run left behind.
- `_needs_translation` takes the spec: for a non-Latin target, a value that is
  already ASCII is *not* finished — a document's printed English half still needs
  Japanese. The exception is `_is_identifier` (a single token containing a digit,
  such as `NM0000095` or `41-01-78-00466`), which is printed as-is in every
  language and must never reach the model.
- `translate_data(data, target_language=...)`, `build_document(...,
  target_language=...)`, `main.py --lang {en,ja}`, and
  `python -m agentic_controller.run --lang {en,ja}` all carry it through.
  `Translation.target_language` reports what a result was rendered into.
- `tests/test_translator.py` covers the spec reaching the model call, per-language
  prompt examples, cache isolation between languages, ASCII-source behaviour under
  a non-Latin target, and identifier exemption.

`_PAIRED_SUFFIXES` was left English-keyed on purpose. It describes the *source
document* — a scan that prints `certificate_title_np` beside
`certificate_title_en` prints both halves whatever we translate into — so making
it per-target would be modelling the wrong thing.

**What remains** is the frontend half. The document carries `targetLanguage`, so a
second translation of the same source is a new document sharing element ids with
the first — which means the side-by-side view from Stage 8 works across any pair
of languages, not just against the original. The API needs the language on the
translate endpoint, and the editor needs a picker fed from `LANGUAGES`.

Font coverage is the practical constraint: CJK output needs a family with the
right glyphs on both the Python and React sides, and Stage 7's font decision is
where that gets settled.

**Done when.** The same scan produces both an English and a Japanese document,
each with correct provenance, and the caches do not cross-contaminate.

---

## Sequencing

Stages 1 through 3 are the critical path — nothing else can start without the
schema, the Python bridge, and the API. Stage 4 can proceed alongside Stage 5,
since the editor renders whatever geometry it is given. Stage 4b needs 4's
normalized coordinate frame but nothing after it, and pays off immediately at the
CLI, so it can be done early. Stages 8 through 10 need Stage 6's command
infrastructure. Stage 11 is independent of the editor; Stage 12's engine half is
already done and its frontend half rides on Stage 8.

```
1 ─▶ 2 ─▶ 3 ─┬─▶ 4 ─┬─▶ 4b
             └─▶ 5 ─┴─▶ 6 ─▶ 7 ─┬─▶ 8 ─▶ 9
                               └─▶ 10
                        11 independent · 12 engine done
```

## Standing rules for the whole effort

- **The round-trip test is the safety net.** Stage 2's byte-identical guarantee
  for all nine document types must keep passing after every change. When it
  breaks, something has silently changed the output of a legal document.
- **`tests/run_all.py` stays green**, and stays free of pytest and of network
  calls.
- **One HTML emitter.** Everything renders through `html_engine`, so the
  monochrome guarantee and the print rules cannot be bypassed by a new path.
- **Run `graphify update .` after changing code**, per `CLAUDE.md`.
- **The document is a legal artifact.** When fidelity to the source and editor
  convenience conflict, fidelity wins.

## Deliberately not in scope

Following PRD §38, and adding what this codebase makes newly relevant:
real-time collaboration; AI layout generation from a prompt; importing arbitrary
HTML; a plugin system; mobile editing; and a PostgreSQL migration, which stays
behind the storage interface until there is a reason for it.

