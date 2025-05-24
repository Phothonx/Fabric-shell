from fabric.widgets.datetime import DateTime

class DateTimeWidget(DateTime):
  def __init__(self, **kwargs) -> None:
    super().__init__(
      name = "date-time",
      formatter = [ "%H:M" ]
    )
