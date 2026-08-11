# Graph Report - babu-documentation  (2026-08-10)

## Corpus Check
- 93 files · ~797,502 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1018 nodes · 2063 edges · 84 communities (66 shown, 18 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 75 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `587c9397`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- translator.py
- test_components.py
- Editable Nepali citizenship certificate (romanized test render)
- html_engine/__init__.py
- base.py
- citizenship/layout.py
- test_translator.py
- test_styles.py
- Spacer
- laalpurja/layout.py
- test_command_sandbox.py
- run.py
- "First make it work, then make it better"
- test_registry_resolution.py
- prd.md
- Babu Document Digitization
- FlexRow
- Component
- required
- Image
- rag_engine.py
- Style
- Salvage record: `controller-old/` → `agentic_controller/`
- langgraph dependency
- python-dotenv dependency
- validate_layout
- text.py
- test_monochrome.py
- Any
- 43. Acceptance Criteria
- .__add__
- route
- DocLayout-YOLO
- Segment Anything Model for document analysis
- components/__init__.py
- verify
- Surya (datalab-to)
- Heading
- CLAUDE.md
- architect.py
- models.py
- 1. Document Verification Rules
- Text
- properties
- 37. MVP Scope
- run_all.py
- LabelValue
- items
- HTML document engine
- Babu task list / tooling backlog
- MultiFieldRow
- 44. Engineering Rules for the Agent
- .__init__
- .to_css
- Babu Document Digitization: Technical Documentation
- Agentic controller
- Future work
- Document builders
- 22. Properties Panel
- letter_no
- municipality
- office_name
- ref_no
- subject
- ward_chairperson_name
- ward_chairperson_title
- ward_no
- 5. Technology Requirements
- spacer.py
- district
- .save
- 3. Target User
- 8. Toolbar
- relationship_certificate.json
- 35. Non-Functional Requirements
- family_members
- PRD — Visual HTML Document Editing Engine
- 4. Core Design Principle
- agentic_controller/__init__.py
- Ideal patching prompt composition
- Perfect-match VerificationReport example
- langchain-openai dependency
- pydantic dependency

## God Nodes (most connected - your core abstractions)
1. `Style` - 135 edges
2. `Component` - 58 edges
3. `Text` - 50 edges
4. `Document` - 39 edges
5. `Spacer` - 34 edges
6. `LabelValue` - 32 edges
7. `FlexRow` - 32 edges
8. `PlaceholderBox` - 32 edges
9. `FlexCol` - 31 edges
10. `Div` - 28 edges

## Surprising Connections (you probably didn't know these)
- `_resources_exist()` --calls--> `resolve_schema_path()`  [INFERRED]
  agentic_controller/run.py → document_builder/resolver.py
- `digitize()` --calls--> `resolve_schema_path()`  [INFERRED]
  agentic_controller/run.py → document_builder/resolver.py
- `test_route_1_style_to_css()` --calls--> `Style`  [EXTRACTED]
  tests/test_monochrome.py → html_engine/styles.py
- `test_route_3_style_raw_escape_hatch()` --calls--> `Style`  [EXTRACTED]
  tests/test_monochrome.py → html_engine/styles.py
- `test_clone_removes_with_none()` --calls--> `Style`  [EXTRACTED]
  tests/test_styles.py → html_engine/styles.py

## Import Cycles
- None detected.

## Communities (84 total, 18 thin omitted)

### Community 0 - "translator.py"
Cohesion: 0.05
Nodes (59): _crop_to_page(), _page_metrics(), Path, render_png(), An unrecognized CSS property name reached ``Style``. Probably a typo., StyleWarning, build_data(), extract() (+51 more)

### Community 1 - "test_components.py"
Cohesion: 0.08
Nodes (31): Div, Generic block container rendered as a ``<div>``. The simplest building block —…, corner_box(), PlaceholderBox, Faint centred text behind the page content. Absolutely positioned and non-…, A labelled outline standing in for artwork that cannot be rendered. Renders a…, A placeholder pinned to one corner of the page — crest, QR block, stamp.…, Watermark (+23 more)

### Community 3 - "html_engine/__init__.py"
Cohesion: 0.11
Nodes (19): Card, Grid, GridItem, Layout components: FlexRow, FlexCol, AbsoluteBox, Div. These are generic…, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, CSS Grid item. Parameters: column_span: Number of columns this item spans (e.g.…, A styled container mimicking a paper card. Includes preset styles: background…, Placeholder components for document furniture the render cannot reproduce. A… (+11 more)

### Community 4 - "base.py"
Cohesion: 0.17
Nodes (11): ABC, coerce_child(), coerce_children(), Any, Abstract base class for all HTML Document Engine components. Every renderable…, Append one or more child components. Returns self for chaining. Accepts the…, Turn one constructor argument into a child component, or reject it. Containers…, Coerce an iterable of constructor arguments, dropping ``None``s. (+3 more)

### Community 5 - "citizenship/layout.py"
Cohesion: 0.23
Nodes (9): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main(), FieldGroup (+1 more)

### Community 6 - "test_translator.py"
Cohesion: 0.07
Nodes (44): Tests for the translation stage. ``information_extraction/translator.py`` sits…, A sentence and a field label want different instructions, so they are batched…, A district repeated down a table is one string, not twenty., A half-converted date prints a year that looks Gregorian and is not., The SEE certificate prints ``certificate_title_np`` on one line and…, Without the English sibling, that value is the only one on the page., A laalpurja's ``plots`` is a list of dicts; every row must be reached., ``<field>_meta`` and ``<field>_citations`` are provenance the extractor… (+36 more)

### Community 7 - "test_styles.py"
Cohesion: 0.08
Nodes (22): Tests for the open property bag that replaced the closed ``Style`` dataclass.…, Monochrome is enforced on the way out, including for unlisted props., The reported crash. Any valid CSS property must survive to the output., Both are deliberate, so neither should look like a typo., The trade for accepting anything: a misspelling is no longer a TypeError. It…, What ``main.py --strict`` relies on., A name CSS could never accept is a bug worth stopping for., CSS resolves duplicates last-one-wins, so ``margin`` emitted after ``margin-… (+14 more)

### Community 8 - "Spacer"
Cohesion: 0.17
Nodes (15): build_citizenship_back(), Any, build_see_certificate(), SEE Certificate Layout — document_builder/see_certificate/layout_1.py…, build_tax_clearance(), Tax Clearance Certificate Layout — document_builder/tax_clearance/layout_1.py…, FlexCol, Vertical flex container (``flex-direction: column``). Parameters: children:… (+7 more)

### Community 9 - "laalpurja/layout.py"
Cohesion: 0.30
Nodes (10): build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th(), _to_float() (+2 more)

### Community 10 - "test_command_sandbox.py"
Cohesion: 0.11
Nodes (30): _protected_originals(), Content of each protected file, or None if it does not exist., Undo any modification to a protected original. Returns what was restored., Gate write_file: inside the writable trees, and never *onto* an original.…, _restore_changed(), _snapshot(), _tool_execute_command(), _write_allowed() (+22 more)

### Community 11 - "run.py"
Cohesion: 0.12
Nodes (23): current_layout_path(), generate_resources(), main(), Create a layout builder and extraction schema for an unseen document type. This…, What the Architect Agent produced on one invocation., Human-readable one-screen summary, for the Phase 3 checkpoint., The layout that will actually be built — whatever ``ACTIVE`` names. This used…, RepairResult (+15 more)

### Community 13 - "test_registry_resolution.py"
Cohesion: 0.06
Nodes (72): _DocumentEntry, Any, The document registry: which types exist, and how to build each one.…, One document type's ``{"builder": ..., "schema": ...}``. ``schema`` is a path…, Document types discovered from the filesystem, resolved on access. Not cached.…, _Registry, active_layout_name(), active_layout_path() (+64 more)

### Community 14 - "prd.md"
Cohesion: 0.05
Nodes (36): 10. Canvas, 11. Page Model, 12. Element Model, 13. Text Element, 14. Image Element, 15. Shape Element, 16. Dynamic Field Element, 17. Selection System (+28 more)

### Community 15 - "Babu Document Digitization"
Cohesion: 0.17
Nodes (12): Babu Document Digitization, Build one document by hand, Full technical documentation, Generate example documents, Output is in English, Output is strictly black and white, Run the full pipeline, Setup (+4 more)

### Community 16 - "FlexRow"
Cohesion: 0.20
Nodes (11): build_citizenship_back(), _ea(), Any, build_letter(), _ea(), Any, AbsoluteBox, FlexRow (+3 more)

### Community 17 - "Component"
Cohesion: 0.16
Nodes (11): Component, Render all children to a concatenated HTML string., Render this component to an HTML string., Base class for all renderable document components. Parameters: style: Optional…, ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList., Renders a list item ``<li>``. Parameters: content: String content or nested… (+3 more)

### Community 18 - "required"
Cohesion: 0.14
Nodes (14): required, date, district, family_members, letter_no, main_text, municipality, office_name (+6 more)

### Community 19 - "Image"
Cohesion: 0.33
Nodes (4): Image, Image component for the HTML Document Engine., Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64.

### Community 20 - "rag_engine.py"
Cohesion: 0.10
Nodes (36): build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python(), _embed() (+28 more)

### Community 21 - "Style"
Cohesion: 0.13
Nodes (3): Any, An open set of CSS declarations. Any keyword is accepted and emitted as a CSS…, Style

### Community 22 - "Salvage record: `controller-old/` → `agentic_controller/`"
Cohesion: 0.33
Nodes (5): Behaviour to reproduce in Phase 2/3, Carried across, Deliberately dropped, Not indexed by RAG, Salvage record: `controller-old/` → `agentic_controller/`

### Community 25 - "validate_layout"
Cohesion: 0.20
Nodes (20): Check that a generated layout module is safe for the caller to use. Four gates,…, validate_layout(), _layout(), Path, Tests for ``architect.validate_layout`` — the gate that let the reported bug…, Blank probe data is the harsh case. A layout indexing a key the schema does not…, A property outside the known list is a cosmetic gap, not a reason to fail a…, Without a schema the builder is probed with ``{}``. (+12 more)

### Community 26 - "text.py"
Cohesion: 0.17
Nodes (7): Link, Paragraph, Text components: Text, Heading, Paragraph, Link., Escape hatch: renders arbitrary HTML verbatim. Use sparingly — this bypasses…, Renders an anchor element ``<a>``. Parameters: content: The text content or…, Block paragraph element rendered as ``<p>``. Parameters: content: The paragraph…, RawHTML

### Community 27 - "test_monochrome.py"
Cohesion: 0.07
Nodes (39): Build the HTML attribute string for this element. Combines ``css_class``,…, find_violations(), normalize_declarations(), normalize_html(), normalize_value(), Monochrome enforcement for the HTML Document Engine. Project rule: a rendered…, Surfaces go white, ink goes black., Rewrite every colour token in a single declaration's *value*. Parameters: prop:… (+31 more)

### Community 28 - "Any"
Cohesion: 0.28
Nodes (4): Any, Record one declaration, warning if the property looks misspelled., Iterate ``(python_name, value)`` for every set property., Return a copy with specific properties overridden. Passing ``None`` removes a…

### Community 29 - "43. Acceptance Criteria"
Cohesion: 0.10
Nodes (21): 43. Acceptance Criteria, AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07 (+13 more)

### Community 31 - "route"
Cohesion: 0.67
Nodes (3): route, index(), process()

### Community 34 - "components/__init__.py"
Cohesion: 0.23
Nodes (8): html_engine.components — All renderable component types., Table components: Table, TableRow, TableCell. Supports both simple table…, A full ``<table>`` element. Can be built from: - Explicit ``TableRow`` objects…, A single table cell (``<td>`` or ``<th>``). Parameters: content: Cell content —…, A table row (``<tr>``) containing one or more cells. Parameters: cells:…, Table, TableCell, TableRow

### Community 35 - "verify"
Cohesion: 0.36
Nodes (7): image_data_url(), main(), Path, Vision-model comparison of a source document against its rendered replica.…, Compare *source* against *rendered* and return a structured report., Validate a local raster image and encode it for a multimodal model message.…, verify()

### Community 37 - "Heading"
Cohesion: 0.32
Nodes (6): build_relationship_certificate(), _ea(), Any, Relationship Certificate Layout —…, Heading, Block heading element rendered as ``<h1>`` through ``<h6>``. Parameters:…

### Community 39 - "architect.py"
Cohesion: 0.12
Nodes (34): analyze_and_repair(), _build_system_prompt(), _dispatch_tool(), _image(), _load_rules(), _log_call(), _parse_contract(), Any (+26 more)

### Community 40 - "models.py"
Cohesion: 0.14
Nodes (17): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., Machine-readable result returned by the vision model. This is the contract the…, Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, A single change to the extraction JSON schema. (+9 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

### Community 42 - "Text"
Cohesion: 0.15
Nodes (17): build_transfer_certificate(), _ea(), Any, Transfer Certificate Layout — document_builder/transfer_certificate/layout_1.py…, Inline text element rendered as a ``<span>``. Parameters: content: The text…, Text, Document, A single page of output. Parameters: title: ``<title>`` text. page_width: Width… (+9 more)

### Community 43 - "properties"
Cohesion: 0.20
Nodes (10): description, type, description, type, properties, date, main_text, province (+2 more)

### Community 44 - "37. MVP Scope"
Cohesion: 0.25
Nodes (8): 37. MVP Scope, Canvas, Editor, Elements, Export, Interaction, Persistence, Properties

### Community 46 - "LabelValue"
Cohesion: 0.29
Nodes (9): build_income_certificate(), _ea(), _lv(), Any, Income Certificate Layout — document_builder/income_certificate/layout_1.py…, LabelValue, A single label–value row rendered as a flex container. The label is displayed…, The label is chrome; only the value is extracted data. (+1 more)

### Community 47 - "items"
Cohesion: 0.17
Nodes (12): items, properties, required, type, description, type, name, relation (+4 more)

### Community 48 - "HTML document engine"
Cohesion: 0.20
Nodes (10): Arbitrary HTML attributes (`attrs`), Component reference, Editable fields (`field=`), HTML document engine, Minimal example, Monochrome enforcement, Placeholders for un-renderable furniture, Rendering (+2 more)

### Community 49 - "Babu task list / tooling backlog"
Cohesion: 0.22
Nodes (9): Information extraction, Translation (`translator.py`), Donut (clovaai), Handwritten Nepali OCR model (TrOCR finetune, Tesseract), HTML abstraction engine over HTML/CSS, OCR JSON → HTML engine integration, Preprocessing engine (CamScanner-style rectification), Programmatic format building from received data (+1 more)

### Community 50 - "MultiFieldRow"
Cohesion: 0.25
Nodes (6): editable_attrs(), Attributes that make one rendered value editable in the browser. The ``data-…, MultiFieldRow, Field components: LabelValue pairs and FieldGroups. These are the workhorses…, A horizontal row containing multiple label–value pairs. Useful for rows like:…, test_editable_attrs_is_the_single_source_of_the_contract()

### Community 51 - "44. Engineering Rules for the Agent"
Cohesion: 0.25
Nodes (8): 44. Engineering Rules for the Agent, Rule 1 — Document model first, Rule 2 — Single source of truth, Rule 3 — Components are renderers, Rule 4 — Commands modify state, Rule 5 — History is operation-based, Rule 6 — No premature complexity, Rule 7 — Extensibility

### Community 53 - ".to_css"
Cohesion: 0.25
Nodes (5): _css_name(), Map a Python keyword to its CSS property name. ``font_size`` -> ``font-size``.…, Set properties in emission order: known first, then unknown. Known properties…, Serialize to an inline CSS declaration string. Colours are normalized to black-…, Return a full ``style="..."`` attribute, or ``""`` if empty.

### Community 54 - "Babu Document Digitization: Technical Documentation"
Cohesion: 0.33
Nodes (4): Architecture, Babu Document Digitization: Technical Documentation, Building one document by hand, Setup and common commands

### Community 55 - "Agentic controller"
Cohesion: 0.33
Nodes (6): Agentic controller, Architect Agent (`architect.py`), Pipeline flow (`run.py`), RAG engine (`rag_engine.py`), Rendering (`rendering.py`), Verification (`verifier.py`)

### Community 56 - "Future work"
Cohesion: 0.40
Nodes (5): Future work, OCR tooling candidates under evaluation, PDF export, Visual editor, HTML editor for human verification and block insertion

### Community 57 - "Document builders"
Cohesion: 0.50
Nodes (4): Adding a new document type, Contenteditable output, Document builders, Which layout is live: the `ACTIVE` pointer

### Community 58 - "22. Properties Panel"
Cohesion: 0.40
Nodes (5): 22. Properties Panel, Advanced, Appearance, Position, Text

### Community 59 - "letter_no"
Cohesion: 0.67
Nodes (3): description, type, letter_no

### Community 60 - "municipality"
Cohesion: 0.67
Nodes (3): description, type, municipality

### Community 61 - "office_name"
Cohesion: 0.67
Nodes (3): description, type, office_name

### Community 62 - "ref_no"
Cohesion: 0.67
Nodes (3): ref_no, description, type

### Community 63 - "subject"
Cohesion: 0.67
Nodes (3): subject, description, type

### Community 64 - "ward_chairperson_name"
Cohesion: 0.67
Nodes (3): ward_chairperson_name, description, type

### Community 65 - "ward_chairperson_title"
Cohesion: 0.67
Nodes (3): ward_chairperson_title, description, type

### Community 66 - "ward_no"
Cohesion: 0.67
Nodes (3): ward_no, description, type

### Community 67 - "5. Technology Requirements"
Cohesion: 0.40
Nodes (5): 5. Technology Requirements, Dragging and interaction, Frontend, Rich text, State management

### Community 68 - "spacer.py"
Cohesion: 0.29
Nodes (5): HorizontalRule, PageBreak, Spacer and divider components., Horizontal rule (``<hr>``) divider. Parameters: style: Override styles (color,…, Renders a page break for print media.

### Community 69 - "district"
Cohesion: 0.67
Nodes (3): description, type, district

### Community 70 - ".save"
Cohesion: 0.40
Nodes (3): Path, Write the rendered HTML to *path*, creating parent directories. Returns the…, Render to a complete, self-contained HTML string.

### Community 71 - "3. Target User"
Cohesion: 0.50
Nodes (4): 3. Target User, Document recreation, Future OCR workflow, Template creation

### Community 72 - "8. Toolbar"
Cohesion: 0.50
Nodes (4): 8. Toolbar, Canvas controls, Document controls, Editing controls

### Community 73 - "relationship_certificate.json"
Cohesion: 0.50
Nodes (3): $schema, title, type

### Community 74 - "35. Non-Functional Requirements"
Cohesion: 0.67
Nodes (3): 35. Non-Functional Requirements, Browser, Performance

### Community 75 - "family_members"
Cohesion: 0.67
Nodes (3): description, type, family_members

## Knowledge Gaps
- **200 isolated node(s):** `$schema`, `title`, `type`, `type`, `description` (+195 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style` to `translator.py`, `test_components.py`, `html_engine/__init__.py`, `base.py`, `citizenship/layout.py`, `test_styles.py`, `Spacer`, `laalpurja/layout.py`, `FlexRow`, `Component`, `Image`, `text.py`, `test_monochrome.py`, `Any`, `.__add__`, `components/__init__.py`, `Heading`, `Text`, `LabelValue`, `MultiFieldRow`, `.__init__`, `.to_css`, `spacer.py`?**
  _High betweenness centrality (0.307) - this node is a cross-community bridge._
- **Why does `active_layout_path()` connect `test_registry_resolution.py` to `run.py`, `architect.py`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `resolve_schema_path()` connect `test_registry_resolution.py` to `run.py`, `architect.py`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Style` (e.g. with `Component` and `FieldGroup`) actually correct?**
  _`Style` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Component` (e.g. with `Text` and `Style`) actually correct?**
  _`Component` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Text` (e.g. with `Component` and `PlaceholderBox`) actually correct?**
  _`Text` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Document` (e.g. with `Component` and `Style`) actually correct?**
  _`Document` has 2 INFERRED edges - model-reasoned connections that need verification._