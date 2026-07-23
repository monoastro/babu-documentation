# Growing a document-layout verification workflow

We will keep one goal throughout: make OCR-derived layouts match their source
documents. Each stage adds a capability that fixes a real limitation in the
previous one.

| Stage | Add | Why it is needed |
| --- | --- | --- |
| 1. Vision verification | A typed report comparing source and render | Free-form visual feedback is unsafe for code to act on. |
| 2. Layout patches | A constrained patch schema | The model must not freely rewrite HTML or layout code. |
| 3. Render-and-retry graph | A bounded repair loop | A repair must be rendered and checked again before acceptance. |
| 4. Human review | Explicit pause and evidence bundle | Low-confidence cases need an accountable human decision. |

## Stage 1 — vision verification (current)

Run:

```bash
python document_verifier.py
```

The important line is:

```python
reviewer = ChatOpenAI(...).with_structured_output(VerificationReport)
```

It is a safe pipeline:

```text
source PNG + rendered PNG -> vision model -> validated VerificationReport
```

The model may observe and report, but cannot alter the document. In Stage 2, we
will define the only permitted layout changes as a typed patch and validate them
in your own renderer.

## Experiment before Stage 2

Put a known-good pair at `input.png` and `output.png`, then run the command.
Repeat with a pair containing an intentional layout mistake.
Inspect the JSON carefully: it is a candidate signal for your code, not ground
truth. Tune the reviewer instruction and discrepancy categories before allowing
any automated repair.
