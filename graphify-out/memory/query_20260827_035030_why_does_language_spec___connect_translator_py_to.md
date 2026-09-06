---
type: "query"
date: "2026-08-27T03:50:30.581300+00:00"
question: "Why does language_spec() connect translator.py to run.py, test_translator.py, architect.py?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["language_spec()", "translate_data()", "build_prompt()", "plan_blocks()", "LanguageSpec"]
---

# Q: Why does language_spec() connect translator.py to run.py, test_translator.py, architect.py?

## Answer

Expanded from original query via vocab: [language, languages, spec, translator, translation, translate, translated, verifier, verification, prompt, target, cache]. Then traversed via explain+path. language_spec() (information_extraction/languages.py:87, degree 12, all EXTRACTED) is the single source of truth for the target language and the only node bridging the translator.py, run.py and architect.py communities. Three consumers each read a different field of the same frozen LanguageSpec: translate_data() at translator.py:398 (transliteration/meaning/office examples plus script_is_ascii, which is the already-in-target-script skip), build_prompt() at verifier.py:110 (name plus the same worked examples, into verification rule 1), and plan_blocks() at architect.py:1436 (name, into the layout planner prompt). Consequence: render, critique and generated layout share one language contract by import, not by convention, which structurally prevents judging a Japanese render against English (every correct translation would read as a data-accuracy defect and the repair loop would chase them forever). Adding a language is one entry in LANGUAGES at languages.py:46; languages.py imports nothing so main.py can build --lang choices without the OpenAI client or OCR path.

## Outcome

- Signal: useful

## Source Nodes

- language_spec()
- translate_data()
- build_prompt()
- plan_blocks()
- LanguageSpec