# Graph Report - babu-documentation  (2026-08-11)

## Corpus Check
- 111 files · ~1,292,334 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1233 nodes · 2564 edges · 95 communities (78 shown, 17 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 74 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `951e8d0d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run.py
- test_components.py
- Editable Nepali citizenship certificate (romanized test render)
- grid.py
- .add
- citizenship/layout.py
- test_translator.py
- Style
- translator.py
- autolayout.py
- test_command_sandbox.py
- analyze_and_repair
- "First make it work, then make it better"
- test_registry_resolution.py
- prd.md
- Stages
- FlexRow
- Component
- required
- Image
- rag_engine.py
- page_geometry
- Salvage record: `controller-old/` → `agentic_controller/`
- langgraph dependency
- python-dotenv dependency
- validate_layout
- text.py
- LabelValue
- build_prompt
- 43. Acceptance Criteria
- Text
- test_autolayout.py
- DocLayout-YOLO
- Segment Anything Model for document analysis
- html_engine/__init__.py
- language_spec
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
- test_monochrome.py
- items
- HTML document engine
- PlaceholderBox
- laalpurja/layout.py
- 44. Engineering Rules for the Agent
- normalize_value
- Any
- .to_css
- 22. Properties Panel
- letter_no
- municipality
- FlexCol
- build_from_geometry
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
- components/__init__.py
- monochrome.py
- district
- Document
- Spacer
- Block
- blocks_from_conversion
- citizenship_old_back/layout.py
- write_plan_schema
- css_surface
- agentic_controller/__init__.py
- Ideal patching prompt composition
- Perfect-match VerificationReport example
- langchain-openai dependency
- pydantic dependency
- ref_no

## God Nodes (most connected - your core abstractions)
1. `Style` - 147 edges
2. `Component` - 58 edges
3. `Text` - 57 edges
4. `LabelValue` - 42 edges
5. `Document` - 41 edges
6. `FlexCol` - 37 edges
7. `FlexRow` - 33 edges
8. `_run()` - 32 edges
9. `PlaceholderBox` - 30 edges
10. `Spacer` - 29 edges

## Surprising Connections (you probably didn't know these)
- `test_an_empty_page_is_refused_not_guessed()` --calls--> `page_geometry()`  [EXTRACTED]
  tests/test_autolayout.py → document_builder/autolayout.py
- `test_route_1_style_to_css()` --calls--> `Style`  [EXTRACTED]
  tests/test_monochrome.py → html_engine/styles.py
- `test_route_3_style_raw_escape_hatch()` --calls--> `Style`  [EXTRACTED]
  tests/test_monochrome.py → html_engine/styles.py
- `test_protected_originals_cover_layouts_and_base_schemas()` --calls--> `_protected_originals()`  [EXTRACTED]
  tests/test_command_sandbox.py → agentic_controller/architect.py
- `current_layout_path()` --calls--> `active_layout_path()`  [EXTRACTED]
  agentic_controller/architect.py → document_builder/resolver.py

## Import Cycles
- None detected.

## Communities (95 total, 17 thin omitted)

### Community 0 - "run.py"
Cohesion: 0.14
Nodes (21): _crop_to_page(), _page_metrics(), Path, render_png(), _collect_decision(), _collect_user_concerns(), digitize(), main() (+13 more)

### Community 1 - "test_components.py"
Cohesion: 0.11
Nodes (23): Div, Generic block container rendered as a ``<div>``. The simplest building block —…, corner_box(), Faint centred text behind the page content. Absolutely positioned and non-…, The signature cluster that closes an official letter. Stacks, top to bottom:…, A placeholder pinned to one corner of the page — crest, QR block, stamp.…, SignatureBlock, Watermark (+15 more)

### Community 3 - "grid.py"
Cohesion: 0.15
Nodes (8): Card, Grid, GridItem, Any, Layout components: FlexRow, FlexCol, AbsoluteBox, Div. These are generic…, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, CSS Grid item. Parameters: column_span: Number of columns this item spans (e.g.…, A styled container mimicking a paper card. Includes preset styles: background…

### Community 5 - "citizenship/layout.py"
Cohesion: 0.42
Nodes (7): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main()

### Community 6 - "test_translator.py"
Cohesion: 0.05
Nodes (54): Tests for the translation stage. ``information_extraction/translator.py`` sits…, A sentence and a field label want different instructions, so they are batched…, A district repeated down a table is one string, not twenty., A half-converted date prints a year that looks Gregorian and is not., The SEE certificate prints ``certificate_title_np`` on one line and…, Without the English sibling, that value is the only one on the page., A laalpurja's ``plots`` is a list of dicts; every row must be reached., ``<field>_meta`` and ``<field>_citations`` are provenance the extractor… (+46 more)

### Community 7 - "Style"
Cohesion: 0.08
Nodes (26): An open set of CSS declarations. Any keyword is accepted and emitted as a CSS…, Return a new Style with *other*'s declarations overriding this one's. ``raw``…, Shorthand for ``merge``: ``combined = style_a + style_b``., Style, Tests for the open property bag that replaced the closed ``Style`` dataclass.…, Monochrome is enforced on the way out, including for unlisted props., The reported crash. Any valid CSS property must survive to the output., Both are deliberate, so neither should look like a typo. (+18 more)

### Community 8 - "translator.py"
Cohesion: 0.06
Nodes (58): build_data(), extract(), load_schema(), LanguageSpec, Everything the translator needs to know about one target language. Parameters:…, build_document(), digitize_document(), _apply() (+50 more)

### Community 9 - "autolayout.py"
Cohesion: 0.13
Nodes (25): _emit_block(), _first_mention(), fit_text(), _font_size(), layout_source(), PageGeometry, place(), Placed (+17 more)

### Community 10 - "test_command_sandbox.py"
Cohesion: 0.11
Nodes (30): _protected_originals(), Content of each protected file, or None if it does not exist., Undo any modification to a protected original. Returns what was restored., Gate write_file: inside the writable trees, and never *onto* an original.…, _restore_changed(), _snapshot(), _tool_execute_command(), _write_allowed() (+22 more)

### Community 11 - "analyze_and_repair"
Cohesion: 0.15
Nodes (18): analyze_and_repair(), _build_system_prompt(), current_layout_path(), generate_resources(), _image(), _load_rules(), main(), Path (+10 more)

### Community 13 - "test_registry_resolution.py"
Cohesion: 0.06
Nodes (72): _DocumentEntry, Any, The document registry: which types exist, and how to build each one.…, One document type's ``{"builder": ..., "schema": ...}``. ``schema`` and…, Document types discovered from the filesystem, resolved on access. Deliberately…, _Registry, active_layout_name(), active_layout_path() (+64 more)

### Community 14 - "prd.md"
Cohesion: 0.05
Nodes (36): 10. Canvas, 11. Page Model, 12. Element Model, 13. Text Element, 14. Image Element, 15. Shape Element, 16. Dynamic Field Element, 17. Selection System (+28 more)

### Community 15 - "Stages"
Cohesion: 0.05
Nodes (36): Decisions settled up front, Deliberately not in scope, Frontend integration plan, How to read the two source documents, Sequencing, Stage 0 — Groundwork, Stage 10 — Export, Stage 11 — The agentic loop, made reviewable (+28 more)

### Community 16 - "FlexRow"
Cohesion: 0.14
Nodes (19): _address_value(), build_citizenship_old(), _ea(), field_row(), multi_row(), Any, Two-line address block matching the old citizenship form: जिल्ला : ............…, Attributes used by the visual editor to identify editable fields. (+11 more)

### Community 17 - "Component"
Cohesion: 0.14
Nodes (12): Component, Render all children to a concatenated HTML string., Build the HTML attribute string for this element. Combines ``css_class``,…, Render this component to an HTML string., Base class for all renderable document components. Parameters: style: Optional…, ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList. (+4 more)

### Community 18 - "required"
Cohesion: 0.14
Nodes (14): required, date, district, family_members, letter_no, main_text, municipality, office_name (+6 more)

### Community 19 - "Image"
Cohesion: 0.40
Nodes (3): Image, Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64.

### Community 20 - "rag_engine.py"
Cohesion: 0.10
Nodes (36): build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python(), _embed() (+28 more)

### Community 21 - "page_geometry"
Cohesion: 0.17
Nodes (25): page_geometry(), Fit the ink extent onto an A4 sheet with one uniform scale. Orientation follows…, _blocks(), _placed(), _plan(), The aspect-ratio guarantee, asserted at its source. Two factors would fit the…, Nothing may sit where a printer's unprintable edge would clip it., Shape follows whichever the caption mentions *first*: a caption names its… (+17 more)

### Community 22 - "Salvage record: `controller-old/` → `agentic_controller/`"
Cohesion: 0.33
Nodes (5): Behaviour to reproduce in Phase 2/3, Carried across, Deliberately dropped, Not indexed by RAG, Salvage record: `controller-old/` → `agentic_controller/`

### Community 25 - "validate_layout"
Cohesion: 0.20
Nodes (20): Check that a generated layout module is safe for the caller to use. Four gates,…, validate_layout(), _layout(), Path, Tests for ``architect.validate_layout`` — the gate that let the reported bug…, Blank probe data is the harsh case. A layout indexing a key the schema does not…, A property outside the known list is a cosmetic gap, not a reason to fail a…, Without a schema the builder is probed with ``{}``. (+12 more)

### Community 26 - "text.py"
Cohesion: 0.14
Nodes (7): Link, Paragraph, Text components: Text, Heading, Paragraph, Link., Escape hatch: renders arbitrary HTML verbatim. Use sparingly — this bypasses…, Renders an anchor element ``<a>``. Parameters: content: The text content or…, Block paragraph element rendered as ``<p>``. Parameters: content: The paragraph…, RawHTML

### Community 27 - "LabelValue"
Cohesion: 0.21
Nodes (9): build_income_certificate(), _ea(), _lv(), Any, Income Certificate Layout — document_builder/income_certificate/layout_1.py…, LabelValue, A single label–value row rendered as a flex container. The label is displayed…, The label is chrome; only the value is extracted data. (+1 more)

### Community 28 - "build_prompt"
Cohesion: 0.18
Nodes (13): build_prompt(), The full verification system prompt for one target language., Tests for the verification prompt's target language.…, Latin examples in a Japanese prompt would teach the wrong script., Only rule 1 varies; placeholders, formatting, and colour do not., ``verification-rules.md`` mirrors this prompt rule by rule., ``SYSTEM_PROMPT`` is what ``verification-rules.md`` documents., test_an_unsupported_language_is_refused() (+5 more)

### Community 29 - "43. Acceptance Criteria"
Cohesion: 0.10
Nodes (21): 43. Acceptance Criteria, AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07 (+13 more)

### Community 30 - "Text"
Cohesion: 0.24
Nodes (6): Inline text element rendered as a ``<span>``. Parameters: content: The text…, Text, ``field=`` uses setdefault, so a layout that needs a non-editable but labelled…, test_container_skips_none_children(), test_explicit_attrs_win_over_field(), test_field_makes_a_component_editable()

### Community 31 - "test_autolayout.py"
Cohesion: 0.10
Nodes (20): Tests for ``document_builder/autolayout.py`` — the geometry half of layout…, 34 Text + 5 Picture. A dropped block is content silently lost., An ``<img alt="...">`` stripped of tags leaves a sentence describing the…, A tall document must not be letterboxed onto a landscape sheet., A label left of its value on the scan stays left of it on the sheet., The bbox is the line box; glyphs are roughly 62 % of it., A translated label runs longer than the Devanagari it replaces., Datalab's alt is a full sentence and overflows the box it labels. (+12 more)

### Community 34 - "html_engine/__init__.py"
Cohesion: 0.14
Nodes (16): Image component for the HTML Document Engine., Placeholder components for document furniture the render cannot reproduce. A…, em(), pct(), pt(), px(), Style descriptor for the HTML Document Engine. ``Style`` is an **open**…, An unrecognized CSS property name reached ``Style``. Probably a typo. (+8 more)

### Community 35 - "language_spec"
Cohesion: 0.15
Nodes (14): Machine-readable result returned by the vision model. This is the contract the…, Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, VerificationReport, image_data_url(), main(), Path, Vision-model comparison of a source document against its rendered replica.…, Validate a local raster image and encode it for a multimodal model message.… (+6 more)

### Community 37 - "office_name"
Cohesion: 0.67
Nodes (3): description, type, office_name

### Community 39 - "architect.py"
Cohesion: 0.13
Nodes (32): _dispatch_tool(), _field_name(), _log_call(), _parse_contract(), _parse_json_object(), _parse_plan(), _plan_block_lines(), plan_blocks() (+24 more)

### Community 40 - "models.py"
Cohesion: 0.17
Nodes (14): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., A single change to the extraction JSON schema., A single structural change to the document layout builder., RepairPlan (+6 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

### Community 42 - "base.py"
Cohesion: 0.11
Nodes (16): ABC, coerce_child(), coerce_children(), editable_attrs(), Any, Abstract base class for all HTML Document Engine components. Every renderable…, Append one or more child components. Returns self for chaining., Turn one constructor argument into a child component, or reject it. Components… (+8 more)

### Community 43 - "properties"
Cohesion: 0.20
Nodes (10): description, type, description, type, properties, date, main_text, province (+2 more)

### Community 44 - "37. MVP Scope"
Cohesion: 0.25
Nodes (8): 37. MVP Scope, Canvas, Editor, Elements, Export, Interaction, Persistence, Properties

### Community 46 - "test_monochrome.py"
Cohesion: 0.13
Nodes (18): find_violations(), Report colour tokens that normalization *would* change. Accepts either a CSS…, Tests for the monochrome guarantee. Project rule: a rendered document is purely…, A component can carry a hand-written style attribute, bypassing Style., A component's own ``to_html()`` can hardcode a style the engine never sees as a…, One document exercising every route at once, audited by find_violations., An autolayout placeholder caption reads "Red circular official seal of the…, The narrowed scan must not have narrowed past a genuine violation. (+10 more)

### Community 47 - "items"
Cohesion: 0.17
Nodes (12): items, properties, required, type, description, type, name, relation (+4 more)

### Community 48 - "HTML document engine"
Cohesion: 0.05
Nodes (39): Adding a new document type, Agentic controller, Arbitrary HTML attributes (`attrs`), Architect Agent (`architect.py`), Architecture, Babu Document Digitization: Technical Documentation, Building one document by hand, Component reference (+31 more)

### Community 49 - "PlaceholderBox"
Cohesion: 0.17
Nodes (13): build_tax_clearance(), _ea(), Any, AbsoluteBox, Absolutely positioned container. Use for elements that need precise pixel…, PlaceholderBox, A labelled outline standing in for artwork that cannot be rendered. Renders a…, A fixed pixel radius would not stay elliptical on a non-square box. (+5 more)

### Community 50 - "laalpurja/layout.py"
Cohesion: 0.25
Nodes (12): build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th(), _to_float() (+4 more)

### Community 51 - "44. Engineering Rules for the Agent"
Cohesion: 0.25
Nodes (8): 44. Engineering Rules for the Agent, Rule 1 — Document model first, Rule 2 — Single source of truth, Rule 3 — Components are renderers, Rule 4 — Commands modify state, Rule 5 — History is operation-based, Rule 6 — No premature complexity, Rule 7 — Extensibility

### Community 52 - "normalize_value"
Cohesion: 0.13
Nodes (15): normalize_value(), Rewrite every colour token in a single declaration's *value*. Parameters: prop:…, Thresholding by luminance would map a dark fill to black and its light text to…, A curated subset leaked ``rebeccapurple``. Any name the regex misses passes…, Alternation is scanned left to right. With "red" ordered before "rebeccapurple"…, Rewriting transparent to white paints over content meant to show through., Corrupting document data is worse than leaking a colour., A url(...) may hold a "#" fragment that is not a colour. (+7 more)

### Community 53 - "Any"
Cohesion: 0.28
Nodes (4): Any, Record one declaration, warning if the property looks misspelled., Iterate ``(python_name, value)`` for every set property., Return a copy with specific properties overridden. Passing ``None`` removes a…

### Community 54 - ".to_css"
Cohesion: 0.25
Nodes (5): _css_name(), Map a Python keyword to its CSS property name. ``font_size`` -> ``font-size``.…, Set properties in emission order: known first, then unknown., Serialize to an inline CSS declaration string. Colours are normalized to black-…, Return a full ``style="..."`` attribute, or ``""`` if empty.

### Community 58 - "22. Properties Panel"
Cohesion: 0.40
Nodes (5): 22. Properties Panel, Advanced, Appearance, Position, Text

### Community 59 - "letter_no"
Cohesion: 0.67
Nodes (3): description, type, letter_no

### Community 60 - "municipality"
Cohesion: 0.67
Nodes (3): description, type, municipality

### Community 61 - "FlexCol"
Cohesion: 0.27
Nodes (13): build_citizenship_back(), _ea(), field_row(), multi_row(), _officer_block(), _officer_row(), _place_block(), Any (+5 more)

### Community 62 - "build_from_geometry"
Cohesion: 0.20
Nodes (13): build_from_geometry(), Build a layout and schema from the scan's own block geometry. The geometry-…, Check that a written schema is valid JSON with the keys the extractor needs.…, validate_schema(), convert(), load_conversion(), Any, Path (+5 more)

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

### Community 78 - "components/__init__.py"
Cohesion: 0.24
Nodes (6): html_engine.components — All renderable component types., Table components: Table, TableRow, TableCell. Supports both simple table…, A single table cell (``<td>`` or ``<th>``). Parameters: content: Cell content —…, A table row (``<tr>``) containing one or more cells. Parameters: cells:…, TableCell, TableRow

### Community 79 - "monochrome.py"
Cohesion: 0.19
Nodes (11): normalize_declarations(), normalize_html(), Monochrome enforcement for the HTML Document Engine. Project rule: a rendered…, Surfaces go white, ink goes black., Rewrite colours across a CSS fragment. Works both on an inline declaration list…, Rewrite colours in a complete HTML document. Only ``style="..."`` attributes…, _target_for(), Render a Document class to a full HTML string. The output is a self-contained… (+3 more)

### Community 80 - "district"
Cohesion: 0.67
Nodes (3): description, type, district

### Community 81 - "Document"
Cohesion: 0.20
Nodes (11): build_transfer_certificate(), _ea(), Any, Transfer Certificate Layout — document_builder/transfer_certificate/layout_1.py…, Document, A single page of output. Parameters: title: ``<title>`` text. page_width: Width…, A clipped overflow and a genuinely missing section look identical in the…, test_clip_false_lets_overflow_show() (+3 more)

### Community 82 - "Spacer"
Cohesion: 0.24
Nodes (8): build_relationship_certificate(), _ea(), Any, Relationship Certificate Layout —…, Empty space of a fixed size. Vertical by default. A ``width`` makes it a…, Spacer, A horizontal spacer inside a flex row needs flex-shrink:0 to survive., test_spacer_gutter_is_not_squeezed_away()

### Community 83 - "Block"
Cohesion: 0.25
Nodes (6): Block, ink_extent(), The bounding box of every block, in source space. Deliberately not the page…, One block from the conversion tree, in the source's coordinate space.…, The conversion page is 1372x980 around ink that is 1201x799. Normalizing…, test_extent_is_the_ink_not_the_page()

### Community 84 - "blocks_from_conversion"
Cohesion: 0.25
Nodes (8): blocks_from_conversion(), _clean(), Strip tags and collapse whitespace, leaving the readable text., Flatten one page of a ``/convert`` tree into :class:`Block` objects. Blocks…, A block with no usable bbox contributes nothing and skews the extent., Same scan, same layout — the reason this half is not a model call., test_blocks_without_geometry_are_dropped(), test_geometry_is_deterministic()

### Community 85 - "citizenship_old_back/layout.py"
Cohesion: 0.46
Nodes (7): build_citizenship_old_back(), _ea(), editable_text(), field_row(), multi_row(), Any, Build the English reproduction of the back side of the old Nepali Citizenship…

### Community 86 - "write_plan_schema"
Cohesion: 0.33
Nodes (6): plan_to_schema(), Build the extraction schema for the value fields *plan* names. Every value…, Write :func:`plan_to_schema` output to the schema directory and return it., write_plan_schema(), ``build_data`` keeps only what the schema lists as required, so a field the…, test_every_field_survives_extraction()

### Community 87 - "css_surface"
Cohesion: 0.50
Nodes (4): css_surface(), The parts of *text* that are actually CSS. A full HTML page contributes its…, A page contributes its style attributes and style blocks, nothing else., test_css_surface_separates_style_from_prose()

### Community 94 - "ref_no"
Cohesion: 0.67
Nodes (3): ref_no, description, type

## Knowledge Gaps
- **224 isolated node(s):** `$schema`, `title`, `type`, `type`, `description` (+219 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style` to `test_components.py`, `grid.py`, `citizenship/layout.py`, `translator.py`, `FlexRow`, `Component`, `Image`, `text.py`, `LabelValue`, `Text`, `html_engine/__init__.py`, `base.py`, `test_monochrome.py`, `PlaceholderBox`, `laalpurja/layout.py`, `Any`, `.to_css`, `FlexCol`, `spacer.py`, `components/__init__.py`, `Document`, `Spacer`, `citizenship_old_back/layout.py`?**
  _High betweenness centrality (0.228) - this node is a cross-community bridge._
- **Why does `find_violations()` connect `test_monochrome.py` to `test_autolayout.py`, `page_geometry`, `css_surface`, `monochrome.py`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `validate_layout()` connect `validate_layout` to `architect.py`, `analyze_and_repair`, `page_geometry`, `build_from_geometry`, `test_autolayout.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Style` (e.g. with `Component` and `FieldGroup`) actually correct?**
  _`Style` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Component` (e.g. with `Text` and `Style`) actually correct?**
  _`Component` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Text` (e.g. with `Component` and `PlaceholderBox`) actually correct?**
  _`Text` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `LabelValue` (e.g. with `Component` and `Style`) actually correct?**
  _`LabelValue` has 2 INFERRED edges - model-reasoned connections that need verification._