import fabric
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow as Window

from modules.datetime import DateTimeWidget
from modules.logo import logo
from modules.workspaces import WorkspacesWidget


class Bar(Window):
    def __init__(self, **kwargs):
        super().__init__(
            name="bar",
            layer="top",
            anchor="left top right",
            exclusivity="auto",
            visible=True,
            all_visible=True,
        )

        self.workspaces = WorkspacesWidget()
        self.date_time = DateTimeWidget()

        self.logo = logo

        self.left_widgets = [self.logo, self.workspaces]
        self.righ_widgets = [
            self.date_time,
        ]

        self.bar_inner = CenterBox(
            name="bar-inner",
            start_children=Box(
                spacing=5,
                name="start-container",
                orientation="h",
                children=self.left_widgets,
            ),
            end_children=Box(
                spacing=5,
                name="end-container",
                orientation="h",
                children=self.righ_widgets,
            ),
        )

        self.children = self.bar_inner
