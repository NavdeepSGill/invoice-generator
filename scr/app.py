import tkinter as tk

from scr.data.client_repository import load_clients
from scr.data.service_repository import load_services
from scr.ui.client_page import ClientPage
from scr.ui.constants import PAGE_MAIN
from scr.ui.main_page import MainPage
from scr.ui.service_page import ServicePage


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.clients = load_clients()
        self.services = load_services()

        self.title("Invoice Generator")
        self.resizable(False, False)

        self.container = tk.Frame(master=self)
        self.container.pack()

        self.show_frame(PAGE_MAIN)

    def show_frame(self, page: str):
        for widget in self.container.winfo_children():
            widget.destroy()

        match page:
            case "main":
                frame = MainPage(self.container, self)
            case "client":
                frame = ClientPage(self.container, self)
            case "service":
                frame = ServicePage(self.container, self)
            case _:
                raise ValueError(f"Unknown page: {page}")

        frame.grid(row=0, column=0, sticky="nsew")
