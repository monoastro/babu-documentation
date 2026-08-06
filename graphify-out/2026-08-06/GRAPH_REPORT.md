# Graph Report - babu-documentation  (2026-08-06)

## Corpus Check
- 57 files · ~563,928 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 616 nodes · 1129 edges · 52 communities (32 shown, 20 thin omitted)
- Extraction: 88% EXTRACTED · 11% INFERRED · 1% AMBIGUOUS · INFERRED: 128 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7c33e4ed`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- graph.py
- citizenship/layout.py
- Editable Nepali citizenship certificate (romanized test render)
- grid.py
- Land Ownership Registration Certificate (Laalpurja)
- build_laalpurja
- VerificationReport
- html_engine/__init__.py
- Nepali Citizenship Certificate Template (canonical static render)
- Laalpurja certificate — editable master template
- text.py
- BaseModel
- "First make it work, then make it better"
- Laalpurja Base Render (output/png)
- VerificationReport
- LangGraph controller
- spacer.py
- Component
- Print media stylesheet (@media print page rules)
- components/__init__.py
- rag_engine.py
- Any
- document_verifier.py
- python-dotenv dependency
- Style
- .to_css
- png_renderer.py
- ._render_children
- .__add__
- route
- DocLayout-YOLO
- Segment Anything Model for document analysis
- Surya (datalab-to)
- analyze_and_repair
- CLAUDE.md
- architect.py
- agentic_controller/models.py
- 1. Document Verification Rules
- Controller — Document Verification, Repair & LangGraph Pipeline
- verify
- controller-old/models.py
- agentic_controller/run.py
- Salvage record: `controller-old/` → `agentic_controller/`
- SchemaPatch
- agentic_controller/__init__.py
- Ideal patching prompt composition
- Perfect-match VerificationReport example
- langchain-openai dependency
- pydantic dependency

## God Nodes (most connected - your core abstractions)
1. `Style` - 79 edges
2. `Component` - 62 edges
3. `build_laalpurja()` - 23 edges
4. `build_citizenship()` - 18 edges
5. `analyze_and_repair()` - 16 edges
6. `build_graph()` - 15 edges
7. `generate_resources()` - 14 edges
8. `digitize()` - 14 edges
9. `PipelineState` - 14 edges
10. `LabelValue` - 14 edges

## Surprising Connections (you probably didn't know these)
- `PipelineState` --uses--> `RepairPlan`  [INFERRED]
  controller-old/graph.py → agentic_controller/models.py
- `_lv()` --calls--> `LabelValue`  [INFERRED]
  document_builder/laalpurja/layout.py → html_engine/components/field.py
- `_th()` --calls--> `TableCell`  [INFERRED]
  document_builder/laalpurja/layout.py → html_engine/components/table.py
- `_td()` --calls--> `TableCell`  [INFERRED]
  document_builder/laalpurja/layout.py → html_engine/components/table.py
- `build_laalpurja()` --calls--> `FieldGroup`  [INFERRED]
  document_builder/laalpurja/layout.py → html_engine/components/field.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fixed-position placeholder boxes plus header and details block compose the certificate page layout** — output_html_citizenship_citizenship_coatofarmsbox, output_html_citizenship_citizenship_officesealbox, output_html_citizenship_citizenship_photographbox, output_html_citizenship_citizenship_headersection, output_html_citizenship_citizenship_detailsblock, output_html_citizenship_citizenship_pagestylesystem [EXTRACTED 1.00]
- **Five near-duplicate renderings of the same laalpurja certificate template (NM0000095, 3 plots, 4332.09 sq.m), differing only in numeral script, evidence-number digits, and fill artifacts** — output_html_laalpurja_laal_certificate_template, output_html_laalpurja_laalpurja_certificate_template, output_html_laalpurja_laalpurja_repaired_certificate_template, output_html_laalpurja_output_certificate_template, output_html_laalpurja_redpaper_certificate_template [INFERRED 0.85]
- **Header + identity block + plot table + footer compose the full certificate page layout** — output_html_laalpurja_laalpurja_headersection, output_html_laalpurja_laalpurja_identityblock, output_html_laalpurja_laalpurja_plottable, output_html_laalpurja_laalpurja_footersection [EXTRACTED 1.00]
- **Rendering defect cluster: 'None' literals, numeral/transliteration drift, stray PF certificate-number prefix, inconsistent District/VDC joining** — output_html_laalpurja_laal_nonefillartifact, output_html_laalpurja_laalpurja_repaired_numeraltranslitvariance, output_html_laalpurja_laalpurja_repaired_certnoprefixanomaly, output_html_laalpurja_output_districtvdcformatting [INFERRED 0.85]
- **Base vs Repaired Render Comparison: script change with layout regressions** — output_png_laalpurja_render, output_png_laalpurja_repaired_render, output_png_laalpurja_repaired_devanagariscriptdata, output_png_laalpurja_repaired_layoutoverlapdefect, output_png_laalpurja_repaired_labelwrappingdefect [INFERRED 0.85]
- **Certificate Region Layout: header, identity block, transaction table, footer** — output_png_laalpurja_headerregion, output_png_laalpurja_identityregion, output_png_laalpurja_transactiontable, output_png_laalpurja_footerregion, output_png_laalpurja_repaired_certificatetemplate [EXTRACTED 1.00]
- **PNG Output Stage Artifacts and Styling System** — output_png_laalpurja_pngoutputstage, output_png_laalpurja_render, output_png_laalpurja_repaired_render, output_png_laalpurja_tabularstylesystem [INFERRED 0.85]
- **Shared Nepali Official Document Chrome: Coat of Arms, Government Header Stack, Seal and Photograph Placeholders** — output_png_manual_laal_screenshot_headerregion, output_png_manual_laal_screenshot_coatofarmsplaceholder, output_png_output_headerregion, output_png_output_coatofarmsplaceholder, output_png_output_roundofficesealplaceholder, output_png_output_photographplaceholder [INFERRED 0.85]
- **Ground-Truth Manual Capture vs Pipeline-Generated Render Comparison Loop** — output_png_manual_laal_screenshot, output_png_manual_laal_screenshot_groundtruthbaseline, output_png_output, output_png_output_htmltopngrenderstage, output_png_output_trailingwhitespaceartifact [INFERRED 0.75]
- **Citizenship Identity Field Family: Personal Details, Parentage, Spouse and Bikram Sambat Dates in Devanagari** — output_png_output_personaldetailsgrid, output_png_output_parentageblock, output_png_output_spouseblock, output_png_output_bikramsambatdatefields, output_png_output_devanagarivaluerendering, output_png_output_nullvaluerenderingartifact [EXTRACTED 1.00]

## Communities (52 total, 20 thin omitted)

### Community 0 - "graph.py"
Cohesion: 0.08
Nodes (43): analyze_repair(), apply_edits(), apply_repair(), build_document(), build_graph(), check_resources(), compile_graph(), extract_data() (+35 more)

### Community 1 - "citizenship/layout.py"
Cohesion: 0.14
Nodes (18): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main(), FieldGroup (+10 more)

### Community 3 - "grid.py"
Cohesion: 0.09
Nodes (13): AbsoluteBox, Card, Div, FlexRow, Grid, GridItem, Layout components: FlexRow, FlexCol, AbsoluteBox, Div. These are generic…, Absolutely positioned container. Use for elements that need precise pixel… (+5 more)

### Community 4 - "Land Ownership Registration Certificate (Laalpurja)"
Cohesion: 0.09
Nodes (31): Manual Laalpurja Screenshot (Reference Capture), Photograph and Right/Left Thumb Impression Cells, Land Ownership Certificate No. Field (4915149), Coat of Arms Placeholder Box, Fully English-Translated Field Labels, Footer Attestation Region (Printing done by / Print Date / Checked by), Ground-Truth Reference Baseline for Generated Renders, Laalpurja Header Region (Government of Nepal / Ministry of Land Reform) (+23 more)

### Community 5 - "build_laalpurja"
Cohesion: 0.25
Nodes (11): Document, build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th() (+3 more)

### Community 7 - "html_engine/__init__.py"
Cohesion: 0.15
Nodes (14): Document, Render a Document class to a full HTML string. The output is a self-contained…, render(), em(), pct(), pt(), px(), Style dataclass for the HTML Document Engine. Captures all CSS properties… (+6 more)

### Community 8 - "Nepali Citizenship Certificate Template (canonical static render)"
Cohesion: 0.10
Nodes (24): आदित्य जोशी (Aditya Joshi) - certificate holder, Aditya Joshi Certificate Instance (Kathmandu DAO, no-shadow digital variant), Address Fields (Birth Place and Permanent Address as District + Municipality/VDC + Ward No.), Nepali Citizenship Certificate Template (canonical static render), Citizenship No. Line (22px bold, Devanagari district-office-year-serial format), Coat of Arms of Nepal Placeholder Box (120x120px, top-left), Details Block (870px wide right column of label/value flex rows), Devanagari Numeral Rendering Convention (०-९ for all numeric values) (+16 more)

### Community 9 - "Laalpurja certificate — editable master template"
Cohesion: 0.11
Nodes (28): Land Ownership Registration Certificate (laal.html rendering), Certificate identifiers: Certificate No. NM0000095, Evd. no. ML-series, B.S. dates २०८२/०४/१४, total area 4332.09 sq.m across 3 plots, Citizenship issuing office: जिल्ला प्रशासन कार्यालय, काठमाण्डौ, Nepali land vocabulary: आबादी/आवादी (cultivated), रैकर निजी (raikar private), एकलौटी (sole title), भिट/पाखो/बारी दोयम (land class), रोपनी area units, Landowner entity: उमा देवी चौलागाई (Uma Devi Chaulagain), Issuing authority: Land Revenue Office, साखु, काठमाण्डौ (Dept. of Land Reform and Management), 'None' literal artifact leaking into Register Page No./serial and transaction cells (unbound Python None serialized into HTML), Page style system: .page 1200px fixed-width white sheet, Times New Roman serif, 1px black borders, inline flexbox layout (+20 more)

### Community 10 - "text.py"
Cohesion: 0.12
Nodes (9): Heading, Link, Paragraph, Text components: Text, Heading, Paragraph, Link., Escape hatch: renders arbitrary HTML verbatim. Use sparingly — this bypasses…, Renders an anchor element ``<a>``. Parameters: content: The text content or…, Block heading element rendered as ``<h1>`` through ``<h6>``. Parameters:…, Block paragraph element rendered as ``<p>``. Parameters: content: The paragraph… (+1 more)

### Community 13 - "Laalpurja Base Render (output/png)"
Cohesion: 0.15
Nodes (20): Certificate Number Field (4915149), Footer Region: Total Area, Print Date, Signatures, Header Region: Government of Nepal / Land Revenue Office, Identity Region: Photograph, Thumb Impression, Landowner Details, Latin-Script Transliterated Field Data, PNG Rasterization Output Stage (output/png directory), Laalpurja Base Render (output/png), Repaired Certificate Number Field (NM0000095) (+12 more)

### Community 15 - "LangGraph controller"
Cohesion: 0.04
Nodes (45): Adding a new document type, Arbitrary HTML attributes (`attrs`), Architecture, Babu Document Digitization: Technical Documentation, Component reference, Contenteditable output, Document builders, Future work (+37 more)

### Community 16 - "spacer.py"
Cohesion: 0.16
Nodes (7): HorizontalRule, PageBreak, Spacer and divider components., Empty vertical space with a fixed height. Parameters: height: CSS height value…, Horizontal rule (``<hr>``) divider. Parameters: style: Override styles (color,…, Renders a page break for print media., Spacer

### Community 17 - "Component"
Cohesion: 0.16
Nodes (12): ABC, Component, Abstract base class for all HTML Document Engine components. Every renderable…, Base class for all renderable document components. Parameters: style: Optional…, Append one or more child components. Returns self for chaining., ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList. (+4 more)

### Community 19 - "components/__init__.py"
Cohesion: 0.23
Nodes (8): html_engine.components — All renderable component types., Table components: Table, TableRow, TableCell. Supports both simple table…, A full ``<table>`` element. Can be built from: - Explicit ``TableRow`` objects…, A single table cell (``<td>`` or ``<th>``). Parameters: content: Cell content —…, A table row (``<tr>``) containing one or more cells. Parameters: cells:…, Table, TableCell, TableRow

### Community 20 - "rag_engine.py"
Cohesion: 0.10
Nodes (37): _tool_query_context(), build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python() (+29 more)

### Community 23 - "document_verifier.py"
Cohesion: 0.46
Nodes (7): Discrepancy, main(), png_data_url(), BaseModel, Path, VerificationReport, verify()

### Community 26 - "Style"
Cohesion: 0.15
Nodes (8): Build the HTML attribute string for this element. Combines ``css_class``,…, Image, Image component for the HTML Document Engine., Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64., Immutable-ish style descriptor that maps 1:1 to CSS properties. Any attribute…, Return a copy of this Style with specific fields overridden. Usage:: base =…, Style

### Community 27 - ".to_css"
Cohesion: 0.33
Nodes (3): Convert a Python attribute name to its CSS property equivalent., Serialize all non-None attributes into a CSS inline style string. Returns: A…, Return a full ``style="..."`` HTML attribute string, or an empty string if…

### Community 28 - "png_renderer.py"
Cohesion: 0.60
Nodes (4): Path, Render html to a PNG via headless Chrome/Chromium. Chrome/Chromium executable…, render_png(), test()

### Community 31 - "route"
Cohesion: 0.67
Nodes (3): route, index(), process()

### Community 37 - "analyze_and_repair"
Cohesion: 0.16
Nodes (18): analyze_and_repair(), generate_resources(), _image(), main(), next_layout_path(), _parse_contract(), Path, Create a layout builder and extraction schema for an unseen document type. This… (+10 more)

### Community 39 - "architect.py"
Cohesion: 0.14
Nodes (28): _build_system_prompt(), _dispatch_tool(), _load_rules(), _log_call(), Any, The Architect Agent — autonomous layout and schema generation. Phase 2 of the…, Check that a written schema is valid JSON with the keys the extractor needs.…, Assemble the system prompt, with the verification rules embedded. (+20 more)

### Community 40 - "agentic_controller/models.py"
Cohesion: 0.14
Nodes (17): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., Machine-readable result returned by the vision model. This is the contract the…, Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, A single change to the extraction JSON schema. (+9 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

### Community 42 - "Controller — Document Verification, Repair & LangGraph Pipeline"
Cohesion: 0.15
Nodes (12): 1. Verify a document, 2. Repair a document (standalone), Architecture, Contenteditable HTML output, Controller — Document Verification, Repair & LangGraph Pipeline, Design choices, Future: visual editor, Individual commands (+4 more)

### Community 43 - "verify"
Cohesion: 0.36
Nodes (7): main(), png_data_url(), Path, Vision-model comparison of a source document against its rendered replica.…, Validate a local PNG and encode it for a multimodal model message., Compare *source* against *rendered* and return a structured report., verify()

### Community 44 - "controller-old/models.py"
Cohesion: 0.28
Nodes (8): LayoutPatch, BaseModel, Pydantic models for the layout-repair pipeline. These define the structured…, A single change to the extraction JSON schema., A single structural change to the document layout builder., The full proposal returned by the analysis LLM call., RepairPlan, SchemaPatch

### Community 45 - "agentic_controller/run.py"
Cohesion: 0.14
Nodes (21): current_layout_path(), Return the schema the pipeline should actually extract with. Prefers a…, Return the highest-numbered existing layout, or ``layout.py``, or None., resolve_schema_path(), Path, render_png(), _collect_decision(), _collect_user_concerns() (+13 more)

### Community 47 - "Salvage record: `controller-old/` → `agentic_controller/`"
Cohesion: 0.33
Nodes (5): Behaviour to reproduce in Phase 2/3, Carried across, Deliberately dropped, Not indexed by RAG, Salvage record: `controller-old/` → `agentic_controller/`

## Ambiguous Edges - Review These
- `@media print Rules (white background, no box-shadow, #444 border, page-break-after, .no-print hidden)` → `Template Instantiation Pattern (one shared markup skeleton re-rendered per person; only field values and district differ)`  [AMBIGUOUS]
  output/html/citizenship/citizenship.html · relation: conceptually_related_to
- `Missing Value Sentinels (literal 'None' and 'XXX' leaking into rendered output)` → `Pratik Pokharel Certificate Instance (Gulmi DAO)`  [AMBIGUOUS]
  output/html/citizenship/pratik.html · relation: conceptually_related_to
- `Certificate identifiers: Certificate No. NM0000095, Evd. no. ML-series, B.S. dates २०८२/०४/१४, total area 4332.09 sq.m across 3 plots` → `Certificate No. anomaly in repaired variant: 'PF002728503 NM0000095' (extra PF prefix not present in sibling renderings)`  [AMBIGUOUS]
  output/html/laalpurja/laalpurja_repaired.html · relation: references
- `Certificate Number Field (4915149)` → `Repaired Certificate Number Field (NM0000095)`  [AMBIGUOUS]
  output/png/laalpurja_repaired.png · relation: shares_data_with
- `Devanagari Script Field Data and Nepali Numerals` → `Layout Overlap Defect in Identity Region`  [AMBIGUOUS]
  output/png/laalpurja_repaired.png · relation: rationale_for
- `Devanagari Script Field Data and Nepali Numerals` → `Repair Pipeline Stage (unicode/script restoration variant)`  [AMBIGUOUS]
  output/png/laalpurja_repaired.png · relation: rationale_for
- `Manual Laalpurja Screenshot (Reference Capture)` → `HTML-Template-to-PNG Render Pipeline Stage`  [AMBIGUOUS]
  output/png/manual_laal_screenshot.png · relation: conceptually_related_to
- `Ground-Truth Reference Baseline for Generated Renders` → `Generated Pipeline Render Output (output.png)`  [AMBIGUOUS]
  output/png/manual_laal_screenshot.png · relation: rationale_for
- `Ground-Truth Reference Baseline for Generated Renders` → `Synthetic PII-Bearing Identity Document Sample`  [AMBIGUOUS]
  output/png/output.png · relation: conceptually_related_to

## Knowledge Gaps
- **83 isolated node(s):** `Carried across`, `Deliberately dropped`, `Behaviour to reproduce in Phase 2/3`, `Not indexed by RAG`, `1.1 Expected transformations — never flag these` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `@media print Rules (white background, no box-shadow, #444 border, page-break-after, .no-print hidden)` and `Template Instantiation Pattern (one shared markup skeleton re-rendered per person; only field values and district differ)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Missing Value Sentinels (literal 'None' and 'XXX' leaking into rendered output)` and `Pratik Pokharel Certificate Instance (Gulmi DAO)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Certificate identifiers: Certificate No. NM0000095, Evd. no. ML-series, B.S. dates २०८२/०४/१४, total area 4332.09 sq.m across 3 plots` and `Certificate No. anomaly in repaired variant: 'PF002728503 NM0000095' (extra PF prefix not present in sibling renderings)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Certificate Number Field (4915149)` and `Repaired Certificate Number Field (NM0000095)`?**
  _Edge tagged AMBIGUOUS (relation: shares_data_with) - confidence is low._
- **What is the exact relationship between `Devanagari Script Field Data and Nepali Numerals` and `Layout Overlap Defect in Identity Region`?**
  _Edge tagged AMBIGUOUS (relation: rationale_for) - confidence is low._
- **What is the exact relationship between `Devanagari Script Field Data and Nepali Numerals` and `Repair Pipeline Stage (unicode/script restoration variant)`?**
  _Edge tagged AMBIGUOUS (relation: rationale_for) - confidence is low._
- **What is the exact relationship between `Manual Laalpurja Screenshot (Reference Capture)` and `HTML-Template-to-PNG Render Pipeline Stage`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._