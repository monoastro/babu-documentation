"""
List components: ListItem, UnorderedList, OrderedList.
"""

from __future__ import annotations

import html
from typing import Optional, Union

from html_engine.components.base import Component
from html_engine.styles import Style


class ListItem(Component):
    """
    Renders a list item ``<li>``.

    Parameters:
        content: String content or nested Component.
        escape: If True, string content will be HTML-escaped. Defaults to True.
        style: Optional inline styles.
        css_class: Optional CSS class name(s).
    """

    def __init__(
        self,
        content: Union[str, Component] = "",
        *,
        escape: bool = True,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class)
        self.content = content
        self.escape = escape

    def to_html(self) -> str:
        attrs = self._build_attrs()
        if isinstance(self.content, Component):
            inner = self.content.to_html()
        else:
            inner = html.escape(str(self.content)) if self.escape else str(self.content)
        return f"<li{attrs}>{inner}</li>"


class UnorderedList(Component):
    """
    Renders an unordered list ``<ul>``.

    Parameters:
        items: List items — can be strings, ListItem components, or other Components.
        style: Optional inline styles for the list container.
        css_class: Optional CSS class name(s).
        item_style: Optional style preset applied to text items.
    """

    def __init__(
        self,
        *items: Union[str, ListItem, Component],
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
        item_style: Optional[Style] = None,
    ):
        children: list[Component] = []
        for item in items:
            if isinstance(item, ListItem):
                children.append(item)
            elif isinstance(item, Component):
                children.append(ListItem(item))
            else:
                children.append(ListItem(str(item), style=item_style))

        super().__init__(style=style, css_class=css_class, children=children)

    def to_html(self) -> str:
        attrs = self._build_attrs()
        inner = self._render_children()
        return f"<ul{attrs}>{inner}</ul>"


class OrderedList(Component):
    """
    Renders an ordered list ``<ol>``.

    Parameters:
        items: List items — can be strings, ListItem components, or other Components.
        style: Optional inline styles for the list container.
        css_class: Optional CSS class name(s).
        item_style: Optional style preset applied to text items.
    """

    def __init__(
        self,
        *items: Union[str, ListItem, Component],
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
        item_style: Optional[Style] = None,
    ):
        children: list[Component] = []
        for item in items:
            if isinstance(item, ListItem):
                children.append(item)
            elif isinstance(item, Component):
                children.append(ListItem(item))
            else:
                children.append(ListItem(str(item), style=item_style))

        super().__init__(style=style, css_class=css_class, children=children)

    def to_html(self) -> str:
        attrs = self._build_attrs()
        inner = self._render_children()
        return f"<ol{attrs}>{inner}</ol>"
