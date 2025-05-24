from fabric.hyprland.widgets import Workspaces, WorkspaceButton

class WorkspacesWidget(Workspaces):
  def __init__(self, **kwargs) -> None:
    super().__init__(
      name = "workspaces",
      buttons = [ self.button_factory(i) for i in range(1, 10) ],
      empty_scroll = True,
      buttons_factory = self.button_factory
    )

  def button_factory(self, id:int):
    # label = str(id) if id != -99 else "0"
    return None if id == -99 else WorkspaceButton(
      name="workspace-button",
      id=id,
      label="",
      v_expand=False,
      h_expand=False,
      h_align="center",
      v_align="center",
    )
