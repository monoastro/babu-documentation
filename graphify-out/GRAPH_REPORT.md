# Graph Report - babu-documentation  (2026-08-27)

## Corpus Check
- 114 files · ~794,939 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1340 nodes · 2755 edges · 106 communities (88 shown, 18 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 74 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7a573952`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run.py
- test_components.py
- Editable Nepali citizenship certificate (romanized test render)
- build_prompt
- LabelValue
- FlexRow
- test_translator.py
- Style
- translator.py
- autolayout.py
- test_command_sandbox.py
- Paragraph
- "First make it work, then make it better"
- test_registry_resolution.py
- prd.md
- Stages
- FlexCol
- Component
- required
- main.py
- rag_engine.py
- page_geometry
- Salvage record: `controller-old/` → `agentic_controller/`
- langgraph dependency
- python-dotenv dependency
- validate_layout
- citizenship_old_back/layout.py
- normalize_value
- monochrome.py
- 43. Acceptance Criteria
- _build_system_prompt
- .to_css
- DocLayout-YOLO
- Segment Anything Model for document analysis
- html_engine/__init__.py
- TableCell
- Surya (datalab-to)
- office_name
- test_main_cli.py
- architect.py
- verifier.py
- 1. Document Verification Rules
- coerce_children
- properties
- 37. MVP Scope
- run_all.py
- test_monochrome.py
- items
- HTML document engine
- Image
- Document Digitization Rules
- 44. Engineering Rules for the Agent
- components/__init__.py
- Any
- _apply
- test_autolayout.py
- AbsoluteBox
- pan/layout.py
- 22. Properties Panel
- letter_no
- municipality
- citizenship/layout.py
- load_conversion
- Babu Document Digitization — agent notes
- ward_chairperson_name
- ward_chairperson_title
- ward_no
- 5. Technology Requirements
- grid.py
- Spacer
- Document
- 3. Target User
- 8. Toolbar
- relationship_certificate.json
- 35. Non-Functional Requirements
- family_members
- PRD — Visual HTML Document Editing Engine
- 4. Core Design Principle
- Text
- find_violations
- blocks_from_conversion
- opencode.json
- One-shot HTML generation contract
- Block
- One-shot example-guided digitization
- subject
- value_fields
- language_spec
- agentic_controller/__init__.py
- Ideal patching prompt composition
- Perfect-match VerificationReport example
- langchain-openai dependency
- pydantic dependency
- graphify.js
- render_png
- Q: Why does language_spec() connect translator.py to run.py, test_translator.py, architect.py?
- district
- StyleWarning
- ref_no
- manifest.json
- examples/README.md

## God Nodes (most connected - your core abstractions)
1. `Style` - 163 edges
2. `Text` - 71 edges
3. `Component` - 58 edges
4. `Document` - 47 edges
5. `LabelValue` - 43 edges
6. `FlexCol` - 43 edges
7. `FlexRow` - 39 edges
8. `Div` - 37 edges
9. `PlaceholderBox` - 36 edges
10. `AbsoluteBox` - 32 edges

## Surprising Connections (you probably didn't know these)
- `test_an_empty_page_is_refused_not_guessed()` --calls--> `page_geometry()`  [EXTRACTED]
  tests/test_autolayout.py → document_builder/autolayout.py
- `test_editable_attrs_is_the_single_source_of_the_contract()` --calls--> `editable_attrs()`  [EXTRACTED]
  tests/test_components.py → html_engine/components/base.py
- `test_route_1_style_to_css()` --calls--> `Style`  [EXTRACTED]
  tests/test_monochrome.py → html_engine/styles.py
- `test_route_3_style_raw_escape_hatch()` --calls--> `Style`  [EXTRACTED]
  tests/test_monochrome.py → html_engine/styles.py
- `test_protected_originals_cover_layouts_and_base_schemas()` --calls--> `_protected_originals()`  [EXTRACTED]
  tests/test_command_sandbox.py → agentic_controller/architect.py

## Import Cycles
- None detected.

## Communities (106 total, 18 thin omitted)

### Community 0 - "run.py"
Cohesion: 0.10
Nodes (34): analyze_and_repair(), build_from_geometry(), current_layout_path(), generate_resources(), _image(), main(), Path, Repair the layout and/or schema so the next render passes verification.… (+26 more)

### Community 1 - "test_components.py"
Cohesion: 0.09
Nodes (28): build_pension_front(), _ea(), Div, Generic block container rendered as a ``<div>``. The simplest building block —…, corner_box(), PlaceholderBox, A labelled outline standing in for artwork that cannot be rendered. Renders a…, A placeholder pinned to one corner of the page — crest, QR block, stamp.… (+20 more)

### Community 3 - "build_prompt"
Cohesion: 0.18
Nodes (13): build_prompt(), The full verification system prompt for one target language., Tests for the verification prompt's target language.…, Latin examples in a Japanese prompt would teach the wrong script., Only rule 1 varies; placeholders, formatting, and colour do not., ``verification-rules.md`` mirrors this prompt rule by rule., ``SYSTEM_PROMPT`` is what ``verification-rules.md`` documents., test_an_unsupported_language_is_refused() (+5 more)

### Community 4 - "LabelValue"
Cohesion: 0.17
Nodes (18): build_citizenship_old(), _ea(), field_row(), multi_row(), Any, Attributes used by the visual editor to identify editable fields., build_income_certificate(), _ea() (+10 more)

### Community 5 - "FlexRow"
Cohesion: 0.16
Nodes (14): build_relationship_certificate(), _ea(), Any, Relationship Certificate Layout —…, build_see_certificate(), SEE Certificate Layout — document_builder/see_certificate/layout_1.py…, FlexRow, Horizontal flex container (``flex-direction: row``). Parameters: children:… (+6 more)

### Community 6 - "test_translator.py"
Cohesion: 0.06
Nodes (52): Tests for the translation stage. ``information_extraction/translator.py`` sits…, A sentence and a field label want different instructions, so they are batched…, A district repeated down a table is one string, not twenty., A half-converted date prints a year that looks Gregorian and is not., The SEE certificate prints ``certificate_title_np`` on one line and…, Without the English sibling, that value is the only one on the page., A laalpurja's ``plots`` is a list of dicts; every row must be reached., ``<field>_meta`` and ``<field>_citations`` are provenance the extractor… (+44 more)

### Community 7 - "Style"
Cohesion: 0.07
Nodes (28): PageBreak, Renders a page break for print media., An open set of CSS declarations. Any keyword is accepted and emitted as a CSS…, Return a new Style with *other*'s declarations overriding this one's. ``raw``…, Shorthand for ``merge``: ``combined = style_a + style_b``., Style, Tests for the open property bag that replaced the closed ``Style`` dataclass.…, Monochrome is enforced on the way out, including for unlisted props. (+20 more)

### Community 8 - "translator.py"
Cohesion: 0.13
Nodes (24): LanguageSpec, Everything the translator needs to know about one target language. Parameters:…, bs_to_ad(), build_prompt(), _cache_key(), _has_letters(), _is_ascii(), _is_identifier() (+16 more)

### Community 9 - "autolayout.py"
Cohesion: 0.14
Nodes (21): _emit_block(), _first_mention(), fit_text(), _font_size(), PageGeometry, place(), Placed, _px() (+13 more)

### Community 10 - "test_command_sandbox.py"
Cohesion: 0.11
Nodes (30): _protected_originals(), Content of each protected file, or None if it does not exist., Undo any modification to a protected original. Returns what was restored., Gate write_file: inside the writable trees, and never *onto* an original.…, _restore_changed(), _snapshot(), _tool_execute_command(), _write_allowed() (+22 more)

### Community 11 - "Paragraph"
Cohesion: 0.20
Nodes (4): Link, Paragraph, Renders an anchor element ``<a>``. Parameters: content: The text content or…, Block paragraph element rendered as ``<p>``. Parameters: content: The paragraph…

### Community 13 - "test_registry_resolution.py"
Cohesion: 0.06
Nodes (72): _DocumentEntry, Any, The document registry: which types exist, and how to build each one.…, One document type's ``{"builder": ..., "schema": ...}``. ``schema`` and…, Document types discovered from the filesystem, resolved on access. Deliberately…, _Registry, active_layout_name(), active_layout_path() (+64 more)

### Community 14 - "prd.md"
Cohesion: 0.05
Nodes (36): 10. Canvas, 11. Page Model, 12. Element Model, 13. Text Element, 14. Image Element, 15. Shape Element, 16. Dynamic Field Element, 17. Selection System (+28 more)

### Community 15 - "Stages"
Cohesion: 0.05
Nodes (36): Decisions settled up front, Deliberately not in scope, Frontend integration plan, How to read the two source documents, Sequencing, Stage 0 — Groundwork, Stage 10 — Export, Stage 11 — The agentic loop, made reviewable (+28 more)

### Community 16 - "FlexCol"
Cohesion: 0.26
Nodes (14): build_citizenship_back(), _ea(), field_row(), multi_row(), _officer_block(), _officer_row(), _place_block(), Any (+6 more)

### Community 17 - "Component"
Cohesion: 0.14
Nodes (12): Component, Render all children to a concatenated HTML string., Build the HTML attribute string for this element. Combines ``css_class``,…, Render this component to an HTML string., Base class for all renderable document components. Parameters: style: Optional…, ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList. (+4 more)

### Community 18 - "required"
Cohesion: 0.14
Nodes (14): required, date, district, family_members, letter_no, main_text, municipality, office_name (+6 more)

### Community 19 - "main.py"
Cohesion: 0.24
Nodes (12): build_data(), extract(), load_schema(), build_document(), digitize_document(), _blank_data(), Path, Manual entry point: turn one document into HTML (and optionally PNG). This is… (+4 more)

### Community 20 - "rag_engine.py"
Cohesion: 0.10
Nodes (37): _tool_query_context(), build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python() (+29 more)

### Community 21 - "page_geometry"
Cohesion: 0.17
Nodes (27): layout_source(), page_geometry(), Fit the ink extent onto an A4 sheet with one uniform scale. Orientation follows…, Emit a complete layout module for *document_type*. Args: placed: Blocks already…, _blocks(), _placed(), _plan(), The aspect-ratio guarantee, asserted at its source. Two factors would fit the… (+19 more)

### Community 22 - "Salvage record: `controller-old/` → `agentic_controller/`"
Cohesion: 0.33
Nodes (5): Behaviour to reproduce in Phase 2/3, Carried across, Deliberately dropped, Not indexed by RAG, Salvage record: `controller-old/` → `agentic_controller/`

### Community 25 - "validate_layout"
Cohesion: 0.20
Nodes (20): Check that a generated layout module is safe for the caller to use. Four gates,…, validate_layout(), _layout(), Path, Tests for ``architect.validate_layout`` — the gate that let the reported bug…, Blank probe data is the harsh case. A layout indexing a key the schema does not…, A property outside the known list is a cosmetic gap, not a reason to fail a…, Without a schema the builder is probed with ``{}``. (+12 more)

### Community 26 - "citizenship_old_back/layout.py"
Cohesion: 0.27
Nodes (9): build_citizenship_old_back(), Any, Build the English reproduction of the back of the old-format Nepali Citizenship…, The shared value style at a specific column width., One label–value row of the reverse sheet., One thumb-impression box, captioned along its bottom edge. The two boxes butt…, _row(), _thumb_box() (+1 more)

### Community 27 - "normalize_value"
Cohesion: 0.13
Nodes (15): normalize_value(), Rewrite every colour token in a single declaration's *value*. Parameters: prop:…, Thresholding by luminance would map a dark fill to black and its light text to…, A curated subset leaked ``rebeccapurple``. Any name the regex misses passes…, Alternation is scanned left to right. With "red" ordered before "rebeccapurple"…, Rewriting transparent to white paints over content meant to show through., Corrupting document data is worse than leaking a colour., A url(...) may hold a "#" fragment that is not a colour. (+7 more)

### Community 28 - "monochrome.py"
Cohesion: 0.25
Nodes (7): css_surface(), Monochrome enforcement for the HTML Document Engine. Project rule: a rendered…, Surfaces go white, ink goes black., The parts of *text* that are actually CSS. A full HTML page contributes its…, _target_for(), A page contributes its style attributes and style blocks, nothing else., test_css_surface_separates_style_from_prose()

### Community 29 - "43. Acceptance Criteria"
Cohesion: 0.10
Nodes (21): 43. Acceptance Criteria, AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07 (+13 more)

### Community 30 - "_build_system_prompt"
Cohesion: 0.67
Nodes (3): _build_system_prompt(), _load_rules(), Assemble the system prompt, with the verification rules embedded.

### Community 31 - ".to_css"
Cohesion: 0.25
Nodes (5): _css_name(), Map a Python keyword to its CSS property name. ``font_size`` -> ``font-size``.…, Set properties in emission order: known first, then unknown., Serialize to an inline CSS declaration string. Colours are normalized to black-…, Return a full ``style="..."`` attribute, or ``""`` if empty.

### Community 34 - "html_engine/__init__.py"
Cohesion: 0.13
Nodes (19): ABC, Abstract base class for all HTML Document Engine components. Every renderable…, Image component for the HTML Document Engine., Placeholder components for document furniture the render cannot reproduce. A…, Text components: Text, Heading, Paragraph, Link., Document — the root of a renderable page. doc = Document("My Certificate",…, Render a Document class to a full HTML string. The output is a self-contained…, render() (+11 more)

### Community 35 - "TableCell"
Cohesion: 0.27
Nodes (5): Table components: Table, TableRow, TableCell. Supports both simple table…, A single table cell (``<td>`` or ``<th>``). Parameters: content: Cell content —…, A table row (``<tr>``) containing one or more cells. Parameters: cells:…, TableCell, TableRow

### Community 37 - "office_name"
Cohesion: 0.67
Nodes (3): description, type, office_name

### Community 38 - "test_main_cli.py"
Cohesion: 0.23
Nodes (14): main(), _out(), Path, Tests for the manual entry point. ``main.py`` is the hand-driven counterpart to…, The engine warns on an unrecognized property rather than raising, so…, Proven by breaking the OCR import: if the extractor were reached, this would…, _run(), test_blank_builds_every_registered_type() (+6 more)

### Community 39 - "architect.py"
Cohesion: 0.11
Nodes (37): _dispatch_tool(), _field_name(), _log_call(), _parse_contract(), _parse_json_object(), _parse_plan(), _plan_block_lines(), plan_blocks() (+29 more)

### Community 40 - "verifier.py"
Cohesion: 0.10
Nodes (24): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., Machine-readable result returned by the vision model. This is the contract the…, Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, A single change to the extraction JSON schema. (+16 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

### Community 42 - "coerce_children"
Cohesion: 0.18
Nodes (9): coerce_child(), coerce_children(), editable_attrs(), Any, Append one or more child components. Returns self for chaining., Turn one constructor argument into a child component, or reject it. Components…, Coerce an iterable of constructor arguments, dropping ``None``s., Attributes that make one rendered value editable in the browser. The ``data-… (+1 more)

### Community 43 - "properties"
Cohesion: 0.20
Nodes (10): description, type, description, type, properties, date, main_text, province (+2 more)

### Community 44 - "37. MVP Scope"
Cohesion: 0.25
Nodes (8): 37. MVP Scope, Canvas, Editor, Elements, Export, Interaction, Persistence, Properties

### Community 46 - "test_monochrome.py"
Cohesion: 0.15
Nodes (14): normalize_declarations(), normalize_html(), Rewrite colours across a CSS fragment. Works both on an inline declaration list…, Rewrite colours in a complete HTML document. Only ``style="..."`` attributes…, Tests for the monochrome guarantee. Project rule: a rendered document is purely…, A component can carry a hand-written style attribute, bypassing Style., A component's own ``to_html()`` can hardcode a style the engine never sees as a…, test_normalize_html_leaves_body_text_alone() (+6 more)

### Community 47 - "items"
Cohesion: 0.17
Nodes (12): items, properties, required, type, description, type, name, relation (+4 more)

### Community 48 - "HTML document engine"
Cohesion: 0.05
Nodes (39): Adding a new document type, Agentic controller, Arbitrary HTML attributes (`attrs`), Architect Agent (`architect.py`), Architecture, Babu Document Digitization: Technical Documentation, Building one document by hand, Component reference (+31 more)

### Community 49 - "Image"
Cohesion: 0.40
Nodes (3): Image, Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64.

### Community 50 - "Document Digitization Rules"
Cohesion: 0.05
Nodes (38): 1.1 Language Translation, 1.2 Faithful Layout Reproduction, 1.3 Typography, 1.4 Colour & Background, 1. General Principles, 2.1 Photographs, 2.2 Government Emblems / Coat of Arms, 2.3 Official Seals (Round / Office Stamps) (+30 more)

### Community 51 - "44. Engineering Rules for the Agent"
Cohesion: 0.25
Nodes (8): 44. Engineering Rules for the Agent, Rule 1 — Document model first, Rule 2 — Single source of truth, Rule 3 — Components are renderers, Rule 4 — Commands modify state, Rule 5 — History is operation-based, Rule 6 — No premature complexity, Rule 7 — Extensibility

### Community 52 - "components/__init__.py"
Cohesion: 0.13
Nodes (18): build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th(), _to_float() (+10 more)

### Community 53 - "Any"
Cohesion: 0.28
Nodes (4): Any, Record one declaration, warning if the property looks misspelled., Iterate ``(python_name, value)`` for every set property., Return a copy with specific properties overridden. Passing ``None`` removes a…

### Community 54 - "_apply"
Cohesion: 0.22
Nodes (10): _apply(), _collect(), _is_meta_key(), _paired_paths(), _paired_sibling(), Any, Whether ``key`` is the script-preserved half of a bilingual field pair. True…, Gather every translatable leaf as ``path → (key, value)``. (+2 more)

### Community 55 - "test_autolayout.py"
Cohesion: 0.10
Nodes (20): Tests for ``document_builder/autolayout.py`` — the geometry half of layout…, 34 Text + 5 Picture. A dropped block is content silently lost., An ``<img alt="...">`` stripped of tags leaves a sentence describing the…, A tall document must not be letterboxed onto a landscape sheet., A label left of its value on the scan stays left of it on the sheet., The bbox is the line box; glyphs are roughly 62 % of it., A translated label runs longer than the Devanagari it replaces., Datalab's alt is a full sentence and overflows the box it labels. (+12 more)

### Community 56 - "AbsoluteBox"
Cohesion: 0.28
Nodes (14): _address_row(), build_pension_book(), _label_line(), _left_page(), _line_value(), _page_frame(), Any, Translated layout for the Police Kitabkhana pension book spread. (+6 more)

### Community 57 - "pan/layout.py"
Cohesion: 0.21
Nodes (13): build_pan(), _date_cells(), _date_parts(), _digits(), _pan_cells(), Any, Translated, source-faithful layout for the Rajendra Rai PAN certificate., The scan has handwritten signatures over a single horizontal rule. (+5 more)

### Community 58 - "22. Properties Panel"
Cohesion: 0.40
Nodes (5): 22. Properties Panel, Advanced, Appearance, Position, Text

### Community 59 - "letter_no"
Cohesion: 0.67
Nodes (3): description, type, letter_no

### Community 60 - "municipality"
Cohesion: 0.67
Nodes (3): description, type, municipality

### Community 61 - "citizenship/layout.py"
Cohesion: 0.42
Nodes (7): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main()

### Community 62 - "load_conversion"
Cohesion: 0.29
Nodes (9): convert(), load_conversion(), Any, Path, Datalab ``/convert``: the block tree a scan's geometry comes from.…, Convert *image_path* to a block tree and return the parsed JSON. Args:…, Read a conversion JSON saved earlier. Datalab deletes results an hour after the…, Write *conversion* to *path* and return it. (+1 more)

### Community 63 - "Babu Document Digitization — agent notes"
Cohesion: 0.29
Nodes (6): Babu Document Digitization — agent notes, Conventions that bite, Environment, graphify, Layout of the repo, Verify changes

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

### Community 68 - "grid.py"
Cohesion: 0.15
Nodes (8): Card, Grid, GridItem, Any, Layout components: FlexRow, FlexCol, AbsoluteBox, Div. These are generic…, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, CSS Grid item. Parameters: column_span: Number of columns this item spans (e.g.…, A styled container mimicking a paper card. Includes preset styles: background…

### Community 69 - "Spacer"
Cohesion: 0.17
Nodes (10): build_letter(), _ea(), Any, HorizontalRule, Spacer and divider components., Empty space of a fixed size. Vertical by default. A ``width`` makes it a…, Horizontal rule (``<hr>``) divider. Parameters: style: Override styles (color,…, Spacer (+2 more)

### Community 70 - "Document"
Cohesion: 0.12
Nodes (15): build_transfer_certificate(), _ea(), Any, Transfer Certificate Layout — document_builder/transfer_certificate/layout_1.py…, Document, Any, Path, A single page of output. Parameters: title: ``<title>`` text. page_width: Width… (+7 more)

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

### Community 78 - "Text"
Cohesion: 0.16
Nodes (11): Faint centred text behind the page content. Absolutely positioned and non-…, Watermark, Inline text element rendered as a ``<span>``. Parameters: content: The text…, Text, Three properties separate a watermark from a heading: it sits behind, it never…, ``field=`` uses setdefault, so a layout that needs a non-editable but labelled…, test_explicit_attrs_win_over_field(), test_field_makes_a_component_editable() (+3 more)

### Community 79 - "find_violations"
Cohesion: 0.18
Nodes (11): find_violations(), Report colour tokens that normalization *would* change. Accepts either a CSS…, One document exercising every route at once, audited by find_violations., An autolayout placeholder caption reads "Red circular official seal of the…, The narrowed scan must not have narrowed past a genuine violation., The guarantee that actually matters: every shipped document type., test_all_bypass_routes_are_closed(), test_find_violations_ignores_document_prose() (+3 more)

### Community 80 - "blocks_from_conversion"
Cohesion: 0.25
Nodes (8): blocks_from_conversion(), _clean(), Strip tags and collapse whitespace, leaving the readable text., Flatten one page of a ``/convert`` tree into :class:`Block` objects. Blocks…, A block with no usable bbox contributes nothing and skews the extent., Same scan, same layout — the reason this half is not a model call., test_blocks_without_geometry_are_dropped(), test_geometry_is_deterministic()

### Community 81 - "opencode.json"
Cohesion: 0.50
Nodes (3): plugin, $schema, .opencode/plugins/graphify.js

### Community 82 - "One-shot HTML generation contract"
Cohesion: 0.33
Nodes (5): Allowed editor types, Exemplar safety, One-shot HTML generation contract, Required output, Visual editor markup

### Community 83 - "Block"
Cohesion: 0.25
Nodes (6): Block, ink_extent(), The bounding box of every block, in source space. Deliberately not the page…, One block from the conversion tree, in the source's coordinate space.…, The conversion page is 1372x980 around ink that is 1201x799. Normalizing…, test_extent_is_the_ink_not_the_page()

### Community 84 - "One-shot example-guided digitization"
Cohesion: 0.33
Nodes (5): Corpus rule, Directory contract, Model contract, One-shot example-guided digitization, Retrieval v0

### Community 85 - "subject"
Cohesion: 0.67
Nodes (3): subject, description, type

### Community 86 - "value_fields"
Cohesion: 0.50
Nodes (4): Every field name the plan binds to a value, in plan order., value_fields(), ``build_data`` keeps only what the schema lists as required, so a field the…, test_every_field_survives_extraction()

### Community 87 - "language_spec"
Cohesion: 0.29
Nodes (6): language_spec(), Target languages the translator can render a document into. One…, Look up a target language, naming the supported codes on failure., The rules do not vary between languages; the worked examples in the target…, test_each_language_prompt_carries_its_own_examples(), test_the_prose_note_names_the_target_language()

### Community 95 - "render_png"
Cohesion: 0.70
Nodes (4): _crop_to_page(), _page_metrics(), Path, render_png()

### Community 100 - "Q: Why does language_spec() connect translator.py to run.py, test_translator.py, architect.py?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Why does language_spec() connect translator.py to run.py, test_translator.py, architect.py?, Source Nodes

### Community 101 - "district"
Cohesion: 0.67
Nodes (3): description, type, district

### Community 102 - "StyleWarning"
Cohesion: 0.67
Nodes (3): An unrecognized CSS property name reached ``Style``. Probably a typo., StyleWarning, UserWarning

### Community 103 - "ref_no"
Cohesion: 0.67
Nodes (3): ref_no, description, type

## Knowledge Gaps
- **273 isolated node(s):** `$schema`, `.opencode/plugins/graphify.js`, `$schema`, `title`, `type` (+268 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style` to `test_components.py`, `LabelValue`, `FlexRow`, `Paragraph`, `FlexCol`, `Component`, `citizenship_old_back/layout.py`, `.to_css`, `html_engine/__init__.py`, `TableCell`, `test_main_cli.py`, `coerce_children`, `test_monochrome.py`, `Image`, `components/__init__.py`, `Any`, `AbsoluteBox`, `pan/layout.py`, `citizenship/layout.py`, `grid.py`, `Spacer`, `Document`, `Text`, `find_violations`?**
  _High betweenness centrality (0.216) - this node is a cross-community bridge._
- **Why does `find_violations()` connect `find_violations` to `monochrome.py`, `page_geometry`, `test_monochrome.py`, `test_autolayout.py`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `language_spec()` connect `language_spec` to `build_prompt`, `test_translator.py`, `architect.py`, `verifier.py`, `translator.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Style` (e.g. with `Component` and `FieldGroup`) actually correct?**
  _`Style` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Text` (e.g. with `Component` and `PlaceholderBox`) actually correct?**
  _`Text` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Component` (e.g. with `Text` and `Style`) actually correct?**
  _`Component` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Document` (e.g. with `Component` and `Style`) actually correct?**
  _`Document` has 2 INFERRED edges - model-reasoned connections that need verification._