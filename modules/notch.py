import fabric

from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.box import Box
from fabric.hyprland.widgets import ActiveWindow

from modules.controls import VolumeSlider
from modules.activewindow import ActiveWindowText


class Notch(Window):
  def __init__(self, **kwargs):
    super().__init__(
      name="notch",
      layer="top",
      anchor="top",
      exclusivity="none",
      margin="-43px 0 0 0",
      visible=True,
      all_visible=True,
    )

    self.volume_slider = VolumeSlider(parent=self)
    self.active_window = ActiveWindowText()

    self.permanent_menus = [ self.active_window ]
    self.menus = [
      self.volume_slider
    ]

    self.children = Box(
      name = "notch-container",
      orientation = "h",
      children = [
        Box(name="left-inverted-corner"),
        Box(
          name = "center-box",
          orientation = "v",
          children = self.permanent_menus + self.menus
        ),
        Box(name="right-inverted-corner")
      ]
    )

  def showMenu(self, menu):
    for other_menu in self.menus:
      other_menu.set_visible(False)
      other_menu.add_style_class("hidden")
    for permanent_menu in self.permanent_menus:
      permanent_menu.set_visible(False)
      permanent_menu.add_style_class("hidden")
    menu.remove_style_class("hidden")
    menu.set_visible(True)

  def hideMenu(self, menu):
    for permanent_menu in self.permanent_menus:
      permanent_menu.set_visible(True)
      permanent_menu.remove_style_class("hidden")
    menu.add_style_class("hidden")
    menu.set_visible(False)
