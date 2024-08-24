import gi
import cairo
from enum import Enum
from typing import Literal
from collections.abc import Iterable
from fabric.core.service import Property
from fabric.widgets.widget import Widget
from fabric.utils.helpers import get_enum_member

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class CornerOrientation(Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4


class Corner(Gtk.DrawingArea, Widget):
    @Property(CornerOrientation, "readable")
    def orientation(self) -> CornerOrientation:
        return self._orientation

    def __init__(
        self,
        orientation: Literal["top-left", "top-right", "bottom-left", "bottom-right"]
        | CornerOrientation = CornerOrientation.TOP_RIGHT,
        name: str | None = None,
        visible: bool = True,
        all_visible: bool = False,
        style: str | None = None,
        tooltip_text: str | None = None,
        tooltip_markup: str | None = None,
        h_align: Literal["fill", "start", "end", "center", "baseline"]
        | Gtk.Align
        | None = None,
        v_align: Literal["fill", "start", "end", "center", "baseline"]
        | Gtk.Align
        | None = None,
        h_expand: bool = False,
        v_expand: bool = False,
        size: Iterable[int] | int | None = None,
        **kwargs,
    ):
        Gtk.DrawingArea.__init__(self)  # type: ignore
        Widget.__init__(
            self,
            name,
            visible,
            all_visible,
            style,
            tooltip_text,
            tooltip_markup,
            h_align,
            v_align,
            h_expand,
            v_expand,
            size,
            **kwargs,
        )
        self._orientation = get_enum_member(CornerOrientation, orientation)
        self.connect("draw", self.on_draw)

    def on_draw(self, widget: "Corner", cr: cairo.Context):
        aloc: cairo.Rectangle = self.get_allocation()  # type: ignore
        # ^ hear me out, Gtk.Allocation == Gdk.Rectangle == cairo.Rectangle
        width, height = aloc.width, aloc.height

        context: Gtk.StyleContext = self.get_style_context()
        background_color: Gdk.RGBA = context.get_background_color(Gtk.StateFlags.NORMAL)

        cr.save()

        Gdk.cairo_set_source_rgba(cr, background_color)

        # _this is fine_
        match self.orientation:
            case CornerOrientation.TOP_LEFT:
                cr.move_to(width, 0)
                cr.curve_to(0, 0, 0, height, 0, height)
                cr.line_to(0, 0)
            case CornerOrientation.TOP_RIGHT:
                cr.move_to(0, 0)
                cr.curve_to(width, 0, width, height, width, height)
                cr.line_to(width, 0)
            case CornerOrientation.BOTTOM_LEFT:
                cr.move_to(width, height)
                cr.curve_to(0, height, 0, 0, 0, 0)
                cr.line_to(0, height)
            case CornerOrientation.BOTTOM_RIGHT:
                cr.move_to(0, height)
                cr.curve_to(width, height, width, 0, width, 0)
                cr.line_to(width, height)

        cr.close_path()
        cr.fill()

        cr.restore()
        return
