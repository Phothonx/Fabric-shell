import fabric
from fabric.hyprland.widgets import ActiveWindow
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow as Window

from modules.controls import VolumeSlider
from modules.datetime import dateTime
from modules.logo import logo
from modules.workspaces import workspaces


class Bar(Window):
    def __init__(self, **kwargs):
        super().__init__(
            name="bar",
            layer="top",
            anchor="left top right",
            exclusivity="auto",
            visible=True,
            all_visible=True,
            **kwargs
        )

        self.workspaces = workspaces()
        self.volume_slider = VolumeSlider()
        self.date_time = dateTime()
        self.active_window = ActiveWindow(name="hyprland-window")
        self.logo = logo

        self.left_widgets = [self.logo, self.workspaces]
        self.center_widgets = [self.active_window]
        self.righ_widgets = [self.date_time, self.volume_slider]

        self.bar_inner = CenterBox(
            name="bar-inner",
            start_children=Box(name="start-container", children=self.left_widgets),
            center_children=Box(
                name="center-container",
                children=[
                    Box(name="left-inverted-corner"),
                    Box(name="center-box", children=self.center_widgets),
                    Box(name="right-inverted-corner"),
                ],
            ),
            end_children=Box(name="end-container", children=self.righ_widgets),
        )

        self.children = self.bar_inner
