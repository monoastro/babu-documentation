# Graph Report - babu-documentation  (2026-08-09)

## Corpus Check
- 65 files · ~759,754 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 633 nodes · 1346 edges · 51 communities (33 shown, 18 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 77 edges (avg confidence: 0.53)
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
- Component
- citizenship/layout.py
- styles.py
- test_styles.py
- Spacer
- laalpurja/layout.py
- normalize_value
- document.py
- "First make it work, then make it better"
- coerce_children
- Watermark
- HTML document engine
- .save
- ListItem
- .__init__
- ._resolve_src
- rag_engine.py
- .to_css
- Salvage record: `controller-old/` → `agentic_controller/`
- langgraph dependency
- python-dotenv dependency
- validate_layout
- Paragraph
- test_monochrome.py
- Any
- normalize_declarations
- .__add__
- route
- DocLayout-YOLO
- Segment Anything Model for document analysis
- Surya (datalab-to)
- Style
- CLAUDE.md
- architect.py
- models.py
- 1. Document Verification Rules
- Text
- ._render_children
- run_all.py
- agentic_controller/__init__.py
- Ideal patching prompt composition
- Perfect-match VerificationReport example
- langchain-openai dependency
- pydantic dependency

## God Nodes (most connected - your core abstractions)
1. `Style` - 122 edges
2. `Component` - 58 edges
3. `Text` - 38 edges
4. `Document` - 27 edges
5. `build_laalpurja()` - 23 edges
6. `Spacer` - 22 edges
7. `FlexRow` - 20 edges
8. `PlaceholderBox` - 20 edges
9. `LabelValue` - 19 edges
10. `Div` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_route_1_style_to_css()` --calls--> `Style`  [EXTRACTED]
  tests/test_monochrome.py → html_engine/styles.py
- `test_route_3_style_raw_escape_hatch()` --calls--> `Style`  [EXTRACTED]
  tests/test_monochrome.py → html_engine/styles.py
- `test_clone_removes_with_none()` --calls--> `Style`  [EXTRACTED]
  tests/test_styles.py → html_engine/styles.py
- `test_merge_overrides_and_concatenates_raw()` --calls--> `Style`  [EXTRACTED]
  tests/test_styles.py → html_engine/styles.py
- `test_merge_with_none_returns_self_equivalent()` --calls--> `Style`  [EXTRACTED]
  tests/test_styles.py → html_engine/styles.py

## Import Cycles
- None detected.

## Communities (51 total, 18 thin omitted)

### Community 0 - "test_main_cli.py"
Cohesion: 0.10
Nodes (31): _crop_to_page(), _page_metrics(), Path, render_png(), An unrecognized CSS property name reached ``Style``. Probably a typo., StyleWarning, build_data(), extract() (+23 more)

### Community 1 - "test_components.py"
Cohesion: 0.11
Nodes (25): Div, FlexRow, Generic block container rendered as a ``<div>``. The simplest building block —…, Horizontal flex container (``flex-direction: row``). Parameters: children:…, corner_box(), PlaceholderBox, A labelled outline standing in for artwork that cannot be rendered. Renders a…, A placeholder pinned to one corner of the page — crest, QR block, stamp.… (+17 more)

### Community 3 - ".__init__"
Cohesion: 0.16
Nodes (7): Card, Grid, GridItem, Any, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, CSS Grid item. Parameters: column_span: Number of columns this item spans (e.g.…, A styled container mimicking a paper card. Includes preset styles: background…

### Community 4 - "Component"
Cohesion: 0.11
Nodes (25): ABC, coerce_child(), Component, editable_attrs(), Abstract base class for all HTML Document Engine components. Every renderable…, Turn one constructor argument into a child component, or reject it. Containers…, Attributes that make one rendered value editable in the browser. The ``data-…, Base class for all renderable document components. Parameters: style: Optional… (+17 more)

### Community 5 - "citizenship/layout.py"
Cohesion: 0.16
Nodes (15): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main(), FieldGroup (+7 more)

### Community 6 - "styles.py"
Cohesion: 0.17
Nodes (11): em(), pct(), pt(), px(), Style descriptor for the HTML Document Engine. ``Style`` is an **open**…, Return value as CSS pixel string., Return value as CSS percentage string., Return value as CSS em string. (+3 more)

### Community 7 - "test_styles.py"
Cohesion: 0.08
Nodes (22): Tests for the open property bag that replaced the closed ``Style`` dataclass.…, Monochrome is enforced on the way out, including for unlisted props., The reported crash. Any valid CSS property must survive to the output., Both are deliberate, so neither should look like a typo., The trade for accepting anything: a misspelling is no longer a TypeError. It…, What ``main.py --strict`` relies on., A name CSS could never accept is a bug worth stopping for., CSS resolves duplicates last-one-wins, so ``margin`` emitted after ``margin-… (+14 more)

### Community 8 - "Spacer"
Cohesion: 0.14
Nodes (18): build_citizenship_back(), Any, build_letter(), _ea(), Any, AbsoluteBox, FlexCol, Absolutely positioned container. Use for elements that need precise pixel… (+10 more)

### Community 9 - "laalpurja/layout.py"
Cohesion: 0.16
Nodes (16): build_laalpurja(), _ea(), _lv(), Any, Land Ownership Registration Certificate (Laal Purja) — Layout Definition,…, _td(), _th(), _to_float() (+8 more)

### Community 10 - "normalize_value"
Cohesion: 0.13
Nodes (15): normalize_value(), Rewrite every colour token in a single declaration's *value*. Parameters: prop:…, Thresholding by luminance would map a dark fill to black and its light text to…, A curated subset leaked ``rebeccapurple``. Any name the regex misses passes…, Alternation is scanned left to right. With "red" ordered before "rebeccapurple"…, Rewriting transparent to white paints over content meant to show through., Corrupting document data is worse than leaking a colour., A url(...) may hold a "#" fragment that is not a colour. (+7 more)

### Community 11 - "document.py"
Cohesion: 0.21
Nodes (9): Document — the root of a renderable page. A ``Document`` holds page geometry…, normalize_html(), Monochrome enforcement for the HTML Document Engine. Project rule: a rendered…, Surfaces go white, ink goes black., Rewrite colours in a complete HTML document. Only ``style="..."`` attributes…, _target_for(), Render a Document class to a full HTML string. The output is a self-contained…, render() (+1 more)

### Community 13 - "coerce_children"
Cohesion: 0.25
Nodes (6): coerce_children(), Any, Append one or more child components. Returns self for chaining. Accepts the…, Coerce an iterable of constructor arguments, dropping ``None``s., Any, Append top-level components. Returns self for chaining. Accepts components,…

### Community 14 - "Watermark"
Cohesion: 0.33
Nodes (6): Faint centred text behind the page content. Absolutely positioned and non-…, Watermark, Three properties separate a watermark from a heading: it sits behind, it never…, test_watermark_centres_on_its_own_midpoint(), test_watermark_is_inert(), test_watermark_rotation_composes_with_the_centring()

### Community 15 - "HTML document engine"
Cohesion: 0.04
Nodes (46): Adding a new document type, Agentic controller, Arbitrary HTML attributes (`attrs`), Architect Agent (`architect.py`), Architecture, Babu Document Digitization: Technical Documentation, Building one document by hand, Component reference (+38 more)

### Community 16 - ".save"
Cohesion: 0.40
Nodes (3): Path, Write the rendered HTML to *path*, creating parent directories. Returns the…, Render to a complete, self-contained HTML string.

### Community 17 - "ListItem"
Cohesion: 0.20
Nodes (7): ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList., Renders a list item ``<li>``. Parameters: content: String content or nested…, Renders an unordered list ``<ul>``. Parameters: items: List items — can be…, Renders an ordered list ``<ol>``. Parameters: items: List items — can be…, UnorderedList

### Community 20 - "rag_engine.py"
Cohesion: 0.10
Nodes (37): _tool_query_context(), build_chunks(), build_index(), Chunk, chunk_file(), chunk_json_schema(), chunk_markdown(), chunk_python() (+29 more)

### Community 21 - ".to_css"
Cohesion: 0.33
Nodes (4): _css_name(), Map a Python keyword to its CSS property name. ``font_size`` -> ``font-size``.…, Serialize to an inline CSS declaration string. Colours are normalized to black-…, Return a full ``style="..."`` attribute, or ``""`` if empty.

### Community 22 - "Salvage record: `controller-old/` → `agentic_controller/`"
Cohesion: 0.33
Nodes (5): Behaviour to reproduce in Phase 2/3, Carried across, Deliberately dropped, Not indexed by RAG, Salvage record: `controller-old/` → `agentic_controller/`

### Community 25 - "validate_layout"
Cohesion: 0.20
Nodes (20): Check that a generated layout module is safe for the caller to use. Four gates,…, validate_layout(), _layout(), Path, Tests for ``architect.validate_layout`` — the gate that let the reported bug…, Blank probe data is the harsh case. A layout indexing a key the schema does not…, A property outside the known list is a cosmetic gap, not a reason to fail a…, Without a schema the builder is probed with ``{}``. (+12 more)

### Community 26 - "Paragraph"
Cohesion: 0.18
Nodes (4): Link, Paragraph, Renders an anchor element ``<a>``. Parameters: content: The text content or…, Block paragraph element rendered as ``<p>``. Parameters: content: The paragraph…

### Community 27 - "test_monochrome.py"
Cohesion: 0.15
Nodes (14): find_violations(), Report colour tokens that normalization *would* change. Returns a list of…, Tests for the monochrome guarantee. Project rule: a rendered document is purely…, A component can carry a hand-written style attribute, bypassing Style., A component's own ``to_html()`` can hardcode a style the engine never sees as a…, One document exercising every route at once, audited by find_violations., The guarantee that actually matters: every shipped document type., test_all_bypass_routes_are_closed() (+6 more)

### Community 28 - "Any"
Cohesion: 0.22
Nodes (5): Any, Record one declaration, warning if the property looks misspelled., Iterate ``(python_name, value)`` for every set property., Set properties in emission order: known first, then unknown. Known properties…, Return a copy with specific properties overridden. Passing ``None`` removes a…

### Community 29 - "normalize_declarations"
Cohesion: 0.40
Nodes (4): Build the HTML attribute string for this element. Combines ``css_class``,…, normalize_declarations(), Rewrite colours across a CSS fragment. Works both on an inline declaration list…, test_selector_is_not_mistaken_for_a_property()

### Community 31 - "route"
Cohesion: 0.67
Nodes (3): route, index(), process()

### Community 37 - "Style"
Cohesion: 0.17
Nodes (4): PageBreak, Renders a page break for print media., An open set of CSS declarations. Any keyword is accepted and emitted as a CSS…, Style

### Community 39 - "architect.py"
Cohesion: 0.06
Nodes (72): analyze_and_repair(), _build_system_prompt(), current_layout_path(), _dispatch_tool(), generate_resources(), _image(), _load_rules(), _log_call() (+64 more)

### Community 40 - "models.py"
Cohesion: 0.14
Nodes (15): Discrepancy, LayoutPatch, Pydantic models — the structured vocabulary the agent may use. Consolidates the…, The full proposal returned by the analysis step., A single visible difference between the source and the rendered output., Discrepancies the agent must fix — ``major`` and ``critical`` only. ``minor``…, A single change to the extraction JSON schema., A single structural change to the document layout builder. (+7 more)

### Community 41 - "1. Document Verification Rules"
Cohesion: 0.14
Nodes (13): 1.1 Expected transformations — never flag these, 1.2 What to actually check, 1.3 Severity guide, 1.4 Uncertainty, 1.5 Report shape, 1. Document Verification Rules, 2.1 Allowed schema patch actions, 2.2 Allowed layout patch actions (+5 more)

### Community 42 - "Text"
Cohesion: 0.16
Nodes (12): Inline text element rendered as a ``<span>``. Parameters: content: The text…, Text, Document, A single page of output. Parameters: title: ``<title>`` text. page_width: Width…, A clipped overflow and a genuinely missing section look identical in the…, ``field=`` uses setdefault, so a layout that needs a non-editable but labelled…, test_clip_false_lets_overflow_show(), test_document_add_coerces_and_names_itself() (+4 more)

## Knowledge Gaps
- **60 isolated node(s):** `graphify`, `What is included`, `Setup`, `Run the full pipeline`, `Build one document by hand` (+55 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Style` connect `Style` to `test_main_cli.py`, `test_components.py`, `.__init__`, `Component`, `citizenship/layout.py`, `styles.py`, `test_styles.py`, `Spacer`, `laalpurja/layout.py`, `document.py`, `coerce_children`, `Watermark`, `ListItem`, `.__init__`, `._resolve_src`, `.to_css`, `Paragraph`, `test_monochrome.py`, `Any`, `normalize_declarations`, `.__add__`, `Text`?**
  _High betweenness centrality (0.287) - this node is a cross-community bridge._
- **Why does `render_png()` connect `test_main_cli.py` to `architect.py`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `Document` connect `Text` to `test_components.py`, `Component`, `citizenship/layout.py`, `Style`, `Spacer`, `laalpurja/layout.py`, `document.py`, `coerce_children`, `.save`, `test_monochrome.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Style` (e.g. with `Component` and `FieldGroup`) actually correct?**
  _`Style` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `Component` (e.g. with `Text` and `Style`) actually correct?**
  _`Component` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Text` (e.g. with `Component` and `PlaceholderBox`) actually correct?**
  _`Text` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Document` (e.g. with `Component` and `Style`) actually correct?**
  _`Document` has 2 INFERRED edges - model-reasoned connections that need verification._