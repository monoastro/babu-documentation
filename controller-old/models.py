"""Pydantic models for the layout-repair pipeline.

These define the structured vocabulary the LLM may use to propose
changes.  Nothing here touches files or runs code — these are pure
data containers.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


# ── Schema-level patches ───────────────────────────────────────────

class SchemaPatch(BaseModel):
    """A single change to the extraction JSON schema."""

    action: Literal["add_field", "modify_field"]
    field_name: str = Field(
        description="Key name in the schema (e.g. 'property_identifier_no').",
    )
    field_type: str = Field(
        default="string",
        description="JSON Schema type for the field.",
    )
    description: str = Field(
        description=(
            "Extraction prompt that tells the OCR model what to look for "
            "and how to format the value."
        ),
    )
    required: bool = Field(
        default=True,
        description="Whether the field should be added to the 'required' list.",
    )


# ── Layout-level patches ──────────────────────────────────────────

class LayoutPatch(BaseModel):
    """A single structural change to the document layout builder."""

    action: Literal[
        "add_header_field",
        "add_info_field",
        "add_table_column",
        "add_section",
        "modify_style",
        "reorder",
    ]
    target_section: str = Field(
        description=(
            "Which part of the layout this patch targets "
            "(e.g. 'header', 'info_panel', 'table', 'footer')."
        ),
    )
    detail: str = Field(
        description="Human-readable description of the change.",
    )
    field_name: str = Field(
        default="",
        description="Schema field name this patch relates to, if any.",
    )


# ── Top-level repair plan ─────────────────────────────────────────

class RepairPlan(BaseModel):
    """The full proposal returned by the analysis LLM call."""

    summary: str = Field(
        description="One-paragraph explanation of what is wrong and what the plan fixes.",
    )
    schema_patches: list[SchemaPatch] = Field(
        default_factory=list,
        description="Ordered list of extraction-schema changes.",
    )
    layout_patches: list[LayoutPatch] = Field(
        default_factory=list,
        description="Ordered list of layout-builder changes.",
    )
    needs_reextraction: bool = Field(
        description=(
            "True when schema_patches added or changed fields, meaning the "
            "OCR must be re-run with the patched schema to get the new data."
        ),
    )
