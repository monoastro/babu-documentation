# Graph Report - babu-documentation  (2026-08-11)

## Corpus Check
- 102 files · ~828,482 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1082 nodes · 2155 edges · 85 communities (68 shown, 17 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 76 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2d838a72`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run.py
- test_components.py
- Editable Nepali citizenship certificate (romanized test render)
- grid.py
- base.py
- LabelValue
- test_translator.py
- Style
- translator.py
- laalpurja/layout.py
- test_command_sandbox.py
- analyze_and_repair
- "First make it work, then make it better"
- test_registry_resolution.py
- prd.md
- Stages
- Spacer
- Component
- required
- Image
- rag_engine.py
- language_spec
- Salvage record: `controller-old/` → `agentic_controller/`
- langgraph dependency
- python-dotenv dependency
- validate_layout
- text.py
- test_monochrome.py
- build_prompt
- 43. Acceptance Criteria
- Text
- test_main_cli.py
- DocLayout-YOLO
- Segment Anything Model for document analysis
- html_engine/__init__.py
- verifier.py
- Surya (datalab-to)
- FlexCol
- CLAUDE.md
- architect.py
- models.py
- 1. Document Verification Rules
- _needs_translation
- properties
- 37. MVP Scope
- run_all.py
- income_certificate/layout.py
- items
- HTML document engine
- render_png
- components/__init__.py
- 44. Engineering Rules for the Agent
- .add
- StyleWarning
- date
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
- .save
- 3. Target User
- 8. Toolbar
- relationship_certificate.json
- 35. Non-Functional Requirements
- family_members
- PRD — Visual HTML Document Editing Engine
- 4. Core Design Principle
- main.py
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
9. `_run()` - 32 edges
10. `FlexCol` - 31 edges

## Surprising Connections (you probably didn't know these)
- `_resources_exist()` --calls--> `resolve_schema_path()`  [INFERRED]
  agentic_controller/run.py → document_builder/resolver.py
- `digitize()` --calls--> `resolve_schema_path()`  [INFERRED]
  agentic_controller/run.py → document_builder/resolver.py
- `test_editable_attrs_is_the_single_source_of_the_contract()` --calls--> `editable_attrs()`  [EXTRACTED]
  tests/test_components.py → html_engine/components/base.py
- `test_container_coerces_numbers()` --calls--> `FlexRow`  [EXTRACTED]
  tests/test_components.py → html_engine/components/grid.py
- `test_signature_block_stacks_every_part()` --calls--> `SignatureBlock`  [EXTRACTED]
  tests/test_components.py → html_engine/components/placeholder.py

## Import Cycles
- None detected.

## Communities (85 total, 17 thin omitted)

### Community 0 - "run.py"
Cohesion: 0.12
Nodes (23): current_layout_path(), generate_resources(), main(), Create a layout builder and extraction schema for an unseen document type. This…, What the Architect Agent produced on one invocation., Human-readable one-screen summary, for the Phase 3 checkpoint., The layout that will actually be built — whatever ``ACTIVE`` names. This used…, RepairResult (+15 more)

### Community 1 - "test_components.py"
Cohesion: 0.09
Nodes (28): Div, Generic block container rendered as a ``<div>``. The simplest building block —…, corner_box(), Faint centred text behind the page content. Absolutely positioned and non-…, A placeholder pinned to one corner of the page — crest, QR block, stamp.…, Watermark, Tests for the components added for this project's documents, and for the…, A fixed pixel radius would not stay elliptical on a non-square box. (+20 more)

### Community 3 - "grid.py"
Cohesion: 0.15
Nodes (8): Card, Grid, GridItem, Any, Layout components: FlexRow, FlexCol, AbsoluteBox, Div. These are generic…, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, CSS Grid item. Parameters: column_span: Number of columns this item spans (e.g.…, A styled container mimicking a paper card. Includes preset styles: background…

### Community 4 - "base.py"
Cohesion: 0.13
Nodes (14): ABC, coerce_child(), coerce_children(), editable_attrs(), Any, Abstract base class for all HTML Document Engine components. Every renderable…, Append one or more child components. Returns self for chaining., Turn one constructor argument into a child component, or reject it. Components… (+6 more)

### Community 5 - "LabelValue"
Cohesion: 0.19
Nodes (13): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main(), FieldGroup (+5 more)

### Community 6 - "test_translator.py"
Cohesion: 0.06
Nodes (52): Tests for the translation stage. ``information_extraction/translator.py`` sits…, A sentence and a field label want different instructions, so they are batched…, A district repeated down a table is one string, not twenty., A half-converted date prints a year that looks Gregorian and is not., The SEE certificate prints ``certificate_title_np`` on one line and…, Without the English sibling, that value is the only one on the page., A laalpurja's ``plots`` is a list of dicts; every row must be reached., ``<field>_meta`` and ``<field>_citations`` are provenance the extractor… (+44 more)

### Community 7 - "Style"
Cohesion: 0.08
Nodes (26): An open set of CSS declarations. Any keyword is accepted and emitted as a CSS…, Return a new Style with *other*'s declarations overriding this one's. ``raw``…, Shorthand for ``merge``: ``combined = style_a + style_b``., Style, Tests for the open property bag that replaced the closed ``Style`` dataclass.…, Monochrome is enforced on the way out, including for unlisted props., The reported crash. Any valid CSS property must survive to the output., Both are deliberate, so neither should look like a typo. (+18 more)

### Community 8 - "translator.py"
Cohesion: 0.17
Nodes (20): _apply(), bs_to_ad(), _cache_key(), _collect(), _is_meta_key(), _load_cache(), _model_name(), _paired_paths() (+12 more)

### Community 9 - "laalpurja/layout.py"
Cohesion: 0.30
Nodes (10): build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th(), _to_float() (+2 more)

### Community 10 - "test_command_sandbox.py"
Cohesion: 0.11
Nodes (30): _protected_originals(), Content of each protected file, or None if it does not exist., Undo any modification to a protected original. Returns what was restored., Gate write_file: inside the writable trees, and never *onto* an original.…, _restore_changed(), _snapshot(), _tool_execute_command(), _write_allowed() (+22 more)

### Community 11 - "analyze_and_repair"
Cohesion: 0.18
Nodes (12): analyze_and_repair(), _build_system_prompt(), _image(), _load_rules(), _parse_contract(), Path, Extract the JSON contract from the agent's final message., Repair the layout and/or schema so the next render passes verification.… (+4 more)

### Community 13 - "test_registry_resolution.py"
Cohesion: 0.06
Nodes (72): _DocumentEntry, Any, The document registry: which types exist, and how to build each one.…, One document type's ``{"builder": ..., "schema": ...}``. ``schema`` and…, Document types discovered from the filesystem, resolved on access. Deliberately…, _Registry, active_layout_name(), active_layout_path() (+64 more)

### Community 14 - "prd.md"
Cohesion: 0.05
Nodes (36): 10. Canvas, 11. Page Model, 12. Element Model, 13. Text Element, 14. Image Element, 15. Shape Element, 16. Dynamic Field Element, 17. Selection System (+28 more)

### Community 15 - "Stages"
Cohesion: 0.05
Nodes (36): Decisions settled up front, Deliberately not in scope, Frontend integration plan, How to read the two source documents, Sequencing, Stage 0 — Groundwork, Stage 10 — Export, Stage 11 — The agentic loop, made reviewable (+28 more)

### Community 16 - "Spacer"
Cohesion: 0.15
Nodes (22): build_citizenship_back(), _ea(), Any, build_citizenship_back(), Any, build_see_certificate(), SEE Certificate Layout — document_builder/see_certificate/layout_1.py…, build_tax_clearance() (+14 more)

### Community 17 - "Component"
Cohesion: 0.14
Nodes (12): Component, Render all children to a concatenated HTML string., Build the HTML attribute string for this element. Combines ``css_class``,…, Render this component to an HTML string., Base class for all renderable document components. Parameters: style: Optional…, ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList. (+4 more)

### Community 18 - "required"
Cohesion: 0.14
Nodes (14): required, date, district, family_members, letter_no, main_text, municipality, office_name (+6 more)

### Community 19 - "Image"
Cohesion: 0.29
Nodes (4): Image, Image component for the HTML Document Engine., Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64.

### Community 20 - "rag_engine.py"
Cohesion: 0.11
Nodes (34): build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python(), _embed() (+26 more)

### Community 21 - "language_spec"
Cohesion: 0.14
Nodes (14): language_spec(), LanguageSpec, Target languages the translator can render a document into. One…, Everything the translator needs to know about one target language. Parameters:…, Look up a target language, naming the supported codes on failure., build_prompt(), The result of translating one document's extracted data., The system prompt for one target language. (+6 more)

### Community 22 - "Salvage record: `controller-old/` → `agentic_controller/`"
Cohesion: 0.33
Nodes (5): Behaviour to reproduce in Phase 2/3, Carried across, Deliberately dropped, Not indexed by RAG, Salvage record: `controller-old/` → `agentic_controller/`

### Community 25 - "validate_layout"
Cohesion: 0.20
Nodes (20): Check that a generated layout module is safe for the caller to use. Four gates,…, validate_layout(), _layout(), Path, Tests for ``architect.validate_layout`` — the gate that let the reported bug…, Blank probe data is the harsh case. A layout indexing a key the schema does not…, A property outside the known list is a cosmetic gap, not a reason to fail a…, Without a schema the builder is probed with ``{}``. (+12 more)

### Community 26 - "text.py"
Cohesion: 0.14
Nodes (7): Link, Paragraph, Text components: Text, Heading, Paragraph, Link., Escape hatch: renders arbitrary HTML verbatim. Use sparingly — this bypasses…, Renders an anchor element ``<a>``. Parameters: content: The text content or…, Block paragraph element rendered as ``<p>``. Parameters: content: The paragraph…, RawHTML

### Community 27 - "test_monochrome.py"
Cohesion: 0.05
Nodes (45): find_violations(), normalize_declarations(), normalize_html(), normalize_value(), Monochrome enforcement for the HTML Document Engine. Project rule: a rendered…, Rewrite every colour token in a single declaration's *value*. Parameters: prop:…, Rewrite colours across a CSS fragment. Works both on an inline declaration list…, Rewrite colours in a complete HTML document. Only ``style="..."`` attributes… (+37 more)

### Community 28 - "build_prompt"
Cohesion: 0.18
Nodes (13): build_prompt(), The full verification system prompt for one target language., Tests for the verification prompt's target language.…, Latin examples in a Japanese prompt would teach the wrong script., Only rule 1 varies; placeholders, formatting, and colour do not., ``verification-rules.md`` mirrors this prompt rule by rule., ``SYSTEM_PROMPT`` is what ``verification-rules.md`` documents., test_an_unsupported_language_is_refused() (+5 more)

### Community 29 - "43. Acceptance Criteria"
Cohesion: 0.10
Nodes (21): 43. Acceptance Criteria, AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07 (+13 more)

### Community 30 - "Text"
Cohesion: 0.12
Nodes (18): build_letter(), _ea(), Any, Inline text element rendered as a ``<span>``. Parameters: content: The text…, Text, Document, A single page of output. Parameters: title: ``<title>`` text. page_width: Width…, A clipped overflow and a genuinely missing section look identical in the… (+10 more)

### Community 31 - "test_main_cli.py"
Cohesion: 0.23
Nodes (13): main(), _out(), Path, Tests for the manual entry point. ``main.py`` is the hand-driven counterpart to…, Proven by breaking the OCR import: if the extractor were reached, this would…, The engine warns on an unrecognized property rather than raising, so…, _run(), test_blank_builds_every_registered_type() (+5 more)

### Community 34 - "html_engine/__init__.py"
Cohesion: 0.15
Nodes (15): Placeholder components for document furniture the render cannot reproduce. A…, Document — the root of a renderable page. doc = Document("My Certificate",…, Render a Document class to a full HTML string. The output is a self-contained…, render(), em(), pct(), pt(), px() (+7 more)

### Community 35 - "verifier.py"
Cohesion: 0.36
Nodes (7): image_data_url(), main(), Path, Vision-model comparison of a source document against its rendered replica.…, Validate a local raster image and encode it for a multimodal model message.…, Compare *source* against *rendered* and return a structured report.…, verify()

### Community 37 - "FlexCol"
Cohesion: 0.17
Nodes (13): build_relationship_certificate(), _ea(), Any, Relationship Certificate Layout —…, build_transfer_certificate(), _ea(), Any, Transfer Certificate Layout — document_builder/transfer_certificate/layout_1.py… (+5 more)

### Community 39 - "architect.py"
Cohesion: 0.17
Nodes (24): _dispatch_tool(), _log_call(), Any, The Architect Agent — autonomous layout and schema generation. Replaces the…, Drive the tool-use loop until the model answers with text. Returns…, Build a RepairResult, trusting the filesystem over the agent's claims., Resolve a model-supplied path against the project root., Return ``(backend, client, model)``. Prefers Anthropic when its key is present… (+16 more)

### Community 40 - "models.py"
Cohesion: 0.14
Nodes (17): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., Machine-readable result returned by the vision model. This is the contract the…, Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, A single change to the extraction JSON schema. (+9 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

### Community 42 - "_needs_translation"
Cohesion: 0.33
Nodes (6): _has_letters(), _is_ascii(), _is_identifier(), _needs_translation(), Whether an ASCII value is a code rather than words. A certificate number like…, Whether this value should be sent to the model at all.

### Community 43 - "properties"
Cohesion: 0.20
Nodes (10): description, type, description, type, properties, district, main_text, province (+2 more)

### Community 44 - "37. MVP Scope"
Cohesion: 0.25
Nodes (8): 37. MVP Scope, Canvas, Editor, Elements, Export, Interaction, Persistence, Properties

### Community 46 - "income_certificate/layout.py"
Cohesion: 0.47
Nodes (5): build_income_certificate(), _ea(), _lv(), Any, Income Certificate Layout — document_builder/income_certificate/layout_1.py…

### Community 47 - "items"
Cohesion: 0.17
Nodes (12): items, properties, required, type, description, type, name, relation (+4 more)

### Community 48 - "HTML document engine"
Cohesion: 0.05
Nodes (38): Adding a new document type, Agentic controller, Arbitrary HTML attributes (`attrs`), Architect Agent (`architect.py`), Architecture, Babu Document Digitization: Technical Documentation, Building one document by hand, Component reference (+30 more)

### Community 49 - "render_png"
Cohesion: 0.70
Nodes (4): _crop_to_page(), _page_metrics(), Path, render_png()

### Community 50 - "components/__init__.py"
Cohesion: 0.23
Nodes (8): html_engine.components — All renderable component types., Table components: Table, TableRow, TableCell. Supports both simple table…, A full ``<table>`` element. Can be built from: - Explicit ``TableRow`` objects…, A single table cell (``<td>`` or ``<th>``). Parameters: content: Cell content —…, A table row (``<tr>``) containing one or more cells. Parameters: cells:…, Table, TableCell, TableRow

### Community 51 - "44. Engineering Rules for the Agent"
Cohesion: 0.25
Nodes (8): 44. Engineering Rules for the Agent, Rule 1 — Document model first, Rule 2 — Single source of truth, Rule 3 — Components are renderers, Rule 4 — Commands modify state, Rule 5 — History is operation-based, Rule 6 — No premature complexity, Rule 7 — Extensibility

### Community 53 - "StyleWarning"
Cohesion: 0.67
Nodes (3): An unrecognized CSS property name reached ``Style``. Probably a typo., StyleWarning, UserWarning

### Community 54 - "date"
Cohesion: 0.67
Nodes (3): description, type, date

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

### Community 78 - "main.py"
Cohesion: 0.26
Nodes (11): build_data(), extract(), load_schema(), build_document(), digitize_document(), _blank_data(), Path, Manual entry point: turn one document into HTML (and optionally PNG). This is… (+3 more)

## Knowledge Gaps
- **222 isolated node(s):** `$schema`, `title`, `type`, `type`, `description` (+217 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style` to `test_components.py`, `html_engine/__init__.py`, `grid.py`, `base.py`, `LabelValue`, `FlexCol`, `spacer.py`, `laalpurja/layout.py`, `income_certificate/layout.py`, `Spacer`, `Component`, `components/__init__.py`, `Image`, `text.py`, `test_monochrome.py`, `Text`, `test_main_cli.py`?**
  _High betweenness centrality (0.310) - this node is a cross-community bridge._
- **Why does `active_layout_path()` connect `test_registry_resolution.py` to `run.py`, `architect.py`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `resolve_schema_path()` connect `test_registry_resolution.py` to `run.py`, `architect.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Style` (e.g. with `Component` and `FieldGroup`) actually correct?**
  _`Style` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Component` (e.g. with `Text` and `Style`) actually correct?**
  _`Component` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Text` (e.g. with `Component` and `PlaceholderBox`) actually correct?**
  _`Text` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Document` (e.g. with `Component` and `Style`) actually correct?**
  _`Document` has 2 INFERRED edges - model-reasoned connections that need verification._