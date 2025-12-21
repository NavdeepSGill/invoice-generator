import tkinter as tk
from tkinter import ttk


class ServicePage(tk.Frame):
    def __init__(self, parent, window):
        super().__init__(parent)
        tk.Label(master=self, text="Service Page", font=("Arial", 20)).pack()
