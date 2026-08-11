# Graph Report - babu-documentation  (2026-08-10)

## Corpus Check
- 85 files · ~782,272 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 848 nodes · 1726 edges · 79 communities (61 shown, 18 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 177 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `587c9397`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_main_cli.py
- test_components.py
- Editable Nepali citizenship certificate (romanized test render)
- grid.py
- base.py
- LabelValue
- html_engine/__init__.py
- Style
- AbsoluteBox
- laalpurja/layout.py
- test_command_sandbox.py
- run.py
- "First make it work, then make it better"
- test_registry_resolution.py
- analyze_and_repair
- Babu Document Digitization
- FlexCol
- Component
- required
- Image
- rag_engine.py
- PageBreak
- Salvage record: `controller-old/` → `agentic_controller/`
- langgraph dependency
- python-dotenv dependency
- validate_layout
- components/__init__.py
- test_monochrome.py
- Any
- FlexRow
- .__add__
- route
- DocLayout-YOLO
- Segment Anything Model for document analysis
- Surya (datalab-to)
- build_relationship_certificate
- CLAUDE.md
- architect.py
- models.py
- 1. Document Verification Rules
- Text
- properties
- _write_allowed
- run_all.py
- build_income_certificate
- items
- HTML document engine
- Babu task list / tooling backlog
- FieldGroup
- Spacer
- .__init__
- .to_css
- Babu Document Digitization: Technical Documentation
- Agentic controller
- Future work
- Document builders
- letter_no
- municipality
- office_name
- ref_no
- subject
- ward_chairperson_name
- ward_chairperson_title
- ward_no
- build_transfer_certificate
- spacer.py
- district
- main_text
- name
- test_typo_warns_but_does_not_raise
- agentic_controller/__init__.py
- Ideal patching prompt composition
- Perfect-match VerificationReport example
- langchain-openai dependency
- pydantic dependency

## God Nodes (most connected - your core abstractions)
1. `Style` - 127 edges
2. `Component` - 58 edges
3. `Text` - 42 edges
4. `_tree()` - 26 edges
5. `Spacer` - 26 edges
6. `LabelValue` - 25 edges
7. `_add_type()` - 24 edges
8. `FlexRow` - 24 edges
9. `PlaceholderBox` - 24 edges
10. `FlexCol` - 23 edges

## Surprising Connections (you probably didn't know these)
- `test_editable_attrs_is_the_single_source_of_the_contract()` --calls--> `editable_attrs()`  [INFERRED]
  tests/test_components.py → html_engine/components/base.py
- `_resources_exist()` --calls--> `resolve_schema_path()`  [INFERRED]
  agentic_controller/run.py → document_builder/resolver.py
- `digitize()` --calls--> `resolve_schema_path()`  [INFERRED]
  agentic_controller/run.py → document_builder/resolver.py
- `build_citizenship_back()` --calls--> `FlexCol`  [INFERRED]
  document_builder/citizenship_back/layout.py → html_engine/components/grid.py
- `build_citizenship_back()` --calls--> `FlexRow`  [INFERRED]
  document_builder/citizenship_back/layout.py → html_engine/components/grid.py

## Import Cycles
- None detected.

## Communities (79 total, 18 thin omitted)

### Community 0 - "test_main_cli.py"
Cohesion: 0.10
Nodes (31): _crop_to_page(), _page_metrics(), Path, render_png(), An unrecognized CSS property name reached ``Style``. Probably a typo., StyleWarning, build_data(), extract() (+23 more)

### Community 1 - "test_components.py"
Cohesion: 0.11
Nodes (22): Div, Generic block container rendered as a ``<div>``. The simplest building block —…, corner_box(), PlaceholderBox, A labelled outline standing in for artwork that cannot be rendered. Renders a…, A placeholder pinned to one corner of the page — crest, QR block, stamp.…, Tests for the components added for this project's documents, and for the…, A fixed pixel radius would not stay elliptical on a non-square box. (+14 more)

### Community 3 - "grid.py"
Cohesion: 0.15
Nodes (8): Card, Grid, GridItem, Layout components: FlexRow, FlexCol, AbsoluteBox, Div. These are generic…, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, CSS Grid item. Parameters: column_span: Number of columns this item spans (e.g.…, A styled container mimicking a paper card. Includes preset styles: background…, Placeholder components for document furniture the render cannot reproduce. A…

### Community 4 - "base.py"
Cohesion: 0.27
Nodes (8): ABC, coerce_child(), coerce_children(), Any, Abstract base class for all HTML Document Engine components. Every renderable…, Append one or more child components. Returns self for chaining. Accepts the…, Turn one constructor argument into a child component, or reject it. Containers…, Coerce an iterable of constructor arguments, dropping ``None``s.

### Community 5 - "LabelValue"
Cohesion: 0.28
Nodes (11): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main(), LabelValue (+3 more)

### Community 6 - "html_engine/__init__.py"
Cohesion: 0.17
Nodes (14): Document — the root of a renderable page. A ``Document`` holds page geometry…, Render a Document class to a full HTML string. The output is a self-contained…, render(), em(), pct(), pt(), px(), Style descriptor for the HTML Document Engine. ``Style`` is an **open**… (+6 more)

### Community 7 - "Style"
Cohesion: 0.10
Nodes (22): An open set of CSS declarations. Any keyword is accepted and emitted as a CSS…, Style, Tests for the open property bag that replaced the closed ``Style`` dataclass.…, Monochrome is enforced on the way out, including for unlisted props., The reported crash. Any valid CSS property must survive to the output., Both are deliberate, so neither should look like a typo., What ``main.py --strict`` relies on., A name CSS could never accept is a bug worth stopping for. (+14 more)

### Community 8 - "AbsoluteBox"
Cohesion: 0.15
Nodes (13): build_citizenship_back(), _ea(), Any, Document, build_citizenship_back(), Any, Document, AbsoluteBox (+5 more)

### Community 9 - "laalpurja/layout.py"
Cohesion: 0.17
Nodes (14): build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th(), _to_float() (+6 more)

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
Cohesion: 0.16
Nodes (17): analyze_and_repair(), _build_system_prompt(), generate_resources(), _image(), _load_rules(), main(), Path, Build a RepairResult, trusting the filesystem over the agent's claims. (+9 more)

### Community 15 - "Babu Document Digitization"
Cohesion: 0.18
Nodes (11): Babu Document Digitization, Build one document by hand, Full technical documentation, Generate example documents, Output is strictly black and white, Run the full pipeline, Setup, Standalone tools (+3 more)

### Community 16 - "FlexCol"
Cohesion: 0.24
Nodes (8): build_letter(), _ea(), Any, FlexCol, Vertical flex container (``flex-direction: column``). Parameters: children:…, Heading, Block heading element rendered as ``<h1>`` through ``<h6>``. Parameters:…, test_container_skips_none_children()

### Community 17 - "Component"
Cohesion: 0.16
Nodes (11): Component, Render all children to a concatenated HTML string., Render this component to an HTML string., Base class for all renderable document components. Parameters: style: Optional…, ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList., Renders a list item ``<li>``. Parameters: content: String content or nested… (+3 more)

### Community 18 - "required"
Cohesion: 0.11
Nodes (17): required, $schema, title, type, date, district, family_members, letter_no (+9 more)

### Community 19 - "Image"
Cohesion: 0.33
Nodes (4): Image, Image component for the HTML Document Engine., Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64.

### Community 20 - "rag_engine.py"
Cohesion: 0.10
Nodes (37): _tool_query_context(), build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python() (+29 more)

### Community 22 - "Salvage record: `controller-old/` → `agentic_controller/`"
Cohesion: 0.33
Nodes (5): Behaviour to reproduce in Phase 2/3, Carried across, Deliberately dropped, Not indexed by RAG, Salvage record: `controller-old/` → `agentic_controller/`

### Community 25 - "validate_layout"
Cohesion: 0.20
Nodes (20): Check that a generated layout module is safe for the caller to use. Four gates,…, validate_layout(), _layout(), Path, Tests for ``architect.validate_layout`` — the gate that let the reported bug…, Blank probe data is the harsh case. A layout indexing a key the schema does not…, A property outside the known list is a cosmetic gap, not a reason to fail a…, Without a schema the builder is probed with ``{}``. (+12 more)

### Community 26 - "components/__init__.py"
Cohesion: 0.13
Nodes (11): html_engine.components — All renderable component types., Table components: Table, TableRow, TableCell. Supports both simple table…, A full ``<table>`` element. Can be built from: - Explicit ``TableRow`` objects…, Table, Link, Paragraph, Text components: Text, Heading, Paragraph, Link., Escape hatch: renders arbitrary HTML verbatim. Use sparingly — this bypasses… (+3 more)

### Community 27 - "test_monochrome.py"
Cohesion: 0.05
Nodes (47): Build the HTML attribute string for this element. Combines ``css_class``,…, Document, Any, Path, Write the rendered HTML to *path*, creating parent directories. Returns the…, A single page of output. Parameters: title: ``<title>`` text. page_width: Width…, Append top-level components. Returns self for chaining. Accepts components,…, Render to a complete, self-contained HTML string. (+39 more)

### Community 28 - "Any"
Cohesion: 0.28
Nodes (4): Any, Record one declaration, warning if the property looks misspelled., Iterate ``(python_name, value)`` for every set property., Return a copy with specific properties overridden. Passing ``None`` removes a…

### Community 29 - "FlexRow"
Cohesion: 0.22
Nodes (7): build_see_certificate(), Document, SEE Certificate Layout — document_builder/see_certificate/layout_1.py…, FlexRow, Horizontal flex container (``flex-direction: row``). Parameters: children:…, test_container_coerces_numbers(), test_container_rejects_a_list_with_position_and_type()

### Community 31 - "route"
Cohesion: 0.67
Nodes (3): route, index(), process()

### Community 37 - "build_relationship_certificate"
Cohesion: 0.40
Nodes (5): build_relationship_certificate(), _ea(), Any, Document, Relationship Certificate Layout —…

### Community 39 - "architect.py"
Cohesion: 0.17
Nodes (23): _dispatch_tool(), _log_call(), _parse_contract(), Any, The Architect Agent — autonomous layout and schema generation. Replaces the…, Drive the tool-use loop until the model answers with text. Returns…, Extract the JSON contract from the agent's final message., Check that a written schema is valid JSON with the keys the extractor needs.… (+15 more)

### Community 40 - "models.py"
Cohesion: 0.10
Nodes (24): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., Machine-readable result returned by the vision model. This is the contract the…, Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, A single change to the extraction JSON schema. (+16 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

### Community 42 - "Text"
Cohesion: 0.13
Nodes (14): Faint centred text behind the page content. Absolutely positioned and non-…, Watermark, Inline text element rendered as a ``<span>``. Parameters: content: The text…, Text, Three properties separate a watermark from a heading: it sits behind, it never…, A clipped overflow and a genuinely missing section look identical in the…, ``field=`` uses setdefault, so a layout that needs a non-editable but labelled…, test_clip_false_lets_overflow_show() (+6 more)

### Community 43 - "properties"
Cohesion: 0.29
Nodes (7): description, type, properties, date, province, description, type

### Community 44 - "_write_allowed"
Cohesion: 0.20
Nodes (10): Gate write_file: inside the writable trees, and never *onto* an original.…, _write_allowed(), The invariant the docs promise: an original that exists is never a target., A type with no directory yet has no original to destroy, and the first layout…, test_write_allows_a_base_schema_that_does_not_exist_yet(), test_write_allows_layout_py_for_a_brand_new_type(), test_write_refuses_an_existing_base_schema(), test_write_refuses_an_existing_layout_py() (+2 more)

### Community 46 - "build_income_certificate"
Cohesion: 0.38
Nodes (6): build_income_certificate(), _ea(), _lv(), Any, Document, Income Certificate Layout — document_builder/income_certificate/layout_1.py…

### Community 47 - "items"
Cohesion: 0.17
Nodes (12): description, items, type, properties, required, type, family_members, relation (+4 more)

### Community 48 - "HTML document engine"
Cohesion: 0.20
Nodes (10): Arbitrary HTML attributes (`attrs`), Component reference, Editable fields (`field=`), HTML document engine, Minimal example, Monochrome enforcement, Placeholders for un-renderable furniture, Rendering (+2 more)

### Community 49 - "Babu task list / tooling backlog"
Cohesion: 0.25
Nodes (8): Information extraction, Donut (clovaai), Handwritten Nepali OCR model (TrOCR finetune, Tesseract), HTML abstraction engine over HTML/CSS, OCR JSON → HTML engine integration, Preprocessing engine (CamScanner-style rectification), Programmatic format building from received data, Babu task list / tooling backlog

### Community 50 - "FieldGroup"
Cohesion: 0.16
Nodes (8): editable_attrs(), Attributes that make one rendered value editable in the browser. The ``data-…, FieldGroup, MultiFieldRow, Any, Field components: LabelValue pairs and FieldGroups. These are the workhorses…, A vertical stack of LabelValue rows or other components. Renders as a ``<div>``…, A horizontal row containing multiple label–value pairs. Useful for rows like:…

### Community 51 - "Spacer"
Cohesion: 0.22
Nodes (7): build_tax_clearance(), Document, Tax Clearance Certificate Layout — document_builder/tax_clearance/layout_1.py…, Empty space of a fixed size. Vertical by default. A ``width`` makes it a…, Spacer, A horizontal spacer inside a flex row needs flex-shrink:0 to survive., test_spacer_gutter_is_not_squeezed_away()

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

### Community 67 - "build_transfer_certificate"
Cohesion: 0.40
Nodes (5): build_transfer_certificate(), _ea(), Any, Document, Transfer Certificate Layout — document_builder/transfer_certificate/layout_1.py…

### Community 68 - "spacer.py"
Cohesion: 0.40
Nodes (3): HorizontalRule, Spacer and divider components., Horizontal rule (``<hr>``) divider. Parameters: style: Override styles (color,…

### Community 69 - "district"
Cohesion: 0.67
Nodes (3): description, type, district

### Community 70 - "main_text"
Cohesion: 0.67
Nodes (3): description, type, main_text

### Community 71 - "name"
Cohesion: 0.67
Nodes (3): description, type, name

## Knowledge Gaps
- **110 isolated node(s):** `What is included`, `Setup`, `Which layout is live`, `Build one document by hand`, `Output is strictly black and white` (+105 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style` to `test_main_cli.py`, `test_components.py`, `grid.py`, `base.py`, `LabelValue`, `html_engine/__init__.py`, `AbsoluteBox`, `laalpurja/layout.py`, `FlexCol`, `Component`, `Image`, `PageBreak`, `components/__init__.py`, `test_monochrome.py`, `Any`, `FlexRow`, `.__add__`, `build_relationship_certificate`, `Text`, `build_income_certificate`, `FieldGroup`, `Spacer`, `.__init__`, `.to_css`, `.__init__`, `build_transfer_certificate`, `spacer.py`, `test_typo_warns_but_does_not_raise`?**
  _High betweenness centrality (0.399) - this node is a cross-community bridge._
- **Why does `active_layout_path()` connect `test_registry_resolution.py` to `run.py`, `architect.py`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Why does `resolve_schema_path()` connect `test_registry_resolution.py` to `run.py`, `analyze_and_repair`, `architect.py`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Style` (e.g. with `build_citizenship_back()` and `build_citizenship_back()`) actually correct?**
  _`Style` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Component` (e.g. with `Style` and `FieldGroup`) actually correct?**
  _`Component` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `Text` (e.g. with `build_citizenship_back()` and `build_citizenship_back()`) actually correct?**
  _`Text` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `Spacer` (e.g. with `build_citizenship_back()` and `build_citizenship_back()`) actually correct?**
  _`Spacer` has 13 INFERRED edges - model-reasoned connections that need verification._