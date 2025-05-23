from fabric.hyprland.widgets import Workspaces, WorkspaceButton
from fabric.widgets.box import Box

def button_factory(id:int):
  # label = str(id) if id != -99 else "0"
  return WorkspaceButton(
    name="workspace-button",
    id=id,
    label="",
    v_expand=False,
    h_expand=False,
    h_align="center",
    v_align="center",
  )

def workspaces():
  return Workspaces(
    name = "workspaces",
    buttons = [ button_factory(i) for i in range(1, 10) ],
    empty_scroll = True,
    buttons_factory = button_factory
  )
