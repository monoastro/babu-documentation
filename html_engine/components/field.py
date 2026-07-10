"""
Field components: LabelValue pairs and FieldGroups.

These are the workhorses for form-like documents (certificates,
ID cards, applications) where information is presented as
label–value rows.
"""

from __future__ import annotations

import html
from typing import Optional, Union

from html_engine.components.base import Component
from html_engine.styles import Style


class LabelValue(Component):
    """
    A single label–value row rendered as a flex container.

    The label is displayed on the left with configurable width,
    followed by the value on the right.

    Parameters:
        label: The label text (e.g. "Full Name:").
        value: The value — can be a plain string or a Component
               (for nested layouts like multi-line addresses).
        escape: If True, string label and value will be HTML-escaped. Defaults to True.
        label_style: Override styles for the label element.
        value_style: Override styles for the value element.
        style: Styles for the outer container.
        label_width: CSS width for the label. Defaults to "240px".
    """

    _default_container_style = Style(
        display="flex",
        align_items="flex-start",
    )

    _default_label_style = Style(
        font_weight="bold",
        flex_shrink="0",
    )

    _default_value_style = Style(
        flex="1",
    )

    def __init__(
        self,
        label: str,
        value: Union[str, Component] = "",
        *,
        escape: bool = True,
        label_style: Optional[Style] = None,
        value_style: Optional[Style] = None,
        style: Optional[Style] = None,
        label_width: str = "240px",
        css_class: Optional[str] = None,
    ):
        merged_container = self._default_container_style.merge(style)
        super().__init__(style=merged_container, css_class=css_class)
        self.label = label
        self.value = value
        self.escape = escape
        self.label_width = label_width

        self.label_style = self._default_label_style.clone(
            width=label_width
        ).merge(label_style)

        self.value_style = self._default_value_style.merge(value_style)

    def to_html(self) -> str:
        attrs = self._build_attrs()
        label_attrs = self.label_style.to_attr()
        value_attrs = self.value_style.to_attr()

        # Value can be a string or a component
        if isinstance(self.value, Component):
            value_html = self.value.to_html()
        else:
            value_html = html.escape(str(self.value)) if self.escape else str(self.value)

        label_html = html.escape(self.label) if self.escape else self.label

        return (
            f"<div{attrs}>"
            f"<div{label_attrs}>{label_html}</div>"
            f"<div{value_attrs}>{value_html}</div>"
            f"</div>"
        )


class FieldGroup(Component):
    """
    A vertical stack of LabelValue rows or other components.

    Renders as a ``<div>`` with each child on its own line,
    with configurable vertical spacing.

    Parameters:
        children: The components to stack vertically.
        spacing: CSS margin-bottom between items. Defaults to "18px".
        style: Override styles for the outer container.
    """

    def __init__(
        self,
        *children: Component,
        spacing: str = "18px",
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class, children=list(children))
        self.spacing = spacing

    def to_html(self) -> str:
        attrs = self._build_attrs()
        items: list[str] = []
        for i, child in enumerate(self.children):
            # Add spacing via margin-bottom except on the last item
            if i < len(self.children) - 1:
                wrapper_style = f' style="margin-bottom:{self.spacing}"'
            else:
                wrapper_style = ""
            items.append(f"<div{wrapper_style}>{child.to_html()}</div>")
        return f"<div{attrs}>{''.join(items)}</div>"


class MultiFieldRow(Component):
    """
    A horizontal row containing multiple label–value pairs.

    Useful for rows like:
        Full Name: Kamal Jaisi          Gender: Male

    Parameters:
        children: LabelValue components to lay out horizontally.
        style: Override styles for the flex container.
    """

    _default_style = Style(
        display="flex",
        align_items="flex-start",
    )

    def __init__(
        self,
        *children: Component,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        merged = self._default_style.merge(style)
        super().__init__(style=merged, css_class=css_class, children=list(children))

    def to_html(self) -> str:
        attrs = self._build_attrs()
        inner = "".join(child.to_html() for child in self.children)
        return f"<div{attrs}>{inner}</div>"
