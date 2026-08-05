# Graph Report - .  (2026-08-05)

## Corpus Check
- Large corpus: 73 files · ~531,042 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 601 nodes · 1095 edges · 36 communities (32 shown, 4 thin omitted)
- Extraction: 79% EXTRACTED · 19% INFERRED · 2% AMBIGUOUS · INFERRED: 208 edges (avg confidence: 0.75)
- Token cost: 666,622 input · 0 output

## Community Hubs (Navigation)
- LangGraph Pipeline Controller
- Document Layout Builders
- Verification and Repair Architecture
- Layout and Container Components
- Manual Reference Render Baseline
- Rendered Certificate PNG Outputs
- Render Defect Findings
- HTML Engine Core
- Citizenship Certificate Templates
- Laalpurja Editable Template Fields
- Spacers, Links and Styles
- Scanned Source Document Fixtures
- Agentic Repair Loop Design
- PNG Rasterization Output Stage
- Base vs Repaired Render Comparison
- Contenteditable Field Editing
- Text Components
- List Components
- Adding New Document Types
- Table Components
- OCR and Extraction Backlog
- Laalpurja HTML Template Sections
- RAG Architect Agent
- Vision Document Verifier
- Autonomous Layout Generator Plan
- CLI Pipeline Runner
- Image Component
- CSS Style Serialization
- Headless Chrome PNG Renderer
- Component Child Rendering
- Style Merging
- Flask Web App
- Document Layout Detection Models
- Segment Anything Document Analysis

## God Nodes (most connected - your core abstractions)
1. `Style` - 80 edges
2. `Component` - 62 edges
3. `build_laalpurja()` - 24 edges
4. `build_citizenship()` - 18 edges
5. `build_graph()` - 15 edges
6. `LabelValue` - 15 edges
7. `PipelineState` - 14 edges
8. `TableCell` - 14 edges
9. `Document` - 14 edges
10. `FlexCol` - 13 edges

## Surprising Connections (you probably didn't know these)
- `label.* editable-label field namespace` --semantically_similar_to--> `Planned visual editor`  [INFERRED] [semantically similar]
  document_builder/laalpurja/laalpurja.html → controller-old/README.md
- `Rendered Nepali citizenship certificate (Devanagari test output)` --semantically_similar_to--> `Editable Nepali citizenship certificate (romanized test render)`  [INFERRED] [semantically similar]
  controller-old/test-data/output_citizenship.html → document_builder/citizenship/test-citizenship.html
- `Land Ownership Registration Certificate (rendered Laal Purja)` --implements--> `Laal Purja layout builder`  [INFERRED]
  laalpurja.html → documentation/DOCUMENTATION.md
- `LangGraph controller StateGraph` --references--> `langgraph dependency`  [INFERRED]
  documentation/DOCUMENTATION.md → requirements.txt
- `VerificationReport` --references--> `pydantic dependency`  [INFERRED]
  documentation/DOCUMENTATION.md → requirements.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **LangGraph controller node flow (extract → build → verify → review → repair)** — documentation_documentation_check_resources, documentation_documentation_extract_data, documentation_documentation_build_document, documentation_documentation_verify, documentation_documentation_human_review, documentation_documentation_analyze_repair, documentation_documentation_apply_repair, documentation_documentation_apply_edits, documentation_documentation_pipelinestate [EXTRACTED 1.00]
- **Editable-field round trip: attrs → data-field markup → human edits → apply_edits → visual editor** — documentation_documentation_attrs_passthrough, documentation_documentation_contenteditable_data_field, documentation_documentation_dotted_path_notation, laalpurja_editable_field_markup, documentation_documentation_apply_edits, documentation_documentation_visual_editor [EXTRACTED 1.00]
- **OCR / layout tooling candidates under evaluation** — documentation_tasks_handwritten_nepali_ocr, documentation_tasks_layoutparser, documentation_tasks_doclayout_yolo, documentation_tasks_donut, documentation_tasks_surya, documentation_tasks_segment_anything_model, documentation_tasks_preprocessing_engine, documentation_documentation_datalab_ocr [EXTRACTED 1.00]
- **Bounded verify-review-repair loop** — controller_old_readme_verify, controller_old_readme_human_review, controller_old_readme_analyze_repair, controller_old_readme_apply_repair, controller_old_readme_apply_edits, controller_old_readme_bounded_iterations [EXTRACTED 1.00]
- **data-field editing contract across rendered document types** — controller_old_readme_contenteditable_output, document_builder_citizenship_test_citizenship_citizenship_fields, document_builder_laalpurja_laalpurja_plots_field, document_builder_laalpurja_laalpurja_label_field, controller_old_readme_extraction_schema [INFERRED 0.95]
- **Shared print-ready page shell across all rendered certificates** — controller_old_test_data_output_citizenship, document_builder_citizenship_test_citizenship, document_builder_laalpurja_laalpurja, document_builder_laalpurja_laalpurja_page_shell [INFERRED 0.95]
- **All person-specific certificate renderings instantiate the single shared citizenship template with differing field values and issuing district** — output_html_citizenship_citizenship_certificatetemplate, output_html_citizenship_aditya_digital_certificateinstance, output_html_citizenship_jenish_certificateinstance, output_html_citizenship_pratik_certificateinstance, output_citizenship_certificatetemplate [EXTRACTED 1.00]
- **Fixed-position placeholder boxes plus header and details block compose the certificate page layout** — output_html_citizenship_citizenship_coatofarmsbox, output_html_citizenship_citizenship_officesealbox, output_html_citizenship_citizenship_photographbox, output_html_citizenship_citizenship_headersection, output_html_citizenship_citizenship_detailsblock, output_html_citizenship_citizenship_pagestylesystem [EXTRACTED 1.00]
- **Identity, address, and relation field groups together constitute the certificate's data schema surfaced as data-field placeholders** — output_html_citizenship_citizenship_identityfields, output_html_citizenship_citizenship_addressfields, output_html_citizenship_citizenship_relationfields, output_citizenship_datafieldschema [INFERRED 0.85]
- **Five near-duplicate renderings of the same laalpurja certificate template (NM0000095, 3 plots, 4332.09 sq.m), differing only in numeral script, evidence-number digits, and fill artifacts** — output_html_laalpurja_laal_certificate_template, output_html_laalpurja_laalpurja_certificate_template, output_html_laalpurja_laalpurja_repaired_certificate_template, output_html_laalpurja_output_certificate_template, output_html_laalpurja_redpaper_certificate_template [INFERRED 0.85]
- **Header + identity block + plot table + footer compose the full certificate page layout** — output_html_laalpurja_laalpurja_headersection, output_html_laalpurja_laalpurja_identityblock, output_html_laalpurja_laalpurja_plottable, output_html_laalpurja_laalpurja_footersection [EXTRACTED 1.00]
- **Rendering defect cluster: 'None' literals, numeral/transliteration drift, stray PF certificate-number prefix, inconsistent District/VDC joining** — output_html_laalpurja_laal_nonefillartifact, output_html_laalpurja_laalpurja_repaired_numeraltranslitvariance, output_html_laalpurja_laalpurja_repaired_certnoprefixanomaly, output_html_laalpurja_output_districtvdcformatting [INFERRED 0.85]
- **Structural regions composing the Land Ownership Certificate scan** — controller_old_test_data_input_headerregion, controller_old_test_data_input_certificatenumberfields, controller_old_test_data_input_photothumbregion, controller_old_test_data_input_ownerdetailfields, controller_old_test_data_input_landparceltable, controller_old_test_data_input_signatureregion [EXTRACTED 1.00]
- **Structural regions composing the Citizenship Certificate scan** — controller_old_test_data_input_citizenship_headerregion, controller_old_test_data_input_citizenship_certificatenumberfield, controller_old_test_data_input_citizenship_photoregion, controller_old_test_data_input_citizenship_sealandemblem, controller_old_test_data_input_citizenship_identityfields, controller_old_test_data_input_citizenship_parentagelinkfields [EXTRACTED 1.00]
- **Both scans act as the INPUT side of the document extraction / HTML reconstruction pipeline test fixtures** — controller_old_test_data_input, controller_old_test_data_input_citizenship, controller_old_test_data_input_pipelineinputrole, controller_old_test_data_input_citizenship_pipelineinputrole, controller_old_test_data_input_devanagarinepalidocumentdomain [INFERRED 0.95]
- **Land Ownership Certificate page assembled from header, owner block, parcel table, and footer** — controller_old_test_data_output_headerregion, controller_old_test_data_output_landownerdetailsblock, controller_old_test_data_output_parceltable, controller_old_test_data_output_totalareasummary, controller_old_test_data_output_footersignatureregion [EXTRACTED 1.00]
- **Citizenship certificate assembled from header, photo/seal boxes, and identity field groups** — controller_old_test_data_output_citizenship_headerregion, controller_old_test_data_output_citizenship_photosealblock, controller_old_test_data_output_citizenship_personaldetailsfields, controller_old_test_data_output_citizenship_addressfields, controller_old_test_data_output_citizenship_parentagefields, controller_old_test_data_output_citizenship_spousefields [EXTRACTED 1.00]
- **Both rendered PNGs are output-stage fixtures of one Nepali government document generation pipeline** — controller_old_test_data_output_png, controller_old_test_data_output_citizenship_png, controller_old_test_data_output_documentgenerationpipeline, controller_old_test_data_output_renderoutputartifact, controller_old_test_data_output_devanagarilocalization, controller_old_test_data_output_placeholderfixturestyle [INFERRED 0.85]
- **Coat of arms, office seal, photograph and thumb-impression boxes all render as empty labeled rectangles across both outputs** — output_citizenship_coatofarmsplaceholder, output_citizenship_sealplaceholder, output_citizenship_photoplaceholder, output_laalpurja_output_biometricregion, output_laalpurja_output_signedstub [INFERRED 0.85]
- **Unbound template values leak Python-ish sentinels ('None', 'XXX') or blank labels into final renders** — output_citizenship_xxxdefect, output_citizenship_nonedefect, output_laalpurja_output_nameblankdefect [INFERRED 0.85]
- **Parcel table columns, three data rows, dual ropani/metric area notation and the total-area footer together form the land-ledger structure** — output_laalpurja_output_parceltable, output_laalpurja_output_parcelrows, output_laalpurja_output_ropanibighanotation, output_laalpurja_output_areatotal [EXTRACTED 1.00]
- **Base Render to Repaired Render Pipeline Flow** — output_laalpurja_certificate, output_laalpurja_baserenderstage, output_laalpurja_repaired_repairstage, output_laalpurja_repaired_certificate, output_laalpurja_repaired_visualparity [INFERRED 0.85]
- **Certificate Structural Regions Forming the Laalpurja Layout** — output_laalpurja_headerregion, output_laalpurja_titleblock, output_laalpurja_biometricregion, output_laalpurja_landownerdetails, output_laalpurja_plotledgertable, output_laalpurja_totalareafooter [EXTRACTED 1.00]
- **Devanagari Text Surfaces Targeted by Encoding Repair** — output_laalpurja_devanagariencoding, output_laalpurja_landownerdetails, output_laalpurja_plotledgertable, output_laalpurja_repaired_glyphrepairhypothesis [INFERRED 0.65]
- **Base vs Repaired Render Comparison: script change with layout regressions** — output_png_laalpurja_render, output_png_laalpurja_repaired_render, output_png_laalpurja_repaired_devanagariscriptdata, output_png_laalpurja_repaired_layoutoverlapdefect, output_png_laalpurja_repaired_labelwrappingdefect [INFERRED 0.85]
- **Certificate Region Layout: header, identity block, transaction table, footer** — output_png_laalpurja_headerregion, output_png_laalpurja_identityregion, output_png_laalpurja_transactiontable, output_png_laalpurja_footerregion, output_png_laalpurja_repaired_certificatetemplate [EXTRACTED 1.00]
- **PNG Output Stage Artifacts and Styling System** — output_png_laalpurja_pngoutputstage, output_png_laalpurja_render, output_png_laalpurja_repaired_render, output_png_laalpurja_tabularstylesystem [INFERRED 0.85]
- **Shared Nepali Official Document Chrome: Coat of Arms, Government Header Stack, Seal and Photograph Placeholders** — output_png_manual_laal_screenshot_headerregion, output_png_manual_laal_screenshot_coatofarmsplaceholder, output_png_output_headerregion, output_png_output_coatofarmsplaceholder, output_png_output_roundofficesealplaceholder, output_png_output_photographplaceholder [INFERRED 0.85]
- **Ground-Truth Manual Capture vs Pipeline-Generated Render Comparison Loop** — output_png_manual_laal_screenshot, output_png_manual_laal_screenshot_groundtruthbaseline, output_png_output, output_png_output_htmltopngrenderstage, output_png_output_trailingwhitespaceartifact [INFERRED 0.75]
- **Citizenship Identity Field Family: Personal Details, Parentage, Spouse and Bikram Sambat Dates in Devanagari** — output_png_output_personaldetailsgrid, output_png_output_parentageblock, output_png_output_spouseblock, output_png_output_bikramsambatdatefields, output_png_output_devanagarivaluerendering, output_png_output_nullvaluerenderingartifact [EXTRACTED 1.00]

## Communities (36 total, 4 thin omitted)

### Community 0 - "LangGraph Pipeline Controller"
Cohesion: 0.08
Nodes (44): analyze_repair(), apply_edits(), apply_repair(), build_document(), build_graph(), check_resources(), compile_graph(), extract_data() (+36 more)

### Community 1 - "Document Layout Builders"
Cohesion: 0.09
Nodes (33): _address_block(), build_citizenship(), _ea(), field_row(), multi_row(), Any, main(), build_laalpurja() (+25 more)

### Community 2 - "Verification and Repair Architecture"
Cohesion: 0.09
Nodes (35): Controller — Document Verification, Repair & LangGraph Pipeline, analyze_repair node, apply_edits node, apply_repair node, Bounded iterations (max_iterations), build_document node, check_resources node, Constrained patch vocabulary (design choice) (+27 more)

### Community 3 - "Layout and Container Components"
Cohesion: 0.09
Nodes (14): Component, Base class for all renderable document components. Parameters: style: Optional…, Append one or more child components. Returns self for chaining., AbsoluteBox, Card, Div, Grid, GridItem (+6 more)

### Community 4 - "Manual Reference Render Baseline"
Cohesion: 0.09
Nodes (31): Manual Laalpurja Screenshot (Reference Capture), Photograph and Right/Left Thumb Impression Cells, Land Ownership Certificate No. Field (4915149), Coat of Arms Placeholder Box, Fully English-Translated Field Labels, Footer Attestation Region (Printing done by / Print Date / Checked by), Ground-Truth Reference Baseline for Generated Renders, Laalpurja Header Region (Government of Nepal / Ministry of Land Reform) (+23 more)

### Community 5 - "Rendered Certificate PNG Outputs"
Cohesion: 0.09
Nodes (30): Bikram Sambat Date Rendering (२०८२/०४/१४), Double-Ruled Full-Page Bordered Print Layout, Land Ownership Certificate No. NM0000095, Birth Place and Permanent Address Fields (District / Municipality-VDC / Ward No.), Certificate of Nepali Citizenship (Nagarikta), Citizenship No. ४१-०१-७८-००४६६, Header Region (Ministry of Home Affairs, District Administration Office गुल्मी), Two-Column Label/Value Grid Layout (no table borders) (+22 more)

### Community 6 - "Render Defect Findings"
Cohesion: 0.09
Nodes (29): Birth Place & Permanent Address (District / Municipality-VDC / Ward No.), Single-page bordered A4-landscape template frame with whitespace tail, Citizenship No. field (Devanagari digits २९-०१-७८-०३८९८), Coat of Arms of Nepal placeholder box (unfilled), Bilingual styling: English serif labels with Devanagari values, Citizenship header region (Govt of Nepal / MoHA / DAO Bhaktapur), Holder identity fields (Full Name, Gender, Date of Birth), Render defect: literal 'None' printed where parent citizenship no. is missing (+21 more)

### Community 7 - "HTML Engine Core"
Cohesion: 0.12
Nodes (18): ABC, Abstract base class for all HTML Document Engine components. Every renderable…, Field components: LabelValue pairs and FieldGroups. These are the workhorses…, Image component for the HTML Document Engine., Document, Render a Document class to a full HTML string. The output is a self-contained…, render(), em() (+10 more)

### Community 8 - "Citizenship Certificate Templates"
Cohesion: 0.10
Nodes (28): Nepali Citizenship Certificate Template (editable render), contenteditable Field Editing System (data-field attributes, hover/focus outline styles), data-field Placeholder Schema (citizenship_no, full_name, gender, birth_ward, perm_ward, dob_year/month/day, father_*, mother_*, spouse_*), Jenish Pant Certificate Data Instance (Bhaktapur DAO, editable variant), आदित्य जोशी (Aditya Joshi) - certificate holder, Aditya Joshi Certificate Instance (Kathmandu DAO, no-shadow digital variant), Address Fields (Birth Place and Permanent Address as District + Municipality/VDC + Ward No.), Nepali Citizenship Certificate Template (canonical static render) (+20 more)

### Community 9 - "Laalpurja Editable Template Fields"
Cohesion: 0.11
Nodes (28): Land Ownership Registration Certificate (laal.html rendering), Certificate identifiers: Certificate No. NM0000095, Evd. no. ML-series, B.S. dates २०८२/०४/१४, total area 4332.09 sq.m across 3 plots, Citizenship issuing office: जिल्ला प्रशासन कार्यालय, काठमाण्डौ, Nepali land vocabulary: आबादी/आवादी (cultivated), रैकर निजी (raikar private), एकलौटी (sole title), भिट/पाखो/बारी दोयम (land class), रोपनी area units, Landowner entity: उमा देवी चौलागाई (Uma Devi Chaulagain), Issuing authority: Land Revenue Office, साखु, काठमाण्डौ (Dept. of Land Reform and Management), 'None' literal artifact leaking into Register Page No./serial and transaction cells (unbound Python None serialized into HTML), Page style system: .page 1200px fixed-width white sheet, Times New Roman serif, 1px black borders, inline flexbox layout (+20 more)

### Community 10 - "Spacers, Links and Styles"
Cohesion: 0.11
Nodes (13): Build the HTML attribute string for this element. Combines ``css_class``,…, HorizontalRule, PageBreak, Spacer and divider components., Empty vertical space with a fixed height. Parameters: height: CSS height value…, Horizontal rule (``<hr>``) divider. Parameters: style: Override styles (color,…, Renders a page break for print media., Spacer (+5 more)

### Community 11 - "Scanned Source Document Fixtures"
Cohesion: 0.11
Nodes (24): input.png — Scanned Nepali Land Ownership Certificate (Laalpurja), Certificate Number Fields — PF002728503 and NM0000095 (top-right), input_citizenship.png — Scanned Nepali Citizenship Certificate, Harsh Bitonal Binarization, Skew and Speckle Artifacts in the Scan, Citizenship Number Field — ना.प्र.नं. ४१-०१-७८-००४५६६, Nepali Citizenship Certificate (नेपाली नागरिकताको प्रमाणपत्र) Document Type, Dotted Fill-Line / Typewritten-Over-Preprinted-Form Layout, Header Region — Government of Nepal / Ministry of Home Affairs / District Administration Office Gulmi (+16 more)

### Community 12 - "Agentic Repair Loop Design"
Cohesion: 0.11
Nodes (22): Observe → Retrieve → Plan → Execute agent loop, LayoutAdjustment proposal, analyze_repair node, apply_repair node, build_document node, controller/document_verifier (vision-model render comparison), human_review node, LangGraph interrupt/resume human-in-the-loop pattern (+14 more)

### Community 13 - "PNG Rasterization Output Stage"
Cohesion: 0.15
Nodes (20): Certificate Number Field (4915149), Footer Region: Total Area, Print Date, Signatures, Header Region: Government of Nepal / Land Revenue Office, Identity Region: Photograph, Thumb Impression, Landowner Details, Latin-Script Transliterated Field Data, PNG Rasterization Output Stage (output/png directory), Laalpurja Base Render (output/png), Repaired Certificate Number Field (NM0000095) (+12 more)

### Community 14 - "Base vs Repaired Render Comparison"
Cohesion: 0.18
Nodes (18): Base Render Pipeline Stage, Bilingual English-Nepali Template System, Photograph and Thumb Impression Region, Laalpurja Base Render (Land Ownership Registration Certificate), Land Ownership Certificate No. Field (NM0000095), Coat of Arms Placeholder Box, Devanagari Script and Nepali Numeral Rendering, Government of Nepal Header Region (+10 more)

### Community 15 - "Contenteditable Field Editing"
Cohesion: 0.20
Nodes (14): apply_edits node, Arbitrary HTML attributes (attrs) passthrough, Component (base renderable node), contenteditable + data-field editable value convention, Dotted field-path notation (plots.0.plot_no), LabelValue component, Style (inline CSS producer), Browser-based visual editor (future work) (+6 more)

### Community 16 - "Text Components"
Cohesion: 0.18
Nodes (8): html_engine.components — All renderable component types., Heading, Paragraph, Text components: Text, Heading, Paragraph, Link., Escape hatch: renders arbitrary HTML verbatim. Use sparingly — this bypasses…, Block heading element rendered as ``<h1>`` through ``<h6>``. Parameters:…, Block paragraph element rendered as ``<p>``. Parameters: content: The paragraph…, RawHTML

### Community 17 - "List Components"
Cohesion: 0.20
Nodes (7): ListItem, OrderedList, List components: ListItem, UnorderedList, OrderedList., Renders a list item ``<li>``. Parameters: content: String content or nested…, Renders an unordered list ``<ul>``. Parameters: items: List items — can be…, Renders an ordered list ``<ol>``. Parameters: items: List items — can be…, UnorderedList

### Community 18 - "Adding New Document Types"
Cohesion: 0.21
Nodes (12): Adding a new document type (3-step procedure), Citizenship layout builder, Document (page-level container), document_builder/registry.py (document type registry), Default HTML escaping policy (RawHTML / escape=False as opt-out), generate_resources node (v2 stub), html_engine (declarative Python HTML document engine), Laal Purja layout builder (+4 more)

### Community 19 - "Table Components"
Cohesion: 0.27
Nodes (5): Table components: Table, TableRow, TableCell. Supports both simple table…, A single table cell (``<td>`` or ``<th>``). Parameters: content: Cell content —…, A table row (``<tr>``) containing one or more cells. Parameters: cells:…, TableCell, TableRow

### Community 20 - "OCR and Extraction Backlog"
Cohesion: 0.18
Nodes (11): check_resources node, Conditional routing (route_after_check_resources, route_after_review), Datalab OCR, extract_data node, information_extraction (OCR extraction and schema registry), Donut (clovaai), Handwritten Nepali OCR model (TrOCR finetune, Tesseract), OCR JSON → HTML engine integration (+3 more)

### Community 21 - "Laalpurja HTML Template Sections"
Cohesion: 0.29
Nodes (11): Photograph and Thumbprint Section, Contenteditable Data Fields Convention, data-field Naming Pattern, Footer Signature Section, Government Header Section, Landowner Information Block, Land Plot Information Table, Print Media Styles (+3 more)

### Community 22 - "RAG Architect Agent"
Cohesion: 0.25
Nodes (9): Architect Agent, controller/architect.py, Embedding strategy (sentence-transformers/all-MiniLM-L6-v2), Knowledge Base (RAG layer over the codebase), query_context(question), controller/rag_engine.py, Vector store (FAISS / ChromaDB), controller.run CLI entry point (+1 more)

### Community 23 - "Vision Document Verifier"
Cohesion: 0.46
Nodes (7): Discrepancy, main(), png_data_url(), BaseModel, Path, VerificationReport, verify()

### Community 24 - "Autonomous Layout Generator Plan"
Cohesion: 0.29
Nodes (8): Plan: Autonomous Agentic Layout & Schema Generator, Annotated[list[dict], add] history reducer, LangGraph controller StateGraph, PipelineState, Babu Technical Documentation, Babu Document Digitization, Digitization Pipeline (image → OCR → JSON → layout → HTML/PNG → controller), langgraph dependency

### Community 25 - "CLI Pipeline Runner"
Cohesion: 0.53
Nodes (5): _collect_decision(), _collect_edits(), main(), CLI runner for the LangGraph document digitization pipeline. python -m…, _show_review()

### Community 26 - "Image Component"
Cohesion: 0.40
Nodes (3): Image, Renders an ``<img>`` element. Parameters: src: Image source — a URL, file path,…, Resolve the image source, optionally embedding as base64.

### Community 27 - "CSS Style Serialization"
Cohesion: 0.33
Nodes (3): Convert a Python attribute name to its CSS property equivalent., Serialize all non-None attributes into a CSS inline style string. Returns: A…, Return a full ``style="..."`` HTML attribute string, or an empty string if…

### Community 28 - "Headless Chrome PNG Renderer"
Cohesion: 0.60
Nodes (4): Path, Render html to a PNG via headless Chrome/Chromium. Chrome/Chromium executable…, render_png(), test()

### Community 31 - "Flask Web App"
Cohesion: 0.67
Nodes (3): route, index(), process()

## Ambiguous Edges - Review These
- `controller/document_verifier.py — source PNG vs rendered PNG comparison` → `Rendered Nepali citizenship certificate (Devanagari test output)`  [AMBIGUOUS]
  controller-old/test-data/output_citizenship.html · relation: shares_data_with
- `@media print Rules (white background, no box-shadow, #444 border, page-break-after, .no-print hidden)` → `Template Instantiation Pattern (one shared markup skeleton re-rendered per person; only field values and district differ)`  [AMBIGUOUS]
  output/html/citizenship/citizenship.html · relation: conceptually_related_to
- `Missing Value Sentinels (literal 'None' and 'XXX' leaking into rendered output)` → `Pratik Pokharel Certificate Instance (Gulmi DAO)`  [AMBIGUOUS]
  output/html/citizenship/pratik.html · relation: conceptually_related_to
- `Certificate identifiers: Certificate No. NM0000095, Evd. no. ML-series, B.S. dates २०८२/०४/१४, total area 4332.09 sq.m across 3 plots` → `Certificate No. anomaly in repaired variant: 'PF002728503 NM0000095' (extra PF prefix not present in sibling renderings)`  [AMBIGUOUS]
  output/html/laalpurja/laalpurja_repaired.html · relation: references
- `Landowner Detail Fields — name, address, husband/father, father-in-law, citizenship no., issue date, issuing office` → `Citizenship Number Field — ना.प्र.नं. ४१-०१-७८-००४५६६`  [AMBIGUOUS]
  controller-old/test-data/input_citizenship.png · relation: shares_data_with
- `Land Ownership Certificate No. NM0000095` → `Citizenship No. ४१-०१-७८-००४६६`  [AMBIGUOUS]
  controller-old/test-data/output_citizenship.png · relation: semantically_similar_to
- `Single-page bordered A4-landscape template frame with whitespace tail` → `Fully English rendering of a natively Nepali form (translated template)`  [AMBIGUOUS]
  output/citizenship.png · relation: conceptually_related_to
- `Pipeline output stage: synthetic Nepali government document renders` → `Synthetic identity-document generation for OCR/extraction training data`  [AMBIGUOUS]
  output/citizenship.png · relation: rationale_for
- `Landowner Identity Field Block` → `Repair Pipeline Stage`  [AMBIGUOUS]
  output/laalpurja_repaired.png · relation: references
- `Plot Ledger Table (16-column transaction grid)` → `Repair Pipeline Stage`  [AMBIGUOUS]
  output/laalpurja_repaired.png · relation: references
- `Devanagari Script and Nepali Numeral Rendering` → `Devanagari Glyph/Encoding Repair Hypothesis`  [AMBIGUOUS]
  output/laalpurja_repaired.png · relation: rationale_for
- `Repair Pipeline Stage` → `Devanagari Glyph/Encoding Repair Hypothesis`  [AMBIGUOUS]
  output/laalpurja_repaired.png · relation: rationale_for
- `Certificate Number Field (4915149)` → `Repaired Certificate Number Field (NM0000095)`  [AMBIGUOUS]
  output/png/laalpurja_repaired.png · relation: shares_data_with
- `Devanagari Script Field Data and Nepali Numerals` → `Layout Overlap Defect in Identity Region`  [AMBIGUOUS]
  output/png/laalpurja_repaired.png · relation: rationale_for
- `Devanagari Script Field Data and Nepali Numerals` → `Repair Pipeline Stage (unicode/script restoration variant)`  [AMBIGUOUS]
  output/png/laalpurja_repaired.png · relation: rationale_for
- `Manual Laalpurja Screenshot (Reference Capture)` → `HTML-Template-to-PNG Render Pipeline Stage`  [AMBIGUOUS]
  output/png/manual_laal_screenshot.png · relation: conceptually_related_to
- `Ground-Truth Reference Baseline for Generated Renders` → `Generated Pipeline Render Output (output.png)`  [AMBIGUOUS]
  output/png/manual_laal_screenshot.png · relation: rationale_for
- `Ground-Truth Reference Baseline for Generated Renders` → `Synthetic PII-Bearing Identity Document Sample`  [AMBIGUOUS]
  output/png/output.png · relation: conceptually_related_to
- `Laalpurja HTML Template` → `HTML Repair Process`  [AMBIGUOUS]
  output/laalpurja_repaired.html · relation: transforms

## Knowledge Gaps
- **68 isolated node(s):** `Style (inline CSS producer)`, `MemorySaver checkpointer`, `Annotated[list[dict], add] history reducer`, `Adding a new document type (3-step procedure)`, `Embedding strategy (sentence-transformers/all-MiniLM-L6-v2)` (+63 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `controller/document_verifier.py — source PNG vs rendered PNG comparison` and `Rendered Nepali citizenship certificate (Devanagari test output)`?**
  _Edge tagged AMBIGUOUS (relation: shares_data_with) - confidence is low._
- **What is the exact relationship between `@media print Rules (white background, no box-shadow, #444 border, page-break-after, .no-print hidden)` and `Template Instantiation Pattern (one shared markup skeleton re-rendered per person; only field values and district differ)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Missing Value Sentinels (literal 'None' and 'XXX' leaking into rendered output)` and `Pratik Pokharel Certificate Instance (Gulmi DAO)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Certificate identifiers: Certificate No. NM0000095, Evd. no. ML-series, B.S. dates २०८२/०४/१४, total area 4332.09 sq.m across 3 plots` and `Certificate No. anomaly in repaired variant: 'PF002728503 NM0000095' (extra PF prefix not present in sibling renderings)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Landowner Detail Fields — name, address, husband/father, father-in-law, citizenship no., issue date, issuing office` and `Citizenship Number Field — ना.प्र.नं. ४१-०१-७८-००४५६६`?**
  _Edge tagged AMBIGUOUS (relation: shares_data_with) - confidence is low._
- **What is the exact relationship between `Land Ownership Certificate No. NM0000095` and `Citizenship No. ४१-०१-७८-००४६६`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Single-page bordered A4-landscape template frame with whitespace tail` and `Fully English rendering of a natively Nepali form (translated template)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._