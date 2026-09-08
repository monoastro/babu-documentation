# Babu Document Digitization — agent notes

Python-only. No build step, no linter, formatter, typechecker, or CI workflow.
`README.md` is the CLI reference; `documentation/DOCUMENTATION.md` the internals.

## Environment

- Deps live only in `.venv/`. Use `.venv/bin/python`; a bare `python` shim has no
  `datalab_sdk`, `html2image`, or `sentence_transformers`.
- `requirements.txt` is incomplete — `datalab-python-sdk` is imported but
  unlisted, so a fresh `pip install -r requirements.txt` gives you no OCR.
  (`html2image`, `pillow`, and `google-genai` are now listed for `one_shot`.)
- `load_dotenv()` does **not** override exported shell vars. A stale
  `DATALAB_API_KEY` in your shell silently beats `.env` → 401 from datalab.to.
  Unset the export rather than editing `.env` again. Debug that with length and
  prefix checks — never print a key value.
- PNG rendering needs Chrome/Chromium on `PATH`, or `CHROME_EXECUTABLE`.
- `GEMINI_API_KEY` (in `.env`) drives `one_shot`; it uses
  `gemini-3.6-flash` with thinking level high. The model can 503 under
  demand — retry, don't rewrite the call.

## Verify changes

```bash
.venv/bin/python tests/run_all.py       # 11 suites, ~200 asserts, no pytest
.venv/bin/python tests/test_styles.py   # one suite is one script
```

Suites are plain `assert` scripts that stub every model call, so they run offline
and cost nothing. This is the only gate in the repo.

Free manual checks — neither touches OCR or an API:

```bash
.venv/bin/python main.py --type laalpurja --blank --png       # layout only
.venv/bin/python main.py --type letter --data <file> --strict
```

`--strict` promotes unrecognized-CSS-property warnings to errors. Any `main.py`
run with an image argument spends a Datalab call plus a translation call.

## Two digitization paths

- **`one_shot/` is the active workflow** — one Gemini call replaces the whole
  extract → translate → build chain. `one_shot/prompt.txt` (tracked) is the
  ruleset; `one_shot/example.txt` (tracked) carries verbatim generated-code
  snippets (page scaffold, circle, box, text field, table, signatures, photo
  box, card scaling) pulled from cleaned finals in `translated/`, newest
  folders preferred. Drafts land in `one_shot/drafts/` (gitignored) for
  cleanup in `html_visual_editor/`.
- **The legacy pipeline** (`main.py`, `agentic_controller/`) still works and is
  the only path with OCR-based extraction, verification, and repair. Prefer
  `one_shot` for new documents.

## one_shot conventions

- Generation is `python -m one_shot.generate --image X [--example E]`. No
  routing, no catalog, no `--family`/schema attachment — those were built,
  live-verified, then removed as overcomplication; example selection is manual.
  Prompt assembly order is rules → reference snippets; the tests assert it.
- **No page border** — the evolved requirement: borders belong to elements
  inside (boxes, tables, stamps), never the document edge. `example.txt`
  snippets already follow it.
- **Gemini free tier is 20 requests/day for `gemini-3.6-flash`.** A generate
  is 1 call. Tests are offline (`tests/test_one_shot.py` stubs every call) —
  never "quickly verify" with live calls; verify one real job instead.
- **No Devanagari in output, ever** — numerals (०–९) become ASCII, proper
  nouns are transliterated. One font stack: Times New Roman. Output is a
  standalone HTML file: no `<img>`, scripts, or external requests.
- `html_visual_editor/` is a **nested git repo** — its changes are committed
  there, not here.

## Layout of the repo

- `document_builder/<type>/layout.py` — one `build_<type>(data) -> Document`.
- `information_extraction/schemas/<type>.json` — that type's extraction schema.
- `agentic_controller/` — `run.py` pipeline, `verifier.py` vision critique,
  `architect.py` repair/generate agent and its command sandbox, `rag_engine.py`.
- `one_shot/` — `client.py` (Gemini wrapper), `generate.py`, `prompt.txt` and
  `example.txt` (tracked; the old root `prompt.txt` is deleted).
- `html_visual_editor/` — the React editor; nested repo.
- `main.py` is the manual single-document build (no verifier, no repair loop) and
  defaults to `translated/<type>.html`; README's `output/<type>.html` is stale.
  The pipeline writes to `output/`.
- Gitignored scratch, not source: `master-data/`, `translate/`, `translated/`,
  `output/`, `work.txt`, `useful.txt`, `agentic_controller/.rag_index/`,
  `one_shot/drafts/`.
- Docstrings cite a `DESIGN-NOTES.md` that does not exist; rationale is in
  `documentation/DOCUMENTATION.md`.

## Conventions that bite

- **Document types are discovered from disk, not registered in code.** Any
  `document_builder/` directory with a resolvable layout *and* a matching schema
  is a valid `--type`. `sorted(DOCUMENTS)` is the only accurate list — there are
  14; README names 9. Adding a type takes no code edit.
- **`ACTIVE` selects the live layout.** A one-line `ACTIVE` file naming
  `layout_N.py`, else `layout.py`. The Architect Agent writes `ACTIVE` only after
  `validate_layout` (`agentic_controller/architect.py:286`) builds the layout on
  blank data, and its sandbox refuses to overwrite an existing `layout.py` or
  base schema — repairs land in `layout_N.py` and `<type>_patched.json`.
- **`resolve_schema_path` prefers `<type>_patched.json`.** Where that sidecar
  exists, editing `<type>.json` is a silent no-op. Check first.
- **Output is enforced monochrome.** `html_engine/monochrome.py` rewrites colour
  on every route out (`Style.to_css`, `Style.raw`, raw `style=` attrs, the final
  `<style>` block) with no opt-out. Never "fix" colour in a layout, and never
  treat a colour difference from the scan as a verification defect.
- **Generated layouts are an exact A4 sheet** — 794×1123 px portrait or 1123×794
  landscape at 96 DPI. `document_builder/autolayout.py` fits the scan's ink
  extent inside a 10 mm margin using **one scale factor on both axes**, then
  centres it. Never fit width and height independently: that makes the page A4
  by distorting everything on it.
- **The translation skips are legacy-pipeline-only.** In `one_shot`, the prompt
  forbids all Devanagari and the editor's date panel handles BS↔AD. In the
  legacy pipeline they are load-bearing: Bikram Sambat dates convert locally
  via `nepali_datetime` (an LLM gets date arithmetic subtly wrong);
  `present`/`absent` are an OCR contract a layout branches on, so rewording one
  removes an element from the page; the `_np` half of a `_np`/`_en` pair stays
  scripted. Cache: `information_extraction/.translation_cache.json`, keyed on
  (model, kind, language, text).
- **`verifier.py`'s prompt and `documentation/verification-rules.md` are
  coupled.** `tests/test_verifier_prompt.py` asserts the doc mirrors the prompt's
  rules 1–5, so editing one without the other fails the suite.
- Rendered value fields carry `contenteditable="true"` and `data-field` — the
  write-back contract for the planned web editor. Do not strip them.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- Do not run `graphify label` unasked — it costs LLM tokens. `graphify update` renames drifted communities by hub name for free, which is usually good enough.
