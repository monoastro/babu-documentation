"""
Abstract base class for all HTML Document Engine components.

Every renderable element (Text, Image, Table, etc.) inherits from
``Component`` and implements ``to_html()``.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from html_engine.styles import Style


class Component(ABC):
    """
    Base class for all renderable document components.

    Parameters:
        style: Optional inline styles applied to this component.
        css_class: Optional CSS class name(s) to add to the element.
        children: Nested child components (for container elements).
    """

    def __init__(
        self,
        *,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
        children: Optional[list[Component]] = None,
    ):
        self.style = style
        self.css_class = css_class
        self.children: list[Component] = children or []

    def add(self, *components: Component) -> Component:
        """Append one or more child components. Returns self for chaining."""
        self.children.extend(components)
        return self

    def _render_children(self) -> str:
        """Render all children to a concatenated HTML string."""
        return "".join(child.to_html() for child in self.children)

    def _build_attrs(self, extra_style: Optional[Style] = None) -> str:
        """
        Build the HTML attribute string for this element.

        Combines ``css_class`` and ``style`` (merged with any extra_style)
        into a string like ``class="foo" style="color:red"``.
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

        return (" " + " ".join(parts)) if parts else ""

    @abstractmethod
    def to_html(self) -> str:
        """Render this component to an HTML string."""
        ...
