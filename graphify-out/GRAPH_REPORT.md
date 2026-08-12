# Graph Report - babu-documentation  (2026-08-11)

## Corpus Check
- 112 files · ~1,397,929 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1256 nodes · 2476 edges · 96 communities (69 shown, 27 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 96 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e31130d2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run.py
- test_components.py
- Editable Nepali citizenship certificate (romanized test render)
- grid.py
- TableCell
- PlaceholderBox
- test_translator.py
- Style
- translator.py
- autolayout.py
- test_command_sandbox.py
- FlexRow
- "First make it work, then make it better"
- test_registry_resolution.py
- prd.md
- Stages
- Paragraph
- Component
- required
- build_citizenship_back
- rag_engine.py
- test_autolayout.py
- Salvage record: `controller-old/` → `agentic_controller/`
- langgraph dependency
- python-dotenv dependency
- validate_layout
- build_citizenship_old_back
- _Recorder
- build_citizenship_old
- 43. Acceptance Criteria
- spacer.py
- field.py
- DocLayout-YOLO
- Segment Anything Model for document analysis
- html_engine/__init__.py
- language_spec
- Surya (datalab-to)
- office_name
- CLAUDE.md
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
- laalpurja/layout.py
- 44. Engineering Rules for the Agent
- test_prose_keys_go_in_a_separate_call
- Any
- test_duplicate_values_are_sent_once
- 22. Properties Panel
- letter_no
- municipality
- LabelValue
- load_conversion
- subject
- ward_chairperson_name
- ward_chairperson_title
- ward_no
- 5. Technology Requirements
- test_a_bilingual_title_keeps_its_nepali_half
- Document
- 3. Target User
- 8. Toolbar
- relationship_certificate.json
- 35. Non-Functional Requirements
- family_members
- PRD — Visual HTML Document Editing Engine
- 4. Core Design Principle
- test_a_lone_np_field_is_still_translated
- test_nested_lists_of_dicts_are_walked
- district
- test_extractor_metadata_is_never_translated
- test_the_cache_spares_the_second_call
- ink_extent
- test_english_text_is_sent_when_the_target_is_not_latin
- test_identifiers_are_never_sent_to_any_language
- plan_to_schema
- test_the_cache_is_keyed_on_the_language
- agentic_controller/__init__.py
- Ideal patching prompt composition
- Perfect-match VerificationReport example
- langchain-openai dependency
- pydantic dependency
- ref_no
- test_sentinel_values_are_never_sent

## God Nodes (most connected - your core abstractions)
1. `Style` - 125 edges
2. `Component` - 58 edges
3. `Text` - 40 edges
4. `_run()` - 32 edges
5. `FlexRow` - 29 edges
6. `PlaceholderBox` - 29 edges
7. `Spacer` - 29 edges
8. `Document` - 29 edges
9. `LabelValue` - 28 edges
10. `_tree()` - 26 edges

## Surprising Connections (you probably didn't know these)
- `_thumb_box()` --calls--> `PlaceholderBox`  [INFERRED]
  document_builder/citizenship_back/layout.py → html_engine/components/placeholder.py
- `build_citizenship_back()` --calls--> `FieldGroup`  [INFERRED]
  document_builder/citizenship_back/layout.py → html_engine/components/field.py
- `build_citizenship_back()` --calls--> `AbsoluteBox`  [INFERRED]
  document_builder/citizenship_back/layout.py → html_engine/components/grid.py
- `build_citizenship_back()` --calls--> `FlexRow`  [INFERRED]
  document_builder/citizenship_back/layout.py → html_engine/components/grid.py
- `build_citizenship_old()` --calls--> `FieldGroup`  [INFERRED]
  document_builder/citizenship_old/layout.py → html_engine/components/field.py

## Import Cycles
- None detected.

## Communities (96 total, 27 thin omitted)

### Community 0 - "run.py"
Cohesion: 0.13
Nodes (23): current_layout_path(), The layout that will actually be built — whatever ``ACTIVE`` names. This used…, _crop_to_page(), _page_metrics(), Path, render_png(), _collect_decision(), _collect_user_concerns() (+15 more)

### Community 1 - "test_components.py"
Cohesion: 0.07
Nodes (36): Div, Generic block container rendered as a ``<div>``. The simplest building block —…, corner_box(), Faint centred text behind the page content. Absolutely positioned and non-…, A placeholder pinned to one corner of the page — crest, QR block, stamp.…, Watermark, Inline text element rendered as a ``<span>``. Parameters: content: The text…, Text (+28 more)

### Community 3 - "grid.py"
Cohesion: 0.15
Nodes (8): Card, Grid, GridItem, Any, Layout components: FlexRow, FlexCol, AbsoluteBox, Div. These are generic…, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, CSS Grid item. Parameters: column_span: Number of columns this item spans (e.g.…, A styled container mimicking a paper card. Includes preset styles: background…

### Community 4 - "TableCell"
Cohesion: 0.16
Nodes (13): build_income_certificate(), _ea(), _lv(), Any, Income Certificate Layout — document_builder/income_certificate/layout_1.py…, build_tax_clearance(), _ea(), Any (+5 more)

### Community 5 - "PlaceholderBox"
Cohesion: 0.16
Nodes (14): build_pan(), Any, Document, Digitally faithful layout for Nepal PAN Certificate (layout_1.py) Resolves…, build_see_certificate(), SEE Certificate Layout — document_builder/see_certificate/layout_1.py…, PlaceholderBox, The signature cluster that closes an official letter. Stacks, top to bottom:… (+6 more)

### Community 6 - "test_translator.py"
Cohesion: 0.14
Nodes (20): Tests for the translation stage. ``information_extraction/translator.py`` sits…, A half-converted date prints a year that looks Gregorian and is not., Shape check against a saved extraction, if one is present: the translated data…, Translate ``data`` with the model call stubbed and the cache disabled., _run(), test_a_bs_date_printed_beside_its_ad_twin_is_left_alone(), test_a_bs_date_with_no_twin_still_converts(), test_a_real_extraction_round_trips() (+12 more)

### Community 7 - "Style"
Cohesion: 0.08
Nodes (26): An open set of CSS declarations. Any keyword is accepted and emitted as a CSS…, Return a new Style with *other*'s declarations overriding this one's. ``raw``…, Shorthand for ``merge``: ``combined = style_a + style_b``., Style, Tests for the open property bag that replaced the closed ``Style`` dataclass.…, Monochrome is enforced on the way out, including for unlisted props., The reported crash. Any valid CSS property must survive to the output., Both are deliberate, so neither should look like a typo. (+18 more)

### Community 8 - "translator.py"
Cohesion: 0.06
Nodes (57): build_data(), extract(), load_schema(), build_document(), digitize_document(), _apply(), bs_to_ad(), build_prompt() (+49 more)

### Community 9 - "autolayout.py"
Cohesion: 0.08
Nodes (35): Block, blocks_from_conversion(), _clean(), _emit_block(), _first_mention(), fit_text(), _font_size(), PageGeometry (+27 more)

### Community 10 - "test_command_sandbox.py"
Cohesion: 0.11
Nodes (30): _protected_originals(), Content of each protected file, or None if it does not exist., Undo any modification to a protected original. Returns what was restored., Gate write_file: inside the writable trees, and never *onto* an original.…, _restore_changed(), _snapshot(), _tool_execute_command(), _write_allowed() (+22 more)

### Community 11 - "FlexRow"
Cohesion: 0.16
Nodes (14): build_relationship_certificate(), _ea(), Any, Relationship Certificate Layout —…, build_transfer_certificate(), _ea(), Any, Transfer Certificate Layout — document_builder/transfer_certificate/layout_1.py… (+6 more)

### Community 13 - "test_registry_resolution.py"
Cohesion: 0.06
Nodes (72): _DocumentEntry, Any, The document registry: which types exist, and how to build each one.…, One document type's ``{"builder": ..., "schema": ...}``. ``schema`` and…, Document types discovered from the filesystem, resolved on access. Deliberately…, _Registry, active_layout_name(), active_layout_path() (+64 more)

### Community 14 - "prd.md"
Cohesion: 0.05
Nodes (36): 10. Canvas, 11. Page Model, 12. Element Model, 13. Text Element, 14. Image Element, 15. Shape Element, 16. Dynamic Field Element, 17. Selection System (+28 more)

### Community 15 - "Stages"
Cohesion: 0.05
Nodes (36): Decisions settled up front, Deliberately not in scope, Frontend integration plan, How to read the two source documents, Sequencing, Stage 0 — Groundwork, Stage 10 — Export, Stage 11 — The agentic loop, made reviewable (+28 more)

### Community 16 - "Paragraph"
Cohesion: 0.18
Nodes (4): Link, Paragraph, Renders an anchor element ``<a>``. Parameters: content: The text content or…, Block paragraph element rendered as ``<p>``. Parameters: content: The paragraph…

### Community 17 - "Component"
Cohesion: 0.14
Nodes (12): Component, Render all children to a concatenated HTML string., Build the HTML attribute string for this element. Combines ``css_class``,…, Render this component to an HTML string., Base class for all renderable document components. Parameters: style: Optional…, ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList. (+4 more)

### Community 18 - "required"
Cohesion: 0.14
Nodes (14): required, date, district, family_members, letter_no, main_text, municipality, office_name (+6 more)

### Community 19 - "build_citizenship_back"
Cohesion: 0.28
Nodes (16): build_citizenship_back(), _ea(), field_row(), multi_row(), _officer_block(), _officer_row(), _place_block(), Any (+8 more)

### Community 20 - "rag_engine.py"
Cohesion: 0.10
Nodes (36): build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python(), _embed() (+28 more)

### Community 21 - "test_autolayout.py"
Cohesion: 0.10
Nodes (45): layout_source(), page_geometry(), Fit the ink extent onto an A4 sheet with one uniform scale. Orientation follows…, Emit a complete layout module for *document_type*. Args: placed: Blocks already…, _blocks(), _placed(), _plan(), Tests for ``document_builder/autolayout.py`` — the geometry half of layout… (+37 more)

### Community 22 - "Salvage record: `controller-old/` → `agentic_controller/`"
Cohesion: 0.33
Nodes (5): Behaviour to reproduce in Phase 2/3, Carried across, Deliberately dropped, Not indexed by RAG, Salvage record: `controller-old/` → `agentic_controller/`

### Community 25 - "validate_layout"
Cohesion: 0.20
Nodes (20): Check that a generated layout module is safe for the caller to use. Four gates,…, validate_layout(), _layout(), Path, Tests for ``architect.validate_layout`` — the gate that let the reported bug…, Blank probe data is the harsh case. A layout indexing a key the schema does not…, A property outside the known list is a cosmetic gap, not a reason to fail a…, Without a schema the builder is probed with ``{}``. (+12 more)

### Community 26 - "build_citizenship_old_back"
Cohesion: 0.22
Nodes (13): Div, build_citizenship_old_back(), Any, Document, LabelValue, Style, Build the English reproduction of the back of the old-format Nepali Citizenship…, The shared value style at a specific column width. (+5 more)

### Community 27 - "_Recorder"
Cohesion: 0.15
Nodes (10): A document rendered in Devanagari beats no document at all, so a failed…, The date does not depend on the model, so it must convert anyway., Keys the model drops fall back to their source value, not to empty., Stands in for ``_translate_batch`` and remembers what it was asked., Every distinct value handed to the model, across all calls., _Recorder, test_a_failed_call_returns_the_original_data(), test_a_partial_reply_keeps_the_missing_originals() (+2 more)

### Community 28 - "build_citizenship_old"
Cohesion: 0.33
Nodes (10): build_citizenship_old(), _ea(), field_row(), multi_row(), Any, Document, LabelValue, MultiFieldRow (+2 more)

### Community 29 - "43. Acceptance Criteria"
Cohesion: 0.10
Nodes (21): 43. Acceptance Criteria, AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07 (+13 more)

### Community 30 - "spacer.py"
Cohesion: 0.20
Nodes (5): HorizontalRule, PageBreak, Spacer and divider components., Horizontal rule (``<hr>``) divider. Parameters: style: Override styles (color,…, Renders a page break for print media.

### Community 31 - "field.py"
Cohesion: 0.29
Nodes (4): editable_attrs(), Attributes that make one rendered value editable in the browser. The ``data-…, Any, Field components: LabelValue pairs and FieldGroups. These are the workhorses…

### Community 34 - "html_engine/__init__.py"
Cohesion: 0.11
Nodes (22): ABC, Abstract base class for all HTML Document Engine components. Every renderable…, Placeholder components for document furniture the render cannot reproduce. A…, Table components: Table, TableRow, TableCell. Supports both simple table…, Text components: Text, Heading, Paragraph, Link., Document — the root of a renderable page. doc = Document("My Certificate",…, Render a Document class to a full HTML string. The output is a self-contained…, render() (+14 more)

### Community 35 - "language_spec"
Cohesion: 0.25
Nodes (8): language_spec(), LanguageSpec, Target languages the translator can render a document into. One…, Everything the translator needs to know about one target language. Parameters:…, Look up a target language, naming the supported codes on failure., The rules do not vary between languages; the worked examples in the target…, test_each_language_prompt_carries_its_own_examples(), test_the_prose_note_names_the_target_language()

### Community 37 - "office_name"
Cohesion: 0.67
Nodes (3): description, type, office_name

### Community 39 - "architect.py"
Cohesion: 0.08
Nodes (55): analyze_and_repair(), build_from_geometry(), _build_system_prompt(), _dispatch_tool(), _field_name(), generate_resources(), _image(), _load_rules() (+47 more)

### Community 40 - "verifier.py"
Cohesion: 0.07
Nodes (37): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., Machine-readable result returned by the vision model. This is the contract the…, Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, A single change to the extraction JSON schema. (+29 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

### Community 42 - "coerce_children"
Cohesion: 0.22
Nodes (8): coerce_child(), coerce_children(), Any, Append one or more child components. Returns self for chaining., Turn one constructor argument into a child component, or reject it. Components…, Coerce an iterable of constructor arguments, dropping ``None``s., Any, Append top-level components. Returns self for chaining. Accepts components,…

### Community 43 - "properties"
Cohesion: 0.20
Nodes (10): description, type, description, type, properties, date, main_text, province (+2 more)

### Community 44 - "37. MVP Scope"
Cohesion: 0.25
Nodes (8): 37. MVP Scope, Canvas, Editor, Elements, Export, Interaction, Persistence, Properties

### Community 46 - "test_monochrome.py"
Cohesion: 0.05
Nodes (46): css_surface(), find_violations(), normalize_declarations(), normalize_html(), normalize_value(), Monochrome enforcement for the HTML Document Engine. Project rule: a rendered…, Surfaces go white, ink goes black., Rewrite every colour token in a single declaration's *value*. Parameters: prop:… (+38 more)

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
Cohesion: 0.22
Nodes (14): build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th(), _to_float() (+6 more)

### Community 51 - "44. Engineering Rules for the Agent"
Cohesion: 0.25
Nodes (8): 44. Engineering Rules for the Agent, Rule 1 — Document model first, Rule 2 — Single source of truth, Rule 3 — Components are renderers, Rule 4 — Commands modify state, Rule 5 — History is operation-based, Rule 6 — No premature complexity, Rule 7 — Extensibility

### Community 53 - "Any"
Cohesion: 0.18
Nodes (7): _css_name(), Any, Map a Python keyword to its CSS property name. ``font_size`` -> ``font-size``.…, Record one declaration, warning if the property looks misspelled., Iterate ``(python_name, value)`` for every set property., Set properties in emission order: known first, then unknown., Return a copy with specific properties overridden. Passing ``None`` removes a…

### Community 58 - "22. Properties Panel"
Cohesion: 0.40
Nodes (5): 22. Properties Panel, Advanced, Appearance, Position, Text

### Community 59 - "letter_no"
Cohesion: 0.67
Nodes (3): description, type, letter_no

### Community 60 - "municipality"
Cohesion: 0.67
Nodes (3): description, type, municipality

### Community 61 - "LabelValue"
Cohesion: 0.12
Nodes (21): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main(), build_letter() (+13 more)

### Community 62 - "load_conversion"
Cohesion: 0.29
Nodes (9): convert(), load_conversion(), Any, Path, Datalab ``/convert``: the block tree a scan's geometry comes from.…, Convert *image_path* to a block tree and return the parsed JSON. Args:…, Read a conversion JSON saved earlier. Datalab deletes results an hour after the…, Write *conversion* to *path* and return it. (+1 more)

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

### Community 70 - "Document"
Cohesion: 0.20
Nodes (9): Document, Path, A single page of output. Parameters: title: ``<title>`` text. page_width: Width…, Render to a complete, self-contained HTML string., Write the rendered HTML to *path*, creating parent directories. Returns the…, A clipped overflow and a genuinely missing section look identical in the…, test_clip_false_lets_overflow_show(), test_document_add_coerces_and_names_itself() (+1 more)

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

### Community 80 - "district"
Cohesion: 0.67
Nodes (3): description, type, district

### Community 83 - "ink_extent"
Cohesion: 0.50
Nodes (4): ink_extent(), The bounding box of every block, in source space. Deliberately not the page…, The conversion page is 1372x980 around ink that is 1201x799. Normalizing…, test_extent_is_the_ink_not_the_page()

### Community 86 - "plan_to_schema"
Cohesion: 0.50
Nodes (4): plan_to_schema(), Build the extraction schema for the value fields *plan* names. Every value…, ``build_data`` keeps only what the schema lists as required, so a field the…, test_every_field_survives_extraction()

### Community 94 - "ref_no"
Cohesion: 0.67
Nodes (3): ref_no, description, type

## Knowledge Gaps
- **224 isolated node(s):** `graphify`, `Generated layouts`, `What is included`, `Setup`, `Which layout is live` (+219 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style` to `test_components.py`, `html_engine/__init__.py`, `grid.py`, `TableCell`, `PlaceholderBox`, `Document`, `translator.py`, `coerce_children`, `FlexRow`, `test_monochrome.py`, `Paragraph`, `Component`, `laalpurja/layout.py`, `Image`, `Any`, `LabelValue`, `spacer.py`, `field.py`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Why does `Document` connect `Document` to `test_components.py`, `html_engine/__init__.py`, `TableCell`, `PlaceholderBox`, `Style`, `coerce_children`, `FlexRow`, `Component`, `laalpurja/layout.py`, `LabelValue`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `AbsoluteBox` connect `LabelValue` to `test_components.py`, `html_engine/__init__.py`, `grid.py`, `TableCell`, `PlaceholderBox`, `Style`, `Component`, `build_citizenship_back`, `build_citizenship_old_back`, `build_citizenship_old`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Style` (e.g. with `Component` and `FieldGroup`) actually correct?**
  _`Style` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Component` (e.g. with `Style` and `FieldGroup`) actually correct?**
  _`Component` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Text` (e.g. with `PlaceholderBox` and `SignatureBlock`) actually correct?**
  _`Text` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `FlexRow` (e.g. with `build_citizenship_back()` and `build_citizenship_old()`) actually correct?**
  _`FlexRow` has 5 INFERRED edges - model-reasoned connections that need verification._