---
Plan: Autonomous Agentic Layout & Schema Generator

Context

The current LangGraph controller is unsatisfactory because it is too rigid to handle complex, open-ended document variations without manual builder intervention. We need a system that can:
1. Retrieve Context: Understand existing layout patterns (html_engine) and extraction schemas (information_extraction/schemas/).
2. Reason: Compare input vs. output and identify structural discrepancies.
3. Generate/Repair: Autonomously emit new layout code and updated schemas.

Proposed Architecture: The "Architect Agent"

1. Knowledge Base (RAG Layer)

We will convert the codebase into a queryable semantic knowledge base.
- Embedding Strategy: Use sentence-transformers/all-MiniLM-L6-v2 to generate embeddings for all .py files in html_engine/, document_builder/, and information_extraction/.
- Vector Store: Use faiss or chromadb for local, fast vector retrieval.
- Indexing: Index files by class, function, and purpose (e.g., "how to define a text component", "how to structure laalpurja schema").

2. The Architect Agent (Reasoning Layer)

A specialized agent (using a "Claude-like" loop) that sits above the OCR/pipeline.
- Agent Persona: Provided with the full project context through RAG-retrieved relevant code snippets.
- Tool-Use: The agent will have access to:
  - Read: View current layout/schema.
  - Write: Propose/apply new layout/schema.
  - Bash: Run verification tests.
- Loop:
  a. Observe: Review VerificationReport.
  b. Retrieve: Query RAG for similar existing document structures.
  c. Plan: Propose a SchemaPatch and a LayoutAdjustment.
  d. Execute: Write the file changes and re-run the pipeline.

3. Verification & Repair Loop

Instead of an interrupt-heavy LangGraph state machine, we use a single, unified agent loop:
1. Pipeline: Input -> OCR -> Build -> Verify (Standard).
2. Agent: If VerificationReport shows discrepancies, the agent is invoked.
3. Dynamic Repair: Agent fetches relevant layout.py and schema, reasons about what is wrong, and applies Write edits to the relevant files.

---
Implementation Steps

Phase 1: Knowledge Base Infrastructure

- Task: Build a script controller/rag_engine.py to ingest the codebase and populate a local FAISS index.
- Deliverable: A functional query_context(question) function that returns the most relevant code snippets.

Phase 2: Architect Agent Definition

- Task: Create controller/architect.py. This script will use the anthropic client to manage a tool-calling loop (the "agent") that has access to the query_context function.
- Deliverable: An agent capable of receiving a prompt like: "The citizenship rendering failed at LabelValue positioning. Fix the layout builder."

Phase 3: The Integrated Pipeline

- Task: Refactor controller/run.py to call the Architect Agent instead of the static repair/edit nodes.
- Deliverable: A CLI command python -m controller.architect <image> <doc_type> that runs the end-to-end autonomous repair loop.

---
Verification

1. Test RAG: Ensure query_context("how to render a table") retrieves html_engine/components/table.py.
2. Test Agent: Provide a failing layout and ensure the agent proposes a correct schema/layout patch.
3. Integration: Run controller/architect.py on a document that is slightly different from the training data to ensure generalization.

---
