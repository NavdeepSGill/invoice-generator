import tkinter as tk

from scr.data.client_repository import load_clients
from scr.data.service_repository import load_services
from scr.ui.client_page import ClientPage
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

        self.show_frame("main")

    def show_frame(self, page: str):
        for widget in self.container.winfo_children():
            widget.grid_remove()
        match page:
            case "main":
                MainPage(self.container, self).grid()
            case "client":
                ClientPage(self.container, self).grid()
            case "service":
                ServicePage(self.container, self).grid()
