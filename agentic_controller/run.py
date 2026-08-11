"""
Integrated autonomous document digitization pipeline.
Flow:
  1. Check whether layout and schema exist for the document type.
  2. If absent: generate_resources() to create them from the source image.
  3. Run the pipeline: OCR → build → render PNG.
  4. Verify: compare source against rendered output.
  5. Single human checkpoint: show report, collect decision.
  6. User chooses: [a]pprove (done), [r]etry auto-fix, or [e]dit with concerns.
  7. Loop up to MAX_REPAIR_ITERATIONS (default 3).

Usage:
  python -m agentic_controller.run <image> --document-type laalpurja
  python -m agentic_controller.run <image> -t citizenship --max-iterations 5
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from uuid import uuid4

from agentic_controller.architect import (
    MAX_REPAIR_ITERATIONS,
    analyze_and_repair,
    current_layout_path,
    generate_resources,
    resolve_schema_path,
)
from agentic_controller.rendering import render_png
from agentic_controller.verifier import verify
from information_extraction.pipeline import build_document

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"

SEP = "═" * 70


def _show_report(report_dict: dict, iteration: int, max_iter: int) -> None:
    """Display verification report to the user."""
    print()
    print(SEP)
    summary = report_dict.get("summary", "")
    disc_count = len(report_dict.get("discrepancies", []))
    print(f"  ITERATION {iteration}/{max_iter}  —  {disc_count} discrepancy(ies)")
    if summary:
        print(f"  {summary}")
    print(SEP)

    matches = report_dict.get("matches_well", [])
    if matches:
        print("\nMatches well:")
        for m in matches[:5]:  # Show first 5
            print(f"    ✓ {m}")
        if len(matches) > 5:
            print(f"    ... and {len(matches) - 5} more")

    discrepancies = report_dict.get("discrepancies", [])
    if discrepancies:
        print(f"\nDiscrepancies ({len(discrepancies)}):")
        for d in discrepancies:
            sev = d.get("severity", "?").upper()
            cat = d.get("category", "?")
            loc = d.get("location", "?")
            src_obs = d.get("source_observation", "")
            rnd_obs = d.get("rendered_observation", "")

            marker = "⚠" if sev == "MINOR" else "✗"
            print(f"\n{marker} [{sev}] {cat} @ {loc}")
            if src_obs:
                print(f"   Source:   {src_obs[:80]}")
            if rnd_obs:
                print(f"   Rendered: {rnd_obs[:80]}")
    else:
        print("\n✓ No discrepancies found.")

    needs_human = report_dict.get("needs_human_review", False)
    if needs_human:
        print("\n⚠ The verifier flagged this for human review.")

    print()


def _collect_decision(iteration: int, max_iter: int, blocking_count: int) -> str:
    """Prompt the user for their decision at the checkpoint.

    Returns "approve", "retry", or "edit".
    """
    at_limit = iteration >= max_iter

    if at_limit:
        print("Maximum iterations reached.")
        print("You can only [a]pprove the current output.")
        print()

    while True:
        if at_limit:
            choices = "[a]pprove"
        elif blocking_count == 0:
            choices = "[a]pprove (no blocking issues) / [r]etry anyway / [e]dit with concerns"
        else:
            choices = "[a]pprove anyway / [r]etry auto-fix / [e]dit with concerns"

        raw = input(f"Decision ({choices}): ").strip().lower()

        if raw in ("a", "approve"):
            return "approve"
        if at_limit:
            print("  → Only 'approve' is available at the iteration limit.")
            continue
        if raw in ("r", "retry"):
            return "retry"
        if raw in ("e", "edit"):
            return "edit"

        print(f"Unknown choice '{raw}'. Try again.")


def _collect_user_concerns() -> str:
    """Collect free-form user concerns for the user-guided repair branch."""
    print()
    print("Describe what needs fixing (free-form text).")
    print("The agent will use this guidance when generating the repair.")
    print("Empty line to finish.")
    print()

    lines = []
    while True:
        line = input(" > ").strip()
        if not line:
            break
        lines.append(line)

    concerns = "\n".join(lines)
    if concerns:
        print(f"\n  User concerns: {concerns[:100]}...")
    return concerns


def _resources_exist(document_type: str) -> tuple[bool, str]:
    """Check whether a usable schema and layout already exist.

    Returns ``(exists, description)``. The description explains what was found
    or what is missing, for display to the user.
    """
    missing = []

    try:
        schema_path = resolve_schema_path(document_type)
        has_schema = schema_path.is_file()
    except Exception:
        schema_path = None
        has_schema = False
    if not has_schema:
        missing.append("schema")

    layout_path = current_layout_path(document_type)
    if layout_path is None or not layout_path.is_file():
        missing.append("layout")

    if missing:
        return False, f"missing: {', '.join(missing)}"

    return True, f"schema={schema_path.name}, layout={layout_path.name}"


def run_pipeline(
    document_type: str,
    image_path: Path,
    output_dir: Path,
    tag: str,
    translate: bool = True,
) -> tuple[Path | None, Path | None]:
    """OCR → translate → build → save HTML → render PNG.

    Returns ``(html_path, png_path)``. Either may be ``None`` if that stage
    failed; a missing PNG degrades verification but does not stop the run.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / f"{document_type}-{tag}.html"

    print(f"  → Extracting and building ({document_type})...")
    try:
        doc = build_document(document_type, str(image_path), translate=translate)
        doc.save(str(html_path))
    except Exception as exc:
        print(f"Pipeline failed: {exc}")
        return None, None
    print(f"HTML: {html_path}")

    png_name = f"{document_type}-{tag}.png"
    print(f"  → Rendering PNG...")
    if render_png(html_path, output_dir, png_name):
        png_path = output_dir / png_name
        print(f"  ✓ PNG:  {png_path}")
        return html_path, png_path

    print("  ⚠ PNG render skipped — verification will be unavailable.")
    return html_path, None


def digitize(
    image_path: Path,
    document_type: str,
    *,
    max_iterations: int = MAX_REPAIR_ITERATIONS,
    output_dir: Path = OUTPUT_DIR,
    auto_approve: bool = False,
    translate: bool = True,
) -> dict:
    """Run the full autonomous digitization flow.

    Returns a result dict with the final artifacts and the append-only history.
    """
    run_id = uuid4().hex[:8]
    history: list[dict] = []

    print(SEP)
    print("  AUTONOMOUS DOCUMENT DIGITIZATION")
    print(SEP)
    print(f"  Image:    {image_path}")
    print(f"  Type:     {document_type}")
    print(f"  Max iter: {max_iterations}")
    print(f"  Run:      {run_id}")
    print(SEP)

    # ---- Stage 0: do the resources exist? -----------------------------------
    exists, description = _resources_exist(document_type)
    print(f"\nResources: {description}")

    if not exists:
        print(f"\n{SEP}")
        print("  GENERATING RESOURCES (unseen document type)")
        print(SEP)
        print("  The agent will analyze the source image and write both a")
        print("  schema and a layout from scratch. This may take a minute.\n")

        try:
            gen = generate_resources(image_path, document_type)
        except Exception as exc:
            print(f"\n✗ Resource generation failed: {exc}", file=sys.stderr)
            return {"status": "generation_failed", "error": str(exc), "history": history}

        print(f"\n{gen.describe()}")
        history.append(
            {
                "iteration": 0,
                "action": "generate_resources",
                "summary": gen.summary,
                "schema": str(gen.schema_path) if gen.schema_path else None,
                "layout": str(gen.layout_path) if gen.layout_path else None,
            }
        )

        if gen.layout_path is None and gen.schema_path is None:
            print("\n✗ The agent produced no usable resources. Stopping.", file=sys.stderr)
            return {"status": "generation_empty", "history": history}

        if gen.layout_valid is False:
            # The gate already built this layout and it raised. Registering it
            # would only move the same traceback from here to the next run's
            # build stage, where it reads as a pipeline bug rather than a
            # generation one.
            print(f"\n✗ The generated layout does not build:", file=sys.stderr)
            print(f"    {gen.validation_message}", file=sys.stderr)
            print(f"\n  Layout kept for inspection: {gen.layout_path}", file=sys.stderr)
            print("  Do not register it until it builds — re-run to regenerate,")
            print("  or fix the layout by hand and verify with:")
            print(f"    python main.py --type {document_type} --blank")
            return {
                "status": "generated_invalid_layout",
                "error": gen.validation_message,
                "schema_path": str(gen.schema_path) if gen.schema_path else None,
                "layout_path": str(gen.layout_path) if gen.layout_path else None,
                "history": history,
            }

        print("\n✓ Generated resources are live:")
        if gen.layout_path:
            print(f"    layout: {gen.layout_path}"
                  f"{'  (ACTIVE)' if gen.promoted else ''}")
        if gen.schema_path:
            print(f"    schema: {gen.schema_path}")

        # The registry discovers types from the filesystem, so a generated type
        # is usually usable immediately. It can still be undiscoverable: a
        # layout with no schema beside it is not a document type, because
        # extraction has nothing to extract with.
        try:
            from document_builder.registry import DOCUMENTS

            if document_type not in DOCUMENTS:
                print(f"\n✗ The registry cannot see '{document_type}'.", file=sys.stderr)
                print("  A type needs both a layout and a schema; one is missing:",
                      file=sys.stderr)
                print(f"    layout: {gen.layout_path or '(none written)'}", file=sys.stderr)
                print(f"    schema: {gen.schema_path or '(none written)'}", file=sys.stderr)
                return {
                    "status": "generated_not_discoverable",
                    "schema_path": str(gen.schema_path) if gen.schema_path else None,
                    "layout_path": str(gen.layout_path) if gen.layout_path else None,
                    "history": history,
                }
        except Exception:
            pass

    # ---- Stage 1..N: pipeline → verify → checkpoint → repair ----------------
    iteration = 1
    final_html: Path | None = None
    final_png: Path | None = None

    while iteration <= max_iterations:
        print(f"\n{SEP}")
        print(f"  PIPELINE RUN {iteration}/{max_iterations}")
        print(SEP)

        html_path, png_path = run_pipeline(
            document_type, image_path, output_dir, tag=f"{run_id}-{iteration}",
            translate=translate,
        )
        if html_path is None:
            return {"status": "pipeline_failed", "iteration": iteration, "history": history}

        final_html, final_png = html_path, png_path

        if png_path is None:
            print("\n⚠ Cannot verify without a rendered PNG.")
            print("  Install chromium or set CHROME_EXECUTABLE, then re-run.")
            return {
                "status": "unverified",
                "html_path": str(html_path),
                "iteration": iteration,
                "history": history,
            }

        # ---- Verify ----
        print("\n  → Verifying against source...")
        try:
            report = verify(image_path, png_path)
        except Exception as exc:
            print(f"  ✗ Verification failed: {exc}", file=sys.stderr)
            return {
                "status": "verification_failed",
                "error": str(exc),
                "html_path": str(html_path),
                "png_path": str(png_path),
                "iteration": iteration,
                "history": history,
            }

        report_dict = report.model_dump()
        blocking = report.blocking()

        report_path = output_dir / f"report-{document_type}-{run_id}-{iteration}.json"
        report_path.write_text(
            json.dumps(report_dict, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        _show_report(report_dict, iteration, max_iterations)
        print(f"Blocking issues (major/critical): {len(blocking)}")
        print(f"Report saved: {report_path}")

        history.append(
            {
                "iteration": iteration,
                "action": "verify",
                "discrepancies": len(report_dict.get("discrepancies", [])),
                "blocking": len(blocking),
                "html": str(html_path),
                "png": str(png_path),
                "report": str(report_path),
            }
        )

        # ---- The single human checkpoint ----
        if auto_approve:
            if not blocking:
                print("\n[auto-approve] No blocking issues — accepting output.")
                decision = "approve"
            elif iteration >= max_iterations:
                print("\n[auto-approve] Iteration limit reached — accepting output.")
                decision = "approve"
            else:
                print(f"\n[auto-approve] {len(blocking)} blocking issue(s) — running auto-fix.")
                decision = "retry"
        else:
            print("\nReview the rendered output:")
            print(f"  {png_path}")
            decision = _collect_decision(iteration, max_iterations, len(blocking))

        if decision == "approve":
            history.append({"iteration": iteration, "action": "approve"})
            print("\n✓ Output approved.")
            break

        user_concerns = _collect_user_concerns() if decision == "edit" else None
        if decision == "edit" and not user_concerns:
            print("  No concerns entered — falling back to autonomous repair.")

        # ---- Repair ----
        print(f"\n{SEP}")
        print(f"  ARCHITECT REPAIR (iteration {iteration})")
        print(SEP)

        try:
            schema_path = resolve_schema_path(document_type)
        except Exception as exc:
            print(f"✗ Cannot resolve schema: {exc}", file=sys.stderr)
            return {"status": "schema_unresolved", "error": str(exc), "history": history}

        try:
            repair = analyze_and_repair(
                report=report,
                source_image=image_path,
                document_type=document_type,
                current_schema_path=schema_path,
                current_layout_path=current_layout_path(document_type),
                rendered_image=png_path,
                user_concerns=user_concerns,
                iteration=iteration,
            )
        except Exception as exc:
            print(f"\n✗ Repair failed: {exc}", file=sys.stderr)
            return {
                "status": "repair_failed",
                "error": str(exc),
                "iteration": iteration,
                "html_path": str(html_path),
                "png_path": str(png_path),
                "history": history,
            }

        print(f"\n{repair.describe()}")
        history.append(
            {
                "iteration": iteration,
                "action": "repair",
                "mode": "user_guided" if user_concerns else "autonomous",
                "summary": repair.summary,
                "needs_reextraction": repair.needs_reextraction,
                "schema": str(repair.schema_path) if repair.schema_path else None,
                "layout": str(repair.layout_path) if repair.layout_path else None,
                "promoted": str(repair.promoted) if repair.promoted else None,
            }
        )
        history.extend(repair.history)

        if repair.schema_path is None and repair.layout_path is None:
            print("\n⚠ The agent changed nothing. Stopping to avoid a no-op loop.")
            break

        if repair.layout_path is not None:
            if repair.promoted:
                print(f"\n✓ Promoted: {repair.layout_path.name} is now the live layout.")
                print("  The next iteration builds from it. Roll back by editing")
                print(f"  {repair.promoted} — layout.py is untouched.")
            else:
                print(f"\n⚠ New layout written but NOT promoted: {repair.layout_path.name}")
                print(f"  It does not build: {repair.validation_message}")
                print("  The previous layout stays live, so the next iteration is")
                print("  unaffected. Kept for inspection.")

        iteration += 1

    # ---- Done ----
    print(f"\n{SEP}")
    print("  RUN COMPLETE")
    print(SEP)
    if final_html:
        print(f"  HTML: {final_html}")
    if final_png:
        print(f"  PNG:  {final_png}")

    print(f"\n  History ({len(history)} entries):")
    for h in history:
        it = h.get("iteration", "?")
        action = h.get("action", "?")
        extra = ""
        if action == "verify":
            extra = f" — {h.get('discrepancies', 0)} disc, {h.get('blocking', 0)} blocking"
        elif action == "repair":
            extra = f" — {h.get('mode', '')}"
        print(f"    [{it}] {action}{extra}")
    print()

    return {
        "status": "complete",
        "html_path": str(final_html) if final_html else None,
        "png_path": str(final_png) if final_png else None,
        "iterations": iteration,
        "history": history,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Autonomous document digitization with a single human checkpoint.",
    )
    parser.add_argument("image", type=Path, help="Source document image (PNG).")
    parser.add_argument(
        "-t",
        "--document-type",
        default="laalpurja",
        help="Document type (default: laalpurja).",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=MAX_REPAIR_ITERATIONS,
        help=f"Maximum repair iterations (default: {MAX_REPAIR_ITERATIONS}).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Directory for HTML, PNG, and report artifacts.",
    )
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Run without prompting: auto-fix while blocking issues remain, "
        "then accept. Use for unattended runs.",
    )
    parser.add_argument(
        "--no-translate",
        dest="translate",
        action="store_false",
        help="Keep extracted values in their original script instead of "
        "translating them into English.",
    )
    parser.add_argument(
        "--result-json",
        type=Path,
        help="Optional path to write the run result (including history) as JSON.",
    )
    args = parser.parse_args()

    if not args.image.is_file():
        print(f"Error: Image not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    if args.max_iterations < 1:
        print("Error: --max-iterations must be at least 1.", file=sys.stderr)
        sys.exit(1)

    result = digitize(
        args.image.resolve(),
        args.document_type,
        max_iterations=args.max_iterations,
        output_dir=args.output_dir,
        auto_approve=args.auto_approve,
        translate=args.translate,
    )

    if args.result_json:
        args.result_json.parent.mkdir(parents=True, exist_ok=True)
        args.result_json.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"Result written to {args.result_json}")

    sys.exit(0 if result.get("status") == "complete" else 2)


if __name__ == "__main__":
    main()
