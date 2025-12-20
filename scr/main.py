"""simple invoice creator"""
import csv
import tkinter as tk
from tkinter import ttk
# import sv_ttk
from popup_entry import PopupEntry


FONT = ("Arial", 12)
PADDING_X, PADDING_Y = 12, 12
BUTTON_COLOR = "#e8e8e8"


def read_client_file() -> dict[str, list[str]]:
    """Return a dictionary with the name of the client as the key,
    and a list of their information as the value, read from the client_list.csv.
    If there is no client list, creates an empty file instead."""
    try:
        with open("client_list.csv", "r", newline="") as file:
            clients_data = {}
            reader = csv.reader(file)
            for row in reader:
                clients_data[row[0]] = row[1:]
        return clients_data
    except FileNotFoundError:
        with open("client_list.csv", "w", newline="") as _:
            pass
        return {}


def read_service_file() -> dict[str, float]:
    """Return a dictionary with the name of the service as the key,
    and its price as the value, read from the service_list.csv.
    If there is no service list, creates an empty file instead."""
    try:
        with open("service_list.csv", "r", newline="") as file:
            service_data = {}
            reader = csv.reader(file)
            for row in reader:
                service_data[row[0]] = float(row[1])
        return service_data
    except FileNotFoundError:
        with open("service_list.csv", "w", newline="") as _:
            pass
        return {}


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.clients = read_client_file()
        self.services = read_service_file()

        self.title("Invoice Generator")
        self.resizable(False, False)

        self.container = tk.Frame(master=self)
        self.container.pack()

        self.frames = {}

        for F in (MainPage, ClientPage, ServicePage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_remove()

        self.show_frame(MainPage)

    def show_frame(self, page):
        for f in self.frames.values():
            f.grid_remove()

        self.frames[page].grid()


class MainPage(tk.Frame):
    def __init__(self, parent, window):
        super().__init__(parent)

        info_frm = tk.Frame(master=self)
        info_frm.grid(row=0, column=0, padx=PADDING_X, pady=PADDING_Y)

        button_frm = tk.Frame(master=self)
        button_frm.grid(row=1, column=0, padx=PADDING_X, pady=PADDING_Y)

        service_frm = tk.Frame(master=self)
        service_frm.grid(row=0, column=1, rowspan=2, padx=PADDING_X, pady=PADDING_Y, sticky="nw")

        labels = ["Name", "Email", "Street", "City", "Province", "Postal Code"]
        self.entries = {}
        for i in range(len(labels)):
            lbl = ttk.Label(master=info_frm, text=f"{labels[i]}: ", font=FONT)
            lbl.grid(row=i, column=0, sticky="w", padx=(PADDING_X, 0), pady=PADDING_Y)
            if labels[i] == "Name":
                self.entries[labels[i]] = PopupEntry(master=info_frm, font=FONT, width=40,
                                                     values=list(window.clients.keys()),
                                                     command=lambda c=window.clients: self.set_info(c))
            else:
                self.entries[labels[i]] = ttk.Entry(master=info_frm, font=FONT, state="readonly")
            self.entries[labels[i]].grid(row=i, column=1, sticky="we", padx=(0, PADDING_X), pady=PADDING_Y)

        edit_client_btn = tk.Button(
            master=button_frm,
            text="Edit Clients",
            font=FONT,
            width=15,
            height=3,
            bg=BUTTON_COLOR,
            command=lambda: window.show_frame(ClientPage))
        edit_client_btn.grid(row=0, column=0, padx=PADDING_X, pady=PADDING_Y)
        edit_service_btn = tk.Button(
            master=button_frm,
            text="Edit Services",
            font=FONT,
            width=15,
            height=3,
            bg=BUTTON_COLOR,
            command=lambda: window.show_frame(ServicePage))
        edit_service_btn.grid(row=0, column=1, padx=PADDING_X, pady=PADDING_Y)

        service_lbl = ttk.Label(master=service_frm, text="Service: ", font=FONT)
        service_lbl.grid(row=0, column=0, sticky="w", padx=(PADDING_X, 0), pady=PADDING_Y)
        self.service_popup_entry = PopupEntry(master=service_frm, font=FONT, width=40,
                                              values=list(window.services.keys()))
        self.service_popup_entry.grid(row=0, column=1, sticky="we", padx=(0, PADDING_X), pady=PADDING_Y)
        service_btn = tk.Button(master=service_frm, text="Add Service", font=FONT,
                                bg=BUTTON_COLOR, command=lambda s=window.services: self.add_service(s))
        service_btn.grid(row=0, column=2)

        self.service_table = tk.Frame(master=service_frm)
        self.service_table.grid(row=1, column=0, columnspan=3, padx=PADDING_X, pady=PADDING_Y, sticky="ew")
        self.service_rows = []
        self.service_list = []  # list of lists with format [[price1, amount1], [price2, amount2], ...]
        headers = ["Services", "Price", "Amount"]
        for col, header in enumerate(headers):
            tk.Label(master=self.service_table, text=header, font=FONT + ("bold",), borderwidth=1, relief=tk.SOLID,
                     pady=3).grid(row=0, column=col, sticky="nsew")
        self.service_table.grid_columnconfigure(0, weight=1, minsize=370)
        self.service_table.grid_columnconfigure(1, weight=1, minsize=80)
        self.service_table.grid_columnconfigure(2, weight=1, minsize=99)

        # TODO continue here

    def set_info(self, clients):
        name = self.entries["Name"].get_value()
        labels = ["Email", "Street", "City", "Province", "Postal Code"]
        if name in clients:
            for i in range(len(labels)):
                self.change_entry_text(labels[i], clients[name][i])
        else:
            for i in range(len(labels)):
                self.change_entry_text(labels[i], "")

    def change_entry_text(self, entry, text):
        self.entries[entry].config(state="normal")
        self.entries[entry].delete(0, tk.END)
        self.entries[entry].insert(0, text)
        self.entries[entry].config(state="readonly")

    def price_format(self, price: float) -> str:
        return f"${price:.2f}"

    def add_service(self, services):
        if self.service_popup_entry.get() in services:
            lbl_service = tk.Label(master=self.service_table, text=self.service_popup_entry.get(), font=FONT,
                                   borderwidth=1, relief="solid", pady=3)
            price = services[self.service_popup_entry.get()]
            lbl_price = tk.Label(master=self.service_table, text=self.price_format(price), font=FONT,
                                 borderwidth=1, relief="solid", pady=3)
            frame_button = tk.Frame(master=self.service_table, borderwidth=1, relief="solid")
            btn_minus = tk.Button(master=frame_button, text=" – ", font=FONT)
            btn_minus.grid(row=0, column=0, padx=5, pady=3)
            lbl_amount = tk.Label(master=frame_button, text=1, font=FONT)
            lbl_amount.grid(row=0, column=1, pady=3)
            btn_plus = tk.Button(master=frame_button, text=" + ", font=FONT)
            btn_plus.grid(row=0, column=2, padx=5, pady=3)

            lbl_service.grid(row=len(self.service_rows) + 1, column=0, sticky="nsew")
            lbl_price.grid(row=len(self.service_rows) + 1, column=1, sticky="nsew")
            frame_button.grid(row=len(self.service_rows) + 1, column=2, sticky="nsew")

            row_widgets = [lbl_service, lbl_price, lbl_amount, frame_button]
            self.service_rows.append(row_widgets)

            price_amount = [price, 1]
            self.service_list.append(price_amount)

            btn_minus.config(command=lambda pr=price_amount, rw=row_widgets: self.decrease_amount(pr, rw))
            btn_plus.config(command=lambda pr=price_amount, rw=row_widgets: self.increase_amount(pr, rw))

            self.service_popup_entry.delete(0, tk.END)
        else:
            print(self.service_list)  # TODO remove debug

    def decrease_amount(self, price_amount, row_widgets):
        if price_amount[1] > 0:
            price_amount[1] -= 1
            if price_amount[1] > 0:
                row_widgets[2].config(text=price_amount[1])
            else:
                self.remove_service(row_widgets)
                self.service_list.remove(price_amount)

    def increase_amount(self, price_amount, row_widgets):
        price_amount[1] += 1
        row_widgets[2].config(text=price_amount[1])

    def remove_service(self, row_widgets):
        for widget in row_widgets:
            widget.grid_forget()
            widget.destroy()


class ClientPage(tk.Frame):
    def __init__(self, parent, window):
        super().__init__(parent)
        tk.Label(master=self, text="Client Page", font=("Arial", 20)).pack()


class ServicePage(tk.Frame):
    def __init__(self, parent, window):
        super().__init__(parent)
        tk.Label(master=self, text="Service Page", font=("Arial", 20)).pack()


if __name__ == "__main__":
    app = App()
    # sv_ttk.set_theme("light")
    app.mainloop()
