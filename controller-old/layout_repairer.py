"""Layout repair module

Stage 1 (analyze): feeds the verification report and current extraction
schema to an LLM, which returns a constrained ``RepairPlan`` — no free-form
code, only a fixed vocabulary of patch operations.

Stage 2 (repair): applies the plan — patches the schema, re-extracts data
from the source image, rebuilds the document with the updated data, and
saves the output.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from controller.models import RepairPlan
from controller.schema_patcher import apply_patches
from document_builder.registry import DOCUMENTS
from information_extraction.extractor import extract, build_data

# ── System prompt for Stage 1 ────────────────────────────────────────────

ANALYSIS_PROMPT = """\
You are a document-digitization repair planner.  You receive:

  1. A **verification report** — a JSON object produced by comparing a source
     document image with a digitally rendered replica.  It lists discrepancies
     between the two.
  2. The **current extraction schema** — the JSON Schema that was used to
     extract structured data from the source image via OCR.

Your job is to propose the minimum set of patches that will fix every
discrepancy marked "major" or "critical".  Ignore "minor" discrepancies.

─────────────────────────────────────────────────────────────────────────
ALLOWED SCHEMA PATCH ACTIONS

  • add_field     — Add a new field that the schema does not yet capture.
                    Provide field_name, field_type (usually "string"), and a
                    clear description that tells the OCR model exactly what
                    to look for and how to format the value.
  • modify_field  — Improve the description of an existing field so the OCR
                    extracts it more accurately.

ALLOWED LAYOUT PATCH ACTIONS

  • add_header_field   — Add a new labelled value to the header area.
  • add_info_field     — Add a new labelled value to the info/details panel.
  • add_table_column   — Add a new column to the main data table.
  • add_section        — Add an entirely new section to the document.
  • modify_style       — Adjust spacing, font size, or alignment of an
                         existing section.
  • reorder            — Change the order of existing sections.

─────────────────────────────────────────────────────────────────────────
RULES

  1. Only use actions from the vocabularies above.  Do NOT propose raw HTML,
     CSS, Python code, or free-form layout changes.
  2. For each schema patch, write a clear, detailed extraction description
     that tells the OCR model exactly where the value appears on the
     document and how to format it.
  3. Set needs_reextraction = true whenever you add or modify any schema
     fields.
  4. For table-related issues where the schema already has the right fields
     but data is incomplete, propose modify_field patches with improved
     descriptions that help the OCR extract more accurately.
  5. Keep patches minimal — only fix what the report flags.
  6. For each layout patch, set field_name to the schema field it relates
     to (if any), so the downstream code knows which data to display.

LAYOUT SECTIONS (use these as target_section values):
  header, info_panel, table, footer
"""



        """Send the verification report + schema to the LLM and get a RepairPlan.

    This stage does NOT use vision — only text.  It is fast and cheap.
    """
def analyze(
    report: dict,
    schema_path: Path,
) -> RepairPlan:
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing.  Copy .env.example to .env and add your key."
        )

    with open(schema_path, encoding="utf-8") as f:
        schema_text = f.read()

    planner = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        temperature=0,
    ).with_structured_output(RepairPlan)

    message = HumanMessage(content=json.dumps({
        "verification_report": report,
        "current_extraction_schema": json.loads(schema_text),
    }, indent=2, ensure_ascii=False))

    return planner.invoke([SystemMessage(ANALYSIS_PROMPT), message])



def repair(
    plan: RepairPlan,
    image_path: Path,
    document_type: str,
    *,
    output_dir: Path = Path("output"),
) -> Path:
    """Apply a RepairPlan: patch schema → re-extract → rebuild → save.

    Returns the path to the saved HTML file.
    """
    config = DOCUMENTS[document_type]
    schema_path: Path = config["schema"]
    builder = config["builder"]

    # 1. Patch the extraction schema (if there are schema patches)
    if plan.schema_patches:
        patched_schema = apply_patches(schema_path, plan.schema_patches)
        print(f"Patched schema written to {patched_schema}")
    else:
        patched_schema = schema_path

    # 2. Re-extract data from the source image with the (possibly patched) schema
    if plan.needs_reextraction:
        print(f"Re-extracting from {image_path} …")
        extracted, schema = extract(
            image_path=str(image_path),
            schema_path=str(patched_schema),
        )
        data = build_data(extracted, schema)
        print(f"Extraction complete — {len(data)} fields")
    else:
        # No re-extraction needed — load existing extracted data
        # (fall back to extracting with the original schema)
        extracted, schema = extract(
            image_path=str(image_path),
            schema_path=str(schema_path),
        )
        data = build_data(extracted, schema)

    # 3. Build the document using the existing builder
    doc = builder(data)

    # 4. Save output
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / f"{document_type}_repaired.html"
    doc.save(str(html_path))
    print(f"  ✓ Saved repaired HTML to {html_path}")

    # 5. Render to PNG (via html2image / headless Chromium)
    png_path = output_dir / f"{document_type}_repaired.png"
    try:
        from html2image import Html2Image
        hti = Html2Image(output_path=str(output_dir), disable_logging=True)
        hti.screenshot(
            url=str(html_path.absolute()),
            save_as=f"{document_type}_repaired.png",
            size=(1300, 1100),
        )
        print(f"Saved repaired PNG  to {png_path}")
    except Exception as exc:
        print(f"PNG render skipped: {exc}")

    return html_path



def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze a verification report and repair the document layout.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("controller/data/report-laalpurja.json"),
        help="Path to the verification report JSON.",
    )
    parser.add_argument(
        "--image",
        type=Path,
        default=Path("controller/data/input.png"),
        help="Path to the source document image.",
    )
    parser.add_argument(
        "--document-type",
        default="laalpurja",
        choices=list(DOCUMENTS.keys()),
        help="Document type to repair.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Directory for output files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print the RepairPlan without applying it.",
    )
    args = parser.parse_args()

    # Load the verification report
    report = json.loads(args.report.read_text(encoding="utf-8"))

    # Resolve schema path from the document registry
    config = DOCUMENTS[args.document_type]
    schema_path: Path = config["schema"]

    # Stage 1: Analyze
    print("═" * 60)
    print("Stage 1: Analyzing verification report …")
    print("═" * 60)
    plan = analyze(report, schema_path)

    print(f"\n  Summary: {plan.summary}")
    print(f"  Schema patches:  {len(plan.schema_patches)}")
    for sp in plan.schema_patches:
        print(f"    • {sp.action}: {sp.field_name} — {sp.description[:80]}")
    print(f"  Layout patches:  {len(plan.layout_patches)}")
    for lp in plan.layout_patches:
        print(f"    • {lp.action} → {lp.target_section}: {lp.detail[:80]}")
    print(f"  Needs re-extraction: {plan.needs_reextraction}")

    if args.dry_run:
        print("\n  [dry-run] Full plan JSON:")
        print(plan.model_dump_json(indent=2))
        return

    # Stage 2: Repair
    print()
    print("═" * 60)
    print("Stage 2: Applying repair plan …")
    print("═" * 60)
    output_path = repair(
        plan,
        args.image,
        args.document_type,
        output_dir=args.output_dir,
    )
    print()
    print(f"Done.  Output: {output_path}")


if __name__ == "__main__":
    main()
