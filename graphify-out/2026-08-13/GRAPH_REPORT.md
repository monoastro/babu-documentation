# Graph Report - babu-documentation  (2026-08-13)

## Corpus Check
- 102 files · ~764,505 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1250 nodes · 2553 edges · 102 communities (81 shown, 21 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 82 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7a573952`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run.py
- test_components.py
- Editable Nepali citizenship certificate (romanized test render)
- grid.py
- components/__init__.py
- Text
- test_translator.py
- test_styles.py
- translator.py
- autolayout.py
- test_command_sandbox.py
- placeholder.py
- "First make it work, then make it better"
- test_registry_resolution.py
- prd.md
- Stages
- LabelValue
- Component
- required
- FlexCol
- rag_engine.py
- test_autolayout.py
- Salvage record: `controller-old/` → `agentic_controller/`
- langgraph dependency
- python-dotenv dependency
- validate_layout
- Document
- test_monochrome.py
- monochrome.py
- 43. Acceptance Criteria
- analyze_and_repair
- .to_css
- DocLayout-YOLO
- Segment Anything Model for document analysis
- html_engine/__init__.py
- css_surface
- Surya (datalab-to)
- office_name
- CLAUDE.md
- architect.py
- models.py
- 1. Document Verification Rules
- base.py
- properties
- 37. MVP Scope
- run_all.py
- find_violations
- items
- HTML document engine
- Image
- laalpurja/layout.py
- 44. Engineering Rules for the Agent
- Style
- Any
- test_orientation_follows_the_source
- Any
- build_pan
- 22. Properties Panel
- letter_no
- municipality
- build_prompt
- build_from_geometry
- main.py
- ward_chairperson_name
- ward_chairperson_title
- ward_no
- 5. Technology Requirements
- test_main_cli.py
- spacer.py
- .save
- 3. Target User
- 8. Toolbar
- relationship_certificate.json
- 35. Non-Functional Requirements
- family_members
- PRD — Visual HTML Document Editing Engine
- 4. Core Design Principle
- Heading
- .__add__
- blocks_from_conversion
- language_spec
- render_png
- Block
- test_route_2_raw_style_string_in_attrs
- subject
- write_plan_schema
- district
- agentic_controller/__init__.py
- Ideal patching prompt composition
- Perfect-match VerificationReport example
- langchain-openai dependency
- pydantic dependency
- ref_no
- test_a_long_string_is_shrunk_to_fit
- test_a_caption_is_cut_to_the_box
- Any

## God Nodes (most connected - your core abstractions)
1. `Style` - 144 edges
2. `Component` - 58 edges
3. `Text` - 55 edges
4. `LabelValue` - 41 edges
5. `Document` - 41 edges
6. `FlexCol` - 35 edges
7. `_run()` - 32 edges
8. `FlexRow` - 31 edges
9. `PlaceholderBox` - 30 edges
10. `Div` - 29 edges

## Surprising Connections (you probably didn't know these)
- `build_pan()` --calls--> `FieldGroup`  [INFERRED]
  document_builder/pan/layout.py → html_engine/components/field.py
- `build_pan()` --calls--> `AbsoluteBox`  [INFERRED]
  document_builder/pan/layout.py → html_engine/components/grid.py
- `build_pan()` --calls--> `Div`  [INFERRED]
  document_builder/pan/layout.py → html_engine/components/grid.py
- `build_pan()` --calls--> `FlexCol`  [INFERRED]
  document_builder/pan/layout.py → html_engine/components/grid.py
- `build_pan()` --calls--> `FlexRow`  [INFERRED]
  document_builder/pan/layout.py → html_engine/components/grid.py

## Import Cycles
- None detected.

## Communities (102 total, 21 thin omitted)

### Community 0 - "run.py"
Cohesion: 0.11
Nodes (28): current_layout_path(), The layout that will actually be built — whatever ``ACTIVE`` names. This used…, Machine-readable result returned by the vision model. This is the contract the…, VerificationReport, _collect_decision(), _collect_user_concerns(), digitize(), main() (+20 more)

### Community 1 - "test_components.py"
Cohesion: 0.07
Nodes (34): Div, Generic block container rendered as a ``<div>``. The simplest building block —…, corner_box(), Faint centred text behind the page content. Absolutely positioned and non-…, A placeholder pinned to one corner of the page — crest, QR block, stamp.…, Watermark, Tests for the components added for this project's documents, and for the…, A fixed pixel radius would not stay elliptical on a non-square box. (+26 more)

### Community 3 - "grid.py"
Cohesion: 0.18
Nodes (7): Card, Grid, GridItem, Layout components: FlexRow, FlexCol, AbsoluteBox, Div. These are generic…, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, CSS Grid item. Parameters: column_span: Number of columns this item spans (e.g.…, A styled container mimicking a paper card. Includes preset styles: background…

### Community 4 - "components/__init__.py"
Cohesion: 0.18
Nodes (10): html_engine.components — All renderable component types., Table components: Table, TableRow, TableCell. Supports both simple table…, A full ``<table>`` element. Can be built from: - Explicit ``TableRow`` objects…, A single table cell (``<td>`` or ``<th>``). Parameters: content: Cell content —…, A table row (``<tr>``) containing one or more cells. Parameters: cells:…, Table, TableCell, TableRow (+2 more)

### Community 5 - "Text"
Cohesion: 0.11
Nodes (29): build_income_certificate(), _ea(), _lv(), Any, Income Certificate Layout — document_builder/income_certificate/layout_1.py…, build_relationship_certificate(), _ea(), Any (+21 more)

### Community 6 - "test_translator.py"
Cohesion: 0.06
Nodes (52): Tests for the translation stage. ``information_extraction/translator.py`` sits…, A sentence and a field label want different instructions, so they are batched…, A district repeated down a table is one string, not twenty., A half-converted date prints a year that looks Gregorian and is not., The SEE certificate prints ``certificate_title_np`` on one line and…, Without the English sibling, that value is the only one on the page., A laalpurja's ``plots`` is a list of dicts; every row must be reached., ``<field>_meta`` and ``<field>_citations`` are provenance the extractor… (+44 more)

### Community 7 - "test_styles.py"
Cohesion: 0.08
Nodes (22): Tests for the open property bag that replaced the closed ``Style`` dataclass.…, Monochrome is enforced on the way out, including for unlisted props., The reported crash. Any valid CSS property must survive to the output., Both are deliberate, so neither should look like a typo., The trade for accepting anything: a misspelling is no longer a TypeError. It…, What ``main.py --strict`` relies on., A name CSS could never accept is a bug worth stopping for., CSS resolves duplicates last-one-wins, so ``margin`` emitted after ``margin-… (+14 more)

### Community 8 - "translator.py"
Cohesion: 0.13
Nodes (26): _apply(), bs_to_ad(), _cache_key(), _collect(), _has_letters(), _is_ascii(), _is_identifier(), _is_meta_key() (+18 more)

### Community 9 - "autolayout.py"
Cohesion: 0.13
Nodes (25): _emit_block(), _first_mention(), fit_text(), _font_size(), layout_source(), PageGeometry, place(), Placed (+17 more)

### Community 10 - "test_command_sandbox.py"
Cohesion: 0.11
Nodes (31): _protected_originals(), Path, Content of each protected file, or None if it does not exist., Undo any modification to a protected original. Returns what was restored., Gate write_file: inside the writable trees, and never *onto* an original.…, _restore_changed(), _snapshot(), _tool_execute_command() (+23 more)

### Community 11 - "placeholder.py"
Cohesion: 0.18
Nodes (6): Placeholder components for document furniture the render cannot reproduce. A…, Link, Text components: Text, Heading, Paragraph, Link., Escape hatch: renders arbitrary HTML verbatim. Use sparingly — this bypasses…, Renders an anchor element ``<a>``. Parameters: content: The text content or…, RawHTML

### Community 13 - "test_registry_resolution.py"
Cohesion: 0.06
Nodes (72): _DocumentEntry, Any, The document registry: which types exist, and how to build each one.…, One document type's ``{"builder": ..., "schema": ...}``. ``schema`` and…, Document types discovered from the filesystem, resolved on access. Deliberately…, _Registry, active_layout_name(), active_layout_path() (+64 more)

### Community 14 - "prd.md"
Cohesion: 0.05
Nodes (36): 10. Canvas, 11. Page Model, 12. Element Model, 13. Text Element, 14. Image Element, 15. Shape Element, 16. Dynamic Field Element, 17. Selection System (+28 more)

### Community 15 - "Stages"
Cohesion: 0.05
Nodes (36): Decisions settled up front, Deliberately not in scope, Frontend integration plan, How to read the two source documents, Sequencing, Stage 0 — Groundwork, Stage 10 — Export, Stage 11 — The agentic loop, made reviewable (+28 more)

### Community 16 - "LabelValue"
Cohesion: 0.17
Nodes (17): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, build_citizenship_old(), _ea() (+9 more)

### Community 17 - "Component"
Cohesion: 0.16
Nodes (11): Component, Render all children to a concatenated HTML string., Render this component to an HTML string., Base class for all renderable document components. Parameters: style: Optional…, ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList., Renders a list item ``<li>``. Parameters: content: String content or nested… (+3 more)

### Community 18 - "required"
Cohesion: 0.14
Nodes (14): required, date, district, family_members, letter_no, main_text, municipality, office_name (+6 more)

### Community 19 - "FlexCol"
Cohesion: 0.29
Nodes (13): build_citizenship_back(), _ea(), field_row(), multi_row(), _officer_block(), _officer_row(), _place_block(), Any (+5 more)

### Community 20 - "rag_engine.py"
Cohesion: 0.10
Nodes (36): build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python(), _embed() (+28 more)

### Community 21 - "test_autolayout.py"
Cohesion: 0.11
Nodes (38): page_geometry(), Fit the ink extent onto an A4 sheet with one uniform scale. Orientation follows…, _blocks(), _placed(), _plan(), Tests for ``document_builder/autolayout.py`` — the geometry half of layout…, 34 Text + 5 Picture. A dropped block is content silently lost., An ``<img alt="...">`` stripped of tags leaves a sentence describing the… (+30 more)

### Community 22 - "Salvage record: `controller-old/` → `agentic_controller/`"
Cohesion: 0.33
Nodes (5): Behaviour to reproduce in Phase 2/3, Carried across, Deliberately dropped, Not indexed by RAG, Salvage record: `controller-old/` → `agentic_controller/`

### Community 25 - "validate_layout"
Cohesion: 0.20
Nodes (20): Check that a generated layout module is safe for the caller to use. Four gates,…, validate_layout(), _layout(), Path, Tests for ``architect.validate_layout`` — the gate that let the reported bug…, Blank probe data is the harsh case. A layout indexing a key the schema does not…, A property outside the known list is a cosmetic gap, not a reason to fail a…, Without a schema the builder is probed with ``{}``. (+12 more)

### Community 26 - "Document"
Cohesion: 0.10
Nodes (23): build_citizenship_old_back(), Any, Build the English reproduction of the back of the old-format Nepali Citizenship…, The shared value style at a specific column width., One label–value row of the reverse sheet., One thumb-impression box, captioned along its bottom edge. The two boxes butt…, _row(), _thumb_box() (+15 more)

### Community 27 - "test_monochrome.py"
Cohesion: 0.14
Nodes (18): normalize_value(), Rewrite every colour token in a single declaration's *value*. Parameters: prop:…, Tests for the monochrome guarantee. Project rule: a rendered document is purely…, Thresholding by luminance would map a dark fill to black and its light text to…, A curated subset leaked ``rebeccapurple``. Any name the regex misses passes…, Alternation is scanned left to right. With "red" ordered before "rebeccapurple"…, Rewriting transparent to white paints over content meant to show through., Corrupting document data is worse than leaking a colour. (+10 more)

### Community 28 - "monochrome.py"
Cohesion: 0.18
Nodes (10): Build the HTML attribute string for this element. Combines ``css_class``,…, normalize_declarations(), normalize_html(), Monochrome enforcement for the HTML Document Engine. Project rule: a rendered…, Surfaces go white, ink goes black., Rewrite colours across a CSS fragment. Works both on an inline declaration list…, Rewrite colours in a complete HTML document. Only ``style="..."`` attributes…, _target_for() (+2 more)

### Community 29 - "43. Acceptance Criteria"
Cohesion: 0.10
Nodes (21): 43. Acceptance Criteria, AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07 (+13 more)

### Community 30 - "analyze_and_repair"
Cohesion: 0.16
Nodes (14): analyze_and_repair(), _dispatch_tool(), main(), Build a RepairResult, trusting the filesystem over the agent's claims., Repair the layout and/or schema so the next render passes verification.…, What the Architect Agent produced on one invocation., Human-readable one-screen summary, for the Phase 3 checkpoint., Resolve a model-supplied path against the project root. (+6 more)

### Community 31 - ".to_css"
Cohesion: 0.25
Nodes (5): _css_name(), Map a Python keyword to its CSS property name. ``font_size`` -> ``font-size``.…, Set properties in emission order: known first, then unknown., Serialize to an inline CSS declaration string. Colours are normalized to black-…, Return a full ``style="..."`` attribute, or ``""`` if empty.

### Community 34 - "html_engine/__init__.py"
Cohesion: 0.14
Nodes (17): Document — the root of a renderable page. doc = Document("My Certificate",…, Render a Document class to a full HTML string. The output is a self-contained…, render(), em(), pct(), pt(), px(), Style descriptor for the HTML Document Engine. ``Style`` is an **open**… (+9 more)

### Community 35 - "css_surface"
Cohesion: 0.50
Nodes (4): css_surface(), The parts of *text* that are actually CSS. A full HTML page contributes its…, A page contributes its style attributes and style blocks, nothing else., test_css_surface_separates_style_from_prose()

### Community 37 - "office_name"
Cohesion: 0.67
Nodes (3): description, type, office_name

### Community 39 - "architect.py"
Cohesion: 0.12
Nodes (33): _build_system_prompt(), _field_name(), generate_resources(), _image(), _load_rules(), _log_call(), _parse_contract(), _parse_json_object() (+25 more)

### Community 40 - "models.py"
Cohesion: 0.14
Nodes (15): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, A single change to the extraction JSON schema., A single structural change to the document layout builder. (+7 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

### Community 42 - "base.py"
Cohesion: 0.13
Nodes (13): ABC, coerce_child(), coerce_children(), editable_attrs(), Any, Abstract base class for all HTML Document Engine components. Every renderable…, Append one or more child components. Returns self for chaining., Turn one constructor argument into a child component, or reject it. Components… (+5 more)

### Community 43 - "properties"
Cohesion: 0.20
Nodes (10): description, type, description, type, properties, date, main_text, province (+2 more)

### Community 44 - "37. MVP Scope"
Cohesion: 0.25
Nodes (8): 37. MVP Scope, Canvas, Editor, Elements, Export, Interaction, Persistence, Properties

### Community 46 - "find_violations"
Cohesion: 0.22
Nodes (9): find_violations(), Report colour tokens that normalization *would* change. Accepts either a CSS…, An autolayout placeholder caption reads "Red circular official seal of the…, The narrowed scan must not have narrowed past a genuine violation., The guarantee that actually matters: every shipped document type., test_find_violations_ignores_document_prose(), test_find_violations_reports_pairs(), test_find_violations_still_catches_a_leak_beside_prose() (+1 more)

### Community 47 - "items"
Cohesion: 0.17
Nodes (12): items, properties, required, type, description, type, name, relation (+4 more)

### Community 48 - "HTML document engine"
Cohesion: 0.05
Nodes (39): Adding a new document type, Agentic controller, Arbitrary HTML attributes (`attrs`), Architect Agent (`architect.py`), Architecture, Babu Document Digitization: Technical Documentation, Building one document by hand, Component reference (+31 more)

### Community 49 - "Image"
Cohesion: 0.29
Nodes (4): Image, Image component for the HTML Document Engine., Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64.

### Community 50 - "laalpurja/layout.py"
Cohesion: 0.25
Nodes (12): build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th(), _to_float() (+4 more)

### Community 51 - "44. Engineering Rules for the Agent"
Cohesion: 0.25
Nodes (8): 44. Engineering Rules for the Agent, Rule 1 — Document model first, Rule 2 — Single source of truth, Rule 3 — Components are renderers, Rule 4 — Commands modify state, Rule 5 — History is operation-based, Rule 6 — No premature complexity, Rule 7 — Extensibility

### Community 52 - "Style"
Cohesion: 0.14
Nodes (4): Any, Any, An open set of CSS declarations. Any keyword is accepted and emitted as a CSS…, Style

### Community 53 - "Any"
Cohesion: 0.28
Nodes (4): Any, Record one declaration, warning if the property looks misspelled., Iterate ``(python_name, value)`` for every set property., Return a copy with specific properties overridden. Passing ``None`` removes a…

### Community 55 - "test_orientation_follows_the_source"
Cohesion: 0.50
Nodes (4): Block, A tall document must not be letterboxed onto a landscape sheet., _synthetic(), test_orientation_follows_the_source()

### Community 57 - "build_pan"
Cohesion: 0.33
Nodes (7): Any, Document, build_pan(), field_row(), main(), LabelValue, Style

### Community 58 - "22. Properties Panel"
Cohesion: 0.40
Nodes (5): 22. Properties Panel, Advanced, Appearance, Position, Text

### Community 59 - "letter_no"
Cohesion: 0.67
Nodes (3): description, type, letter_no

### Community 60 - "municipality"
Cohesion: 0.67
Nodes (3): description, type, municipality

### Community 61 - "build_prompt"
Cohesion: 0.18
Nodes (13): build_prompt(), The full verification system prompt for one target language., Tests for the verification prompt's target language.…, Latin examples in a Japanese prompt would teach the wrong script., Only rule 1 varies; placeholders, formatting, and colour do not., ``verification-rules.md`` mirrors this prompt rule by rule., ``SYSTEM_PROMPT`` is what ``verification-rules.md`` documents., test_an_unsupported_language_is_refused() (+5 more)

### Community 62 - "build_from_geometry"
Cohesion: 0.20
Nodes (13): build_from_geometry(), Build a layout and schema from the scan's own block geometry. The geometry-…, Check that a written schema is valid JSON with the keys the extractor needs.…, validate_schema(), convert(), load_conversion(), Any, Path (+5 more)

### Community 63 - "main.py"
Cohesion: 0.24
Nodes (12): build_data(), extract(), load_schema(), build_document(), digitize_document(), _blank_data(), Path, Manual entry point: turn one document into HTML (and optionally PNG). This is… (+4 more)

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

### Community 68 - "test_main_cli.py"
Cohesion: 0.23
Nodes (14): main(), _out(), Path, Tests for the manual entry point. ``main.py`` is the hand-driven counterpart to…, The engine warns on an unrecognized property rather than raising, so…, Proven by breaking the OCR import: if the extractor were reached, this would…, _run(), test_blank_builds_every_registered_type() (+6 more)

### Community 69 - "spacer.py"
Cohesion: 0.25
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

### Community 78 - "Heading"
Cohesion: 0.38
Nodes (5): build_letter(), _ea(), Any, Heading, Block heading element rendered as ``<h1>`` through ``<h6>``. Parameters:…

### Community 80 - "blocks_from_conversion"
Cohesion: 0.25
Nodes (8): blocks_from_conversion(), _clean(), Strip tags and collapse whitespace, leaving the readable text., Flatten one page of a ``/convert`` tree into :class:`Block` objects. Blocks…, A block with no usable bbox contributes nothing and skews the extent., Same scan, same layout — the reason this half is not a model call., test_blocks_without_geometry_are_dropped(), test_geometry_is_deterministic()

### Community 81 - "language_spec"
Cohesion: 0.14
Nodes (14): language_spec(), LanguageSpec, Target languages the translator can render a document into. One…, Everything the translator needs to know about one target language. Parameters:…, Look up a target language, naming the supported codes on failure., build_prompt(), The result of translating one document's extracted data., The system prompt for one target language. (+6 more)

### Community 82 - "render_png"
Cohesion: 0.70
Nodes (4): _crop_to_page(), _page_metrics(), Path, render_png()

### Community 83 - "Block"
Cohesion: 0.25
Nodes (6): Block, ink_extent(), The bounding box of every block, in source space. Deliberately not the page…, One block from the conversion tree, in the source's coordinate space.…, The conversion page is 1372x980 around ink that is 1201x799. Normalizing…, test_extent_is_the_ink_not_the_page()

### Community 84 - "test_route_2_raw_style_string_in_attrs"
Cohesion: 0.33
Nodes (4): A component can carry a hand-written style attribute, bypassing Style., A component's own ``to_html()`` can hardcode a style the engine never sees as a…, test_route_2_raw_style_string_in_attrs(), test_route_4_hardcoded_to_html_fstring()

### Community 85 - "subject"
Cohesion: 0.67
Nodes (3): subject, description, type

### Community 86 - "write_plan_schema"
Cohesion: 0.33
Nodes (6): plan_to_schema(), Build the extraction schema for the value fields *plan* names. Every value…, Write :func:`plan_to_schema` output to the schema directory and return it., write_plan_schema(), ``build_data`` keeps only what the schema lists as required, so a field the…, test_every_field_survives_extraction()

### Community 87 - "district"
Cohesion: 0.67
Nodes (3): description, type, district

### Community 94 - "ref_no"
Cohesion: 0.67
Nodes (3): ref_no, description, type

## Knowledge Gaps
- **224 isolated node(s):** `$schema`, `title`, `type`, `type`, `description` (+219 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style` to `test_components.py`, `grid.py`, `components/__init__.py`, `Text`, `test_styles.py`, `placeholder.py`, `LabelValue`, `Component`, `FlexCol`, `Document`, `test_monochrome.py`, `monochrome.py`, `.to_css`, `html_engine/__init__.py`, `base.py`, `Image`, `laalpurja/layout.py`, `Any`, `spacer.py`, `Heading`, `.__add__`?**
  _High betweenness centrality (0.191) - this node is a cross-community bridge._
- **Why does `language_spec()` connect `language_spec` to `run.py`, `test_translator.py`, `architect.py`, `translator.py`, `build_prompt`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `Text` connect `Text` to `test_components.py`, `html_engine/__init__.py`, `components/__init__.py`, `base.py`, `placeholder.py`, `Heading`, `LabelValue`, `Component`, `laalpurja/layout.py`, `FlexCol`, `Style`, `test_route_2_raw_style_string_in_attrs`, `Document`, `test_monochrome.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Style` (e.g. with `Component` and `FieldGroup`) actually correct?**
  _`Style` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Component` (e.g. with `Style` and `FieldGroup`) actually correct?**
  _`Component` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Text` (e.g. with `PlaceholderBox` and `SignatureBlock`) actually correct?**
  _`Text` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `LabelValue` (e.g. with `Component` and `Style`) actually correct?**
  _`LabelValue` has 2 INFERRED edges - model-reasoned connections that need verification._