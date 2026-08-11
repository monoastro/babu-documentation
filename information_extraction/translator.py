"""LLM translation of extracted field values into English.

Extraction (Datalab OCR) returns values in the script they were printed in,
usually Devanagari. The rendered document is meant to be readable English, so a
translation stage sits between extraction and the layout builder:

    extract() → build_data() → translate_data() → builder(data)

``translate_data`` walks the extracted structure — nested, because a laalpurja's
``plots`` is a list of dicts — and returns the same structure with every
translatable string replaced by its English equivalent, plus a flat map of the
originals so the Devanagari is never lost.

Three rules make the output usable rather than literally correct:

  * **Proper nouns are transliterated, not translated.** ``उमा देवी चौलागाई``
    becomes ``Uma Devi Chaulagai``, not an attempt at meaning. Same for place
    names: ``काठमाण्डौ`` → ``Kathmandu``.
  * **Devanagari digits become ASCII.** ``८`` → ``8``. The laalpurja layout
    already parses plot areas this way (its ``_DEVA`` table); doing it here
    means every layout gets it, not just the one that remembered.
  * **Bikram Sambat dates become Gregorian.** ``२०४९/०३/०९`` → ``1992-06-22``,
    via ``nepali_datetime``. Done locally, not by the model — date arithmetic is
    exactly the kind of thing an LLM gets subtly wrong.

Some strings must survive untouched. ``present`` / ``absent`` are an OCR
contract, not content: layouts branch on them to decide whether to draw a thumb
impression box at all, so rewording one silently removes a box from the page.
Values that are already English, bare numbers, and the extractor's own
provenance metadata (``<field>_meta``, ``<field>_citations``) are skipped too —
the first two because there is nothing to do, the third because it is never
rendered.

Everything translatable in one document goes out in a single request, keyed by
path. Batching is not only cheaper than a call per field, it is more accurate:
the model sees ``district`` and ``municipality`` together and can tell that a
word is a place name.

Translated values are cached on disk by ``(text, model)``, so the repair loop's
second and third iterations re-translate nothing.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

CACHE_PATH = Path(__file__).resolve().parent / ".translation_cache.json"

# Provenance the extractor attaches beside each value. Never rendered, never
# translated. See any ``plots[i]`` entry in a saved laalpurja JSON.
_META_SUFFIXES = ("_citations", "_meta")

# OCR contract tokens. A layout reads these to decide whether to draw an
# element; translating one changes the page, not just its wording.
_SENTINELS = {"present", "absent", "unreadable signature", "unknown", "n/a", "none"}

# Whole Nepali sentences rather than field values — translated as prose, with no
# transliteration rule applied.
_PROSE_KEYS = {"remarks", "nepal_citizenship_act_sentence"}

# Suffix pairs that mark a deliberately bilingual field. The SEE certificate
# prints ``certificate_title_np`` on one line and ``certificate_title_en`` on
# the next; translating the first makes the document say "Certificate" twice.
# Same for a ``<field>_bs`` date printed beside its ``<field>_ad`` counterpart.
# Only the presence of the *sibling* triggers this — a lone ``foo_np`` is the
# only value there is, and is translated normally.
_PAIRED_SUFFIXES = {
    "_np": ("_en", "_eng", "_english"),
    "_nepali": ("_en", "_english"),
    "_devanagari": ("_en", "_english", "_roman"),
    "_bs": ("_ad",),
}

# Values that are Bikram Sambat dates. Converted locally, never by the model.
_BS_DATE_KEYS = {
    "issue_date", "issue_date_bs", "print_date", "checked_by_date",
    "evd_date", "registration_date", "date_bs", "issue_date_nepali",
    "print_date_nepali",
}

_DEVA_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
_BS_DATE_RE = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$")
# Any character that is a letter in some script — used to decide whether a
# value contains anything a translator could act on.
_LETTER_RE = re.compile(r"[^\W\d_]", re.UNICODE)
_ASCII_ONLY_RE = re.compile(r"^[\x00-\x7f]*$")

_SYSTEM_PROMPT = """You translate field values extracted from Nepali government
documents into English, for a digitized replica of the document.

You will receive a JSON object mapping opaque keys to values. Return a JSON
object with exactly the same keys, where each value is the English rendering of
the input value. Return only the JSON object — no prose, no code fence.

Rules:
1. PROPER NOUNS ARE TRANSLITERATED, NOT TRANSLATED. Person names, place names,
   district and municipality names, and office names keep their identity:
   "उमा देवी चौलागाई" -> "Uma Devi Chaulagai", "काठमाण्डौ" -> "Kathmandu",
   "नाङ्गलेभारे" -> "Nangalebhare". Use the conventional English spelling when
   one exists (Kathmandu, not Kathmandau).
2. Everything else is translated for meaning: "वंशज" -> "By descent",
   "मृत्युपछिको नामसारी" -> "Transfer after death", "प्रशासकीय अधिकृत" ->
   "Administrative Officer".
3. Devanagari digits become ASCII digits: "८" -> "8", "२०७८" -> "2078".
4. Do not add, explain, expand, or annotate. No parentheses with the original.
   No "(lit. ...)". The value is going straight onto a printed document.
5. If a value is already English, return it unchanged.
6. If you cannot translate a value, return it unchanged rather than guessing.

Office names combine both rules: "जिल्ला प्रशासन कार्यालय, काठमाण्डौ" ->
"District Administration Office, Kathmandu" — the office type is translated,
the place name transliterated."""

_PROSE_NOTE = """Some values are full sentences (legal text, printed remarks).
Translate those as natural English prose, complete and unabridged, keeping the
sentence a sentence."""


@dataclass
class Translation:
    """The result of translating one document's extracted data."""

    data: dict[str, Any]
    original: dict[str, str] = field(default_factory=dict)
    translated: int = 0
    skipped: int = 0
    error: str | None = None

    def describe(self) -> str:
        if self.error:
            return f"translation skipped ({self.error})"
        return f"{self.translated} translated, {self.skipped} left as-is"


# ── Classification ────────────────────────────────────────────────

def _is_meta_key(key: str) -> bool:
    return key.endswith(_META_SUFFIXES)


def _has_letters(value: str) -> bool:
    return bool(_LETTER_RE.search(value))


def _is_ascii(value: str) -> bool:
    return bool(_ASCII_ONLY_RE.match(value))


def _to_ascii_digits(value: str) -> str:
    return value.translate(_DEVA_DIGITS)


def bs_to_ad(value: str) -> str:
    """Convert one Bikram Sambat date to an ISO Gregorian date.

    Returns the input unchanged when it is not a date this can parse, or when
    the date falls outside ``nepali_datetime``'s supported range — a partial
    conversion is worse than none, because the layout would print a year that
    looks Gregorian and is not.
    """
    digits = _to_ascii_digits(value.strip())
    match = _BS_DATE_RE.match(digits)
    if not match:
        return value
    try:
        from nepali_datetime import date as bs_date

        year, month, day = (int(g) for g in match.groups())
        return bs_date(year, month, day).to_datetime_date().isoformat()
    except Exception:
        return value


def _needs_translation(key: str, value: str) -> bool:
    """Whether this value should be sent to the model at all."""
    stripped = value.strip()
    if not stripped:
        return False
    if stripped.lower() in _SENTINELS:
        return False
    if _is_ascii(stripped):
        # Already Latin script: English text, an ID like "NM0000095", a number.
        return False
    if not _has_letters(stripped):
        # Devanagari digits and punctuation only — handled locally.
        return False
    return True


# ── Structure walking ─────────────────────────────────────────────

def _paired_sibling(node: dict, key: str) -> bool:
    """Whether ``key`` is the script-preserved half of a bilingual field pair.

    True when the same dict also holds the English counterpart named by
    ``_PAIRED_SUFFIXES`` — ``certificate_title_np`` beside
    ``certificate_title_en``, ``date_of_birth_bs`` beside ``date_of_birth_ad``.
    """
    for suffix, siblings in _PAIRED_SUFFIXES.items():
        if not key.endswith(suffix):
            continue
        stem = key[: -len(suffix)]
        return any(f"{stem}{s}" in node for s in siblings)
    return False


def _collect(node: Any, path: str, key: str, out: dict[str, tuple[str, str]]) -> None:
    """Gather every translatable leaf as ``path → (key, value)``."""
    if isinstance(node, dict):
        for k, v in node.items():
            if _is_meta_key(k):
                continue
            _collect(v, f"{path}.{k}" if path else k, k, out)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            _collect(item, f"{path}[{i}]", key, out)
    elif isinstance(node, str):
        out[path] = (key, node)


def _paired_paths(node: Any, path: str, out: set[str]) -> None:
    """Collect the paths of every script-preserved half of a bilingual pair."""
    if isinstance(node, dict):
        for k, v in node.items():
            child = f"{path}.{k}" if path else k
            if _paired_sibling(node, k):
                out.add(child)
            _paired_paths(v, child, out)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            _paired_paths(item, f"{path}[{i}]", out)


def _apply(node: Any, path: str, key: str, new: dict[str, str]) -> Any:
    """Rebuild the structure with ``new[path]`` substituted at each leaf."""
    if isinstance(node, dict):
        return {
            k: v if _is_meta_key(k)
            else _apply(v, f"{path}.{k}" if path else k, k, new)
            for k, v in node.items()
        }
    if isinstance(node, list):
        return [_apply(item, f"{path}[{i}]", key, new) for i, item in enumerate(node)]
    if isinstance(node, str):
        return new.get(path, node)
    return node


# ── Cache ─────────────────────────────────────────────────────────

def _load_cache() -> dict[str, str]:
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_cache(cache: dict[str, str]) -> None:
    try:
        CACHE_PATH.write_text(
            json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8"
        )
    except OSError:
        # A cache that cannot be written is a slower run, not a failed one.
        pass


def _cache_key(model: str, kind: str, value: str) -> str:
    return f"{model}\x1f{kind}\x1f{value}"


# ── Model call ────────────────────────────────────────────────────

def _model_name() -> str:
    return os.getenv("TRANSLATOR_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _translate_batch(values: dict[str, str], *, prose: bool, model: str) -> dict[str, str]:
    """Send one batch of ``id → value`` and return ``id → translation``.

    Keys the model omits or mangles are simply absent from the result; the
    caller keeps the original for those, so a partial reply degrades to a
    partial translation rather than lost data.
    """
    from openai import OpenAI

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set — needed for translation.")

    system = _SYSTEM_PROMPT + ("\n\n" + _PROSE_NOTE if prose else "")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # No temperature: the newer models reject anything but their default, and
    # the JSON response format plus an instruction-only prompt already leaves
    # little to sample over.
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(values, ensure_ascii=False, indent=1)},
        ],
    )
    raw = (response.choices[0].message.content or "").strip()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    if not isinstance(parsed, dict):
        return {}
    return {k: v for k, v in parsed.items() if isinstance(v, str) and v.strip()}


# ── Entry point ───────────────────────────────────────────────────

def translate_data(
    data: dict[str, Any],
    *,
    model: str | None = None,
    use_cache: bool = True,
    verbose: bool = False,
) -> Translation:
    """Translate every translatable string in ``data`` into English.

    Returns a :class:`Translation` holding the new data, a flat
    ``path → original value`` map for everything that changed, and counts. A
    failed model call is reported on the result rather than raised: a document
    that renders in Devanagari is better than no document at all.
    """
    model = model or _model_name()
    leaves: dict[str, tuple[str, str]] = {}
    _collect(data, "", "", leaves)

    preserved: set[str] = set()
    _paired_paths(data, "", preserved)

    cache = _load_cache() if use_cache else {}
    resolved: dict[str, str] = {}      # path → final English value
    original: dict[str, str] = {}      # path → the value before translation
    pending: dict[str, dict[str, str]] = {"label": {}, "prose": {}}

    for path, (key, value) in leaves.items():
        stripped = value.strip()

        if path in preserved:
            # The English half is printed on the next line; touching this one
            # would make the document say the same thing twice.
            continue

        if key in _BS_DATE_KEYS:
            converted = bs_to_ad(value)
            if converted != value:
                resolved[path] = converted
                original[path] = value
            continue

        if not _needs_translation(key, value):
            # Devanagari digits with no letters ("८", "२०७८-०९-२६") still get
            # their numerals normalised — that costs nothing and no model.
            ascii_digits = _to_ascii_digits(value)
            if ascii_digits != value:
                resolved[path] = ascii_digits
                original[path] = value
            continue

        kind = "prose" if key in _PROSE_KEYS else "label"
        cached = cache.get(_cache_key(model, kind, stripped))
        if cached is not None:
            resolved[path] = cached
            original[path] = value
            continue

        pending[kind][path] = stripped

    error: str | None = None
    for kind, batch in pending.items():
        if not batch:
            continue
        # Identical values appear many times (a district repeated down a table).
        # Send each distinct string once and fan the answer back out.
        distinct = {}
        for path, value in batch.items():
            distinct.setdefault(value, []).append(path)
        request = {f"v{i}": value for i, value in enumerate(distinct)}
        if verbose:
            print(f"  → translating {len(request)} {kind} value(s)...")
        try:
            reply = _translate_batch(request, prose=(kind == "prose"), model=model)
        except Exception as exc:
            error = str(exc)
            continue

        for ident, value in request.items():
            english = reply.get(ident)
            if not english or english == value:
                continue
            cache[_cache_key(model, kind, value)] = english
            for path in distinct[value]:
                resolved[path] = english
                original[path] = batch[path]

    if use_cache and resolved:
        _save_cache(cache)

    return Translation(
        data=_apply(data, "", "", resolved),
        original=original,
        translated=len(resolved),
        skipped=len(leaves) - len(resolved),
        error=error,
    )
