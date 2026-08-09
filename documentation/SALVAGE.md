# Salvage record: `controller-old/` → `agentic_controller/`

`controller-old/` is deprecated and will be deleted once Phase 3 lands. This file
records what was carried across, what was deliberately dropped, and why — so the
deletion is safe and reviewable.

Status: **Phase 1 complete.** Phases 2–3 pending.

---

## Carried across

| Old file | New home | Notes |
|---|---|---|
| `models.py` | `models.py` | `SchemaPatch`, `LayoutPatch`, `RepairPlan` kept as-is. `LayoutPatch.target_section` was a free-form `str` whose valid values lived only in a prompt; it is now a `Literal["header","info_panel","table","footer"]` so an invalid section fails at parse time. |
| `document_verifier.py` (`SYSTEM_PROMPT`) | `verifier.py` | **The single most valuable artifact in the old controller.** Defines what a "matched" document means: which transformations are intended (English labels over Devanagari values, placeholder boxes for seals/photos/signatures) and which are real defects. Copied verbatim. Mirrored in prose in `documentation/verification-rules.md`. |
| `document_verifier.py` (`Discrepancy`, `VerificationReport`) | `models.py` | Moved next to the patch models — they are all one vocabulary. Added `VerificationReport.blocking()`, which returns only `major`/`critical` findings; every call site previously re-implemented that filter from a prompt instruction. |
| `document_verifier.py` (`png_data_url`, `verify`) | `verifier.py` | Unchanged, except `OPENAI_MODEL` now has a `gpt-4.1-mini` default instead of passing `None` to `ChatOpenAI` when the env var is unset. |
| `png_renderer.py` | `rendering.py` | Consolidated. PNG rendering existed in **three** places (`graph.build_document`, `layout_repairer.repair`, `png_renderer.render_png`) with three different error paths and **two different viewport sizes** — `(1300, 1100)` in the graph, `(1500, 1500)` in the renderer's own test. Differently-cropped PNGs between the base and repaired render are a real source of phantom "layout" discrepancies. One implementation, one `DEFAULT_SIZE`. Also now returns `False` on `ImportError` and verifies the file actually landed. |
| `schema_patcher.py` | `schema_patcher.py` | Logic unchanged, import retargeted. The `*_patched.json` sidecar convention (never mutate the original) is preserved — it is the ancestor of the `layout_N.py` / `schema_N.json` scheme. |
| `layout_repairer.py` (`ANALYSIS_PROMPT`) | `documentation/verification-rules.md` §2 | The patch vocabulary and its rules are now prose in the shared reference rather than a Python string constant, because the Phase 2 agent consumes them as retrieved context, not as a system prompt to a single-shot call. |

## Deliberately dropped

| Old file | Why |
|---|---|
| `graph.py` | The LangGraph `StateGraph` is the thing being replaced. `PipelineState`, the `interrupt()`-based `human_review`, `route_after_check`, and `route_after_review` all encode the rigid multi-interrupt flow. The new design has one checkpoint, after the first render. |
| `run.py` | CLI for the graph above. `_show_review()`'s report formatting is worth re-reading when building the Phase 3 CLI — it prints severity, category, location, and both observations per discrepancy, which is the right shape for the single human checkpoint. `_collect_edits()`'s dotted-path syntax (`plots.0.plot_no`) should be preserved in the user-guided branch. |
| `layout_repairer.py` (`analyze`, `repair`, `main`) | Superseded by the agent loop. `repair()`'s ordering is still the correct sequence and Phase 2 must reproduce it: patch schema → re-extract **if** `needs_reextraction` → rebuild → save HTML → render PNG. |
| `generate_resources` (in `graph.py`) | Was a `NotImplementedError` stub for auto-generating layout + schema for an unknown document type. This is precisely what the Architect Agent exists to do — it is the feature, not salvageable code. |

## Behaviour to reproduce in Phase 2/3

Recorded here because it lives in dropped files:

1. **Re-extraction ordering** — schema patch must land *before* OCR re-runs, and the
   rebuild must use the patched schema's data. `layout_repairer.repair()` lines 131–155.
2. **Patched-schema preference** — `graph.apply_repair` checked for a `*_patched.json`
   sidecar and preferred it over the original when re-extracting. Without this the
   pipeline silently re-extracts with the unpatched schema and the repair appears to
   do nothing.
3. **Iteration cap** — `max_iterations`, default 3, with a forced stop. The agent loop
   needs the same bound.
4. **Append-only history** — `Annotated[list[dict], add]` on `PipelineState["history"]`
   gave full traceability across iterations. Worth keeping in whatever state the agent
   carries.
5. **Dotted-path edits** — `plots.0.plot_no = 1433` for the user-guided branch.

## Not indexed by RAG

`agentic_controller/rag_engine.py` excludes `controller-old/` from the index
(`EXCLUDE_PATTERNS`). Indexing it would let the agent retrieve and imitate code that is
scheduled for deletion. Everything worth retrieving has been salvaged into this package
and is indexed here instead.
