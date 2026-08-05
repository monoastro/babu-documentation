""" wiring stuff together from the existing pipeline stages:

    check_resources → extract → build → verify → [human review]
                                                   ├─ approve → END
                                                   ├─ retry   → analyze → repair → build …
                                                   └─ edit    → apply edits → build …

iteration is recorded in state["history"] for full traceability.
"""

from __future__ import annotations

import json
from operator import add
from pathlib import Path
from typing import Annotated, Any, Literal, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from controller.document_verifier import verify as verify_document
from controller.layout_repairer import analyze as analyze_report, repair as apply_repair_plan
from controller.models import RepairPlan
from controller.png_renderer import render_png
from document_builder.registry import DOCUMENTS
from information_extraction.extractor import extract, build_data


class PipelineState(TypedDict):
    image_path: str
    document_type: str
    schema_path: str
    layout_exists: bool
    data: dict
    html_path: str
    png_path: str
    report: dict
    overall_match: str          # "pass" | "needs_review" | "fail"
    repair_plan: dict
    iteration: int
    max_iterations: int
    history: Annotated[list[dict], add]
    human_decision: str         # "approve" | "retry" | "edit"
    human_edits: dict           # field_name → new_value



#first check whether a layout and extraction schema exist
def check_resources(state: PipelineState) -> dict:
    doc_type = state["document_type"]
    if doc_type in DOCUMENTS:
        config = DOCUMENTS[doc_type]
        return { "layout_exists": True, "schema_path": str(config["schema"]), }
    return {"layout_exists": False, "schema_path": ""}


def generate_resources(state: PipelineState) -> dict:
    """Placeholder — auto-generate layout + schema for an unknown doc type.

    Not implemented in v1. Only pre-registered document types are supported.
    """
    raise NotImplementedError(
        f"Document type '{state['document_type']}' is not registered. "
        f"Available types: {', '.join(DOCUMENTS.keys())}. "
        "Auto-generation of layout + schema from images is planned for v2."
    )

def extract_data(state: PipelineState) -> dict:
    extracted, schema = extract( image_path=state["image_path"], schema_path=state["schema_path"],)
    data = build_data(extracted, schema)
    return {"data": data}


def build_document(state: PipelineState) -> dict:
    doc_type = state["document_type"]
    config = DOCUMENTS[doc_type]
    builder = config["builder"]
    data = state["data"]

    doc = builder(data)
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / f"{doc_type}.html"
    doc.save(str(html_path))

    png_path = output_dir / f"{doc_type}.png"
    try:
        from html2image import Html2Image
        hti = Html2Image(output_path=str(output_dir), disable_logging=True)
        hti.screenshot(
            url=str(html_path.absolute()),
            save_as=f"{doc_type}.png",
            size=(1300, 1100),
        )
    except Exception as exc:
        print(f"  ⚠ PNG render skipped: {exc}")

    return {"html_path": str(html_path), "png_path": str(png_path)}


def verify(state: PipelineState) -> dict:
    source = Path(state["image_path"])
    rendered = Path(state["png_path"])

    if not rendered.is_file():
        return {
            "report": {"summary": "PNG not available — skipping verification"},
            "overall_match": "needs_review",
        }

    report = verify_document(source, rendered)
    report_dict = report.model_dump()
    return { "report": report_dict,
        "overall_match": report_dict["overall_match"],
    }


"""Pause for human review via LangGraph interrupt().
Presents the verification report and output paths. The human responds
with a decision dict: ``{"decision": "approve"|"retry"|"edit", "edits": {...}}``.
"""
def human_review(state: PipelineState) -> dict:
    iteration = state.get("iteration", 0)
    max_iter = state.get("max_iterations", 3)
    at_limit = iteration >= max_iter

    review_payload = {
        "iteration": iteration,
        "max_iterations": max_iter,
        "at_limit": at_limit,
        "overall_match": state.get("overall_match", "unknown"),
        "report_summary": state.get("report", {}).get("summary", ""),
        "discrepancies": state.get("report", {}).get("discrepancies", []),
        "html_path": state.get("html_path", ""),
        "png_path": state.get("png_path", ""),
    }

    # Pause execution
    response = interrupt(review_payload)

    decision = response.get("decision", "approve") if isinstance(response, dict) else str(response)
    edits = response.get("edits", {}) if isinstance(response, dict) else {}

    # Record this iteration in history
    history_entry = {
        "iteration": iteration,
        "overall_match": state.get("overall_match"),
        "decision": decision,
        "report_summary": state.get("report", {}).get("summary", ""),
    }

    return {
        "human_decision": decision,
        "human_edits": edits,
        "history": [history_entry],
    }


def analyze_repair(state: PipelineState) -> dict:
    schema_path = Path(state["schema_path"])
    report = state["report"]
    plan = analyze_report(report, schema_path)
    return {"repair_plan": plan.model_dump()}


def apply_repair(state: PipelineState) -> dict:
    plan_dict = state["repair_plan"]
    plan = RepairPlan(**plan_dict)
    image_path = Path(state["image_path"])
    doc_type = state["document_type"]

    output_path = apply_repair_plan(plan, image_path, doc_type)

    config = DOCUMENTS[doc_type]
    patched_schema = Path(state["schema_path"])
    patched_candidate = patched_schema.with_name(
        patched_schema.stem + "_patched" + patched_schema.suffix
    )
    if patched_candidate.is_file():
        active_schema = patched_candidate
    else:
        active_schema = patched_schema

    extracted, schema = extract(
        image_path=state["image_path"],
        schema_path=str(active_schema),
    )
    data = build_data(extracted, schema)

    return {
        "data": data,
        "schema_path": str(active_schema),
        "html_path": str(output_path),
        "iteration": state.get("iteration", 0) + 1,
    }

def apply_edits(state: PipelineState) -> dict:
    data = dict(state.get("data", {}))
    edits = state.get("human_edits", {})

    for field_path, new_value in edits.items():
        parts = field_path.split(".")
        target = data
        for part in parts[:-1]:
            if part.isdigit():
                target = target[int(part)]
            else:
                target = target[part]
        final_key = parts[-1]
        if final_key.isdigit():
            target[int(final_key)] = new_value
        else:
            target[final_key] = new_value

    return {
        "data": data,
        "iteration": state.get("iteration", 0) + 1,
    }


def route_after_check(state: PipelineState) -> str:
    """Route based on whether resources exist."""
    if state.get("layout_exists"):
        return "extract_data"
    return "generate_resources"


def route_after_review(state: PipelineState) -> str:
    """Route based on human decision + iteration limit."""
    decision = state.get("human_decision", "approve")
    iteration = state.get("iteration", 0)
    max_iter = state.get("max_iterations", 3)

    if decision == "approve":
        return END
    if iteration >= max_iter:
        # Forced stop — too many iterations
        return END
    if decision == "retry":
        return "analyze_repair"
    if decision == "edit":
        return "apply_edits"
    # Unknown decision — default to end
    return END



def build_graph() -> StateGraph:
    """Assemble and compile the document digitization pipeline graph."""
    builder = StateGraph(PipelineState)

    # Register nodes
    builder.add_node("check_resources", check_resources)
    builder.add_node("generate_resources", generate_resources)
    builder.add_node("extract_data", extract_data)
    builder.add_node("build_document", build_document)
    builder.add_node("verify", verify)
    builder.add_node("human_review", human_review)
    builder.add_node("analyze_repair", analyze_repair)
    builder.add_node("apply_repair", apply_repair)
    builder.add_node("apply_edits", apply_edits)

    # Edges
    builder.add_edge(START, "check_resources")
    builder.add_conditional_edges(
        "check_resources",
        route_after_check,
        ["extract_data", "generate_resources"],
    )
    builder.add_edge("generate_resources", "extract_data")
    builder.add_edge("extract_data", "build_document")
    builder.add_edge("build_document", "verify")
    builder.add_edge("verify", "human_review")
    builder.add_conditional_edges(
        "human_review",
        route_after_review,
        ["analyze_repair", "apply_edits", END],
    )
    builder.add_edge("analyze_repair", "apply_repair")
    builder.add_edge("apply_repair", "build_document")
    builder.add_edge("apply_edits", "build_document")

    return builder


def compile_graph(checkpointer=None):
    """Build and compile the graph with an optional checkpointer."""
    if checkpointer is None:
        checkpointer = MemorySaver()
    builder = build_graph()
    return builder.compile(checkpointer=checkpointer)
