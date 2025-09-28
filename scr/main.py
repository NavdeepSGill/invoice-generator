"""simple invoice creator"""
import csv
import tkinter as tk
from tkinter import ttk
import sv_ttk

FONT = ("Arial", 12)
PADDING_X, PADDING_Y = 15, 15


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

    main_frm = ttk.Frame()
    main_frm.pack(padx=PADDING_X, pady=PADDING_Y)

    name_frm = ttk.Frame(master=main_frm)
    name_frm.grid(row=0, column=0, sticky='ew', padx=PADDING_X, pady=PADDING_Y)
    name_lbl = ttk.Label(master=name_frm, text="Client: ", font=FONT)
    name_lbl.pack(side=tk.LEFT)
    name_combobox = ttk.Combobox(master=name_frm, values=list(clients.keys()), width=30, font=FONT)
    name_combobox.pack(side=tk.LEFT)

    lables = ["Email", "Street", "City", "Province", "Postal Code"]
    entries = {}

    for i in range(len(lables)):
        frm = ttk.Frame(master=main_frm)
        frm.grid(row=i+1, column=0, sticky='ew', padx=PADDING_X, pady=PADDING_Y)
        lbl = ttk.Label(master=frm, text=f"{lables[i]}: ", font=FONT)
        lbl.pack(side=tk.LEFT)
        entries[lables[i]] = ttk.Entry(master=frm, font=FONT, state="readonly")
        entries[lables[i]].pack(side=tk.LEFT)

    sv_ttk.set_theme("light")
    root.mainloop()


if __name__ == "__main__":
    clients = read_client_file()
    build_interface()
