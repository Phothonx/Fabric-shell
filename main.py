import fabric
from fabric import Application
from modules.bar import Bar

if __name__ == "__main__":
    bar = Bar()
    app = Application("bar", bar)
    app.run()
