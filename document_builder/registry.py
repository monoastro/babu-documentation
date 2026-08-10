"""
The document registry: which types exist, and how to build each one.

``DOCUMENTS`` still looks and reads like the dict it replaced::

    DOCUMENTS[document_type]["builder"](data)   -> Document
    DOCUMENTS[document_type]["schema"]          -> Path
    sorted(DOCUMENTS)                           -> ["citizenship", ...]

but nothing is resolved until it is asked for, and nothing is hard-coded. The
previous version was four top-level ``from ... import build_x`` statements, which
had two costs:

*Promotion was a manual edit.* The architect writes ``layout_2.py``; a human then
had to repoint the import. Miss it and the repair loop rebuilds from the old
layout forever — the agent's own fixes were invisible to it. Get it wrong and the
import dangles: one bad line took down all four types at once, because a
top-level import failure makes the whole module unimportable.

*A new document type needed a code edit* before it could be built at all, even
though its layout and schema were already sitting on disk.

Both are now filesystem questions, answered in ``resolver.py``. ``ACTIVE`` names
the live layout per type; discovery finds any directory with a layout and a
schema. Resolution is per-entry and lazy, so a layout that fails to import breaks
only its own type — the other three still build.
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

    ``schema`` is a path lookup; ``builder`` imports the active layout. Keeping
    them separate matters: iterating the registry to read schemas must not
    import every layout in the project, or one broken layout would again take
    the whole registry with it.
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

    Not cached. A generation run that writes a new type, or a repair that
    promotes a new layout, is visible immediately — including to the process
    that performed it, which is what lets the repair loop iterate on its own
    output instead of rebuilding the layout it started from.
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
