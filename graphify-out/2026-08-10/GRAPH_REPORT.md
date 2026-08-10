# Graph Report - babu-documentation  (2026-08-10)

## Corpus Check
- 85 files · ~776,284 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 832 nodes · 1816 edges · 76 communities (59 shown, 17 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 75 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d1faa3c5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_main_cli.py
- test_components.py
- Editable Nepali citizenship certificate (romanized test render)
- .__init__
- coerce_children
- LabelValue
- html_engine/__init__.py
- Style
- FlexRow
- laalpurja/layout.py
- test_command_sandbox.py
- run.py
- "First make it work, then make it better"
- test_registry_resolution.py
- analyze_and_repair
- Babu Document Digitization
- .save
- Component
- required
- Image
- rag_engine.py
- TableCell
- Salvage record: `controller-old/` → `agentic_controller/`
- langgraph dependency
- python-dotenv dependency
- validate_layout
- Spacer
- normalize_value
- Any
- test_monochrome.py
- .__add__
- route
- DocLayout-YOLO
- Segment Anything Model for document analysis
- Surya (datalab-to)
- PlaceholderBox
- CLAUDE.md
- architect.py
- models.py
- 1. Document Verification Rules
- Text
- ._render_children
- verify
- run_all.py
- normalize_declarations
- items
- HTML document engine
- Babu task list / tooling backlog
- .to_css
- SignatureBlock
- properties
- income_certificate/layout_1.py
- Babu Document Digitization: Technical Documentation
- Agentic controller
- Future work
- Document builders
- RawHTML
- date
- letter_no
- main_text
- municipality
- name
- office_name
- ref_no
- subject
- ward_chairperson_name
- ward_chairperson_title
- ward_no
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
- `test_editable_attrs_is_the_single_source_of_the_contract()` --calls--> `editable_attrs()`  [EXTRACTED]
  tests/test_components.py → html_engine/components/base.py
- `test_route_1_style_to_css()` --calls--> `Style`  [EXTRACTED]
  tests/test_monochrome.py → html_engine/styles.py
- `test_route_3_style_raw_escape_hatch()` --calls--> `Style`  [EXTRACTED]
  tests/test_monochrome.py → html_engine/styles.py

## Import Cycles
- None detected.

## Communities (76 total, 17 thin omitted)

### Community 0 - "test_main_cli.py"
Cohesion: 0.10
Nodes (31): _crop_to_page(), _page_metrics(), Path, render_png(), An unrecognized CSS property name reached ``Style``. Probably a typo., StyleWarning, build_data(), extract() (+23 more)

### Community 1 - "test_components.py"
Cohesion: 0.11
Nodes (20): Div, Generic block container rendered as a ``<div>``. The simplest building block —…, corner_box(), Faint centred text behind the page content. Absolutely positioned and non-…, A placeholder pinned to one corner of the page — crest, QR block, stamp.…, Watermark, Tests for the components added for this project's documents, and for the…, Three properties separate a watermark from a heading: it sits behind, it never… (+12 more)

### Community 3 - ".__init__"
Cohesion: 0.16
Nodes (7): Card, Grid, GridItem, Any, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, CSS Grid item. Parameters: column_span: Number of columns this item spans (e.g.…, A styled container mimicking a paper card. Includes preset styles: background…

### Community 4 - "coerce_children"
Cohesion: 0.24
Nodes (8): coerce_child(), coerce_children(), Any, Append one or more child components. Returns self for chaining. Accepts the…, Turn one constructor argument into a child component, or reject it. Containers…, Coerce an iterable of constructor arguments, dropping ``None``s., Any, Append top-level components. Returns self for chaining. Accepts components,…

### Community 5 - "LabelValue"
Cohesion: 0.28
Nodes (11): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main(), LabelValue (+3 more)

### Community 6 - "html_engine/__init__.py"
Cohesion: 0.10
Nodes (25): Abstract base class for all HTML Document Engine components. Every renderable…, Field components: LabelValue pairs and FieldGroups. These are the workhorses…, Layout components: FlexRow, FlexCol, AbsoluteBox, Div. These are generic…, Image component for the HTML Document Engine., html_engine.components — All renderable component types., Placeholder components for document furniture the render cannot reproduce. A…, HorizontalRule, Spacer and divider components. (+17 more)

### Community 7 - "Style"
Cohesion: 0.07
Nodes (28): PageBreak, Renders a page break for print media., Link, Renders an anchor element ``<a>``. Parameters: content: The text content or…, An open set of CSS declarations. Any keyword is accepted and emitted as a CSS…, Style, Tests for the open property bag that replaced the closed ``Style`` dataclass.…, Monochrome is enforced on the way out, including for unlisted props. (+20 more)

### Community 8 - "FlexRow"
Cohesion: 0.15
Nodes (17): build_citizenship_back(), _ea(), Any, build_citizenship_back(), Any, build_letter(), _ea(), Any (+9 more)

### Community 9 - "laalpurja/layout.py"
Cohesion: 0.15
Nodes (15): build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th(), _to_float() (+7 more)

### Community 10 - "test_command_sandbox.py"
Cohesion: 0.17
Nodes (20): _protected_originals(), Content of each protected file, or None if it does not exist., Undo any modification to a protected original. Returns what was restored., _restore_changed(), _snapshot(), _tool_execute_command(), Tests for the ``execute_command`` sandbox in the Architect Agent. These exist…, _refused() (+12 more)

### Community 11 - "run.py"
Cohesion: 0.17
Nodes (17): current_layout_path(), The layout that will actually be built — whatever ``ACTIVE`` names. This used…, _collect_decision(), _collect_user_concerns(), digitize(), main(), Path, Integrated autonomous document digitization pipeline. Flow: 1. Check whether… (+9 more)

### Community 13 - "test_registry_resolution.py"
Cohesion: 0.06
Nodes (72): _DocumentEntry, Any, The document registry: which types exist, and how to build each one.…, One document type's ``{"builder": ..., "schema": ...}``. ``schema`` is a path…, Document types discovered from the filesystem, resolved on access. Not cached.…, _Registry, active_layout_name(), active_layout_path() (+64 more)

### Community 14 - "analyze_and_repair"
Cohesion: 0.15
Nodes (19): analyze_and_repair(), _build_system_prompt(), generate_resources(), _image(), _load_rules(), main(), Path, Build a RepairResult, trusting the filesystem over the agent's claims. (+11 more)

### Community 15 - "Babu Document Digitization"
Cohesion: 0.18
Nodes (11): Babu Document Digitization, Build one document by hand, Full technical documentation, Generate example documents, Output is strictly black and white, Run the full pipeline, Setup, Standalone tools (+3 more)

### Community 16 - ".save"
Cohesion: 0.40
Nodes (3): Path, Write the rendered HTML to *path*, creating parent directories. Returns the…, Render to a complete, self-contained HTML string.

### Community 17 - "Component"
Cohesion: 0.13
Nodes (13): ABC, Component, editable_attrs(), Build the HTML attribute string for this element. Combines ``css_class``,…, Attributes that make one rendered value editable in the browser. The ``data-…, Base class for all renderable document components. Parameters: style: Optional…, ListItem, OrderedList (+5 more)

### Community 18 - "required"
Cohesion: 0.11
Nodes (17): required, $schema, title, type, date, district, family_members, letter_no (+9 more)

### Community 19 - "Image"
Cohesion: 0.40
Nodes (3): Image, Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64.

### Community 20 - "rag_engine.py"
Cohesion: 0.10
Nodes (37): _tool_query_context(), build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python() (+29 more)

### Community 21 - "TableCell"
Cohesion: 0.27
Nodes (6): A full ``<table>`` element. Can be built from: - Explicit ``TableRow`` objects…, A single table cell (``<td>`` or ``<th>``). Parameters: content: Cell content —…, A table row (``<tr>``) containing one or more cells. Parameters: cells:…, Table, TableCell, TableRow

### Community 22 - "Salvage record: `controller-old/` → `agentic_controller/`"
Cohesion: 0.33
Nodes (5): Behaviour to reproduce in Phase 2/3, Carried across, Deliberately dropped, Not indexed by RAG, Salvage record: `controller-old/` → `agentic_controller/`

### Community 25 - "validate_layout"
Cohesion: 0.20
Nodes (20): Check that a generated layout module is safe for the caller to use. Four gates,…, validate_layout(), _layout(), Path, Tests for ``architect.validate_layout`` — the gate that let the reported bug…, Blank probe data is the harsh case. A layout indexing a key the schema does not…, A property outside the known list is a cosmetic gap, not a reason to fail a…, Without a schema the builder is probed with ``{}``. (+12 more)

### Community 26 - "Spacer"
Cohesion: 0.17
Nodes (12): build_tax_clearance(), Tax Clearance Certificate Layout — document_builder/tax_clearance/layout_1.py…, build_transfer_certificate(), _ea(), Any, Transfer Certificate Layout — document_builder/transfer_certificate/layout_1.py…, Empty space of a fixed size. Vertical by default. A ``width`` makes it a…, Spacer (+4 more)

### Community 27 - "normalize_value"
Cohesion: 0.13
Nodes (15): normalize_value(), Rewrite every colour token in a single declaration's *value*. Parameters: prop:…, Thresholding by luminance would map a dark fill to black and its light text to…, A curated subset leaked ``rebeccapurple``. Any name the regex misses passes…, Alternation is scanned left to right. With "red" ordered before "rebeccapurple"…, Rewriting transparent to white paints over content meant to show through., Corrupting document data is worse than leaking a colour., A url(...) may hold a "#" fragment that is not a colour. (+7 more)

### Community 28 - "Any"
Cohesion: 0.28
Nodes (4): Any, Record one declaration, warning if the property looks misspelled., Iterate ``(python_name, value)`` for every set property., Return a copy with specific properties overridden. Passing ``None`` removes a…

### Community 29 - "test_monochrome.py"
Cohesion: 0.16
Nodes (12): find_violations(), Report colour tokens that normalization *would* change. Returns a list of…, Tests for the monochrome guarantee. Project rule: a rendered document is purely…, A component can carry a hand-written style attribute, bypassing Style., A component's own ``to_html()`` can hardcode a style the engine never sees as a…, The guarantee that actually matters: every shipped document type., test_find_violations_reports_pairs(), test_registered_layouts_render_monochrome() (+4 more)

### Community 31 - "route"
Cohesion: 0.67
Nodes (3): route, index(), process()

### Community 37 - "PlaceholderBox"
Cohesion: 0.18
Nodes (12): build_relationship_certificate(), _ea(), Any, Relationship Certificate Layout —…, PlaceholderBox, A labelled outline standing in for artwork that cannot be rendered. Renders a…, A fixed pixel radius would not stay elliptical on a non-square box., Dashed = a human still has to supply it. Solid = the document has it. (+4 more)

### Community 39 - "architect.py"
Cohesion: 0.18
Nodes (22): _dispatch_tool(), _log_call(), _parse_contract(), Any, The Architect Agent — autonomous layout and schema generation. Replaces the…, Drive the tool-use loop until the model answers with text. Returns…, Extract the JSON contract from the agent's final message., Check that a written schema is valid JSON with the keys the extractor needs.… (+14 more)

### Community 40 - "models.py"
Cohesion: 0.17
Nodes (14): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., A single change to the extraction JSON schema., A single structural change to the document layout builder., RepairPlan (+6 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

### Community 42 - "Text"
Cohesion: 0.13
Nodes (14): Inline text element rendered as a ``<span>``. Parameters: content: The text…, Text, Document, A single page of output. Parameters: title: ``<title>`` text. page_width: Width…, A clipped overflow and a genuinely missing section look identical in the…, ``field=`` uses setdefault, so a layout that needs a non-editable but labelled…, test_clip_false_lets_overflow_show(), test_document_add_coerces_and_names_itself() (+6 more)

### Community 44 - "verify"
Cohesion: 0.23
Nodes (10): Machine-readable result returned by the vision model. This is the contract the…, Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, VerificationReport, image_data_url(), main(), Path, Vision-model comparison of a source document against its rendered replica.…, Compare *source* against *rendered* and return a structured report. (+2 more)

### Community 46 - "normalize_declarations"
Cohesion: 0.19
Nodes (11): normalize_declarations(), normalize_html(), Monochrome enforcement for the HTML Document Engine. Project rule: a rendered…, Surfaces go white, ink goes black., Rewrite colours across a CSS fragment. Works both on an inline declaration list…, Rewrite colours in a complete HTML document. Only ``style="..."`` attributes…, _target_for(), Render a Document class to a full HTML string. The output is a self-contained… (+3 more)

### Community 47 - "items"
Cohesion: 0.17
Nodes (12): description, items, type, properties, required, type, family_members, relation (+4 more)

### Community 48 - "HTML document engine"
Cohesion: 0.20
Nodes (10): Arbitrary HTML attributes (`attrs`), Component reference, Editable fields (`field=`), HTML document engine, Minimal example, Monochrome enforcement, Placeholders for un-renderable furniture, Rendering (+2 more)

### Community 49 - "Babu task list / tooling backlog"
Cohesion: 0.25
Nodes (8): Information extraction, Donut (clovaai), Handwritten Nepali OCR model (TrOCR finetune, Tesseract), HTML abstraction engine over HTML/CSS, OCR JSON → HTML engine integration, Preprocessing engine (CamScanner-style rectification), Programmatic format building from received data, Babu task list / tooling backlog

### Community 50 - ".to_css"
Cohesion: 0.25
Nodes (5): _css_name(), Map a Python keyword to its CSS property name. ``font_size`` -> ``font-size``.…, Set properties in emission order: known first, then unknown. Known properties…, Serialize to an inline CSS declaration string. Colours are normalized to black-…, Return a full ``style="..."`` attribute, or ``""`` if empty.

### Community 51 - "SignatureBlock"
Cohesion: 0.33
Nodes (6): build_see_certificate(), SEE Certificate Layout — document_builder/see_certificate/layout_1.py…, The signature cluster that closes an official letter. Stacks, top to bottom:…, SignatureBlock, test_signature_block_parts_are_optional(), test_signature_block_stacks_every_part()

### Community 52 - "properties"
Cohesion: 0.29
Nodes (7): description, type, properties, district, province, description, type

### Community 53 - "income_certificate/layout_1.py"
Cohesion: 0.47
Nodes (5): build_income_certificate(), _ea(), _lv(), Any, Income Certificate Layout — document_builder/income_certificate/layout_1.py…

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

### Community 59 - "date"
Cohesion: 0.67
Nodes (3): description, type, date

### Community 60 - "letter_no"
Cohesion: 0.67
Nodes (3): description, type, letter_no

### Community 61 - "main_text"
Cohesion: 0.67
Nodes (3): description, type, main_text

### Community 62 - "municipality"
Cohesion: 0.67
Nodes (3): description, type, municipality

### Community 63 - "name"
Cohesion: 0.67
Nodes (3): description, type, name

### Community 64 - "office_name"
Cohesion: 0.67
Nodes (3): description, type, office_name

### Community 65 - "ref_no"
Cohesion: 0.67
Nodes (3): ref_no, description, type

### Community 66 - "subject"
Cohesion: 0.67
Nodes (3): subject, description, type

### Community 67 - "ward_chairperson_name"
Cohesion: 0.67
Nodes (3): ward_chairperson_name, description, type

### Community 68 - "ward_chairperson_title"
Cohesion: 0.67
Nodes (3): ward_chairperson_title, description, type

### Community 69 - "ward_no"
Cohesion: 0.67
Nodes (3): ward_no, description, type

## Knowledge Gaps
- **110 isolated node(s):** `$schema`, `title`, `type`, `type`, `description` (+105 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style` to `test_main_cli.py`, `test_components.py`, `.__init__`, `LabelValue`, `html_engine/__init__.py`, `FlexRow`, `laalpurja/layout.py`, `Component`, `Image`, `TableCell`, `Spacer`, `Any`, `test_monochrome.py`, `.__add__`, `PlaceholderBox`, `Text`, `.to_css`, `SignatureBlock`, `income_certificate/layout_1.py`, `RawHTML`?**
  _High betweenness centrality (0.391) - this node is a cross-community bridge._
- **Why does `active_layout_path()` connect `test_registry_resolution.py` to `run.py`, `architect.py`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `resolve_schema_path()` connect `test_registry_resolution.py` to `run.py`, `analyze_and_repair`, `architect.py`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Style` (e.g. with `Component` and `FieldGroup`) actually correct?**
  _`Style` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Component` (e.g. with `Text` and `Style`) actually correct?**
  _`Component` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Text` (e.g. with `Component` and `PlaceholderBox`) actually correct?**
  _`Text` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Document` (e.g. with `Component` and `Style`) actually correct?**
  _`Document` has 2 INFERRED edges - model-reasoned connections that need verification._