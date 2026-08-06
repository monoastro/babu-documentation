"""Pydantic models — the structured vocabulary the agent may use.

Consolidates the model definitions that were split across
``controller-old/models.py`` (patch vocabulary) and
``controller-old/document_verifier.py`` (report shape). Nothing here touches
files or runs code — these are pure data containers.

The patch vocabulary is deliberately constrained: the agent proposes named
operations, not raw HTML/CSS/Python. See ``documentation/verification-rules.md``
§2 for the rules that govern their use, and §3 for why the constraint exists.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


# ── Verification

class Discrepancy(BaseModel):
    """A single visible difference between the source and the rendered output."""

    category: Literal[
        "text", "layout", "table", "image", "missing_content", "extra_content",
        "reading_order", "other",
    ]
    location: str = Field(description="Where the issue appears, such as 'top-right logo'.")
    source_observation: str
    rendered_observation: str
    severity: Literal["minor", "major", "critical"]
    confidence: float = Field(ge=0, le=1)


class VerificationReport(BaseModel):
    """Machine-readable result returned by the vision model.

    This is the contract the Architect Agent loops on: its job is to drive
    ``overall_match`` to ``"pass"``.
    """

    overall_match: Literal["pass", "needs_review", "fail"]
    summary: str
    matches_well: list[str]
    discrepancies: list[Discrepancy]
    needs_human_review: bool

    def blocking(self) -> list[Discrepancy]:
        """Discrepancies the agent must fix — ``major`` and ``critical`` only.

        ``minor`` findings are explicitly out of scope (verification-rules §2.3
        rule 7); repairing them tends to churn the layout without improving the
        match.
        """
        return [d for d in self.discrepancies if d.severity in ("major", "critical")]


# ── Schema-level patches ──────────────────────────────────────────

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
    target_section: Literal["header", "info_panel", "table", "footer"] = Field(
        description="Which part of the layout this patch targets.",
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
    """The full proposal returned by the analysis step."""

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
