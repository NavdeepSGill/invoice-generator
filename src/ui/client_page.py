import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from src.models.client import Client
from src.ui.constants import BUTTON_COLOR, DEFAULT_ENTRY_BG, ERROR_ENTRY_BG, FONT, PADDING_X, PADDING_Y, PAGE_MAIN
from src.ui.widgets.scrollable_frame import ScrollableFrame


class ClientPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        table_frm = ScrollableFrame(master=self)
        table_frm.grid(row=0, column=0, padx=PADDING_X * 2, pady=PADDING_Y, sticky="nsew")

        info_frm = tk.Frame(master=self)
        info_frm.grid(row=1, column=0, padx=PADDING_X, pady=PADDING_Y, sticky="ew")

        self.header_widths = []

        # Table Frame
        self.client_table_header = tk.Frame(master=table_frm.inner)
        self.client_table_header.grid(row=0, column=0, padx=0, pady=(PADDING_Y, 0), sticky="ew")
        self.client_table = tk.Frame(master=table_frm.inner)
        self.client_table.grid(row=1, column=0, padx=0, pady=(0, PADDING_Y), sticky="nsew")
        for col, (_, header) in enumerate(Client.FIELDS):
            lbl = tk.Label(master=self.client_table_header, text=header, font=FONT + ("bold",),
                           borderwidth=1, relief=tk.SOLID, padx=5, pady=3)
            lbl.grid(row=0, column=col, sticky="nsew")
            self.header_widths.append(lbl.winfo_reqwidth())
        lbl = tk.Label(master=self.client_table_header, text="Buttons", font=FONT + ("bold",),
                       borderwidth=1, relief=tk.SOLID, padx=5, pady=3)
        lbl.grid(row=0, column=len(Client.FIELDS), sticky="nsew")
        self.header_widths.append(lbl.winfo_reqwidth())

        # Client Information Frame
        self.entries = {}

        for i, (attr, label) in enumerate(Client.FIELDS):
            lbl = ttk.Label(master=info_frm, text=f"{label}: ", font=FONT)
            lbl.grid(row=i, column=0, sticky="w", padx=(PADDING_X, 0), pady=PADDING_Y)
            self.entries[attr] = tk.Entry(master=info_frm, font=FONT, width=40)
            self.entries[attr].grid(row=i, column=1, sticky="we", padx=(0, PADDING_X), pady=PADDING_Y)
            self.entries[attr].bind("<KeyRelease>", self.reset_entry_bg)
        (tk.Button(master=info_frm, text="Add Client", font=FONT, width=10, height=1, bg=BUTTON_COLOR,
                   command=lambda: self.add_client())
         .grid(row=len(Client.FIELDS), column=0, sticky="w", padx=PADDING_X, pady=PADDING_Y))

        info_frm.grid_columnconfigure(2, weight=1)
        (tk.Button(master=info_frm, text="Save and Exit", font=FONT, width=10, height=1, bg=BUTTON_COLOR, padx=5,
                   command=lambda: self.save())
         .grid(row=len(Client.FIELDS), column=2, sticky="e", padx=PADDING_X, pady=PADDING_Y))

        self.display_clients()

    def display_clients(self):
        for widget in self.client_table.winfo_children():
            widget.destroy()

        clients_row = 0
        self.table_widths = [0] * (len(self.header_widths))

        button_frm = None

        for client in self.app.clients.get_all():
            for i, (attr, _) in enumerate(Client.FIELDS):
                lbl = tk.Label(master=self.client_table, text=getattr(client, attr), font=FONT, borderwidth=1,
                               relief="solid", padx=5, pady=3)
                lbl.grid(row=clients_row, column=i, sticky="nswe")
                if lbl.winfo_reqwidth() > self.table_widths[i]:
                    self.table_widths[i] = lbl.winfo_reqwidth()
                    self.client_table_header.grid_columnconfigure(i, minsize=self.table_widths[i])

            button_frm = tk.Frame(master=self.client_table, borderwidth=1, relief="solid")
            button_frm.grid(row=clients_row, column=len(Client.FIELDS), sticky="nswe")
            edit_btn = tk.Button(master=button_frm, text="Edit", font=FONT, width=5, height=1, bg=BUTTON_COLOR,
                                 command=lambda c=client: self.edit_client(c))
            edit_btn.pack(side=tk.LEFT, padx=2, pady=2)
            delete_btn = tk.Button(master=button_frm, text="Delete", font=FONT, width=5, height=1, bg=BUTTON_COLOR,
                                   command=lambda c=client: self.delete_client(c))
            delete_btn.pack(side=tk.LEFT, padx=2, pady=2)

            clients_row += 1

        if button_frm is None:
            for i in range(len(self.header_widths)):
                self.table_widths[-1] = 0
                if self.header_widths[i] > self.table_widths[i]:
                    self.client_table_header.grid_columnconfigure(i, minsize=self.header_widths[i])
        else:
            self.client_table.update_idletasks()
            if button_frm.winfo_reqwidth() > self.table_widths[-1]:
                self.table_widths[-1] = button_frm.winfo_reqwidth()
                self.client_table_header.grid_columnconfigure(len(Client.FIELDS), minsize=self.table_widths[-1])

        for i in range(len(self.header_widths)):
            if self.header_widths[i] > self.table_widths[i]:
                self.client_table.grid_columnconfigure(i, minsize=self.header_widths[i])

    def add_client(self):
        if self.validate_entries():
            return
        values = {}
        for attr, _ in Client.FIELDS:
            values[attr] = self.entries[attr].get()
        client = Client(**values)
        try:
            self.app.clients.add(client)
        except ValueError as e:
            messagebox.showerror("Duplicate Client", str(e))
            return
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.display_clients()

    def edit_client(self, client: Client):
        for attr, _ in Client.FIELDS:
            self.entries[attr].config(bg=DEFAULT_ENTRY_BG)
            self.entries[attr].delete(0, tk.END)
            self.entries[attr].insert(0, getattr(client, attr))
        self.app.clients.remove(client)
        self.display_clients()

    def delete_client(self, client: Client):
        if not tk.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this client?"):
            return
        self.app.clients.remove(client)
        self.display_clients()

    def reset_entry_bg(self, event):
        event.widget.config(bg=DEFAULT_ENTRY_BG)

    def validate_entries(self) -> bool:
        error = False
        empty_field = False
        for attr, label in Client.FIELDS:
            entry_widget = self.entries[attr]
            value = entry_widget.get().strip()

            if attr == "phone":
                if "-" in value or "/" in value or "(" in value or ")" in value or " " in value:
                    value = (value
                             .replace("-", "")
                             .replace("/", "")
                             .replace("(", "")
                             .replace(")", "")
                             .replace(" ", ""))
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, value)
                    tk.messagebox.showinfo("Phone Number Formatting",
                                           "Removed formatting characters from phone number")
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
                else:
                    if len(value) != 10:
                        entry_widget.config(bg=ERROR_ENTRY_BG)
                        tk.messagebox.showerror("Invalid Phone Number",
                                                "Phone number must be 10 digits long")
                        error = True
                    if not value.isdigit():
                        entry_widget.config(bg=ERROR_ENTRY_BG)
                        tk.messagebox.showerror("Invalid Phone Number",
                                                "Phone number must only contain digits")
                        error = True
            elif attr in ("name", "street", "city"):
                if value != value.title():
                    value = value.title()
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, value)
                    tk.messagebox.showinfo("Text Formatting",
                                           f"Converted {label} to Title Case")
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
            elif attr == "province":
                if value != value.upper():
                    value = value.upper()
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, value)
                    tk.messagebox.showinfo("Text Formatting",
                                           f"Converted {label} to Upper Case")
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
                else:
                    if value not in {"AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", "QC", "SK", "YT"}:
                        entry_widget.config(bg=ERROR_ENTRY_BG)
                        tk.messagebox.showerror("Invalid Province",
                                                f"{value} is not a valid Canadian province code. Must be one of: "
                                                "ON, AB, BC, MB, NB, NL, NS, NT, NU, PE, QC, SK, YT.")
                        error = True
            elif attr == "postal_code":
                if value != value.upper():
                    value = value.upper()
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, value)
                    tk.messagebox.showinfo("Postal Code Formatting",
                                           f"Converted postal code to Upper Case")
                if len(value) == 6:
                    value = value[:3] + " " + value[3:]
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, value)
                    tk.messagebox.showinfo("Postal Code Formatting",
                                           "Added space to postal code")
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
                else:
                    if len(value) != 7:
                        entry_widget.config(bg=ERROR_ENTRY_BG)
                        tk.messagebox.showerror("Invalid Postal Code",
                                                "Postal code must be 7 characters long (including space)")
                        error = True
                    else:
                        checks = [
                            (value[0] in "ABCEGHJKLMNPRSTVXY", "first character must be a valid letter"),
                            (value[1].isdigit(), "second character must be a digit"),
                            (value[2] in "ABCEGHJKLMNPRSTVWXYZ", "third character must be a valid letter"),
                            (value[3] == " ", "fourth character must be a space"),
                            (value[4].isdigit(), "fifth character must be a digit"),
                            (value[5] in "ABCEGHJKLMNPRSTVWXYZ", "sixth character must be a valid letter"),
                            (value[6].isdigit(), "seventh character must be a digit"),
                        ]
                        for ok, msg in checks:
                            if not ok:
                                entry_widget.config(bg=ERROR_ENTRY_BG)
                                tk.messagebox.showerror("Invalid Postal Code", f"Postal code {msg}")
                                error = True
                                break
            elif 'email' in attr:
                if value != value.lower():
                    value = value.lower()
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, value)
                    tk.messagebox.showinfo("Email Formatting",
                                           "Converted email to Lower Case")
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
                else:
                    if "@" not in value or "." not in value:
                        entry_widget.config(bg=ERROR_ENTRY_BG)
                        tk.messagebox.showerror("Invalid Email",
                                                "Email must contain '@' and '.' characters")
                        error = True

        if empty_field:
            tk.messagebox.showerror("Empty Fields",
                                    "Please fill in all required fields")
            error = True
        return error

    def save(self):
        for entry in self.entries.values():
            if entry.get() != "":
                if not tk.messagebox.askyesno("Unsaved Data",
                                              "Are you sure you want to save and exit?\n"
                                              "There is unsaved data in the entry fields."):
                    return
                else:
                    break

        self.app.client_repo.save(self.app.clients)
        self.app.show_frame(PAGE_MAIN)
