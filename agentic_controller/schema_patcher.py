"""Apply SchemaPatch operations to a JSON extraction schema.

Salvaged from ``controller-old/schema_patcher.py``. The original schema file is
never overwritten — a patched copy is written next to it with a ``_patched``
suffix (e.g. ``laalpurja.json`` → ``laalpurja_patched.json``).

The Architect Agent will call this after proposing schema repairs. The patched
schema is then fed back to the OCR extraction step to re-extract data with the
improved field descriptions.
"""

from __future__ import annotations

import json
from pathlib import Path

from agentic_controller.models import SchemaPatch


def apply_patches(
    schema_path: Path,
    patches: list[SchemaPatch],
    *,
    output_path: Path | None = None,
) -> Path:
    """Read *schema_path*, apply *patches*, write the result.

    Parameters
    ----------
    schema_path:
        Path to the original JSON schema.
    patches:
        Ordered list of ``SchemaPatch`` operations.
    output_path:
        Where to write the patched schema. Defaults to
        ``<stem>_patched.json`` alongside the original.

    Returns
    -------
    Path to the written patched schema.
    """
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)

    properties: dict = schema.setdefault("properties", {})
    required: list = schema.setdefault("required", [])

    for patch in patches:
        if patch.action == "add_field":
            if patch.field_name in properties:
                # Already present — skip silently rather than erroring.
                # The agent may propose a field that was added in a prior
                # iteration but is still missing from the report it received.
                continue
            properties[patch.field_name] = {
                "type": patch.field_type,
                "description": patch.description,
            }
            if patch.required and patch.field_name not in required:
                required.append(patch.field_name)

        elif patch.action == "modify_field":
            if patch.field_name not in properties:
                # Cannot modify a nonexistent field — add it instead.
                properties[patch.field_name] = {
                    "type": patch.field_type,
                    "description": patch.description,
                }
            else:
                entry = properties[patch.field_name]
                if patch.description:
                    entry["description"] = patch.description
                if patch.field_type:
                    entry["type"] = patch.field_type

            if patch.required and patch.field_name not in required:
                required.append(patch.field_name)

    if output_path is None:
        output_path = schema_path.with_name(
            schema_path.stem + "_patched" + schema_path.suffix
        )

    output_path.write_text(
        json.dumps(schema, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output_path
