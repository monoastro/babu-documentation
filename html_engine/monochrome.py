"""
Monochrome enforcement for the HTML Document Engine.

Project rule: a rendered document is purely black and white. Foreground ink
(text, borders, rules, shadows) is ``#000000``; every surface is ``#ffffff``.

The rule is enforced structurally rather than by convention, because a
convention only holds for code a human reviewed — and the Architect Agent
writes layouts unattended. Normalization happens on the way *out*, at every
route CSS can reach the page:

    1. ``Style.to_css()``           — the ordinary component path
    2. ``Component._build_attrs()`` — a raw ``style`` string in ``attrs``
    3. ``Style.raw``                — the documented escape hatch
    4. ``renderer.render()``        — the ``<style>`` block, ``extra_css``,
                                      ``Document(background=...)``, and any
                                      style hardcoded into a ``to_html()``
                                      f-string

There is deliberately no opt-out. A layout cannot emit colour.

Why the target depends on the *property* and not on the colour's luminance:
thresholding by luminance would map a dark fill to black and its light text
to white — or the reverse — and either way the two can collide into an
unreadable block. Pinning surfaces white and ink black guarantees contrast
for any input.
"""

from __future__ import annotations

import re

BLACK = "#000000"
WHITE = "#ffffff"

# Keywords that are not colours, or that resolve to something already safe.
# ``transparent`` in particular must survive: rewriting it to white would
# paint opaque boxes over content that is meant to show through.
_KEEP = frozenset(
    {
        "transparent",
        "currentcolor",
        "inherit",
        "initial",
        "unset",
        "revert",
        "none",
        "auto",
    }
)

# Every CSS named colour. A curated subset was tried first and leaked:
# ``rebeccapurple`` is not an exotic choice for a model writing a layout, and
# any name missing from the list passes through as real colour. The list is
# closed and standardised, so completeness costs one constant and removes the
# entire class of near-miss.
#
# Longest-first ordering matters: the alternation is scanned left to right, so
# with "red" before "rebeccapurple" the regex would match "red" and leave
# "beccapurple" behind as stray text.
_NAMED = "|".join(
    sorted(
        (
            "aliceblue antiquewhite aqua aquamarine azure beige bisque black"
            " blanchedalmond blue blueviolet brown burlywood cadetblue"
            " chartreuse chocolate coral cornflowerblue cornsilk crimson cyan"
            " darkblue darkcyan darkgoldenrod darkgray darkgrey darkgreen"
            " darkkhaki darkmagenta darkolivegreen darkorange darkorchid"
            " darkred darksalmon darkseagreen darkslateblue darkslategray"
            " darkslategrey darkturquoise darkviolet deeppink deepskyblue"
            " dimgray dimgrey dodgerblue firebrick floralwhite forestgreen"
            " fuchsia gainsboro ghostwhite gold goldenrod gray grey green"
            " greenyellow honeydew hotpink indianred indigo ivory khaki"
            " lavender lavenderblush lawngreen lemonchiffon lightblue"
            " lightcoral lightcyan lightgoldenrodyellow lightgray lightgrey"
            " lightgreen lightpink lightsalmon lightseagreen lightskyblue"
            " lightslategray lightslategrey lightsteelblue lightyellow lime"
            " limegreen linen magenta maroon mediumaquamarine mediumblue"
            " mediumorchid mediumpurple mediumseagreen mediumslateblue"
            " mediumspringgreen mediumturquoise mediumvioletred midnightblue"
            " mintcream mistyrose moccasin navajowhite navy oldlace olive"
            " olivedrab orange orangered orchid palegoldenrod palegreen"
            " paleturquoise palevioletred papayawhip peachpuff peru pink plum"
            " powderblue purple rebeccapurple red rosybrown royalblue"
            " saddlebrown salmon sandybrown seagreen seashell sienna silver"
            " skyblue slateblue slategray slategrey snow springgreen steelblue"
            " tan teal thistle tomato turquoise violet wheat white whitesmoke"
            " yellow yellowgreen"
        ).split(),
        key=len,
        reverse=True,
    )
)

_COLOR_TOKEN = re.compile(
    r"#[0-9a-fA-F]{3,8}\b"          # #abc / #aabbcc / #aabbccdd
    r"|(?:rgba?|hsla?)\([^)]*\)"    # rgb() rgba() hsl() hsla()
    rf"|\b(?:{_NAMED})\b",
    re.IGNORECASE,
)

# ``content`` holds author text — a "#" inside it is a character, not a colour.
_SKIP_PROPS = frozenset({"content", "font-family", "src"})

# A CSS declaration. The value stops at ``;`` or a brace so that a selector
# such as ``a:hover {`` is not mistaken for a ``hover`` property.
_DECLARATION = re.compile(r"([-a-zA-Z]+)\s*:\s*([^;{}]*)")

_URL = re.compile(r"url\([^)]*\)", re.IGNORECASE)


def _target_for(prop: str) -> str:
    """Surfaces go white, ink goes black."""
    return WHITE if "background" in prop else BLACK


def normalize_value(prop: str, value: str) -> str:
    """
    Rewrite every colour token in a single declaration's *value*.

    Parameters:
        prop: CSS property name (e.g. ``"border"``, ``"background-color"``).
        value: The declaration value (e.g. ``"1.8px dashed #4a90d9"``).

    Returns:
        The value with colours replaced, other tokens untouched::

            normalize_value("border", "2px solid #4a90d9")
            # -> "2px solid #000000"
    """
    prop = prop.strip().lower()
    if prop in _SKIP_PROPS:
        return value

    # A url(...) may contain anything, including a "#" fragment. Stash it so
    # the colour regex cannot reach inside.
    stashed: list[str] = []

    def _stash(match: re.Match[str]) -> str:
        stashed.append(match.group(0))
        return f"\x00{len(stashed) - 1}\x00"

    protected = _URL.sub(_stash, value)

    target = _target_for(prop)

    def _replace(match: re.Match[str]) -> str:
        token = match.group(0)
        return token if token.lower() in _KEEP else target

    result = _COLOR_TOKEN.sub(_replace, protected)
    return re.sub(r"\x00(\d+)\x00", lambda m: stashed[int(m.group(1))], result)


def normalize_declarations(css: str) -> str:
    """
    Rewrite colours across a CSS fragment.

    Works both on an inline declaration list (``"color:red;margin:0"``) and on
    a full stylesheet with selectors and braces, since it matches declarations
    wherever they appear.
    """
    if not css:
        return css
    return _DECLARATION.sub(
        lambda m: f"{m.group(1)}:{normalize_value(m.group(1), m.group(2))}", css
    )


def normalize_html(html: str) -> str:
    """
    Rewrite colours in a complete HTML document.

    Only ``style="..."`` attributes and ``<style>`` blocks are touched. Text
    content is left exactly as-is — a land record may legitimately contain a
    token that looks like a hex colour, and corrupting document data would be
    far worse than leaking a colour.
    """
    if not html:
        return html

    html = re.sub(
        r'style="([^"]*)"',
        lambda m: f'style="{normalize_declarations(m.group(1))}"',
        html,
    )
    return re.sub(
        r"(<style[^>]*>)(.*?)(</style>)",
        lambda m: m.group(1) + normalize_declarations(m.group(2)) + m.group(3),
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )


def find_violations(css: str) -> list[tuple[str, str]]:
    """
    Report colour tokens that normalization *would* change.

    Returns a list of ``(property, token)`` pairs. Empty means the fragment is
    already monochrome. Used by the test suite and by the source-rewrite audit
    to prove the rule holds, rather than assuming it.
    """
    found: list[tuple[str, str]] = []
    for match in _DECLARATION.finditer(css or ""):
        prop, value = match.group(1).strip().lower(), match.group(2)
        if prop in _SKIP_PROPS:
            continue
        for token_match in _COLOR_TOKEN.finditer(_URL.sub("", value)):
            token = token_match.group(0)
            if token.lower() in _KEEP:
                continue
            if token.lower() not in (BLACK, WHITE):
                found.append((prop, token))
    return found
