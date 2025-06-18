from threading import Timer

from fabric.audio.service import Audio
from fabric.widgets.scale import Scale


class VolumeSlider(Scale):
  def __init__(self, **kwargs):
    super().__init__(
      name="control-slider",
      orientation="h",
      visible=False
    )

    self.audio = Audio()
    self.timer = None
    self.parent = kwargs["parent"]

    self.audio.connect("notify::speaker", self.connectSpeaker)
    # self.connect("notify::value", self.setVolume)

  def connectSpeaker(self, *_):
    if self.audio.speaker:
      self.audio.speaker.connect("changed", self.on_speaker_changed)

  def on_speaker_changed(self, *_):
    self.setValue()
    self.setMuted()

  def setMuted(self, *_):
    if self.audio.speaker:
      if self.audio.speaker.muted:
        self.add_style_class("muted")
      else:
        self.remove_style_class("muted")
      self.resetShowTimer()

  def setValue(self, *_):
    if self.audio.speaker:
      self.value = self.audio.speaker.volume/100
      self.resetShowTimer()

  def setVolume(self, *_):
    if self.audio.speaker:
      self.audio.speaker.volume = self.value*100
      self.resetShowTimer()

  def resetShowTimer(self):
    if self.timer:
      self.timer.cancel()
    self.parent.showMenu(self)
    self.timer = Timer(3, self.parent.hideMenu, args=(self,))
    self.timer.start()
