# Graph Report - /home/moon/pragya/babu-documentation  (2026-07-29)

## Corpus Check
- 52 files · ~33,356 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 371 nodes · 844 edges · 27 communities (20 shown, 7 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 85 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c19fd9fa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- components/__init__.py
- graph.py
- Style
- controller/ — LangGraph StateGraph Pipeline (extract→build→verify→review→repair)
- html_engine/__init__.py
- Repaired Laal Purja – Land Ownership Registration Certificate (PF002728503 NM0000095)
- output/
- Land Ownership Registration Certificate (Nepal)
- TableCell
- list.py
- text.py
- run.py
- spacer.py
- document_verifier.py
- Image
- .to_css
- base.py
- ._render_children
- .__add__
- Stage 1: Vision Verification
- study_plan.py
- GridItem
- Stage 3: Render-and-Retry Graph
- Stage 4: Human Review
- Python Dependencies (requirements.txt)

## God Nodes (most connected - your core abstractions)
1. `Style` - 80 edges
2. `Component` - 62 edges
3. `build_laalpurja()` - 24 edges
4. `build_citizenship()` - 18 edges
5. `build_graph()` - 15 edges
6. `LabelValue` - 15 edges
7. `Document` - 15 edges
8. `Land Ownership Registration Certificate (Nepal)` - 15 edges
9. `PipelineState` - 14 edges
10. `TableCell` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Donut / Surya — End-to-end OCR Candidates` --semantically_similar_to--> `Datalab OCR — External OCR Service for Document Extraction`  [INFERRED] [semantically similar]
  documentation/tasks.txt → README.md
- `TrOCR / Tesseract — Handwritten Nepali OCR Candidates` --semantically_similar_to--> `Datalab OCR — External OCR Service for Document Extraction`  [INFERRED] [semantically similar]
  documentation/tasks.txt → README.md
- `Laal Purja (Land Ownership Certificate) — Root-level HTML Sample` --semantically_similar_to--> `Laal Purja (Land Ownership Certificate) — Output HTML (Devanagari data)`  [INFERRED] [semantically similar]
  laalpurja.html → output/laalpurja.html
- `Nepali Citizenship Certificate — Rendered HTML Sample` --implements--> `document_builder — Citizenship & Laal Purja Layout Builders`  [INFERRED]
  document_builder/citizenship/test-citizenship.html → documentation/DOCUMENTATION.md
- `Laal Purja (Land Ownership Certificate) — Root-level HTML Sample` --implements--> `document_builder — Citizenship & Laal Purja Layout Builders`  [INFERRED]
  laalpurja.html → documentation/DOCUMENTATION.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Full Digitization Pipeline: OCR → Extraction → Builder → html_engine → Controller** — datalab_ocr, information_extraction, document_builder, html_engine, controller_langgraph [EXTRACTED 1.00]
- **Human-in-the-Loop Repair Loop: VerificationReport → HumanReview → RepairPlan/Edits → Rebuild** — verification_report, human_in_the_loop_review, repair_plan, schema_patcher [EXTRACTED 1.00]
- **Contenteditable Editing Foundation: html_engine attrs + document_builder + apply_edits node** — contenteditable_data_field_pattern, html_engine, document_builder, visual_editor_future [EXTRACTED 1.00]

## Communities (27 total, 7 thin omitted)

### Community 0 - "components/__init__.py"
Cohesion: 0.07
Nodes (43): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, Return editable attrs dict for a data-bearing element., main() (+35 more)

### Community 1 - "graph.py"
Cohesion: 0.07
Nodes (52): analyze_repair(), apply_edits(), apply_repair(), build_document(), build_graph(), check_resources(), extract_data(), generate_resources() (+44 more)

### Community 2 - "Style"
Cohesion: 0.12
Nodes (11): Component, Base class for all renderable document components. Parameters: style: Optional…, Append one or more child components. Returns self for chaining., Build the HTML attribute string for this element. Combines ``css_class``,…, Card, Grid, CSS Grid container. Parameters: columns: Grid template columns (e.g. 12 or…, A styled container mimicking a paper card. Includes preset styles: background… (+3 more)

### Community 3 - "controller/ — LangGraph StateGraph Pipeline (extract→build→verify→review→repair)"
Cohesion: 0.13
Nodes (29): Bounded Repair Loop — max_iterations Prevents Infinite Auto-Repair Cycles, Constrained Patch Vocabulary — LLM Cannot Emit Raw HTML/CSS/Python, contenteditable + data-field Pattern — In-browser Direct Field Editing, controller/ — LangGraph StateGraph Pipeline (extract→build→verify→review→repair), Controller — Document Verification, Repair & LangGraph Pipeline README, Datalab OCR — External OCR Service for Document Extraction, document_builder — Citizenship & Laal Purja Layout Builders, Nepali Citizenship Certificate — Rendered HTML Sample (+21 more)

### Community 4 - "html_engine/__init__.py"
Cohesion: 0.14
Nodes (15): Document, html_engine — Programmatic HTML Document Generation Engine. Build pixel-…, html_to_pdf(), Render a Document class to a full HTML string. The output is a self-contained…, render(), em(), pct(), pt() (+7 more)

### Community 5 - "Repaired Laal Purja – Land Ownership Registration Certificate (PF002728503 NM0000095)"
Cohesion: 0.21
Nodes (21): Land Ownership Certificate No. PF002728503 NM0000095, Citizenship No. 10005, Issued 2049/03/09 by Jilla Prashasan Karyalaya, Kathmandu, Deurubhi Chaulagain (देउरुभी चौलागाईं) – Father-in-law, Deurushi Chaulagain (देउरुषी चौलागाईं), Government of Nepal - Ministry of Land Reform and Management, Hemkant Chaulagain (हेमकान्त चौलागाईं), Hira Lal (हिरा लाल) – Tenant (Plots 692 & 652), Hira Lal Chaulagain (हिरा लाल चौलागाईं) (+13 more)

### Community 6 - "output/"
Cohesion: 0.23
Nodes (12): आदित्य जोशी, Document Builder, जेनिश पन्त, Land Ownership Registration Certificate, Plot 555 — काठमाण्डौ नाङ्गलेभारे, Plot 612 — काठमाण्डौ नाङ्गलेभारे, Plot 652 — काठमाण्डौ नाङ्गलेभारे, Nepali Citizenship Certificate (+4 more)

### Community 7 - "Land Ownership Registration Certificate (Nepal)"
Cohesion: 0.25
Nodes (16): Address: District Gorkha, M.C./V.D.C. Makaising, Ward No. 7, Land Ownership Certificate No. 4915149, Citizenship No. 443015/343, Issued 2007/02/16, Department of Land Reform and Management, District Administration Office: Gorkha, Jit Bahadur Shrestha (Father-in-Law), Government of Nepal, Plot No. 1431, Sanagaun, Ward 8/8ka (Residential + Private land, Sole ownership, 0-2-0 / 15.90 Sq.Mt.) (+8 more)

### Community 8 - "TableCell"
Cohesion: 0.24
Nodes (7): Table components: Table, TableRow, TableCell. Supports both simple table…, A full ``<table>`` element. Can be built from: - Explicit ``TableRow`` objects…, A single table cell (``<td>`` or ``<th>``). Parameters: content: Cell content —…, A table row (``<tr>``) containing one or more cells. Parameters: cells:…, Table, TableCell, TableRow

### Community 9 - "list.py"
Cohesion: 0.23
Nodes (6): ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList., Renders a list item ``<li>``. Parameters: content: String content or nested…, Renders an unordered list ``<ul>``. Parameters: items: List items — can be…, UnorderedList

### Community 10 - "text.py"
Cohesion: 0.17
Nodes (7): Link, Paragraph, Text components: Text, Heading, Paragraph, Link., Escape hatch: renders arbitrary HTML verbatim. Use sparingly — this bypasses…, Renders an anchor element ``<a>``. Parameters: content: The text content or…, Block paragraph element rendered as ``<p>``. Parameters: content: The paragraph…, RawHTML

### Community 11 - "run.py"
Cohesion: 0.25
Nodes (10): compile_graph(), Build and compile the graph with an optional checkpointer., _collect_decision(), _collect_edits(), main(), CLI runner for the LangGraph document digitization pipeline. Drives the graph…, Interactively collect field edits from the user., Pretty-print the verification results for human review. (+2 more)

### Community 12 - "spacer.py"
Cohesion: 0.20
Nodes (5): HorizontalRule, PageBreak, Spacer and divider components., Horizontal rule (``<hr>``) divider. Parameters: style: Override styles (color,…, Renders a page break for print media.

### Community 13 - "document_verifier.py"
Cohesion: 0.39
Nodes (8): Discrepancy, main(), png_data_url(), BaseModel, Path, To compare a source document PNG with a rendered PNG without modifying either., VerificationReport, verify()

### Community 14 - "Image"
Cohesion: 0.40
Nodes (3): Image, Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64.

### Community 15 - ".to_css"
Cohesion: 0.33
Nodes (3): Convert a Python attribute name to its CSS property equivalent., Serialize all non-None attributes into a CSS inline style string. Returns: A…, Return a full ``style="..."`` HTML attribute string, or an empty string if…

### Community 16 - "base.py"
Cohesion: 0.40
Nodes (3): ABC, Abstract base class for all HTML Document Engine components. Every renderable…, Image component for the HTML Document Engine.

### Community 19 - "Stage 1: Vision Verification"
Cohesion: 0.67
Nodes (3): Stage 1: Vision Verification, Stage 2: Layout Patches, VerificationReport Typed Output

## Ambiguous Edges - Review These
- `Hira Lal Chaulagain (हिरा लाल चौलागाईं)` → `Hira Lal (हिरा लाल) – Tenant (Plots 692 & 652)`  [AMBIGUOUS]
  output/laalpurja_repaired.png · relation: semantically_similar_to

## Knowledge Gaps
- **11 isolated node(s):** `Stage 2: Layout Patches`, `Stage 3: Render-and-Retry Graph`, `Stage 4: Human Review`, `VerificationReport Typed Output`, `Python Dependencies (requirements.txt)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.
