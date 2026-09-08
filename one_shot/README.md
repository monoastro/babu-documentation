# one_shot

One Gemini call replaces the whole extract → translate → build chain.

## Pipeline

```
scan + one_shot/prompt.txt + one_shot/example.txt
        └─ one call to gemini-3.6-flash (thinking high) ─→ draft HTML
             └─ manual cleanup in html_visual_editor ─→ final in translated/
```

## Commands

```bash
.venv/bin/python -m one_shot.generate --image <scan>            # uses example.txt
.venv/bin/python -m one_shot.generate --image <scan> --example translated/5. pragya/bill7.html
```

Drafts land in `one_shot/drafts/` (gitignored). No routing, no catalog — pick
the `--example` yourself when the default snippets aren't enough.

## Files

- `prompt.txt` — the ruleset: translation, monochrome style, page rules
  (**no border on the page div** — the evolved requirement), element
  replacement (photo/seal/stamp/QR boxes), `contenteditable` + `data-field`,
  standalone output. Tracked.
- `example.txt` — real generated-code snippets (page scaffold, circle, box,
  text field, table, signatures, photo box, card-on-A4 scaling, dashed thumb
  impression, rowspan land table) pulled verbatim from cleaned finals in
  `translated/`, preferring the newest folders (5 → 1). Tracked.
- `client.py` — google-genai wrapper; `gemini-3.6-flash`, thinking level high,
  key from `GEMINI_API_KEY` (`.env`). 503s under demand: retry, don't rewrite.
- `generate.py` — prompt assembly (rules → reference snippets) and draft
  output to `drafts/`.
- `tests/test_one_shot.py` — offline suite (all calls stubbed).

## Conventions

- **No Devanagari in output, ever** — numerals (०–९) become ASCII, proper
  nouns transliterated. One font stack: Times New Roman. Standalone HTML: no
  `<img>`, scripts, or external requests.
- **No page border** — borders belong to elements inside (boxes, tables,
  stamps), never the document edge.
- `data-field` snake_case; repeated structures dot notation (`items.0.rate`).
- Quota: 20 requests/day free tier for `gemini-3.6-flash`; one generate = 1
  call. Never "quickly verify" with live calls; tests are offline.

## History

v0 (generate) and v1 (two-stage router + catalog + thumbnails) were built and
live-verified, then simplified at the user's call: the router/catalog
machinery was removed as overcomplication. Routing by example selection is
now manual (`--example`). The `data-component` tag contract was dropped along
with it — cleaned finals never carried those tags anyway.
