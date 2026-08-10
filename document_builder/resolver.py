"""
Which layout is live, and which document types exist.

Both questions used to be answered by hand-written import statements in
``registry.py``. That made promotion a two-step edit — write ``layout_2.py``,
then repoint the registry — and a missed second step left the tree unimportable:
one dangling ``from document_builder.citizenship_back.layout_1 import ...`` took
down all four document types, ``main.py``, and four of six test suites.

The answers now come from the filesystem.

**Which layout is live** is whatever ``ACTIVE`` names. It holds one bare
filename, nothing else::

    document_builder/citizenship_back/ACTIVE   ->  "layout_1.py"

No ``ACTIVE`` file means ``layout.py``, so a directory that never patched
anything needs no bookkeeping. The architect writes ``ACTIVE`` only after
``validate_layout`` passes, which is what makes automatic promotion safe: a
layout that does not build cannot become live, and the previous good one stays
up. Rolling back is editing one line, and ``git diff`` shows the history.

**Which types exist** is every directory holding both a layout and a schema. A
generated document type is usable on the next run with no code edit.

This module deliberately imports nothing from ``agentic_controller`` or
``html_engine`` — ``registry.py`` and ``architect.py`` both depend on it, and a
cycle between them is how the duplicated path logic got out of sync in the first
place.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any, Callable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILDER_DIR = PROJECT_ROOT / "document_builder"
SCHEMA_DIR = PROJECT_ROOT / "information_extraction" / "schemas"

ACTIVE_FILENAME = "ACTIVE"
DEFAULT_LAYOUT = "layout.py"

# A layout filename and nothing else. `ACTIVE` is writable by the agent, so its
# contents are untrusted input: this pattern is what stops `../../etc/passwd`
# or an absolute path from being loaded as a builder.
_LAYOUT_NAME = re.compile(r"^layout(_\d+)?\.py$")


def _type_dir(document_type: str, *, builder_dir: Path | None = None) -> Path:
    return (builder_dir or BUILDER_DIR) / document_type


# ── Schemas ───────────────────────────────────────────────────────

def resolve_schema_path(document_type: str, *, schema_dir: Path | None = None) -> Path:
    """Return the schema the pipeline should actually extract with.

    Prefers a ``<doc>_patched.json`` sidecar over the original. Skipping this is
    what makes a schema repair look like a silent no-op: OCR re-runs against the
    unpatched base and the repaired fields never appear.
    """
    directory = schema_dir or SCHEMA_DIR
    patched = directory / f"{document_type}_patched.json"
    if patched.is_file():
        return patched
    return directory / f"{document_type}.json"


# ── Layout paths ──────────────────────────────────────────────────

def active_layout_path(
    document_type: str, *, builder_dir: Path | None = None
) -> Path | None:
    """Return the layout ``ACTIVE`` names, or ``layout.py``, or None.

    Never raises and never returns a path outside the type's own directory. A
    malformed or dangling pointer degrades to the rollback original with a
    warning, because a stale pointer should cost a stale render, not a crash.
    """
    directory = _type_dir(document_type, builder_dir=builder_dir)
    if not directory.is_dir():
        return None

    default = directory / DEFAULT_LAYOUT
    pointer = directory / ACTIVE_FILENAME

    if not pointer.is_file():
        return default if default.is_file() else None

    try:
        name = pointer.read_text(encoding="utf-8").strip()
    except OSError as exc:
        print(f"  warning: cannot read {pointer} ({exc}); using {DEFAULT_LAYOUT}",
              file=sys.stderr)
        return default if default.is_file() else None

    if not name:
        return default if default.is_file() else None

    if not _LAYOUT_NAME.match(name):
        print(f"  warning: {pointer} names {name!r}, which is not a layout filename; "
              f"using {DEFAULT_LAYOUT}", file=sys.stderr)
        return default if default.is_file() else None

    target = directory / name
    if not target.is_file():
        print(f"  warning: {pointer} points at {name}, which does not exist; "
              f"using {DEFAULT_LAYOUT}", file=sys.stderr)
        return default if default.is_file() else None

    return target


def latest_layout_path(
    document_type: str, *, builder_dir: Path | None = None
) -> Path | None:
    """Highest-numbered ``layout_N.py``, else ``layout.py``, else None.

    The newest layout written, which is not necessarily the live one — an
    unpromoted ``layout_3.py`` sits here while ``ACTIVE`` still names
    ``layout_2.py``. Use :func:`active_layout_path` to decide what to build.
    """
    directory = _type_dir(document_type, builder_dir=builder_dir)
    if not directory.is_dir():
        return None
    versioned = sorted(
        (p for p in directory.glob("layout_*.py") if p.stem.split("_")[-1].isdigit()),
        key=lambda p: int(p.stem.split("_")[-1]),
    )
    if versioned:
        return versioned[-1]
    base = directory / DEFAULT_LAYOUT
    return base if base.is_file() else None


def next_layout_path(document_type: str, *, builder_dir: Path | None = None) -> Path:
    """Return the next unused ``layout_N.py`` for *document_type*.

    ``layout.py`` is the rollback original and is never written to; iterations
    land beside it as ``layout_1.py``, ``layout_2.py``, ... .
    """
    directory = _type_dir(document_type, builder_dir=builder_dir)
    n = 1
    while (directory / f"layout_{n}.py").exists():
        n += 1
    return directory / f"layout_{n}.py"


def promote_layout(
    document_type: str, layout_path: Path, *, builder_dir: Path | None = None
) -> Path:
    """Make *layout_path* the live layout by writing ``ACTIVE``.

    Callers must only reach this after ``validate_layout`` passes — that gate is
    the entire reason automatic promotion is safe. Returns the ``ACTIVE`` path.

    Promotion writes a pointer, never the layout itself, so ``layout.py`` stays
    byte-identical as the rollback original. Copying a patch over ``layout.py``
    is what destroyed the original the manual process was supposed to protect.
    """
    directory = _type_dir(document_type, builder_dir=builder_dir)
    if not directory.is_dir():
        raise FileNotFoundError(f"no builder directory for {document_type!r}: {directory}")

    name = Path(layout_path).name
    if not _LAYOUT_NAME.match(name):
        raise ValueError(
            f"refusing to promote {name!r}: expected layout.py or layout_N.py"
        )
    if not (directory / name).is_file():
        raise FileNotFoundError(f"cannot promote {name}: not in {directory}")

    pointer = directory / ACTIVE_FILENAME
    pointer.write_text(f"{name}\n", encoding="utf-8")
    return pointer


def active_layout_name(document_type: str, *, builder_dir: Path | None = None) -> str:
    """``ACTIVE``'s filename for display, or ``"(none)"``."""
    path = active_layout_path(document_type, builder_dir=builder_dir)
    return path.name if path else "(none)"


# ── Discovery ─────────────────────────────────────────────────────

def discover_document_types(
    *, builder_dir: Path | None = None, schema_dir: Path | None = None
) -> list[str]:
    """Every document type with both a resolvable layout and a schema.

    A directory with a layout but no schema is not yet a document type: the
    pipeline cannot extract for it, so offering it in ``--type`` would only
    produce a confusing failure later.
    """
    directory = builder_dir or BUILDER_DIR
    if not directory.is_dir():
        return []

    found: list[str] = []
    for child in sorted(directory.iterdir()):
        if not child.is_dir():
            continue
        name = child.name
        # A builder name has to be a Python identifier: it becomes part of
        # `build_<type>`. `__pycache__` is excluded by the same rule that
        # excludes `tax-clearance`.
        if name.startswith("_") or not name.isidentifier():
            continue
        if active_layout_path(name, builder_dir=directory) is None:
            continue
        if not resolve_schema_path(name, schema_dir=schema_dir).is_file():
            continue
        found.append(name)
    return found


# ── Loading ───────────────────────────────────────────────────────

def load_builder(
    document_type: str, *, builder_dir: Path | None = None
) -> Callable[[dict[str, Any]], Any]:
    """Import the active layout and return its ``build_<document_type>``.

    Loaded from a file path rather than by module name. ``ACTIVE`` can name any
    ``layout_N.py``, and a promotion inside a live process has to take effect
    without a stale ``sys.modules`` entry serving the old builder — which is the
    mid-run promotion this whole mechanism exists to allow.
    """
    layout_path = active_layout_path(document_type, builder_dir=builder_dir)
    if layout_path is None:
        raise FileNotFoundError(
            f"no layout for {document_type!r} in "
            f"{_type_dir(document_type, builder_dir=builder_dir)}"
        )

    module_name = f"_babu_layout_{document_type}_{layout_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, layout_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {layout_path}")

    module = importlib.util.module_from_spec(spec)
    # Registered before exec so a layout doing `from __future__ import ...` or
    # a dataclass referring to its own module resolves normally.
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise

    func_name = f"build_{document_type}"
    builder = getattr(module, func_name, None)
    if builder is None:
        raise AttributeError(f"{layout_path} defines no {func_name}()")
    if not callable(builder):
        raise TypeError(f"{layout_path}: {func_name} is not callable")
    return builder
