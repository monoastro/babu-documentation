"""
CLI runner for the LangGraph document digitization pipeline.
python -m controller.run <image> [--document-type TYPE] [--max-iterations N]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from uuid import uuid4

from langgraph.types import Command

from controller.graph import compile_graph


SEP = "═" * 60

def _show_review(values: dict) -> None:
    report = values.get("report", {})
    iteration = values.get("iteration", 0)
    max_iter = values.get("max_iterations", 3)
    match = values.get("overall_match", "unknown")

    print()
    print(SEP)
    print(f"  ITERATION {iteration + 1}/{max_iter}  —  Verification: {match.upper()}")
    print(SEP)

    summary = report.get("summary", "")
    if summary:
        print(f"\nSummary: {summary}")

    matches = report.get("matches_well", [])
    if matches:
        print("\nMatches well:")
        for m in matches:
            print(f"    • {m}")

    discrepancies = report.get("discrepancies", [])
    if discrepancies:
        print(f"\nDiscrepancies ({len(discrepancies)}):")
        for d in discrepancies:
            sev = d.get("severity", "?")
            cat = d.get("category", "?")
            loc = d.get("location", "?")
            src = d.get("source_observation", "")
            rnd = d.get("rendered_observation", "")
            print(f"[{sev.upper()}] {cat} @ {loc}")
            if src:
                print(f"Source: {src[:100]}")
            if rnd:
                print(f"Rendered: {rnd[:100]}")
    else:
        print("\nNo discrepancies found.")

    html_path = values.get("html_path", "")
    png_path = values.get("png_path", "")
    if html_path:
        print(f"\nOutput HTML: {html_path}")
    if png_path:
        print(f"Output PNG:  {png_path}")

    needs_human = report.get("needs_human_review", False)
    if needs_human:
        print("\n The verifier flagged this for human review.")

    print()


def _collect_decision(at_limit: bool) -> dict:
    if at_limit:
        print("Maximum iterations reached.")
        print("You can only [a]pprove the current output.")
        print()

    while True:
        if at_limit:
            choices = "[a]pprove"
        else:
            choices = "[a]pprove / [r]etry / [e]dit"

        raw = input(f"Decision ({choices}): ").strip().lower()

        if raw in ("a", "approve"):
            return {"decision": "approve", "edits": {}}
        if at_limit:
            print("  → Only 'approve' is available at the iteration limit.")
            continue
        if raw in ("r", "retry"):
            return {"decision": "retry", "edits": {}}
        if raw in ("e", "edit"):
            edits = _collect_edits()
            return {"decision": "edit", "edits": edits}

        print(f"Unknown choice '{raw}'. Try again.")


def _collect_edits() -> dict[str, str]:
    print()
    print("Enter field edits (one per line).  Format:  field_name = new value")
    print("For plot fields use dotted paths:  plots.0.plot_no = 1433")
    print("Empty line to finish.")
    print()

    edits: dict[str, str] = {}
    while True:
        line = input(" > ").strip()
        if not line:
            break
        if "=" not in line:
            print("Expected 'field = value' format. Try again.")
            continue
        key, _, value = line.partition("=")
        edits[key.strip()] = value.strip()

    if edits:
        print(f"\n  Edits to apply: {json.dumps(edits, indent=4)}")
    return edits


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the document digitization pipeline with human-in-the-loop review.",
    )
    parser.add_argument(
        "image",
        type=Path,
        help="Path to the source document image (PNG).",
    )
    parser.add_argument(
        "--document-type",
        default="laalpurja",
        help="Document type (default: laalpurja).",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=3,
        help="Maximum repair iterations (default: 3).",
    )
    args = parser.parse_args()

    if not args.image.is_file():
        print(f"Error: Image not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    graph = compile_graph()
    thread_id = uuid4().hex
    config = {"configurable": {"thread_id": thread_id}}

    print(SEP)
    print(f"Document Digitization Pipeline")
    print(f"Image:    {args.image}")
    print(f"Type:     {args.document_type}")
    print(f"Max iter: {args.max_iterations}")
    print(f"Thread:   {thread_id[:12]}")
    print(SEP)

    print("\nStarting pipeline\n")
    initial_state = {
        "image_path": str(args.image.resolve()),
        "document_type": args.document_type,
        "iteration": 0,
        "max_iterations": args.max_iterations,
        "history": [],
        "data": {},
        "report": {},
        "repair_plan": {},
        "human_edits": {},
        "human_decision": "",
        "html_path": "",
        "png_path": "",
        "schema_path": "",
        "layout_exists": False,
        "overall_match": "",
    }

    result = graph.invoke(initial_state, config)

    while True:
        snapshot = graph.get_state(config)
        if not snapshot.next:
            break

        state_values = snapshot.values
        _show_review(state_values)

        iteration = state_values.get("iteration", 0)
        max_iter = state_values.get("max_iterations", 3)
        at_limit = iteration >= max_iter

        response = _collect_decision(at_limit)

        print(f"\n  → Resuming with decision: {response['decision']}")
        if response.get("edits"):
            print(f"    Edits: {json.dumps(response['edits'])}")
        print()

        result = graph.invoke(Command(resume=response), config)

    print()
    print(SEP)
    print(f"Pipeline complete.")
    print(SEP)
    final_html = result.get("html_path", "")
    final_png = result.get("png_path", "")
    if final_html:
        print(f"  HTML: {final_html}")
    if final_png:
        print(f"  PNG:  {final_png}")

    history = result.get("history", [])
    if history:
        print(f"\n  History ({len(history)} iterations):")
        for h in history:
            print(f"    [{h.get('iteration', '?')}] "
                  f"{h.get('overall_match', '?')} → {h.get('decision', '?')}")
    print()


if __name__ == "__main__":
    main()
