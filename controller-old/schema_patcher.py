"""Apply SchemaPatch operations to a JSON extraction schema.

The original schema file is never overwritten.  A patched copy is
written next to it with a ``_patched`` suffix (e.g.
``laalpurja.json`` → ``laalpurja_patched.json``).
"""

from __future__ import annotations

import json
from pathlib import Path

from controller.models import SchemaPatch


"""Read *schema_path*, apply *patches*, write the result.

Parameters
----------
schema_path:
    Path to the original JSON schema.
patches:
    Ordered list of ``SchemaPatch`` operations.
output_path:
    Where to write the patched schema.  Defaults to
    ``<stem>_patched.json`` alongside the original.

Returns
-------
Path to the written patched schema.
"""
def apply_patches(
    schema_path: Path,
    patches: list[SchemaPatch],
    *,
    output_path: Path | None = None,
) -> Path:
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)

    properties: dict = schema.setdefault("properties", {})
    required: list = schema.setdefault("required", [])

    for patch in patches:
        if patch.action == "add_field":
            if patch.field_name in properties:
                continue  # already present — skip silently
            properties[patch.field_name] = {
                "type": patch.field_type,
                "description": patch.description,
            }
            if patch.required and patch.field_name not in required:
                required.append(patch.field_name)

        elif patch.action == "modify_field":
            if patch.field_name not in properties:
                # Cannot modify a field that doesn't exist — add it instead
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
