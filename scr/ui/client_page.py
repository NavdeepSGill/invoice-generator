import tkinter as tk
from tkinter import ttk


class ClientPage(tk.Frame):
    def __init__(self, parent, window):
        super().__init__(parent)
        self.window = window
        tk.Label(master=self, text="Client Page", font=("Arial", 20)).pack()  # TODO remove placeholder
