import sys
import tkinter as tk
from pathlib import Path

from src.data.client_repository import ClientRepository
from src.data.service_repository import ServiceRepository
from src.data.settings_repository import SettingsRepository
from src.ui.client_page import ClientPage
from src.constants import ACTIVE_BG, FG, HOVER_BG, NAV_BG, PAGE_CLIENT, PAGE_MAIN, PAGE_SERVICE, PAGE_SETTINGS
from src.ui.main_page import MainPage
from src.ui.service_page import ServicePage
from src.ui.settings_page import SettingsPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        data_dir = self.app_data_dir()
        data_dir.mkdir(parents=True, exist_ok=True)

        self.client_repo = ClientRepository(str(data_dir / "client_list.csv"))
        self.service_repo = ServiceRepository(str(data_dir / "service_list.csv"))
        self.settings_repo = SettingsRepository(str(data_dir / "settings.json"))

        self.title("Invoice Generator")
        self.geometry("+100+50")
        self.resizable(False, False)
        self.current_page = None

        navigation = tk.Frame(self, bg=NAV_BG)
        navigation.pack(fill="x")

        def nav_button(parent, text, command=None):
            btn = tk.Label(master=parent, text=text, bg=NAV_BG, fg=FG, padx=12, pady=5, cursor="hand2")

            def on_enter(_):
                if btn["bg"] != ACTIVE_BG:
                    btn.config(bg=HOVER_BG)

            def on_leave(_):
                if btn["bg"] != ACTIVE_BG:
                    btn.config(bg=NAV_BG)

            def on_click(_):
                if command:
                    command()

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn.bind("<Button-1>", on_click)

            return btn

        self.nav_buttons = []
        self.nav_buttons.append(nav_button(navigation, "Create Invoice", lambda: self.show_frame(PAGE_MAIN)))
        self.nav_buttons.append(nav_button(navigation, "Edit Clients", lambda: self.show_frame(PAGE_CLIENT)))
        self.nav_buttons.append(nav_button(navigation, "Edit Services", lambda: self.show_frame(PAGE_SERVICE)))
        self.nav_buttons.append(nav_button(navigation, "Edit Business Settings",
                                           lambda: self.show_frame(PAGE_SETTINGS)))

        for b in self.nav_buttons:
            b.pack(side="left")

        self.container = tk.Frame(master=self)
        self.container.pack()

        if not self.settings_repo.load():
            self.show_frame(PAGE_SETTINGS)
        else:
            self.show_frame(PAGE_MAIN)

    def show_frame(self, page: str):
        if self.current_page:
            if not self.current_page.can_leave():
                return

        if self.current_page:
            self.current_page.destroy()

        if page == PAGE_MAIN:
            self.clients = self.client_repo.load()
            self.services = self.service_repo.load()

        match page:
            case "main":
                frame = MainPage(self.container, self)
                self.set_active(self.nav_buttons[0])
            case "client":
                frame = ClientPage(self.container, self)
                self.set_active(self.nav_buttons[1])
            case "service":
                frame = ServicePage(self.container, self)
                self.set_active(self.nav_buttons[2])
            case "settings":
                frame = SettingsPage(self.container, self)
                self.set_active(self.nav_buttons[3])
            case _:
                raise ValueError(f"Unknown page: {page}")

        self.current_page = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def set_active(self, active_btn):
        for bnt in self.nav_buttons:
            bnt.config(bg=NAV_BG)
        active_btn.config(bg=ACTIVE_BG)

    def app_data_dir(self, app_name="InvoiceGenerator"):
        if sys.platform == "win32":
            return Path.home() / "AppData" / "Local" / app_name
        else:
            return Path.home() / f".{app_name.lower()}"
