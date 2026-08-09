"""
Abstract base class for all HTML Document Engine components.

Every renderable element (Text, Image, Table, etc.) inherits from
``Component`` and implements ``to_html()``.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Iterable, Optional

if TYPE_CHECKING:
    from html_engine.styles import Style


def coerce_child(value: Any, *, owner: str = "Component", index: int = 0) -> Optional[Component]:
    """
    Turn one constructor argument into a child component, or reject it.

    Containers take components, but a bare string is not ambiguous —
    ``Div("(Signed)")`` can only mean a div containing that text. Left
    uncoerced it used to survive construction and then fail during rendering
    with ``AttributeError: 'str' object has no attribute 'to_html'``, raised
    from inside ``_render_children`` with nothing in the traceback naming the
    layout, the container, or the string. Numbers are coerced for the same
    reason.

    ``None`` is skipped, so a conditional child (``Div(*(row if rows else
    None))``) collapses instead of crashing, matching the project rule that a
    missing value renders as nothing rather than as ``"None"``.

    Anything else is a real mistake — a list, a dict, a raw ``Style`` — and
    raises ``TypeError`` naming the position and the type.
    """
    from html_engine.components.text import Text

    if value is None:
        return None
    if isinstance(value, Component):
        return value
    if isinstance(value, str):
        # Text escapes by default, which is the safe reading of a bare string.
        return Text(value)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return Text(str(value))
    raise TypeError(
        f"{owner} child at position {index} is {type(value).__name__}, "
        f"which cannot be rendered. Pass a Component, a string, or None — "
        f"got {value!r}."
    )


def coerce_children(
    values: Optional[Iterable[Any]], *, owner: str = "Component"
) -> list[Component]:
    """Coerce an iterable of constructor arguments, dropping ``None``s."""
    if not values:
        return []
    out: list[Component] = []
    for index, value in enumerate(values):
        child = coerce_child(value, owner=owner, index=index)
        if child is not None:
            out.append(child)
    return out


def editable_attrs(field: str) -> dict[str, str]:
    """
    Attributes that make one rendered value editable in the browser.

    The ``data-field`` path is the contract the web editor writes back
    through, so it must match the extraction schema's key exactly — dotted for
    nesting, indexed for list rows (``plots.0.plot_no``). Every layout used to
    redeclare this as a private ``_ea()`` helper; centralizing it means a
    builder cannot render a value that silently is not editable.
    """
    return {"contenteditable": "true", "data-field": field}


class Component(ABC):
    """
    Base class for all renderable document components.

    Parameters:
        style: Optional inline styles applied to this component.
        css_class: Optional CSS class name(s) to add to the element.
        children: Nested child components (for container elements).
        attrs: Optional dict of arbitrary HTML attributes (e.g.
            ``{"contenteditable": "true", "data-field": "name"}``).
        field: Dotted path of the data field this element renders, e.g.
            ``"owner_name"`` or ``"plots.0.plot_no"``. Expands to
            ``contenteditable="true" data-field="<path>"`` — see
            ``editable_attrs``.
    """

    def __init__(
        self,
        *,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
        children: Optional[list[Component]] = None,
        attrs: Optional[dict[str, str]] = None,
        field: Optional[str] = None,
    ):
        self.style = style
        self.css_class = css_class
        self.children: list[Component] = coerce_children(
            children, owner=type(self).__name__
        )
        self.attrs: dict[str, str] = dict(attrs or {})
        self.field = field
        if field:
            # Explicit attrs win, so a layout can override either half.
            for key, value in editable_attrs(field).items():
                self.attrs.setdefault(key, value)

    def add(self, *components: Any) -> Component:
        """Append one or more child components. Returns self for chaining.

        Accepts the same values as the constructor — components, strings,
        numbers, or ``None`` — see :func:`coerce_child`.
        """
        self.children.extend(
            coerce_children(components, owner=type(self).__name__)
        )
        return self

    def _render_children(self) -> str:
        """Render all children to a concatenated HTML string."""
        return "".join(child.to_html() for child in self.children)

    def _build_attrs(self, extra_style: Optional[Style] = None) -> str:
        """
        Build the HTML attribute string for this element.

        Combines ``css_class``, ``style`` (merged with any extra_style),
        and arbitrary ``attrs`` into a string like
        ``class="foo" style="color:red" contenteditable="true"``.
        """
        from html_engine.styles import Style as _Style

        parts: list[str] = []

        if self.css_class:
            parts.append(f'class="{self.css_class}"')

        merged = self.style
        if extra_style:
            merged = (merged or _Style()).merge(extra_style)

        if merged:
            attr = merged.to_attr()
            if attr:
                parts.append(attr.strip())

        for key, val in self.attrs.items():
            # A raw style attribute bypasses Style.to_css() entirely, so it
            # needs normalizing here too — see html_engine.monochrome.
            if key.strip().lower() == "style":
                from html_engine.monochrome import normalize_declarations

                val = normalize_declarations(val)
            parts.append(f'{key}="{val}"')

        return (" " + " ".join(parts)) if parts else ""

    @abstractmethod
    def to_html(self) -> str:
        """Render this component to an HTML string."""
        ...
