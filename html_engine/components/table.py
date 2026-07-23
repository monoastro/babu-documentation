"""
Table components: Table, TableRow, TableCell.

Supports both simple table creation from lists of data and
fine-grained control via TableRow/TableCell objects.
"""

from __future__ import annotations

import html
from typing import Optional, Sequence, Union

from html_engine.components.base import Component
from html_engine.styles import Style


class TableCell(Component):
    """
    A single table cell (``<td>`` or ``<th>``).

    Parameters:
        content: Cell content — a string or a nested Component.
        colspan: Number of columns this cell spans.
        rowspan: Number of rows this cell spans.
        is_header: If True, renders as ``<th>`` instead of ``<td>``.
        escape: If True, string content will be HTML-escaped. Defaults to True.
        style: Inline styles for this cell.
    """

    def __init__(
        self,
        content: Union[str, Component] = "",
        *,
        colspan: int = 1,
        rowspan: int = 1,
        is_header: bool = False,
        escape: bool = True,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        super().__init__(style=style, css_class=css_class)
        self.content = content
        self.colspan = colspan
        self.rowspan = rowspan
        self.is_header = is_header
        self.escape = escape

    def to_html(self) -> str:
        tag = "th" if self.is_header else "td"
        attrs = self._build_attrs()

        span_attrs = ""
        if self.colspan > 1:
            span_attrs += f' colspan="{self.colspan}"'
        if self.rowspan > 1:
            span_attrs += f' rowspan="{self.rowspan}"'

        if isinstance(self.content, Component):
            inner = self.content.to_html()
        else:
            inner = html.escape(str(self.content)) if self.escape else str(self.content)

        return f"<{tag}{span_attrs}{attrs}>{inner}</{tag}>"


class TableRow(Component):
    """
    A table row (``<tr>``) containing one or more cells.

    Parameters:
        cells: TableCell objects, or plain strings (auto-wrapped in TableCell).
        style: Inline styles for the ``<tr>``.
    """

    def __init__(
        self,
        *cells: Union[str, TableCell, Component],
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
        cell_style: Optional[Style] = None,
    ):
        super().__init__(style=style, css_class=css_class)
        self.cell_style = cell_style
        self.cells: list[TableCell] = []
        for cell in cells:
            if isinstance(cell, TableCell):
                self.cells.append(cell)
            else:
                self.cells.append(TableCell(cell, style=cell_style))

    def to_html(self) -> str:
        attrs = self._build_attrs()
        inner = "".join(cell.to_html() for cell in self.cells)
        return f"<tr{attrs}>{inner}</tr>"


class Table(Component):
    """
    A full ``<table>`` element.

    Can be built from:
    - Explicit ``TableRow`` objects passed as children.
    - Simple data via ``headers`` and ``rows`` lists.

    Parameters:
        headers: Optional list of header strings.
        rows: Optional list of row data (each row is a list of strings).
        style: Styles for the ``<table>`` element.
        header_style: Styles applied to ``<th>`` cells.
        cell_style: Styles applied to ``<td>`` cells.
        children: Explicit TableRow objects.
    """

    _default_style = Style(
        border_collapse="collapse",
        width="100%",
    )

    def __init__(
        self,
        *,
        headers: Optional[Sequence[Union[str, TableRow, TableCell]]] = None,
        rows: Optional[Sequence[Sequence[str]]] = None,
        style: Optional[Style] = None,
        header_style: Optional[Style] = None,
        cell_style: Optional[Style] = None,
        children: Optional[list[TableRow]] = None,
        thead_rows: Optional[list[TableRow]] = None,
        tfoot_rows: Optional[list[TableRow]] = None,
        css_class: Optional[str] = None,
    ):
        merged = self._default_style.merge(style)
        super().__init__(style=merged, css_class=css_class, children=children or [])
        self.headers = headers
        self.rows = rows
        self.header_style = header_style
        self.cell_style = cell_style
        self.thead_rows = thead_rows
        self.tfoot_rows = tfoot_rows

    def to_html(self) -> str:
        attrs = self._build_attrs()
        parts: list[str] = [f"<table{attrs}>"]

        # Render header row from simple data or direct list of TableRows
        if self.thead_rows:
            parts.append("<thead>")
            for row in self.thead_rows:
                parts.append(row.to_html())
            parts.append("</thead>")
        elif self.headers:
            parts.append("<thead>")
            # If the user passed TableRow objects directly in headers
            if all(isinstance(h, TableRow) for h in self.headers):
                for row in self.headers:
                    parts.append(row.to_html())
            else:
                parts.append("<tr>")
                for h in self.headers:
                    if isinstance(h, TableCell):
                        h.is_header = True
                        parts.append(h.to_html())
                    elif isinstance(h, Component):
                        parts.append(TableCell(h, is_header=True, style=self.header_style).to_html())
                    else:
                        parts.append(TableCell(str(h), is_header=True, style=self.header_style).to_html())
                parts.append("</tr>")
            parts.append("</thead>")

        # Render body rows from simple data or children
        has_tbody = False
        if self.rows or self.children:
            parts.append("<tbody>")
            has_tbody = True

        if self.rows:
            for row_data in self.rows:
                row = TableRow(*row_data, cell_style=self.cell_style)
                parts.append(row.to_html())

        # Render explicit TableRow children
        if self.children:
            for child in self.children:
                parts.append(child.to_html())

        if has_tbody:
            parts.append("</tbody>")

        # Render footer rows
        if self.tfoot_rows:
            parts.append("<tfoot>")
            for row in self.tfoot_rows:
                parts.append(row.to_html())
            parts.append("</tfoot>")

        parts.append("</table>")
        return "".join(parts)
