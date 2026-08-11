## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Generated layouts

Layouts generated from a scan (`document_builder/autolayout.py`) are always an
exact A4 sheet — 794×1123 px portrait or 1123×794 landscape at 96 DPI, with the
orientation taken from the source. The scan's ink extent is fitted inside a
10 mm margin by a **single scale factor applied to both axes**, then centred, so
the source aspect ratio and every block's relative position survive the trip.
Never fit width and height independently: that would make the page A4 by
distorting everything on it.
