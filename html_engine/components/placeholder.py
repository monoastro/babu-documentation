"""
Placeholder components for document furniture the render cannot reproduce.

A source scan carries a photo, a round office seal, an embossed crest, a
handwritten signature, a QR block, a watermark. None of that survives OCR, and
none of it should be invented. What the render owes the reader is an outline in
the right place at the right size, so the verifier compares *layout* against
the scan rather than reporting a missing seal as lost content.

Every layout in this project was already drawing these by hand — an
``AbsoluteBox`` wrapping a ``Text`` with a border, a radius, a flex centring
trio, and a font size, repeated five times per document with slightly different
numbers each time. These components are that pattern, named.
"""

from __future__ import annotations

from typing import Optional

from html_engine.components.base import Component
from html_engine.components.grid import AbsoluteBox
from html_engine.components.text import Text
from html_engine.styles import Style


class PlaceholderBox(Component):
    """
    A labelled outline standing in for artwork that cannot be rendered.

    Renders a centred caption inside a bordered box::

        PlaceholderBox("Photo", width="110px", height="130px", field="photo")
        PlaceholderBox("Office Seal", shape="circle", size="98px")

    Parameters:
        label: Caption text drawn inside the box.
        width: CSS width. Defaults to *size* when given.
        height: CSS height. Defaults to *size* when given, else *width*
            (a square).
        size: Convenience for a square or circle — sets both dimensions.
        shape: ``"rect"`` (default), ``"rounded"``, or ``"circle"``.
        dashed: Draw a dashed border. The convention in this project is dashed
            for something a human still has to supply (a signature), solid for
            something the original document simply has (a seal).
        font_size: Caption size. Defaults to "13px".
        style: Extra styles merged over the box.
        field: Dotted data-field path, making the caption editable.
    """

    def __init__(
        self,
        label: str = "",
        *,
        width: Optional[str] = None,
        height: Optional[str] = None,
        size: Optional[str] = None,
        shape: str = "rect",
        dashed: bool = False,
        font_size: str = "13px",
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
        attrs: Optional[dict[str, str]] = None,
        field: Optional[str] = None,
    ):
        box_w = width or size
        box_h = height or size or box_w

        radius = None
        if shape == "circle":
            # 50% keeps the ellipse correct even when the box is not square,
            # which a fixed pixel radius would not.
            radius = "50%"
        elif shape == "rounded":
            radius = "6px"

        base = Style(
            width=box_w,
            height=box_h,
            border=f"2px {'dashed' if dashed else 'solid'} #000000",
            border_radius=radius,
            display="flex",
            align_items="center",
            justify_content="center",
            text_align="center",
            font_size=font_size,
            # Long captions in a small box must wrap rather than spill past
            # the border and collide with whatever sits next to it.
            padding="4px",
            box_sizing="border-box",
            overflow="hidden",
        )
        super().__init__(
            style=base.merge(style),
            css_class=css_class,
            attrs=attrs,
            field=field,
        )
        self.label = label

    def to_html(self) -> str:
        inner = Text(self.label).to_html() if self.label else ""
        return f"<div{self._build_attrs()}>{inner}</div>"


class Watermark(Component):
    """
    Faint centred text behind the page content.

    Absolutely positioned and non-interactive, so it never intercepts a click
    meant for an editable field underneath it, and never lands in the user's
    selection when they copy a paragraph.

    Under the monochrome rule a watermark can only be black, so *opacity* is
    the sole control over how faint it is. Keep it low: at the default 0.10 it
    reads as a background wash; much above 0.2 the vision verifier starts
    reporting the text over it as illegible.

    Parameters:
        text: The watermark string.
        font_size: Defaults to "86px".
        opacity: Defaults to "0.10".
        rotate: Degrees of rotation, e.g. -30. Omitted when None.
        top/left/width/height: Placement. Defaults to a centred band.
        style: Extra styles merged over the defaults.
    """

    def __init__(
        self,
        text: str = "",
        *,
        font_size: str = "86px",
        opacity: str = "0.10",
        rotate: Optional[float] = None,
        top: str = "50%",
        left: str = "50%",
        width: Optional[str] = None,
        height: Optional[str] = None,
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
    ):
        # The -50%/-50% translate centres the box on its own midpoint, so the
        # caller does not have to know the rendered text width to centre it.
        transform = "translate(-50%, -50%)"
        if rotate is not None:
            transform = f"{transform} rotate({rotate}deg)"

        base = Style(
            position="absolute",
            top=top,
            left=left,
            width=width,
            height=height,
            transform=transform,
            font_size=font_size,
            font_weight="bold",
            opacity=opacity,
            text_align="center",
            white_space="nowrap",
            # Behind everything, inert to input, invisible to selection —
            # the three properties that separate a watermark from a heading.
            z_index="0",
            pointer_events="none",
            user_select="none",
        )
        super().__init__(style=base.merge(style), css_class=css_class)
        self.text = text

    def to_html(self) -> str:
        return f"<div{self._build_attrs()}>{Text(self.text).to_html()}</div>"


class SignatureBlock(Component):
    """
    The signature cluster that closes an official letter.

    Stacks, top to bottom: blank signing space, an optional dashed box marking
    where the physical signature goes, the signatory's name, their title, and
    an optional round stamp outline::

        SignatureBlock(
            name="Ram Bahadur",
            title="Campus Chief",
            signature_label="(Signed)",
            stamp_label="Office Seal",
            name_field="signed_name",
        )

    Every part is optional — omit ``stamp_label`` and no stamp is drawn. The
    ``*_field`` arguments make the corresponding value editable, which matters
    because the signatory's name and title are extracted data even though the
    signature and stamp are not.

    Parameters:
        name: Signatory's name.
        title: Their office or position.
        signature_label: Caption for the dashed signing box. None omits it.
        stamp_label: Caption for the round stamp outline. None omits it.
        rule_gap: Blank height reserved above the block for a wet signature.
        align: ``"center"`` (default), ``"left"``, or ``"right"``.
        name_field/title_field/signature_field/stamp_field: Dotted data-field
            paths making each part editable.
    """

    def __init__(
        self,
        *,
        name: str = "",
        title: str = "",
        signature_label: Optional[str] = None,
        stamp_label: Optional[str] = None,
        rule_gap: str = "58px",
        align: str = "center",
        style: Optional[Style] = None,
        css_class: Optional[str] = None,
        name_field: Optional[str] = None,
        title_field: Optional[str] = None,
        signature_field: Optional[str] = None,
        stamp_field: Optional[str] = None,
    ):
        base = Style(
            display="flex",
            flex_direction="column",
            align_items={"left": "flex-start", "right": "flex-end"}.get(
                align, "center"
            ),
            text_align=align,
        )
        super().__init__(style=base.merge(style), css_class=css_class)
        self.name = name
        self.title = title
        self.signature_label = signature_label
        self.stamp_label = stamp_label
        self.rule_gap = rule_gap
        self.name_field = name_field
        self.title_field = title_field
        self.signature_field = signature_field
        self.stamp_field = stamp_field

    def to_html(self) -> str:
        from html_engine.components.spacer import Spacer

        parts: list[Component] = [Spacer(height=self.rule_gap)]

        if self.signature_label is not None:
            # Dashed, because unlike the seal this is space for something a
            # human still has to add by hand.
            parts.append(
                PlaceholderBox(
                    self.signature_label,
                    dashed=True,
                    font_size="15px",
                    field=self.signature_field,
                    style=Style(
                        width="auto",
                        height="auto",
                        padding="6px 13px",
                        margin_bottom="5px",
                    ),
                )
            )
        if self.name:
            parts.append(
                Text(
                    self.name,
                    field=self.name_field,
                    style=Style(font_weight="bold", font_size="18px", margin_bottom="2.5px"),
                )
            )
        if self.title:
            parts.append(
                Text(
                    self.title,
                    field=self.title_field,
                    style=Style(font_size="16px", margin_bottom="8px"),
                )
            )
        if self.stamp_label is not None:
            parts.append(
                PlaceholderBox(
                    self.stamp_label,
                    size="110px",
                    shape="circle",
                    font_size="13.5px",
                    field=self.stamp_field,
                    style=Style(margin="5px auto 2px auto"),
                )
            )

        inner = "".join(p.to_html() for p in parts)
        return f"<div{self._build_attrs()}>{inner}</div>"


def corner_box(
    label: str,
    *,
    corner: str = "top-left",
    size: str = "68px",
    offset: str = "18px",
    shape: str = "rounded",
    field: Optional[str] = None,
) -> AbsoluteBox:
    """
    A placeholder pinned to one corner of the page — crest, QR block, stamp.

    ``corner`` is one of ``top-left``, ``top-right``, ``bottom-left``,
    ``bottom-right``. Returns an ``AbsoluteBox``, so it must be added to a
    ``Document`` (whose ``.page`` is ``position: relative``) or to another
    positioned container.
    """
    vertical, _, horizontal = corner.partition("-")
    placement = {
        vertical: offset,
        horizontal: offset,
    }
    return AbsoluteBox(
        PlaceholderBox(label, size=size, shape=shape, field=field),
        **placement,
    )
