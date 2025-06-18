from fabric.hyprland.widgets import ActiveWindow

class ActiveWindowText(ActiveWindow):
  def __init__(self, **kwargs):
    super().__init__(
      name="hyprland-window",
      v_expand=True,
      h_expand=False,
      h_align="center",
      v_align="center"
    )
