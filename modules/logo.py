from fabric.hyprland.service import Hyprland
from fabric.utils.helpers import get_desktop_applications, get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.entry import Entry
from fabric.widgets.image import Image
from fabric.widgets.wayland import WaylandWindow
from fabric.widgets.window import Window


def create_launcher():
    hyprland = Hyprland()
    apps = get_desktop_applications()
    current_selection = 0
    current_page = 0
    apps_per_page = 15
    app_buttons = []
    filtered_apps = []

    launcher_window = WaylandWindow(
        title="app-launcher",
        size=(400, 500),
        layer="top",
        keyboard_mode="exclusive",
        name="app-launcher",
    )

    def setup_window_rules():
        hyprland.send_command("keyword windowrulev2 float,title:^(app-launcher)$")
        hyprland.send_command("keyword windowrulev2 center,title:^(app-launcher)$")
        hyprland.send_command("keyword windowrulev2 stayfocused,title:^(app-launcher)$")

    setup_window_rules()

    main_box = Box(orientation="vertical", spacing=10)
    search_entry = Entry(placeholder="Search applications...", h_expand=True)
    app_container = Box(orientation="vertical", spacing=5)

    def update_app_list(search_text=""):
        nonlocal current_selection, app_buttons, filtered_apps, current_page
        app_container.children = []
        app_buttons = []
        current_selection = 0
        current_page = 0

        filtered_apps = (
            [app for app in apps if search_text.lower() in app.name.lower()]
            if search_text
            else apps
        )

        display_current_page()

    def display_current_page():
        nonlocal current_selection, app_buttons
        app_container.children = []
        app_buttons = []
        current_selection = 0

        start_idx = current_page * apps_per_page
        end_idx = start_idx + apps_per_page
        page_apps = filtered_apps[start_idx:end_idx]

        for i, app in enumerate(page_apps):
            app_button = Button(label=app.name, h_expand=True)

            def make_click_handler(application):
                return lambda btn: (application.launch(), launcher_window.close())

            app_button.connect("clicked", make_click_handler(app))
            app_buttons.append((app_button, app))
            app_container.children = app_container.children + [app_button]

        update_selection()

    def update_selection():
        for i, (button, _) in enumerate(app_buttons):
            if i == current_selection:
                button.get_style_context().add_class("selected")
            else:
                button.get_style_context().remove_class("selected")

    def scroll_to_next_page():
        nonlocal current_page
        max_page = (len(filtered_apps) - 1) // apps_per_page
        if current_page < max_page:
            current_page += 1
            display_current_page()

    def scroll_to_prev_page():
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            display_current_page()

    def on_key_press(window, event):
        nonlocal current_selection

        if event.keyval == 65307:  # Escape
            window.close()
            return True
        elif event.keyval == 65362:  # Up arrow
            if app_buttons:
                if current_selection == 0:
                    scroll_to_prev_page()
                    if app_buttons:
                        current_selection = len(app_buttons) - 1
                        update_selection()
                else:
                    current_selection = max(0, current_selection - 1)
                    update_selection()
            return True
        elif event.keyval == 65364:  # Down arrow
            if app_buttons:
                if current_selection == len(app_buttons) - 1:
                    scroll_to_next_page()
                    current_selection = 0
                    update_selection()
                else:
                    current_selection = min(len(app_buttons) - 1, current_selection + 1)
                    update_selection()
            return True
        elif event.keyval == 65293:  # Enter
            if app_buttons:
                _, app = app_buttons[current_selection]
                app.launch()
                window.close()
            return True
        return False

    launcher_window.connect("key-press-event", on_key_press)
    search_entry.connect("changed", lambda entry: update_app_list(entry.get_text()))

    update_app_list()

    main_box.children = [search_entry, app_container]
    launcher_window.children = main_box
    launcher_window.show_all()

    search_entry.grab_focus()


logo = Button(
    name="logo",
    child=Image(
        size=20,
        image_file=get_relative_path("../assets/NixOS.png"),
    ),
)

logo.connect("clicked", lambda button: create_launcher())
