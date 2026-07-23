# Document-layout verification with LangChain

This is a safe first step toward checking OCR-derived document layouts. It
compares a source PNG with a PNG rendered from your layout and returns a
validated JSON discrepancy report. It does **not** change the layout or either
image.

## Setup

You need Python 3.10+ and an OpenAI API key.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and replace `your_api_key_here` with your key. Never commit this file.

## Run the document verifier

```bash
python document_verifier.py
```

Put your reference image at `input.png` and your rendered image at `output.png`
in this project folder first. The JSON report prints in the terminal.

To save the report:

```bash
python document_verifier.py --output report.json
```

You can still pass other paths when needed:

```bash
python document_verifier.py path/to/source.png path/to/rendered.png
```

Both images are sent to the configured model for visual review. Do not use this
with sensitive documents until your data-handling and API-retention requirements
are approved.

## What LangChain contributes here

`ChatOpenAI(...).with_structured_output(VerificationReport)` sends a multimodal
comparison request and returns validated Python data rather than fragile,
free-form text. The Pydantic models define exactly what later repair code may
consume: a match decision, discrepancies, confidence, and whether human review
is required.

The verifier only observes. The next stage will define a constrained layout-patch
schema and validate each requested change in your own renderer.

The earlier `main.py` study-plan example remains as a tiny prompt-chain reference.
Read [LEARNING_PATH.md](LEARNING_PATH.md) for the document-workflow roadmap.
