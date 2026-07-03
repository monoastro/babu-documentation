# Nepali Citizenship Document Translation Pipeline

An end-to-end pipeline that converts an uploaded Nepali citizenship
document image into a structured, translated, printable HTML document.

```
IMAGE INPUT
    -> IMAGE PREPROCESSING
    -> OCR EXTRACTION (Azure Document Intelligence + GPT context correction)
    -> STRUCTURED FIELD EXTRACTION (GPT, JSON mode)
    -> TRANSLATION / NORMALIZATION (transliteration + GPT translation)
    -> HTML TEMPLATE GENERATION (Jinja2, A4 printable)
```

## Project layout

```
src/
├── main.py                     FastAPI app (upload -> translated HTML/JSON)
├── config.py                   Environment-variable based settings (pydantic-settings)
├── pipeline/
│   ├── processor.py            CitizenshipPipeline orchestrator
│   ├── preprocessing.py        ImagePreprocessor (OpenCV/Pillow)
│   ├── ocr.py                  AzureOCR + GPTOCRCorrector
│   ├── extraction.py           CitizenshipData model + FieldExtractor (GPT JSON mode)
│   ├── translator.py           Translator (transliteration/translation/normalization)
│   └── html_generator.py       HTMLGenerator (Jinja2 -> printable A4 HTML)
├── prompts/
│   ├── ocr_context.py          OCR correction prompt
│   └── extraction_prompt.py    Field extraction prompt + schema
├── templates/
│   └── citizenship.html         A4 printable Jinja2 template
└── utils/
    ├── image_utils.py           Image load/save/convert helpers
    ├── validators.py            Rule-based validation of extracted fields
    └── logging_config.py        Shared logging setup

requirements.txt
.env.example
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Fill in AZURE_DOC_INTELLIGENCE_ENDPOINT / KEY and OPENAI_API_KEY
```

## Running the API

```bash
cd src
uvicorn main:app --reload
```

- `GET  /healthz` - liveness check
- `POST /api/v1/citizenship/translate` - upload an image, get back the
  rendered translated HTML document
- `POST /api/v1/citizenship/extract` - upload an image, get back JSON
  with the extracted/translated fields and validation warnings

## Running the pipeline programmatically

```python
import asyncio
from pathlib import Path
from pipeline.processor import CitizenshipPipeline

async def main():
    pipeline = CitizenshipPipeline()
    result = await pipeline.process(Path("sample_citizenship.jpg"))
    print(result.html_path)

asyncio.run(main())
```

## Design notes

- **Preprocessing** (`pipeline/preprocessing.py`) is conservative by
  default (mild denoise/sharpen, CLAHE contrast, EXIF orientation
  correction, resize into a target range) to avoid destroying
  Devanagari glyph detail. Grayscale conversion and adaptive
  thresholding are available but **off by default**.

- **OCR** (`pipeline/ocr.py`) uses Azure Document Intelligence's
  `prebuilt-read` model by default (configurable via
  `AZURE_DOC_INTELLIGENCE_MODEL`), returning raw text plus per-line
  polygons. The raw text is then passed to `GPTOCRCorrector`, which
  fixes common OCR errors using document context **without inventing
  missing information** (see `prompts/ocr_context.py` for the exact
  constraints).

- **Extraction** (`pipeline/extraction.py`) defines the canonical
  `CitizenshipData` Pydantic model and uses GPT in JSON mode to populate
  it from corrected OCR text. Missing fields are `null`, never guessed.
  `utils/validators.py` performs independent rule-based checks (date
  formats, required fields, digit normalization) that are surfaced as
  warnings/errors without mutating the extracted data.

- **Translation** (`pipeline/translator.py`) distinguishes:
  - **Transliteration** (sound-preserving) for personal names -
    `राम बहादुर श्रेष्ठ` -> `Ram Bahadur Shrestha`, not a semantic
    translation.
  - **Translation** (meaning-preserving) for addresses/places/titles,
    using a static glossary for fixed official terms (District,
    Municipality, Ward No., etc.) plus GPT for proper nouns.
  - **Static normalization** (no GPT) for `gender` and
    `citizenship_type` via small lookup tables.

- **HTML generation** (`pipeline/html_generator.py`) renders
  `templates/citizenship.html`, a clean, table-based, printable A4
  layout. Missing fields render as blank cells - no placeholder text.

- **Orchestration** (`pipeline/processor.py`) sequences all stages,
  wraps every stage's exceptions in a `PipelineError` tagged with the
  failing `stage`, and returns a `PipelineResult` containing the final
  HTML path plus all intermediate artifacts (raw OCR, corrected text,
  extracted/translated data, validation results) for debugging/audit.

## Error handling

Every external call (Azure Document Intelligence, GPT) is wrapped in a
stage-specific exception (`AzureOCRError`, `GPTCorrectionError`,
`ExtractionError`, `TranslationError`, `HTMLGenerationError`), which the
orchestrator converts into a `PipelineError(stage, message)`. The
FastAPI layer maps these to appropriate HTTP status codes (502 for
upstream OCR/GPT failures, 400 for validation issues, 500 otherwise).
