"""agentic_controller — autonomous layout & schema generation for document digitization.

Replaces the rigid LangGraph state machine in ``controller-old/`` with a single
Architect Agent loop backed by a RAG index over the codebase.

Phase 1: the knowledge base — ``rag_engine``.
Phase 2: ``architect`` — the tool-calling agent that reads a
    ``VerificationReport`` plus both document images and writes ``layout_N.py`` /
    ``<doc>_patched.json``. Also generates both from scratch for an unseen
    document type.
Phase 3: ``run`` — the integrated CLI pipeline.

Everything worth keeping from ``controller-old/`` has been carried across; see
``SALVAGE.md`` for the file-by-file provenance. ``controller-old/`` is deprecated
and will be deleted once Phase 3 lands.
"""

from __future__ import annotations

__all__ = ["architect", "models", "rag_engine", "rendering", "schema_patcher", "verifier"]
