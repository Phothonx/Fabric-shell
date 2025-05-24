from fabric import Application
from modules.bar import Bar
from modules.notch import Notch
from fabric.utils import monitor_file, get_relative_path

if __name__ == "__main__":
  bar = Bar()
  notch = Notch()

  app = Application("fabric-shell", bar, notch)

  app.set_stylesheet_from_file(get_relative_path("main.css"))
  app.run()
