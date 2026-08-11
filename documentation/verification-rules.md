# Verification & Repair Rules

Extracted verbatim-in-substance from `controller-old/document_verifier.py` (SYSTEM_PROMPT) and
`controller-old/layout_repairer.py` (ANALYSIS_PROMPT). `controller-old/` is deprecated and kept
only as reference — these rules are the part that must survive into the agentic controller.

The Architect Agent is optimizing toward one thing: driving a `VerificationReport.overall_match`
from `"fail"` / `"needs_review"` to `"pass"`. Everything below defines what that means.

---

## 1. Document Verification Rules

Source: `controller-old/document_verifier.py`

The rendered output is a **structured digital replica** of the source, not a pixel-perfect copy.
The source document is the reference of truth.

### 1.1 Expected transformations — never flag these

| # | Transformation | Detail |
|---|---|---|
| 1 | **Language** | The output is **fully English**. Labels are translated (`नाम थर:` → `Full Name:`), and so are **values**: phrases translated (`वंशज` → `By descent`), person and place names transliterated (`उमा देवी चौलागाई` → `Uma Devi Chaulagai`), Devanagari numerals converted to ASCII (`८` → `8`), and Bikram Sambat dates converted to Gregorian (`२०४९/०३/०९` → `1992-06-22`). A script difference is never a discrepancy — judge a value on whether it is the *correct* English rendering. Applied by `information_extraction/translator.py`; suppress with `--no-translate`. |
| 2 | **Visual elements** | Photographs, coat of arms, official seals, stamps, thumb impressions, and signatures are intentionally replaced by bordered placeholder boxes of similar size carrying a descriptive label — `Coat of Arms of Nepal`, `Round Office Seal`, `Photograph Sd.`, `Thumb Impression`, `(Signed)`. |
| 3 | **Formatting** | Clean digital typography, consistent spacing, and structured layout in place of handwriting, rubber stamps, and scan artifacts. The output is *supposed* to look cleaner than the source. |
| 4 | **Handwritten elements** | Handwritten text, manual signatures, and ink stamps become typed text or placeholder labels. |

### 1.2 What to actually check

- **Data accuracy** — every extracted field value matches the source **character by character**:
  names, numbers, dates, addresses.
- **Field completeness** — every data field present in the source is present in the output;
  nothing missing, nothing invented.
- **Structural match** — the logical structure (header, data fields, sections, footer) is
  preserved and fields appear in a sensible order.
- **Placeholder correctness** — placeholder boxes sit in roughly the right position at roughly
  the right size, and their labels match what they replace.

### 1.3 Severity guide

| Severity | Meaning |
|---|---|
| `minor` | Small inaccuracy that does not change meaning — spacing difference, slight placeholder offset. |
| `major` | A data value is wrong, a field is missing, or a placeholder is mislabeled. |
| `critical` | Multiple fields wrong or missing, or the document structure is fundamentally broken. |

### 1.4 Uncertainty

If the source image is too blurry to confirm a value: say so and set `needs_human_review`.
**Do not guess. Do not suggest fixes** (the verifier reports; the repairer proposes).

### 1.5 Report shape

`VerificationReport`:
- `overall_match`: `"pass" | "needs_review" | "fail"`
- `summary`: str
- `matches_well`: list[str]
- `discrepancies`: list[`Discrepancy`]
- `needs_human_review`: bool

`Discrepancy`:
- `category`: `"text" | "layout" | "table" | "image" | "missing_content" | "extra_content" | "reading_order" | "other"`
- `location`: str — where the issue appears, e.g. `"top-right logo"`
- `source_observation`: str
- `rendered_observation`: str
- `severity`: `"minor" | "major" | "critical"`
- `confidence`: float, 0–1

---

## 2. Repair Planning Rules

Source: `controller-old/layout_repairer.py`

Input to the planner: the verification report **plus** the current extraction schema.
Output: the minimum set of patches that fixes every `major` or `critical` discrepancy.

### 2.1 Allowed schema patch actions

| Action | Use |
|---|---|
| `add_field` | Add a field the schema does not yet capture. Requires `field_name`, `field_type` (usually `"string"`), and a `description` that tells the OCR model exactly what to look for and how to format the value. |
| `modify_field` | Improve an existing field's description so OCR extracts it more accurately. |

### 2.2 Allowed layout patch actions

| Action | Use |
|---|---|
| `add_header_field` | Add a labelled value to the header area. |
| `add_info_field` | Add a labelled value to the info/details panel. |
| `add_table_column` | Add a column to the main data table. |
| `add_section` | Add an entirely new section. |
| `modify_style` | Adjust spacing, font size, or alignment of an existing section. |
| `reorder` | Change the order of existing sections. |

Valid `target_section` values: `header`, `info_panel`, `table`, `footer`.

### 2.3 Rules

1. Use only the vocabularies above. **No raw HTML, CSS, Python, or free-form layout changes.**
2. Every schema patch carries a clear, detailed extraction description — where the value appears
   on the document and how to format it.
3. Set `needs_reextraction = true` whenever any schema field is added or modified.
4. Table issues where the schema already has the right fields but data is incomplete →
   `modify_field` with a better description, **not** new fields.
5. Keep patches minimal — fix only what the report flags.
6. Each layout patch sets `field_name` to the schema field it relates to, so downstream code
   knows which data to display.
7. Ignore `minor` discrepancies.

---

## 3. Design decisions carried forward

These are the load-bearing choices from the old controller. The agentic controller may change the
*mechanism* but should preserve the *intent*.

- **Constrained vocabulary over free-form code.** The old controller never let the LLM emit raw
  HTML/CSS/Python. If the new agent writes `layout_N.py` directly, that generation must be gated
  by a validation step before it lands on disk — the guarantee is "no unreviewed code path,"
  not "no code."
- **Schema-first.** A weak extraction is more often a bad field *description* than a missing
  field. Try improving the description before adding structure.
- **Re-extraction is triggered by schema change.** If the schema changed, OCR must be re-run with
  the patched schema before the document is rebuilt. The agent decides this automatically:
  schema touched → re-extract.
- **Originals are never mutated.** The old controller wrote `*_patched.json` sidecars. The new
  flow's `layout_1.py` / `schema_1.json` is the same idea. A **promotion rule is still open**:
  after user approval, either repoint `document_builder/registry.py` at the versioned file or
  copy it back over the canonical one and drop the version.
- **The verification report is the contract.** `matches_well`, `discrepancies`, and
  `needs_human_review` are the feedback signal the agent loops on.

---

## 4. Open questions

- **Promotion rule** — when and how does `layout_1.py` become `layout.py`?
- **contenteditable** — currently baked into hand-written templates; to be integrated into
  `html_engine` directly *after* the agentic controller lands.
- **`html_engine` is not final** — components may still be added. The agent's RAG context over
  `html_engine/` must be rebuildable, not a one-time snapshot.
