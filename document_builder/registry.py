"""The document registry: which types exist, and how to build each one.

``DOCUMENTS`` reads like a plain dict::

    DOCUMENTS[document_type]["builder"](data)   -> Document
    DOCUMENTS[document_type]["schema"]          -> Path
    sorted(DOCUMENTS)                           -> ["citizenship", ...]

Nothing is resolved until it is asked for and nothing is hard-coded: ``ACTIVE``
names the live layout per type, and discovery finds any directory with both a
layout and a schema. See ``resolver.py``, and DESIGN-NOTES.md for the rationale.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any, Iterator

from document_builder.resolver import (
    active_layout_path,
    discover_document_types,
    load_builder,
    resolve_schema_path,
)


class _DocumentEntry(Mapping):
    """One document type's ``{"builder": ..., "schema": ...}``.

    ``schema`` and ``layout`` are path lookups; only ``builder`` imports the
    active layout, so iterating the registry imports nothing.
    """

    _KEYS = ("builder", "schema", "layout")

    def __init__(self, document_type: str):
        self.document_type = document_type

    def __getitem__(self, key: str) -> Any:
        if key == "schema":
            return resolve_schema_path(self.document_type)
        if key == "layout":
            return active_layout_path(self.document_type)
        if key == "builder":
            return load_builder(self.document_type)
        raise KeyError(key)

    def __iter__(self) -> Iterator[str]:
        return iter(self._KEYS)

    def __len__(self) -> int:
        return len(self._KEYS)

    def __repr__(self) -> str:
        layout = active_layout_path(self.document_type)
        return (f"<{self.document_type}: layout={layout.name if layout else 'none'}, "
                f"schema={resolve_schema_path(self.document_type).name}>")


class _Registry(Mapping):
    """Document types discovered from the filesystem, resolved on access.

    Deliberately not cached: a newly written type or a freshly promoted layout
    is visible immediately, including to the process that wrote it.
    """

    def __getitem__(self, document_type: str) -> _DocumentEntry:
        if document_type not in discover_document_types():
            raise KeyError(document_type)
        return _DocumentEntry(document_type)

    def __iter__(self) -> Iterator[str]:
        return iter(discover_document_types())

    def __len__(self) -> int:
        return len(discover_document_types())

    def __repr__(self) -> str:
        return f"<DOCUMENTS: {', '.join(discover_document_types()) or 'empty'}>"


DOCUMENTS = _Registry()

__all__ = ["DOCUMENTS"]
