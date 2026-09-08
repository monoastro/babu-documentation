from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-3.6-flash"
THINKING = types.ThinkingConfig(thinking_level="high")


def get_client() -> genai.Client:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Put it in .env or export it."
        )
    return genai.Client(api_key=key)


def part_text(text: str) -> types.Part:
    return types.Part.from_text(text=text)


def part_image(path, mime: str) -> types.Part:
    return types.Part.from_bytes(data=Path(path).read_bytes(), mime_type=mime)


def call_parts(parts: list[types.Part], *, temperature: float = 0.2) -> str:
    gen_client = get_client()
    response = gen_client.models.generate_content(
        model=MODEL,
        contents=parts,
        config=types.GenerateContentConfig(
            thinking_config=THINKING,
            temperature=temperature,
        ),
    )
    return response.text or ""


def call(
    prompt: str,
    *,
    images: list[tuple[str, bytes]] | None = None,
    temperature: float = 0.2,
) -> str:
    parts: list[types.Part] = []
    for mime, data in images or []:
        parts.append(types.Part.from_bytes(data=data, mime_type=mime))
    parts.append(types.Part.from_text(text=prompt))
    return call_parts(parts, temperature=temperature)
