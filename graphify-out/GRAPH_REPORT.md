# Graph Report - babu-documentation  (2026-08-06)

## Corpus Check
- 49 files · ~559,557 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 527 nodes · 1010 edges · 36 communities (22 shown, 14 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 1% AMBIGUOUS · INFERRED: 97 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e94999bd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- pipeline.py
- components/__init__.py
- Editable Nepali citizenship certificate (romanized test render)
- Component
- Land Ownership Registration Certificate (Laalpurja)
- html_engine/__init__.py
- Nepali Citizenship Certificate Template (canonical static render)
- Laalpurja certificate — editable master template
- Style
- "First make it work, then make it better"
- Laalpurja Base Render (output/png)
- LangGraph controller
- list.py
- rag_engine.py
- python-dotenv dependency
- spacer.py
- .to_css
- ._render_children
- .__add__
- route
- DocLayout-YOLO
- Segment Anything Model for document analysis
- Surya (datalab-to)
- CLAUDE.md
- architect.py
- models.py
- 1. Document Verification Rules
- Salvage record: `controller-old/` → `agentic_controller/`
- agentic_controller/__init__.py
- Ideal patching prompt composition
- Perfect-match VerificationReport example
- langchain-openai dependency
- pydantic dependency

## God Nodes (most connected - your core abstractions)
1. `Style` - 80 edges
2. `Component` - 62 edges
3. `build_laalpurja()` - 23 edges
4. `build_citizenship()` - 18 edges
5. `analyze_and_repair()` - 16 edges
6. `LabelValue` - 15 edges
7. `generate_resources()` - 14 edges
8. `digitize()` - 14 edges
9. `TableCell` - 14 edges
10. `Document` - 14 edges

## Surprising Connections (you probably didn't know these)
- `LangGraph controller` --references--> `langgraph dependency`  [INFERRED]
  documentation/DOCUMENTATION.md → requirements.txt
- `run_pipeline()` --calls--> `build_document()`  [EXTRACTED]
  agentic_controller/run.py → information_extraction/pipeline.py
- `field_row()` --references--> `Style`  [EXTRACTED]
  document_builder/citizenship/layout.py → html_engine/styles.py
- `multi_row()` --references--> `Style`  [EXTRACTED]
  document_builder/citizenship/layout.py → html_engine/styles.py
- `_address_block()` --calls--> `Style`  [EXTRACTED]
  document_builder/citizenship/layout.py → html_engine/styles.py

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

## Communities (36 total, 14 thin omitted)

### Community 0 - "pipeline.py"
Cohesion: 0.46
Nodes (5): build_data(), extract(), load_schema(), build_document(), digitize_document()

### Community 1 - "components/__init__.py"
Cohesion: 0.07
Nodes (41): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main(), build_laalpurja() (+33 more)

### Community 3 - "Component"
Cohesion: 0.09
Nodes (15): Component, Base class for all renderable document components. Parameters: style: Optional…, Append one or more child components. Returns self for chaining., Build the HTML attribute string for this element. Combines ``css_class``,…, AbsoluteBox, Card, Div, Grid (+7 more)

### Community 4 - "Land Ownership Registration Certificate (Laalpurja)"
Cohesion: 0.09
Nodes (31): Manual Laalpurja Screenshot (Reference Capture), Photograph and Right/Left Thumb Impression Cells, Land Ownership Certificate No. Field (4915149), Coat of Arms Placeholder Box, Fully English-Translated Field Labels, Footer Attestation Region (Printing done by / Print Date / Checked by), Ground-Truth Reference Baseline for Generated Renders, Laalpurja Header Region (Government of Nepal / Ministry of Land Reform) (+23 more)

### Community 7 - "html_engine/__init__.py"
Cohesion: 0.12
Nodes (18): ABC, Abstract base class for all HTML Document Engine components. Every renderable…, Image component for the HTML Document Engine., Table components: Table, TableRow, TableCell. Supports both simple table…, Document, Render a Document class to a full HTML string. The output is a self-contained…, render(), em() (+10 more)

### Community 8 - "Nepali Citizenship Certificate Template (canonical static render)"
Cohesion: 0.10
Nodes (24): आदित्य जोशी (Aditya Joshi) - certificate holder, Aditya Joshi Certificate Instance (Kathmandu DAO, no-shadow digital variant), Address Fields (Birth Place and Permanent Address as District + Municipality/VDC + Ward No.), Nepali Citizenship Certificate Template (canonical static render), Citizenship No. Line (22px bold, Devanagari district-office-year-serial format), Coat of Arms of Nepal Placeholder Box (120x120px, top-left), Details Block (870px wide right column of label/value flex rows), Devanagari Numeral Rendering Convention (०-९ for all numeric values) (+16 more)

### Community 9 - "Laalpurja certificate — editable master template"
Cohesion: 0.11
Nodes (28): Land Ownership Registration Certificate (laal.html rendering), Certificate identifiers: Certificate No. NM0000095, Evd. no. ML-series, B.S. dates २०८२/०४/१४, total area 4332.09 sq.m across 3 plots, Citizenship issuing office: जिल्ला प्रशासन कार्यालय, काठमाण्डौ, Nepali land vocabulary: आबादी/आवादी (cultivated), रैकर निजी (raikar private), एकलौटी (sole title), भिट/पाखो/बारी दोयम (land class), रोपनी area units, Landowner entity: उमा देवी चौलागाई (Uma Devi Chaulagain), Issuing authority: Land Revenue Office, साखु, काठमाण्डौ (Dept. of Land Reform and Management), 'None' literal artifact leaking into Register Page No./serial and transaction cells (unbound Python None serialized into HTML), Page style system: .page 1200px fixed-width white sheet, Times New Roman serif, 1px black borders, inline flexbox layout (+20 more)

### Community 10 - "Style"
Cohesion: 0.11
Nodes (13): Image, Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64., Link, Paragraph, Text components: Text, Heading, Paragraph, Link., Escape hatch: renders arbitrary HTML verbatim. Use sparingly — this bypasses…, Renders an anchor element ``<a>``. Parameters: content: The text content or… (+5 more)

### Community 13 - "Laalpurja Base Render (output/png)"
Cohesion: 0.15
Nodes (20): Certificate Number Field (4915149), Footer Region: Total Area, Print Date, Signatures, Header Region: Government of Nepal / Land Revenue Office, Identity Region: Photograph, Thumb Impression, Landowner Details, Latin-Script Transliterated Field Data, PNG Rasterization Output Stage (output/png directory), Laalpurja Base Render (output/png), Repaired Certificate Number Field (NM0000095) (+12 more)

### Community 15 - "LangGraph controller"
Cohesion: 0.05
Nodes (40): Adding a new document type, Arbitrary HTML attributes (`attrs`), Architecture, Babu Document Digitization: Technical Documentation, Component reference, Contenteditable output, Document builders, Future work (+32 more)

### Community 17 - "list.py"
Cohesion: 0.20
Nodes (7): ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList., Renders a list item ``<li>``. Parameters: content: String content or nested…, Renders an unordered list ``<ul>``. Parameters: items: List items — can be…, Renders an ordered list ``<ol>``. Parameters: items: List items — can be…, UnorderedList

### Community 20 - "rag_engine.py"
Cohesion: 0.10
Nodes (37): _tool_query_context(), build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python() (+29 more)

### Community 26 - "spacer.py"
Cohesion: 0.20
Nodes (5): HorizontalRule, PageBreak, Spacer and divider components., Horizontal rule (``<hr>``) divider. Parameters: style: Override styles (color,…, Renders a page break for print media.

### Community 27 - ".to_css"
Cohesion: 0.33
Nodes (3): Convert a Python attribute name to its CSS property equivalent., Serialize all non-None attributes into a CSS inline style string. Returns: A…, Return a full ``style="..."`` HTML attribute string, or an empty string if…

### Community 31 - "route"
Cohesion: 0.67
Nodes (3): route, index(), process()

### Community 39 - "architect.py"
Cohesion: 0.05
Nodes (76): analyze_and_repair(), _build_system_prompt(), current_layout_path(), _dispatch_tool(), generate_resources(), _image(), _load_rules(), _log_call() (+68 more)

### Community 40 - "models.py"
Cohesion: 0.14
Nodes (15): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, A single change to the extraction JSON schema., A single structural change to the document layout builder. (+7 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

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
- **72 isolated node(s):** `graphify`, `What is included`, `Setup`, `Run the full pipeline`, `Generate example documents` (+67 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

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