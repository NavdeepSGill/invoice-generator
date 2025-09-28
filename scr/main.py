"""simple invoice creator"""
import csv
import tkinter as tk
from tkinter import ttk
import sv_ttk

FONT = ("Arial", 12)
PADDING_X, PADDING_Y = 12, 12


def read_client_file() -> dict[str, list[str]]:
    """Return a string dictionary with the name of the client as the key,
    and a list of their information as the value, read from the client_list.txt.
    If there is no client list, creates an empty file instead."""
    try:
        with open("client_list.csv", 'r', newline='') as file:
            clients_data = {}
            reader = csv.reader(file)
            for row in reader:
                clients_data[row[0]] = row[1:]
        return clients_data
    except FileNotFoundError:
        with open("client_list.csv", 'w', newline='') as _:
            pass
        return {}


def build_interface():
    """Builds and displays the UI"""
    root = tk.Tk()
    root.title("Invoice Generator")
    root.resizable(False, False)

    info_frm = tk.Frame()
    info_frm.pack(padx=PADDING_X, pady=PADDING_Y)

    lables = ["Name", "Email", "Street", "City", "Province", "Postal Code"]
    entries = {}

    for i in range(len(lables)):
        lbl = ttk.Label(master=info_frm, text=f"{lables[i]}: ", font=FONT)
        lbl.grid(row=i, column=0, sticky='w', padx=(PADDING_X, 0), pady=PADDING_Y)
        if lables[i] == "Name":
            entries[lables[i]] = ttk.Combobox(master=info_frm, font=FONT, width=27, values=list(clients.keys()))
        else:
            entries[lables[i]] = ttk.Entry(master=info_frm, font=FONT, width=30, state="readonly")
        entries[lables[i]].grid(row=i, column=1, sticky='e', padx=(0, PADDING_X), pady=PADDING_Y)

    sv_ttk.set_theme("light")
    root.mainloop()


if __name__ == "__main__":
    clients = read_client_file()
    build_interface()
