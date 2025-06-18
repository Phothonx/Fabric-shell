from fabric.utils.helpers import get_relative_path
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from modules.launcher import create_launcher

logo = Button(
    name="logo",
    child=Image(
        size=20,
        image_file=get_relative_path("../assets/NixOS.png"),
    ),
)

logo.connect("clicked", lambda button: create_launcher())
