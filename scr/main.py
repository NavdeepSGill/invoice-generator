"""simple invoice creator"""
import csv
import tkinter as tk
from tkinter import ttk
# import sv_ttk

FONT = ("Arial", 12)
PADDING_X, PADDING_Y = 12, 12


def read_client_file() -> dict[str, list[str]]:
    """Return a dictionary with the name of the client as the key,
    and a list of their information as the value, read from the client_list.csv.
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


def read_service_file() -> dict[str, int]:
    """Return a dictionary with the name of the service as the key,
    and its price as the value, read from the service_list.csv.
    If there is no service list, creates an empty file instead."""
    try:
        with open("service_list.csv", 'r', newline='') as file:
            service_data = {}
            reader = csv.reader(file)
            for row in reader:
                service_data[row[0]] = int(row[1])
        return service_data
    except FileNotFoundError:
        with open("service_list.csv", 'w', newline='') as _:
            pass
        return {}


def build_interface():
    """Builds and displays the UI"""
    root = tk.Tk()
    root.title("Invoice Generator")
    root.resizable(False, False)

    info_frm = tk.Frame()
    info_frm.grid(row=0, column=0, padx=PADDING_X, pady=PADDING_Y)

    button_frm = tk.Frame()
    button_frm.grid(row=0, column=1, padx=(30, PADDING_X), pady=PADDING_Y)

    service_frm = tk.Frame(bg="red")
    service_frm.grid(row=1, column=0, columnspan=2, padx=PADDING_X, pady=PADDING_Y)

    labels = ["Name", "Email", "Street", "City", "Province", "Postal Code"]
    entries = {}
    for i in range(len(labels)):
        lbl = ttk.Label(master=info_frm, text=f"{labels[i]}: ", font=FONT)
        lbl.grid(row=i, column=0, sticky='w', padx=(PADDING_X, 0), pady=PADDING_Y)
        if labels[i] == "Name":
            entries[labels[i]] = ttk.Combobox(master=info_frm, font=FONT, width=30, values=list(clients.keys()))
        else:
            entries[labels[i]] = ttk.Entry(master=info_frm, font=FONT, state="readonly")
        entries[labels[i]].grid(row=i, column=1, sticky='we', padx=(0, PADDING_X), pady=PADDING_Y)

    edit_client_btn = tk.Button(master=button_frm, text="Edit Client", font=FONT, width=15, height=5)
    edit_client_btn.grid(row=0, column=0, padx=PADDING_X, pady=PADDING_Y)

    edit_service_btn = tk.Button(master=button_frm, text="Edit Service", font=FONT, width=15, height=5)
    edit_service_btn.grid(row=1, column=0, padx=PADDING_X, pady=PADDING_Y)

    # TODO replace placeholder label
    service_lbl = ttk.Label(master=service_frm, text="Placeholder")
    service_lbl.pack()

    # sv_ttk.set_theme("light")
    root.mainloop()


if __name__ == "__main__":
    clients = read_client_file()
    services = read_service_file()
    build_interface()
