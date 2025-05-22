import fabric
from fabric.widgets.wayland import WaylandWindow as Window

from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox

from fabric.hyprland.widgets import Workspaces, WorkspaceButton

class Bar(Window):
  def __init__(self, **kwargs):
    super().__init__(
      name = "bar",
      layer="top",
      anchor="left top right",
      exclusivity="auto",
      visible = True,
      all_visible = True,
      **kwargs
    )

    self.workspaces = Workspaces(
      buttons = [ WorkspaceButton(id=i, label=str(i)) for i in range(1, 10) ],
      empty_scroll=True,
    )

    self.bar_inner = CenterBox(
      name = "bar_inner",
      h_align="fill",
      v_align="fill",
      start_children = Box(
        children = [
          self.workspaces
        ]
      ),
      center_children = None,
      end_children = None,
    )

    self.children = [
      self.bar_inner
    ]
