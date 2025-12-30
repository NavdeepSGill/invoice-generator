import tkinter as tk
from tkinter import messagebox, ttk

from src.models.service import Service
from src.constants import BUTTON_COLOR, DEFAULT_ENTRY_BG, ERROR_ENTRY_BG, FONT, PADDING_X, PADDING_Y, PAGE_MAIN
from src.ui.base_page import Page
from src.ui.widgets.scrollable_frame import ScrollableFrame


class ServicePage(Page):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.old_service_list = self.app.services.get_all().copy()

        table_frm = ScrollableFrame(master=self)
        table_frm.grid(row=0, column=0, padx=PADDING_X * 2, pady=PADDING_Y, sticky="nsw")

        info_frm = tk.Frame(master=self)
        info_frm.grid(row=1, column=0, padx=PADDING_X, pady=PADDING_Y, sticky="ew")

        self.header_widths = []

        # Table Frame
        self.service_table_header = tk.Frame(master=table_frm.inner)
        self.service_table_header.grid(row=0, column=0, padx=0, pady=(PADDING_Y, 0), sticky="ew")
        self.service_table = tk.Frame(master=table_frm.inner)
        self.service_table.grid(row=1, column=0, padx=0, pady=(0, PADDING_Y), sticky="nsew")
        for col, (_, header) in enumerate(Service.FIELDS):
            lbl = tk.Label(master=self.service_table_header, text=header, font=FONT + ("bold",),
                           borderwidth=1, relief=tk.SOLID, padx=5, pady=3)
            lbl.grid(row=0, column=col, sticky="nsew")
            self.header_widths.append(lbl.winfo_reqwidth())
        lbl = tk.Label(master=self.service_table_header, text="Buttons", font=FONT + ("bold",),
                       borderwidth=1, relief=tk.SOLID, padx=5, pady=3)
        lbl.grid(row=0, column=len(Service.FIELDS), sticky="nsew")
        self.header_widths.append(lbl.winfo_reqwidth())

        # Service Information Frame
        self.entries = {}

        for i, (attr, label) in enumerate(Service.FIELDS):
            lbl = ttk.Label(master=info_frm, text=f"{label}: ", font=FONT)
            lbl.grid(row=i, column=0, sticky="w", padx=(PADDING_X, 0), pady=PADDING_Y)
            self.entries[attr] = tk.Entry(master=info_frm, font=FONT, width=30)
            self.entries[attr].grid(row=i, column=1, sticky="we", padx=(0, PADDING_X), pady=PADDING_Y)
            self.entries[attr].bind("<KeyRelease>", self.reset_entry_bg)
        (tk.Button(master=info_frm, text="Add Service", font=FONT, width=10, height=1, bg=BUTTON_COLOR,
                   command=lambda: self.add_service())
         .grid(row=len(Service.FIELDS), column=0, sticky="w", padx=PADDING_X, pady=PADDING_Y))

        info_frm.grid_columnconfigure(2, weight=1)
        (tk.Button(master=info_frm, text="Save and Exit", font=FONT, width=10, height=1, bg=BUTTON_COLOR, padx=5,
                   command=lambda: self.save())
         .grid(row=len(Service.FIELDS), column=2, sticky="e", padx=PADDING_X, pady=PADDING_Y))

        self.display_services()

    def display_services(self):
        for widget in self.service_table.winfo_children():
            widget.destroy()

        service_row = 0
        self.table_widths = [0] * (len(self.header_widths))

        button_frm = None

        for service in self.app.services.get_all():
            for i, (attr, _) in enumerate(Service.FIELDS):
                if type(getattr(service, attr)) == float:
                    value = f"${getattr(service, attr):.2f}"
                    lbl = tk.Label(master=self.service_table, text=value, font=FONT, borderwidth=1,
                                   relief="solid", padx=5, pady=3)
                    lbl.grid(row=service_row, column=i, sticky="nswe")
                else:
                    lbl = tk.Label(master=self.service_table, text=getattr(service, attr), font=FONT, borderwidth=1,
                                   relief="solid", padx=5, pady=3)
                    lbl.grid(row=service_row, column=i, sticky="nswe")
                if lbl.winfo_reqwidth() > self.table_widths[i]:
                    self.table_widths[i] = lbl.winfo_reqwidth()
                    self.service_table_header.grid_columnconfigure(i, minsize=self.table_widths[i])

            button_frm = tk.Frame(master=self.service_table, borderwidth=1, relief="solid")
            button_frm.grid(row=service_row, column=len(Service.FIELDS), sticky="nswe")
            edit_btn = tk.Button(master=button_frm, text="Edit", font=FONT, width=5, height=1, bg=BUTTON_COLOR,
                                 command=lambda c=service: self.edit_service(c))
            edit_btn.pack(side=tk.LEFT, padx=2, pady=2)
            delete_btn = tk.Button(master=button_frm, text="Delete", font=FONT, width=5, height=1, bg=BUTTON_COLOR,
                                   command=lambda c=service: self.delete_service(c))
            delete_btn.pack(side=tk.LEFT, padx=2, pady=2)

            service_row += 1

        if button_frm is None:
            for i in range(len(self.header_widths)):
                self.table_widths[-1] = 0
                if self.header_widths[i] > self.table_widths[i]:
                    self.service_table_header.grid_columnconfigure(i, minsize=self.header_widths[i])
        else:
            self.service_table.update_idletasks()
            if button_frm.winfo_reqwidth() > self.table_widths[-1]:
                self.table_widths[-1] = button_frm.winfo_reqwidth()
                self.service_table_header.grid_columnconfigure(len(Service.FIELDS), minsize=self.table_widths[-1])

        for i in range(len(self.header_widths)):
            if self.header_widths[i] > self.table_widths[i]:
                self.service_table.grid_columnconfigure(i, minsize=self.header_widths[i])

    def add_service(self):
        if self.validate_entries():
            return
        values = {}
        for attr, _ in Service.FIELDS:
            values[attr] = self.entries[attr].get()
        service = Service(**values)
        try:
            self.app.services.add(service)
        except ValueError as e:
            messagebox.showerror("Duplicate Service", str(e))
            return
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.display_services()

    def edit_service(self, service: Service):
        for attr, _ in Service.FIELDS:
            self.entries[attr].config(bg=DEFAULT_ENTRY_BG)
            self.entries[attr].delete(0, tk.END)
            self.entries[attr].insert(0, getattr(service, attr))
        self.app.services.remove(service)
        self.display_services()

    def delete_service(self, service: Service):
        if not tk.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this service?"):
            return
        self.app.services.remove(service)
        self.display_services()

    def reset_entry_bg(self, event):
        event.widget.config(bg=DEFAULT_ENTRY_BG)

    def validate_entries(self) -> bool:
        error = False
        empty_field = False
        for attr, label in Service.FIELDS:
            entry_widget = self.entries[attr]
            value = entry_widget.get().strip()

            if attr == "name":
                if value != value.title():
                    value = value.title()
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, value)
                    tk.messagebox.showinfo("Text Formatting",
                                           f"Converted {label} to Title Case")
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True

            elif attr == "price":
                if "$" in value:
                    value = value.replace("$", "").strip()
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, value)
                    tk.messagebox.showinfo("Text Formatting",
                                           f"Removed '$' from {label}")
                if "." in value:
                    parts = value.split(".")
                    if len(parts[1]) > 2:
                        value = f"{parts[0]}.{parts[1][:2]}"
                        entry_widget.delete(0, tk.END)
                        entry_widget.insert(0, value)
                        tk.messagebox.showinfo("Text Formatting",
                                               f"Truncated {label} to two decimal places")
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
                else:
                    try:
                        float(value)
                    except ValueError:
                        entry_widget.config(bg=ERROR_ENTRY_BG)
                        tk.messagebox.showerror("Invalid Input",
                                                f"{label} must be a valid number")
                        error = True

        if empty_field:
            tk.messagebox.showerror("Empty Fields",
                                    "Please fill in all required fields")
            error = True
        return error

    def can_leave(self) -> bool:
        if self.old_service_list != self.app.services.get_all():
            result = messagebox.askyesno("Unsaved Changes",
                                         "You have unsaved changes. Are you sure you want to leave?")
            return result

        for entry in self.entries.values():
            if entry.get() != "":
                result = messagebox.askyesno("Unsaved Changes",
                                             "You have unsaved changes. Are you sure you want to leave?")
                return result

        return True

    def save(self):
        for entry in self.entries.values():
            if entry.get() != "":
                if not tk.messagebox.askyesno("Unsaved Data",
                                              "Are you sure you want to save and exit?\n"
                                              "There is unsaved data in the entry fields."):
                    return
                else:
                    break

        self.app.service_repo.save(self.app.services)
        self.old_service_list = self.app.services.get_all().copy()
        self.app.show_frame(PAGE_MAIN)
