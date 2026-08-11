# Graph Report - babu-documentation  (2026-08-11)

## Corpus Check
- 93 files · ~796,472 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1019 nodes · 2049 edges · 81 communities (64 shown, 17 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 78 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3b199335`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run.py
- test_components.py
- Editable Nepali citizenship certificate (romanized test render)
- grid.py
- base.py
- citizenship/layout.py
- test_translator.py
- Style
- translator.py
- laalpurja/layout.py
- test_command_sandbox.py
- analyze_and_repair
- "First make it work, then make it better"
- test_registry_resolution.py
- prd.md
- Babu Document Digitization
- Spacer
- Component
- required
- Image
- rag_engine.py
- MultiFieldRow
- Salvage record: `controller-old/` → `agentic_controller/`
- langgraph dependency
- python-dotenv dependency
- validate_layout
- components/__init__.py
- test_monochrome.py
- Any
- 43. Acceptance Criteria
- Text
- route
- DocLayout-YOLO
- Segment Anything Model for document analysis
- html_engine/__init__.py
- .header
- Surya (datalab-to)
- FlexCol
- CLAUDE.md
- architect.py
- models.py
- 1. Document Verification Rules
- Document
- properties
- 37. MVP Scope
- run_all.py
- LabelValue
- items
- HTML document engine
- Babu task list / tooling backlog
- 44. Engineering Rules for the Agent
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
3. `Text` - 48 edges
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
- `main()` --calls--> `resolve_schema_path()`  [EXTRACTED]
  agentic_controller/architect.py → document_builder/resolver.py

## Import Cycles
- None detected.

## Communities (81 total, 17 thin omitted)

### Community 0 - "run.py"
Cohesion: 0.06
Nodes (51): _crop_to_page(), _page_metrics(), Path, render_png(), _collect_decision(), _collect_user_concerns(), digitize(), main() (+43 more)

### Community 1 - "test_components.py"
Cohesion: 0.11
Nodes (27): build_see_certificate(), SEE Certificate Layout — document_builder/see_certificate/layout_1.py…, Div, Generic block container rendered as a ``<div>``. The simplest building block —…, corner_box(), PlaceholderBox, The signature cluster that closes an official letter. Stacks, top to bottom:…, A labelled outline standing in for artwork that cannot be rendered. Renders a… (+19 more)

### Community 3 - "grid.py"
Cohesion: 0.15
Nodes (8): Card, Grid, GridItem, Any, Layout components: FlexRow, FlexCol, AbsoluteBox, Div. These are generic…, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, CSS Grid item. Parameters: column_span: Number of columns this item spans (e.g.…, A styled container mimicking a paper card. Includes preset styles: background…

### Community 4 - "base.py"
Cohesion: 0.12
Nodes (15): ABC, coerce_child(), coerce_children(), editable_attrs(), Any, Abstract base class for all HTML Document Engine components. Every renderable…, Append one or more child components. Returns self for chaining., Turn one constructor argument into a child component, or reject it. Components… (+7 more)

### Community 5 - "citizenship/layout.py"
Cohesion: 0.42
Nodes (7): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main()

### Community 6 - "test_translator.py"
Cohesion: 0.07
Nodes (44): Tests for the translation stage. ``information_extraction/translator.py`` sits…, A sentence and a field label want different instructions, so they are batched…, A district repeated down a table is one string, not twenty., A half-converted date prints a year that looks Gregorian and is not., The SEE certificate prints ``certificate_title_np`` on one line and…, Without the English sibling, that value is the only one on the page., A laalpurja's ``plots`` is a list of dicts; every row must be reached., ``<field>_meta`` and ``<field>_citations`` are provenance the extractor… (+36 more)

### Community 7 - "Style"
Cohesion: 0.08
Nodes (26): An open set of CSS declarations. Any keyword is accepted and emitted as a CSS…, Return a new Style with *other*'s declarations overriding this one's. ``raw``…, Shorthand for ``merge``: ``combined = style_a + style_b``., Style, Tests for the open property bag that replaced the closed ``Style`` dataclass.…, Monochrome is enforced on the way out, including for unlisted props., The reported crash. Any valid CSS property must survive to the output., Both are deliberate, so neither should look like a typo. (+18 more)

### Community 8 - "translator.py"
Cohesion: 0.11
Nodes (28): _apply(), bs_to_ad(), _cache_key(), _collect(), _has_letters(), _is_ascii(), _is_meta_key(), _load_cache() (+20 more)

### Community 9 - "laalpurja/layout.py"
Cohesion: 0.13
Nodes (16): build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th(), _to_float() (+8 more)

### Community 10 - "test_command_sandbox.py"
Cohesion: 0.11
Nodes (30): _protected_originals(), Content of each protected file, or None if it does not exist., Undo any modification to a protected original. Returns what was restored., Gate write_file: inside the writable trees, and never *onto* an original.…, _restore_changed(), _snapshot(), _tool_execute_command(), _write_allowed() (+22 more)

### Community 11 - "analyze_and_repair"
Cohesion: 0.16
Nodes (17): analyze_and_repair(), _build_system_prompt(), current_layout_path(), generate_resources(), _image(), _load_rules(), main(), Path (+9 more)

### Community 13 - "test_registry_resolution.py"
Cohesion: 0.06
Nodes (72): _DocumentEntry, Any, The document registry: which types exist, and how to build each one.…, One document type's ``{"builder": ..., "schema": ...}``. ``schema`` and…, Document types discovered from the filesystem, resolved on access. Deliberately…, _Registry, active_layout_name(), active_layout_path() (+64 more)

### Community 14 - "prd.md"
Cohesion: 0.05
Nodes (36): 10. Canvas, 11. Page Model, 12. Element Model, 13. Text Element, 14. Image Element, 15. Shape Element, 16. Dynamic Field Element, 17. Selection System (+28 more)

### Community 15 - "Babu Document Digitization"
Cohesion: 0.17
Nodes (12): Babu Document Digitization, Build one document by hand, Full technical documentation, Generate example documents, Output is in English, Output is strictly black and white, Run the full pipeline, Setup (+4 more)

### Community 16 - "Spacer"
Cohesion: 0.14
Nodes (18): build_citizenship_back(), _ea(), Any, build_citizenship_back(), Any, build_letter(), _ea(), Any (+10 more)

### Community 17 - "Component"
Cohesion: 0.16
Nodes (11): Component, Render all children to a concatenated HTML string., Render this component to an HTML string., Base class for all renderable document components. Parameters: style: Optional…, ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList., Renders a list item ``<li>``. Parameters: content: String content or nested… (+3 more)

### Community 18 - "required"
Cohesion: 0.14
Nodes (14): required, date, district, family_members, letter_no, main_text, municipality, office_name (+6 more)

### Community 19 - "Image"
Cohesion: 0.40
Nodes (3): Image, Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64.

### Community 20 - "rag_engine.py"
Cohesion: 0.13
Nodes (32): build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python(), _embed() (+24 more)

### Community 21 - "MultiFieldRow"
Cohesion: 0.40
Nodes (3): MultiFieldRow, Any, A horizontal row containing multiple label–value pairs. Useful for rows like:…

### Community 22 - "Salvage record: `controller-old/` → `agentic_controller/`"
Cohesion: 0.33
Nodes (5): Behaviour to reproduce in Phase 2/3, Carried across, Deliberately dropped, Not indexed by RAG, Salvage record: `controller-old/` → `agentic_controller/`

### Community 25 - "validate_layout"
Cohesion: 0.20
Nodes (20): Check that a generated layout module is safe for the caller to use. Four gates,…, validate_layout(), _layout(), Path, Tests for ``architect.validate_layout`` — the gate that let the reported bug…, Blank probe data is the harsh case. A layout indexing a key the schema does not…, A property outside the known list is a cosmetic gap, not a reason to fail a…, Without a schema the builder is probed with ``{}``. (+12 more)

### Community 26 - "components/__init__.py"
Cohesion: 0.14
Nodes (8): html_engine.components — All renderable component types., Link, Paragraph, Text components: Text, Heading, Paragraph, Link., Escape hatch: renders arbitrary HTML verbatim. Use sparingly — this bypasses…, Renders an anchor element ``<a>``. Parameters: content: The text content or…, Block paragraph element rendered as ``<p>``. Parameters: content: The paragraph…, RawHTML

### Community 27 - "test_monochrome.py"
Cohesion: 0.06
Nodes (43): Build the HTML attribute string for this element. Combines ``css_class``,…, find_violations(), normalize_declarations(), normalize_html(), normalize_value(), Monochrome enforcement for the HTML Document Engine. Project rule: a rendered…, Rewrite every colour token in a single declaration's *value*. Parameters: prop:…, Rewrite colours across a CSS fragment. Works both on an inline declaration list… (+35 more)

### Community 28 - "Any"
Cohesion: 0.22
Nodes (5): Any, Record one declaration, warning if the property looks misspelled., Iterate ``(python_name, value)`` for every set property., Set properties in emission order: known first, then unknown., Return a copy with specific properties overridden. Passing ``None`` removes a…

### Community 29 - "43. Acceptance Criteria"
Cohesion: 0.10
Nodes (21): 43. Acceptance Criteria, AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07 (+13 more)

### Community 30 - "Text"
Cohesion: 0.14
Nodes (13): Faint centred text behind the page content. Absolutely positioned and non-…, Watermark, Inline text element rendered as a ``<span>``. Parameters: content: The text…, Text, Three properties separate a watermark from a heading: it sits behind, it never…, A clipped overflow and a genuinely missing section look identical in the…, ``field=`` uses setdefault, so a layout that needs a non-editable but labelled…, test_clip_false_lets_overflow_show() (+5 more)

### Community 31 - "route"
Cohesion: 0.67
Nodes (3): route, index(), process()

### Community 34 - "html_engine/__init__.py"
Cohesion: 0.12
Nodes (19): Image component for the HTML Document Engine., Placeholder components for document furniture the render cannot reproduce. A…, Table components: Table, TableRow, TableCell. Supports both simple table…, A full ``<table>`` element. Can be built from: - Explicit ``TableRow`` objects…, Table, em(), pct(), pt() (+11 more)

### Community 37 - "FlexCol"
Cohesion: 0.19
Nodes (11): build_relationship_certificate(), _ea(), Any, Relationship Certificate Layout —…, build_tax_clearance(), Tax Clearance Certificate Layout — document_builder/tax_clearance/layout_1.py…, FlexCol, Vertical flex container (``flex-direction: column``). Parameters: children:… (+3 more)

### Community 39 - "architect.py"
Cohesion: 0.14
Nodes (27): _dispatch_tool(), _log_call(), _parse_contract(), Any, The Architect Agent — autonomous layout and schema generation. Replaces the…, Drive the tool-use loop until the model answers with text. Returns…, Extract the JSON contract from the agent's final message., Build a RepairResult, trusting the filesystem over the agent's claims. (+19 more)

### Community 40 - "models.py"
Cohesion: 0.14
Nodes (17): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., Machine-readable result returned by the vision model. This is the contract the…, Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, A single change to the extraction JSON schema. (+9 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

### Community 42 - "Document"
Cohesion: 0.20
Nodes (11): build_transfer_certificate(), _ea(), Any, Transfer Certificate Layout — document_builder/transfer_certificate/layout_1.py…, Document, A single page of output. Parameters: title: ``<title>`` text. page_width: Width…, test_document_add_coerces_and_names_itself(), test_document_save_creates_parent_directories() (+3 more)

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

### Community 51 - "44. Engineering Rules for the Agent"
Cohesion: 0.25
Nodes (8): 44. Engineering Rules for the Agent, Rule 1 — Document model first, Rule 2 — Single source of truth, Rule 3 — Components are renderers, Rule 4 — Commands modify state, Rule 5 — History is operation-based, Rule 6 — No premature complexity, Rule 7 — Extensibility

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
Cohesion: 0.20
Nodes (5): HorizontalRule, PageBreak, Spacer and divider components., Horizontal rule (``<hr>``) divider. Parameters: style: Override styles (color,…, Renders a page break for print media.

### Community 69 - "district"
Cohesion: 0.67
Nodes (3): description, type, district

### Community 70 - ".save"
Cohesion: 0.40
Nodes (3): Path, Render to a complete, self-contained HTML string., Write the rendered HTML to *path*, creating parent directories. Returns the…

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
- **200 isolated node(s):** `What is included`, `Setup`, `Which layout is live`, `Build one document by hand`, `Output is in English` (+195 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style` to `run.py`, `test_components.py`, `grid.py`, `base.py`, `citizenship/layout.py`, `laalpurja/layout.py`, `Spacer`, `Component`, `Image`, `MultiFieldRow`, `components/__init__.py`, `test_monochrome.py`, `Any`, `Text`, `html_engine/__init__.py`, `FlexCol`, `Document`, `LabelValue`, `spacer.py`?**
  _High betweenness centrality (0.271) - this node is a cross-community bridge._
- **Why does `resolve_schema_path()` connect `test_registry_resolution.py` to `run.py`, `analyze_and_repair`, `architect.py`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `active_layout_path()` connect `test_registry_resolution.py` to `analyze_and_repair`, `architect.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Style` (e.g. with `Component` and `FieldGroup`) actually correct?**
  _`Style` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Component` (e.g. with `Style` and `FieldGroup`) actually correct?**
  _`Component` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Text` (e.g. with `PlaceholderBox` and `SignatureBlock`) actually correct?**
  _`Text` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Document` (e.g. with `Component` and `Style`) actually correct?**
  _`Document` has 2 INFERRED edges - model-reasoned connections that need verification._