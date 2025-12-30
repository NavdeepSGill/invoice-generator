import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from src.models.client import Client
from src.models.pdf_generator import download_pdf
from src.models.service import ServiceItem
from src.constants import BUTTON_COLOR, FONT, HST, PADDING_X, PADDING_Y
from src.ui.base_page import Page
from src.ui.widgets.popup_entry import PopupEntry


class MainPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        info_frm = tk.Frame(master=self)
        info_frm.grid(row=0, column=0, padx=PADDING_X, pady=PADDING_Y)

        service_frm = tk.Frame(master=self)
        service_frm.grid(row=0, column=1, rowspan=2, padx=PADDING_X, pady=PADDING_Y, sticky="nsew")

        # Client Information Frame
        (ttk.Label(master=info_frm, text="Search for Client", font=("Arial", 20, "bold"))
         .grid(row=0, column=0, columnspan=2, sticky="w", padx=PADDING_X, pady=PADDING_Y))
        self.entries = {}
        for i, (attr, label) in enumerate(Client.FIELDS):
            lbl = ttk.Label(master=info_frm, text=f"{label}: ", font=FONT)
            lbl.grid(row=i + 1, column=0, sticky="w", padx=(PADDING_X, 0), pady=PADDING_Y)
            self.entries[attr] = PopupEntry(master=info_frm, font=FONT, width=40,
                                            values=list(self.app.clients.get_attribute(attr)),
                                            command=lambda a=attr: self.set_info(a)
                                            )
            self.entries[attr].grid(row=i + 1, column=1, sticky="we", padx=(0, PADDING_X), pady=PADDING_Y)

        # Service Table Frame
        (ttk.Label(master=service_frm, text="Enter Services", font=("Arial", 20, "bold"))
         .grid(row=0, column=0, columnspan=3, sticky="w", padx=PADDING_X, pady=PADDING_Y))
        service_lbl = ttk.Label(master=service_frm, text="Service: ", font=FONT)
        service_lbl.grid(row=1, column=0, sticky="w", padx=(PADDING_X, 0), pady=PADDING_Y)
        self.service_popup_entry = PopupEntry(master=service_frm, font=FONT, width=40,
                                              values=self.app.services.get_names())
        self.service_popup_entry.grid(row=1, column=1, sticky="we", padx=(0, PADDING_X), pady=PADDING_Y)
        service_btn = tk.Button(master=service_frm, text="Add Service", font=FONT,
                                bg=BUTTON_COLOR, command=self.add_service)
        service_btn.grid(row=1, column=2)

        self.service_table = tk.Frame(master=service_frm)
        self.service_table.grid(row=2, column=0, columnspan=3, padx=PADDING_X, pady=PADDING_Y, sticky="ew")
        self.next_service_row = 1
        self.service_list = []
        for col, (attr, header) in enumerate(ServiceItem.FIELDS):
            tk.Label(master=self.service_table, text=header, font=FONT + ("bold",), borderwidth=1, relief=tk.SOLID,
                     pady=3).grid(row=0, column=col, sticky="nsew")
            self.service_table.grid_columnconfigure(col, weight=1, minsize=ServiceItem.COLUMN_MINSIZES[attr])

        subtotal_frm = tk.Frame(master=service_frm)
        subtotal_frm.grid(row=3, column=0, columnspan=3, padx=PADDING_X, sticky="e")
        ttk.Label(master=subtotal_frm, text="Subtotal:", font=FONT).pack(side=tk.LEFT)
        self.subtotal_lbl = ttk.Label(master=subtotal_frm, text=f"${0:.2f}", font=FONT)
        self.subtotal_lbl.pack(side=tk.LEFT)

        hst_frm = tk.Frame(master=service_frm)
        hst_frm.grid(row=4, column=0, columnspan=3, padx=PADDING_X, sticky="e")
        ttk.Label(master=hst_frm, text="HST:", font=FONT).pack(side=tk.LEFT)
        self.hst_lbl = ttk.Label(master=hst_frm, text=f"${0:.2f}", font=FONT)
        self.hst_lbl.pack(side=tk.LEFT)

        total_frm = tk.Frame(master=service_frm)
        total_frm.grid(row=5, column=0, columnspan=3, padx=PADDING_X, sticky="e")
        ttk.Label(master=total_frm, text="Total:", font=FONT + ("bold",)).pack(side=tk.LEFT)
        self.total_lbl = ttk.Label(master=total_frm, text=f"${0:.2f}", font=FONT + ("bold",))
        self.total_lbl.pack(side=tk.LEFT)

        service_frm.grid_rowconfigure(6, weight=1)
        (tk.Button(master=service_frm, text="Save as PDF", font=FONT, width=10, height=1, bg=BUTTON_COLOR, padx=5,
                   command=lambda: self.save_as_pdf())
         .grid(row=7, column=0, columnspan=3, sticky="se", padx=PADDING_X, pady=PADDING_Y))

    def set_info(self, attribute):
        entry = self.entries[attribute].get_value()
        if entry in self.app.clients.get_attribute(attribute):
            client = self.app.clients.get_client(attribute, entry)
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

        service = self.app.services.get(service_name)
        if service is None:
            return

        for item in self.service_list:
            if item.service.name == service.name:
                item.quantity += 1
                item.quantity_label.config(text=item.quantity)
                self.service_popup_entry.delete(0, tk.END)
                self.update_total()
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

        btn_minus = tk.Button(qty_frame, text=" – ", font=FONT)
        btn_minus.grid(row=0, column=0, padx=5, pady=3)

        qty_lbl = tk.Label(qty_frame, text=item.quantity, font=FONT)
        qty_lbl.grid(row=0, column=1, pady=3)

        btn_plus = tk.Button(qty_frame, text=" + ", font=FONT)
        btn_plus.grid(row=0, column=2, padx=5, pady=3)

        qty_frame.grid(row=row_index, column=2, sticky="nsew")

        item.quantity_label = qty_lbl
        item.widgets = (name_lbl, price_lbl, qty_frame)

        btn_minus.config(command=lambda i=item: self._decrease_quantity(i))
        btn_plus.config(command=lambda i=item: self._increase_quantity(i))

        self.service_popup_entry.delete(0, tk.END)
        self.update_total()

    def _increase_quantity(self, item: ServiceItem):
        item.quantity += 1
        item.quantity_label.config(text=item.quantity)
        self.update_total()

    def _decrease_quantity(self, item: ServiceItem):
        item.quantity -= 1

        if item.quantity <= 0:
            for widget in item.widgets:
                widget.destroy()
            self.service_list.remove(item)
        else:
            item.quantity_label.config(text=item.quantity)
        self.update_total()

    def update_total(self):
        subtotal = 0
        for item in self.service_list:
            subtotal += item.service.price * item.quantity

        hst = round(subtotal * HST, 2)
        total = subtotal + hst

        self.subtotal_lbl.config(text=f"${subtotal:.2f}")
        self.hst_lbl.config(text=f"${hst:.2f}")
        self.total_lbl.config(text=f"${total:.2f}")

    def can_leave(self) -> bool:
        if any(entry.get() != "" for entry in self.entries.values()) or self.service_list:
            result = messagebox.askyesno("Unsaved Changes",
                                         "You have unsaved changes. Are you sure you want to leave?")
            return result
        return True
