from fabric.audio.service import Audio
from fabric.widgets.label import Label
from fabric.widgets.scale import Scale

audio = Audio()


class VolumeSlider(Scale):
    def setVolume(self, *args):
        if audio.speaker:
            self.value = round(audio.speaker.volume) / 100

    def __init__(self, **kwargs):
        super().__init__(
            name="control-slider",
            orientation="h",
            **kwargs,
        )
        audio.connect("changed", self.setVolume)
