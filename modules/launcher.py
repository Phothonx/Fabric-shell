from fabric.hyprland.service import Hyprland
from fabric.utils.helpers import get_desktop_applications
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.entry import Entry
from fabric.widgets.wayland import WaylandWindow


class Launcher(Box):
    def __init__(self):
        self.hyprland = Hyprland()
        self.apps = get_desktop_applications()

        self.current_selection = 0
        self.current_page = 0
        self.apps_per_page = 15
        self.app_buttons = []
        self.filtered_apps = []

        self.window = None
        self.built = False

    def setup_window_rules(self):
        self.hyprland.send_command("keyword windowrulev2 float,title:^(app-launcher)$")
        self.hyprland.send_command("keyword windowrulev2 center,title:^(app-launcher)$")
        self.hyprland.send_command(
            "keyword windowrulev2 stayfocused,title:^(app-launcher)$"
        )

    def build_ui(self):
        self.built = True

        self.window = WaylandWindow(
            title="app-launcher",
            size=(400, 500),
            layer="top",
            keyboard_mode="exclusive",
            name="app-launcher",
            visible=False,
        )

        self.setup_window_rules()

        self.main_box = Box(orientation="vertical", spacing=10)
        self.search_entry = Entry(placeholder="Search applications...", h_expand=True)
        self.app_container = Box(orientation="vertical", spacing=5)

        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("destroy", self.on_destroy)

        self.search_entry.connect(
            "changed", lambda entry: self.update_app_list(entry.get_text())
        )

        self.main_box.children = [self.search_entry, self.app_container]
        self.window.children = self.main_box

        self.update_app_list()

    def show(self):
        if self.window is None:
            self.build_ui()

        self.window.show_all()
        self.search_entry.grab_focus()

    def on_destroy(self, *args):
        self.window = None
        self.built = False
        self.app_buttons = []
        self.filtered_apps = []
        self.current_selection = 0
        self.current_page = 0

    def update_app_list(self, search_text=""):
        self.app_container.children = []
        self.app_buttons = []
        self.current_selection = 0
        self.current_page = 0

        self.filtered_apps = (
            [app for app in self.apps if search_text.lower() in app.name.lower()]
            if search_text
            else self.apps
        )

        self.display_current_page()

    def display_current_page(self):
        self.app_container.children = []
        self.app_buttons = []
        self.current_selection = 0

        start_idx = self.current_page * self.apps_per_page
        end_idx = start_idx + self.apps_per_page
        page_apps = self.filtered_apps[start_idx:end_idx]

        for app in page_apps:
            app_button = Button(label=app.name, h_expand=True)

            def make_click_handler(application):
                return lambda btn: (application.launch(), self.window.close())

            app_button.connect("clicked", make_click_handler(app))
            self.app_buttons.append((app_button, app))
            self.app_container.children += [app_button]

        self.update_selection()

    def update_selection(self):
        for i, (button, _) in enumerate(self.app_buttons):
            if i == self.current_selection:
                button.get_style_context().add_class("selected")
            else:
                button.get_style_context().remove_class("selected")

    def scroll_to_next_page(self):
        max_page = (len(self.filtered_apps) - 1) // self.apps_per_page
        if self.current_page < max_page:
            self.current_page += 1
            self.display_current_page()

    def scroll_to_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_current_page()

    def on_key_press(self, window, event):
        key = event.keyval

        if key == 65307:  # Escape
            self.window.close()
            return True
        elif key == 65362:  # Up arrow
            if self.app_buttons:
                if self.current_selection == 0:
                    self.scroll_to_prev_page()
                    if self.app_buttons:
                        self.current_selection = len(self.app_buttons) - 1
                        self.update_selection()
                else:
                    self.current_selection = max(0, self.current_selection - 1)
                    self.update_selection()
            return True
        elif key == 65364:  # Down arrow
            if self.app_buttons:
                if self.current_selection == len(self.app_buttons) - 1:
                    self.scroll_to_next_page()
                    self.current_selection = 0
                    self.update_selection()
                else:
                    self.current_selection = min(
                        len(self.app_buttons) - 1, self.current_selection + 1
                    )
                    self.update_selection()
            return True
        elif key == 65293:  # Enter
            if self.app_buttons:
                _, app = self.app_buttons[self.current_selection]
                app.launch()
                self.window.close()
            return True
        return False
