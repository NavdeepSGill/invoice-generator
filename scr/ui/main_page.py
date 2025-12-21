import tkinter as tk
from tkinter import ttk

from scr.models.client import Client
from scr.models.service import ServiceItem
from scr.ui.constants import BUTTON_COLOR, FONT, PADDING_X, PADDING_Y, PAGE_CLIENT, PAGE_SERVICE
from scr.ui.widgets.popup_entry import PopupEntry


class MainPage(tk.Frame):
    def __init__(self, parent, window):
        super().__init__(parent)
        self.window = window

        info_frm = tk.Frame(master=self)
        info_frm.grid(row=0, column=0, padx=PADDING_X, pady=PADDING_Y)

        button_frm = tk.Frame(master=self)
        button_frm.grid(row=1, column=0, padx=PADDING_X, pady=PADDING_Y)

        service_frm = tk.Frame(master=self)
        service_frm.grid(row=0, column=1, rowspan=2, padx=PADDING_X, pady=PADDING_Y, sticky="nw")

        self.entries = {}
        for i, (attr, label) in enumerate(Client.FIELDS):
            lbl = ttk.Label(master=info_frm, text=f"{label}: ", font=FONT)
            lbl.grid(row=i, column=0, sticky="w", padx=(PADDING_X, 0), pady=PADDING_Y)
            self.entries[attr] = PopupEntry(master=info_frm, font=FONT, width=40,
                                            values=list(self.window.clients.get_attribute(attr)),
                                            command=lambda a=attr: self.set_info(a)
                                            )
            self.entries[attr].grid(row=i, column=1, sticky="we", padx=(0, PADDING_X), pady=PADDING_Y)

        edit_client_btn = tk.Button(master=button_frm, text="Edit Clients", font=FONT, width=15, height=3,
                                    bg=BUTTON_COLOR, command=lambda: self.window.show_frame(PAGE_CLIENT))
        edit_client_btn.grid(row=0, column=0, padx=PADDING_X, pady=PADDING_Y)
        edit_service_btn = tk.Button(master=button_frm, text="Edit Services", font=FONT, width=15, height=3,
                                     bg=BUTTON_COLOR, command=lambda: self.window.show_frame(PAGE_SERVICE))
        edit_service_btn.grid(row=0, column=1, padx=PADDING_X, pady=PADDING_Y)

        service_lbl = ttk.Label(master=service_frm, text="Service: ", font=FONT)
        service_lbl.grid(row=0, column=0, sticky="w", padx=(PADDING_X, 0), pady=PADDING_Y)
        self.service_popup_entry = PopupEntry(master=service_frm, font=FONT, width=40,
                                              values=self.window.services.get_names())
        self.service_popup_entry.grid(row=0, column=1, sticky="we", padx=(0, PADDING_X), pady=PADDING_Y)
        service_btn = tk.Button(master=service_frm, text="Add Service", font=FONT,
                                bg=BUTTON_COLOR, command=self.add_service)
        service_btn.grid(row=0, column=2)

        self.service_table = tk.Frame(master=service_frm)
        self.service_table.grid(row=1, column=0, columnspan=3, padx=PADDING_X, pady=PADDING_Y, sticky="ew")
        self.next_service_row = 1
        self.service_list = []
        for col, (attr, header) in enumerate(ServiceItem.FIELDS):
            tk.Label(master=self.service_table, text=header, font=FONT + ("bold",), borderwidth=1, relief=tk.SOLID,
                     pady=3).grid(row=0, column=col, sticky="nsew")
            self.service_table.grid_columnconfigure(col, weight=1, minsize=ServiceItem.COLUMN_MINSIZES[attr])

        # TODO continue here

    def set_info(self, attribute):
        entry = self.entries[attribute].get_value()
        if entry in self.window.clients.get_attribute(attribute):
            client = self.window.clients.get_client(attribute, entry)
            for attr, _ in Client.FIELDS:
                if attr != attribute:
                    self.entries[attr].delete(0, tk.END)
                    self.entries[attr].insert(0, getattr(client, attr))
        else:
            for attr, _ in Client.FIELDS:
                if attr != attribute:
                    self.entries[attr].delete(0, tk.END)

    def add_service(self):
        service_name = self.service_popup_entry.get()

        service = self.window.services.get(service_name)
        if service is None:
            print([(x.service.name, x.service.price, x.quantity) for x in self.service_list])  # TODO remove debug
            return

        for item in self.service_list:
            if item.service.name == service.name:
                item.quantity += 1
                item.quantity_label.config(text=item.quantity)
                self.service_popup_entry.delete(0, tk.END)
                return

        row_index = self.next_service_row
        self.next_service_row += 1

        item = ServiceItem(service)
        self.service_list.append(item)

        name_lbl = tk.Label(master=self.service_table, text=service.name, font=FONT, borderwidth=1,
                            relief="solid", pady=3)
        name_lbl.grid(row=row_index, column=0, sticky="nsew")

        price_lbl = tk.Label(master=self.service_table, text=f"${service.price:.2f}", font=FONT, borderwidth=1,
                             relief="solid", pady=3)
        price_lbl.grid(row=row_index, column=1, sticky="nsew")

        qty_frame = tk.Frame(master=self.service_table, borderwidth=1, relief="solid")

        btn_minus = tk.Button(qty_frame, text=" – ", font=FONT)  # text=" – "
        btn_minus.grid(row=0, column=0, padx=5, pady=3)  # padx=5, pady=3

        qty_lbl = tk.Label(qty_frame, text=item.quantity, font=FONT)
        qty_lbl.grid(row=0, column=1, pady=3)  # row=0, column=1, pady=3

        btn_plus = tk.Button(qty_frame, text=" + ", font=FONT)  # text=" + "
        btn_plus.grid(row=0, column=2, padx=5, pady=3)  # , pady=3

        qty_frame.grid(row=row_index, column=2, sticky="nsew")

        item.quantity_label = qty_lbl
        item.widgets = (name_lbl, price_lbl, qty_frame)

        btn_minus.config(command=lambda i=item: self._decrease_quantity(i))
        btn_plus.config(command=lambda i=item: self._increase_quantity(i))

        self.service_popup_entry.delete(0, tk.END)

    def _increase_quantity(self, item: ServiceItem):
        item.quantity += 1
        item.quantity_label.config(text=item.quantity)

    def _decrease_quantity(self, item: ServiceItem):
        item.quantity -= 1

        if item.quantity <= 0:
            for widget in item.widgets:
                widget.destroy()
            self.service_list.remove(item)
        else:
            item.quantity_label.config(text=item.quantity)
