from fabric.widgets.datetime import DateTime

def dateTime():
  return DateTime(
    name = "date-time",
    formatters = ["%H:%M"]
  )
