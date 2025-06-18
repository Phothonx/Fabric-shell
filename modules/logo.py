from fabric.utils.helpers import get_relative_path
from fabric.widgets.button import Button
from fabric.widgets.image import Image

from modules.launcher import Launcher

logo = Button(
    name="logo",
    child=Image(
        size=20,
        image_file=get_relative_path("../assets/NixOS.png"),
    ),
)
launcher = Launcher()
logo.connect("clicked", lambda button: launcher.show())
