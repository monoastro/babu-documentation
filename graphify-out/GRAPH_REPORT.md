# Graph Report - babu-documentation  (2026-09-06)

## Corpus Check
- 109 files · ~793,963 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1334 nodes · 2708 edges · 98 communities (81 shown, 17 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 92 edges (avg confidence: 0.57)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2f8d1afe`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run.py
- Text
- Editable Nepali citizenship certificate (romanized test render)
- build_prompt
- TableCell
- Document
- test_translator.py
- test_styles.py
- translator.py
- autolayout.py
- test_command_sandbox.py
- components/__init__.py
- "First make it work, then make it better"
- test_registry_resolution.py
- prd.md
- Stages
- LabelValue
- Component
- required
- Style
- rag_engine.py
- page_geometry
- Salvage record: `controller-old/` → `agentic_controller/`
- langgraph dependency
- python-dotenv dependency
- validate_layout
- Div
- normalize_value
- monochrome.py
- 43. Acceptance Criteria
- build_from_geometry
- .to_css
- DocLayout-YOLO
- Segment Anything Model for document analysis
- html_engine/__init__.py
- normalize_declarations
- Surya (datalab-to)
- office_name
- build_pension_front
- architect.py
- verifier.py
- 1. Document Verification Rules
- base.py
- properties
- 37. MVP Scope
- run_all.py
- test_monochrome.py
- items
- HTML document engine
- Image
- Document Digitization Rules
- 44. Engineering Rules for the Agent
- laalpurja/layout.py
- Any
- .__add__
- test_autolayout.py
- _right_page
- build_pan
- 22. Properties Panel
- letter_no
- municipality
- AbsoluteBox
- load_conversion
- Babu Document Digitization — agent notes
- ward_chairperson_name
- ward_chairperson_title
- ward_no
- 5. Technology Requirements
- grid.py
- spacer.py
- .save
- 3. Target User
- 8. Toolbar
- relationship_certificate.json
- 35. Non-Functional Requirements
- family_members
- PRD — Visual HTML Document Editing Engine
- 4. Core Design Principle
- find_violations
- blocks_from_conversion
- opencode.json
- Block
- subject
- value_fields
- agentic_controller/__init__.py
- Ideal patching prompt composition
- Perfect-match VerificationReport example
- langchain-openai dependency
- pydantic dependency
- graphify.js
- Q: Why does language_spec() connect translator.py to run.py, test_translator.py, architect.py?
- district
- ref_no

## God Nodes (most connected - your core abstractions)
1. `Style` - 160 edges
2. `Component` - 58 edges
3. `Text` - 55 edges
4. `LabelValue` - 41 edges
5. `Document` - 41 edges
6. `FlexCol` - 34 edges
7. `PlaceholderBox` - 33 edges
8. `_run()` - 32 edges
9. `FlexRow` - 30 edges
10. `Spacer` - 30 edges

## Surprising Connections (you probably didn't know these)
- `_pan_cells()` --calls--> `Style`  [INFERRED]
  document_builder/pan/layout.py → html_engine/styles.py
- `_date_cells()` --calls--> `Style`  [INFERRED]
  document_builder/pan/layout.py → html_engine/styles.py
- `_signature_line()` --calls--> `Style`  [INFERRED]
  document_builder/pan/layout.py → html_engine/styles.py
- `build_pan()` --calls--> `PlaceholderBox`  [INFERRED]
  document_builder/pan/layout.py → html_engine/components/placeholder.py
- `build_pan()` --calls--> `Style`  [INFERRED]
  document_builder/pan/layout.py → html_engine/styles.py

## Import Cycles
- None detected.

## Communities (98 total, 17 thin omitted)

### Community 0 - "run.py"
Cohesion: 0.13
Nodes (23): current_layout_path(), The layout that will actually be built — whatever ``ACTIVE`` names. This used…, _crop_to_page(), _page_metrics(), Path, render_png(), _collect_decision(), _collect_user_concerns() (+15 more)

### Community 1 - "Text"
Cohesion: 0.08
Nodes (35): corner_box(), PlaceholderBox, Faint centred text behind the page content. Absolutely positioned and non-…, The signature cluster that closes an official letter. Stacks, top to bottom:…, A labelled outline standing in for artwork that cannot be rendered. Renders a…, A placeholder pinned to one corner of the page — crest, QR block, stamp.…, SignatureBlock, Watermark (+27 more)

### Community 3 - "build_prompt"
Cohesion: 0.18
Nodes (13): build_prompt(), The full verification system prompt for one target language., Tests for the verification prompt's target language.…, Latin examples in a Japanese prompt would teach the wrong script., Only rule 1 varies; placeholders, formatting, and colour do not., ``verification-rules.md`` mirrors this prompt rule by rule., ``SYSTEM_PROMPT`` is what ``verification-rules.md`` documents., test_an_unsupported_language_is_refused() (+5 more)

### Community 4 - "TableCell"
Cohesion: 0.18
Nodes (14): build_income_certificate(), _ea(), _lv(), Any, Income Certificate Layout — document_builder/income_certificate/layout_1.py…, build_tax_clearance(), _ea(), Any (+6 more)

### Community 5 - "Document"
Cohesion: 0.11
Nodes (26): build_letter(), _ea(), Any, build_relationship_certificate(), _ea(), Any, Relationship Certificate Layout —…, build_see_certificate() (+18 more)

### Community 6 - "test_translator.py"
Cohesion: 0.06
Nodes (52): Tests for the translation stage. ``information_extraction/translator.py`` sits…, A sentence and a field label want different instructions, so they are batched…, A district repeated down a table is one string, not twenty., A half-converted date prints a year that looks Gregorian and is not., The SEE certificate prints ``certificate_title_np`` on one line and…, Without the English sibling, that value is the only one on the page., A laalpurja's ``plots`` is a list of dicts; every row must be reached., ``<field>_meta`` and ``<field>_citations`` are provenance the extractor… (+44 more)

### Community 7 - "test_styles.py"
Cohesion: 0.08
Nodes (22): Tests for the open property bag that replaced the closed ``Style`` dataclass.…, Monochrome is enforced on the way out, including for unlisted props., The reported crash. Any valid CSS property must survive to the output., Both are deliberate, so neither should look like a typo., The trade for accepting anything: a misspelling is no longer a TypeError. It…, What ``main.py --strict`` relies on., A name CSS could never accept is a bug worth stopping for., CSS resolves duplicates last-one-wins, so ``margin`` emitted after ``margin-… (+14 more)

### Community 8 - "translator.py"
Cohesion: 0.05
Nodes (66): build_data(), extract(), load_schema(), language_spec(), LanguageSpec, Target languages the translator can render a document into. One…, Everything the translator needs to know about one target language. Parameters:…, Look up a target language, naming the supported codes on failure. (+58 more)

### Community 9 - "autolayout.py"
Cohesion: 0.14
Nodes (21): _emit_block(), _first_mention(), fit_text(), _font_size(), PageGeometry, place(), Placed, _px() (+13 more)

### Community 10 - "test_command_sandbox.py"
Cohesion: 0.11
Nodes (30): _protected_originals(), Content of each protected file, or None if it does not exist., Undo any modification to a protected original. Returns what was restored., Gate write_file: inside the writable trees, and never *onto* an original.…, _restore_changed(), _snapshot(), _tool_execute_command(), _write_allowed() (+22 more)

### Community 11 - "components/__init__.py"
Cohesion: 0.12
Nodes (10): html_engine.components — All renderable component types., Placeholder components for document furniture the render cannot reproduce. A…, Table components: Table, TableRow, TableCell. Supports both simple table…, Link, Paragraph, Text components: Text, Heading, Paragraph, Link., Escape hatch: renders arbitrary HTML verbatim. Use sparingly — this bypasses…, Renders an anchor element ``<a>``. Parameters: content: The text content or… (+2 more)

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
Cohesion: 0.21
Nodes (18): build_citizenship_back(), _ea(), field_row(), multi_row(), _officer_block(), _officer_row(), _place_block(), Any (+10 more)

### Community 17 - "Component"
Cohesion: 0.16
Nodes (11): Component, Render all children to a concatenated HTML string., Render this component to an HTML string., Base class for all renderable document components. Parameters: style: Optional…, ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList., Renders a list item ``<li>``. Parameters: content: String content or nested… (+3 more)

### Community 18 - "required"
Cohesion: 0.14
Nodes (14): required, date, district, family_members, letter_no, main_text, municipality, office_name (+6 more)

### Community 19 - "Style"
Cohesion: 0.16
Nodes (3): Any, An open set of CSS declarations. Any keyword is accepted and emitted as a CSS…, Style

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

### Community 26 - "Div"
Cohesion: 0.15
Nodes (15): build_citizenship_old_back(), Any, Build the English reproduction of the back of the old-format Nepali Citizenship…, The shared value style at a specific column width., One label–value row of the reverse sheet., One thumb-impression box, captioned along its bottom edge. The two boxes butt…, _row(), _thumb_box() (+7 more)

### Community 27 - "normalize_value"
Cohesion: 0.13
Nodes (15): normalize_value(), Rewrite every colour token in a single declaration's *value*. Parameters: prop:…, Thresholding by luminance would map a dark fill to black and its light text to…, A curated subset leaked ``rebeccapurple``. Any name the regex misses passes…, Alternation is scanned left to right. With "red" ordered before "rebeccapurple"…, Rewriting transparent to white paints over content meant to show through., Corrupting document data is worse than leaking a colour., A url(...) may hold a "#" fragment that is not a colour. (+7 more)

### Community 28 - "monochrome.py"
Cohesion: 0.25
Nodes (7): css_surface(), Monochrome enforcement for the HTML Document Engine. Project rule: a rendered…, Surfaces go white, ink goes black., The parts of *text* that are actually CSS. A full HTML page contributes its…, _target_for(), A page contributes its style attributes and style blocks, nothing else., test_css_surface_separates_style_from_prose()

### Community 29 - "43. Acceptance Criteria"
Cohesion: 0.10
Nodes (21): 43. Acceptance Criteria, AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07 (+13 more)

### Community 30 - "build_from_geometry"
Cohesion: 0.13
Nodes (22): analyze_and_repair(), build_from_geometry(), _build_system_prompt(), generate_resources(), _image(), _load_rules(), main(), Path (+14 more)

### Community 31 - ".to_css"
Cohesion: 0.25
Nodes (5): _css_name(), Map a Python keyword to its CSS property name. ``font_size`` -> ``font-size``.…, Set properties in emission order: known first, then unknown., Serialize to an inline CSS declaration string. Colours are normalized to black-…, Return a full ``style="..."`` attribute, or ``""`` if empty.

### Community 34 - "html_engine/__init__.py"
Cohesion: 0.14
Nodes (17): Document — the root of a renderable page. doc = Document("My Certificate",…, Render a Document class to a full HTML string. The output is a self-contained…, render(), em(), pct(), pt(), px(), Style descriptor for the HTML Document Engine. ``Style`` is an **open**… (+9 more)

### Community 35 - "normalize_declarations"
Cohesion: 0.40
Nodes (4): Build the HTML attribute string for this element. Combines ``css_class``,…, normalize_declarations(), Rewrite colours across a CSS fragment. Works both on an inline declaration list…, test_selector_is_not_mistaken_for_a_property()

### Community 37 - "office_name"
Cohesion: 0.67
Nodes (3): description, type, office_name

### Community 38 - "build_pension_front"
Cohesion: 0.67
Nodes (3): build_pension_front(), _ea(), Document

### Community 39 - "architect.py"
Cohesion: 0.12
Nodes (33): _dispatch_tool(), _field_name(), _log_call(), _parse_contract(), _parse_json_object(), _parse_plan(), _plan_block_lines(), plan_blocks() (+25 more)

### Community 40 - "verifier.py"
Cohesion: 0.10
Nodes (24): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., Machine-readable result returned by the vision model. This is the contract the…, Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, A single change to the extraction JSON schema. (+16 more)

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

### Community 46 - "test_monochrome.py"
Cohesion: 0.18
Nodes (10): normalize_html(), Rewrite colours in a complete HTML document. Only ``style="..."`` attributes…, Tests for the monochrome guarantee. Project rule: a rendered document is purely…, A component can carry a hand-written style attribute, bypassing Style., A component's own ``to_html()`` can hardcode a style the engine never sees as a…, test_normalize_html_leaves_body_text_alone(), test_route_1_style_to_css(), test_route_2_raw_style_string_in_attrs() (+2 more)

### Community 47 - "items"
Cohesion: 0.17
Nodes (12): items, properties, required, type, description, type, name, relation (+4 more)

### Community 48 - "HTML document engine"
Cohesion: 0.05
Nodes (39): Adding a new document type, Agentic controller, Arbitrary HTML attributes (`attrs`), Architect Agent (`architect.py`), Architecture, Babu Document Digitization: Technical Documentation, Building one document by hand, Component reference (+31 more)

### Community 49 - "Image"
Cohesion: 0.29
Nodes (4): Image, Image component for the HTML Document Engine., Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64.

### Community 50 - "Document Digitization Rules"
Cohesion: 0.05
Nodes (38): 1.1 Language Translation, 1.2 Faithful Layout Reproduction, 1.3 Typography, 1.4 Colour & Background, 1. General Principles, 2.1 Photographs, 2.2 Government Emblems / Coat of Arms, 2.3 Official Seals (Round / Office Stamps) (+30 more)

### Community 51 - "44. Engineering Rules for the Agent"
Cohesion: 0.25
Nodes (8): 44. Engineering Rules for the Agent, Rule 1 — Document model first, Rule 2 — Single source of truth, Rule 3 — Components are renderers, Rule 4 — Commands modify state, Rule 5 — History is operation-based, Rule 6 — No premature complexity, Rule 7 — Extensibility

### Community 52 - "laalpurja/layout.py"
Cohesion: 0.30
Nodes (10): build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th(), _to_float() (+2 more)

### Community 53 - "Any"
Cohesion: 0.28
Nodes (4): Any, Record one declaration, warning if the property looks misspelled., Iterate ``(python_name, value)`` for every set property., Return a copy with specific properties overridden. Passing ``None`` removes a…

### Community 55 - "test_autolayout.py"
Cohesion: 0.10
Nodes (20): Tests for ``document_builder/autolayout.py`` — the geometry half of layout…, 34 Text + 5 Picture. A dropped block is content silently lost., An ``<img alt="...">`` stripped of tags leaves a sentence describing the…, A tall document must not be letterboxed onto a landscape sheet., A label left of its value on the scan stays left of it on the sheet., The bbox is the line box; glyphs are roughly 62 % of it., A translated label runs longer than the Devanagari it replaces., Datalab's alt is a full sentence and overflows the box it labels. (+12 more)

### Community 56 - "_right_page"
Cohesion: 0.29
Nodes (18): AbsoluteBox, Div, _address_row(), build_pension_book(), _label_line(), _left_page(), _line_value(), _page_frame() (+10 more)

### Community 57 - "build_pan"
Cohesion: 0.17
Nodes (17): build_pan(), _date_cells(), _date_parts(), _digits(), _pan_cells(), Any, Document, FlexCol (+9 more)

### Community 58 - "22. Properties Panel"
Cohesion: 0.40
Nodes (5): 22. Properties Panel, Advanced, Appearance, Position, Text

### Community 59 - "letter_no"
Cohesion: 0.67
Nodes (3): description, type, letter_no

### Community 60 - "municipality"
Cohesion: 0.67
Nodes (3): description, type, municipality

### Community 61 - "AbsoluteBox"
Cohesion: 0.12
Nodes (20): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, build_citizenship_old(), _ea() (+12 more)

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
Cohesion: 0.18
Nodes (7): Card, Grid, GridItem, Layout components: FlexRow, FlexCol, AbsoluteBox, Div. These are generic…, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, CSS Grid item. Parameters: column_span: Number of columns this item spans (e.g.…, A styled container mimicking a paper card. Includes preset styles: background…

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

### Community 79 - "find_violations"
Cohesion: 0.18
Nodes (11): find_violations(), Report colour tokens that normalization *would* change. Accepts either a CSS…, One document exercising every route at once, audited by find_violations., An autolayout placeholder caption reads "Red circular official seal of the…, The narrowed scan must not have narrowed past a genuine violation., The guarantee that actually matters: every shipped document type., test_all_bypass_routes_are_closed(), test_find_violations_ignores_document_prose() (+3 more)

### Community 80 - "blocks_from_conversion"
Cohesion: 0.25
Nodes (8): blocks_from_conversion(), _clean(), Strip tags and collapse whitespace, leaving the readable text., Flatten one page of a ``/convert`` tree into :class:`Block` objects. Blocks…, A block with no usable bbox contributes nothing and skews the extent., Same scan, same layout — the reason this half is not a model call., test_blocks_without_geometry_are_dropped(), test_geometry_is_deterministic()

### Community 81 - "opencode.json"
Cohesion: 0.50
Nodes (3): plugin, $schema, .opencode/plugins/graphify.js

### Community 83 - "Block"
Cohesion: 0.25
Nodes (6): Block, ink_extent(), The bounding box of every block, in source space. Deliberately not the page…, One block from the conversion tree, in the source's coordinate space.…, The conversion page is 1372x980 around ink that is 1201x799. Normalizing…, test_extent_is_the_ink_not_the_page()

### Community 85 - "subject"
Cohesion: 0.67
Nodes (3): subject, description, type

### Community 86 - "value_fields"
Cohesion: 0.50
Nodes (4): Every field name the plan binds to a value, in plan order., value_fields(), ``build_data`` keeps only what the schema lists as required, so a field the…, test_every_field_survives_extraction()

### Community 100 - "Q: Why does language_spec() connect translator.py to run.py, test_translator.py, architect.py?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Why does language_spec() connect translator.py to run.py, test_translator.py, architect.py?, Source Nodes

### Community 101 - "district"
Cohesion: 0.67
Nodes (3): description, type, district

### Community 103 - "ref_no"
Cohesion: 0.67
Nodes (3): ref_no, description, type

## Knowledge Gaps
- **263 isolated node(s):** `$schema`, `.opencode/plugins/graphify.js`, `Environment`, `Verify changes`, `Layout of the repo` (+258 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style` to `Text`, `TableCell`, `Document`, `test_styles.py`, `translator.py`, `components/__init__.py`, `LabelValue`, `Component`, `Div`, `.to_css`, `html_engine/__init__.py`, `normalize_declarations`, `build_pension_front`, `base.py`, `test_monochrome.py`, `Image`, `laalpurja/layout.py`, `Any`, `.__add__`, `_right_page`, `build_pan`, `AbsoluteBox`, `grid.py`, `spacer.py`, `find_violations`?**
  _High betweenness centrality (0.219) - this node is a cross-community bridge._
- **Why does `find_violations()` connect `find_violations` to `monochrome.py`, `page_geometry`, `test_monochrome.py`, `test_autolayout.py`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `language_spec()` connect `translator.py` to `verifier.py`, `build_prompt`, `test_translator.py`, `architect.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 44 inferred relationships involving `Style` (e.g. with `build_pan()` and `_date_cells()`) actually correct?**
  _`Style` has 44 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Component` (e.g. with `Style` and `FieldGroup`) actually correct?**
  _`Component` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Text` (e.g. with `PlaceholderBox` and `SignatureBlock`) actually correct?**
  _`Text` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `LabelValue` (e.g. with `Component` and `Style`) actually correct?**
  _`LabelValue` has 2 INFERRED edges - model-reasoned connections that need verification._