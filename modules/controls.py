from threading import Timer

from fabric.audio.service import Audio
from fabric.widgets.scale import Scale

audio = Audio()

class VolumeSlider(Scale):
  def setValue(self, *args):
    if audio.speaker:
      self.value = round(audio.speaker.volume)/100

      if self.timer:
        self.timer.cancel()
      self.parent.showMenu(self)
      self.timer = Timer(2, self.parent.hideMenu, args=(self,))
      self.timer.start()


  def __init__(self, **kwargs):
    super().__init__(
      name="control-slider",
      orientation="h",
    )

    self.timer = None
    self.parent = kwargs["parent"]

    audio.connect("changed", self.setValue)
