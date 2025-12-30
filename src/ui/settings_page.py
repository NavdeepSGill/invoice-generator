import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import tkinter.font as tkfont

from src.constants import BUTTON_COLOR, DEFAULT_ENTRY_BG, ERROR_ENTRY_BG, FONT, PADDING_X, PADDING_Y, PAGE_MAIN
from src.models.settings import Settings
from src.ui.base_page import Page


class SettingsPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        info_frm = tk.Frame(master=self)
        info_frm.grid(row=0, column=0, padx=PADDING_X, pady=PADDING_Y)

        self.file_path = None
        self.folder_path = None

        self.entries = {}

        self.path_font = tkfont.Font(font=FONT)
        self.path_font_strike = tkfont.Font(font=FONT)
        self.path_font_strike.configure(overstrike=True)

        fields_middle_index = len(Settings.FIELDS) // 2
        for i, (attr, label, field_type) in enumerate(Settings.FIELDS):
            lbl = ttk.Label(master=info_frm, text=f"{label}: ", font=FONT)
            if i < fields_middle_index:
                lbl.grid(row=i, column=0, sticky="w", padx=(PADDING_X, 0), pady=PADDING_Y)
            else:
                lbl.grid(row=i - fields_middle_index, column=2, sticky="w", padx=(PADDING_X, 0), pady=PADDING_Y)

            if field_type == "entry":
                self.entries[attr] = tk.Entry(master=info_frm, font=FONT, width=40)
                self.entries[attr].bind("<KeyRelease>", self.reset_entry_bg)
            elif field_type == "file":
                self.entries[attr] = tk.Button(master=info_frm, text="Select File", font=FONT, width=10, height=1,
                                               bg=BUTTON_COLOR, padx=5, command=self.select_file)
                self.file_lbl = ttk.Label(master=info_frm, text="", font=FONT)
                self.file_lbl.config(font=self.path_font, cursor="hand2")
                self.file_lbl.bind("<Enter>", lambda _: self._on_path_hover_enter("file"))
                self.file_lbl.bind("<Leave>", lambda _: self._on_path_hover_leave("file"))
                self.file_lbl.bind("<Button-1>", lambda _: self._clear_path("file"))

                if i < fields_middle_index:
                    self.file_lbl.grid(row=i, column=1, sticky="w", padx=(120, PADDING_X), pady=PADDING_Y)
                else:
                    self.file_lbl.grid(row=i - fields_middle_index, column=3, sticky="w", padx=(120, PADDING_X),
                                       pady=PADDING_Y)
            elif field_type == "folder":
                self.entries[attr] = tk.Button(master=info_frm, text="Select Folder", font=FONT, width=10, height=1,
                                               bg=BUTTON_COLOR, padx=5, command=self.select_folder)
                self.folder_lbl = ttk.Label(master=info_frm, text="", font=FONT)
                self.folder_lbl.config(font=self.path_font, cursor="hand2")
                self.folder_lbl.bind("<Enter>", lambda _: self._on_path_hover_enter("folder"))
                self.folder_lbl.bind("<Leave>", lambda _: self._on_path_hover_leave("folder"))
                self.folder_lbl.bind("<Button-1>", lambda _: self._clear_path("folder"))
                if i < fields_middle_index:
                    self.folder_lbl.grid(row=i, column=1, sticky="w", padx=(120, PADDING_X), pady=PADDING_Y)
                else:
                    self.folder_lbl.grid(row=i - fields_middle_index, column=3, sticky="w", padx=(120, PADDING_X), )
            else:
                raise ValueError(f"Unknown field type: {field_type}")

            if i < fields_middle_index:
                self.entries[attr].grid(row=i, column=1, sticky="we", padx=(0, PADDING_X), pady=PADDING_Y)
            else:
                self.entries[attr].grid(row=i - fields_middle_index, column=3, sticky="w", padx=(0, PADDING_X),
                                        pady=PADDING_Y)

        (tk.Button(master=info_frm, text="Save and Exit", font=FONT, width=10, height=1, bg=BUTTON_COLOR, padx=5,
                   command=lambda: self.saveandexit())
         .grid(row=len(Settings.FIELDS), column=0, columnspan=4, sticky="e", padx=PADDING_X, pady=PADDING_Y))

        self.display_settings()

    def display_settings(self):
        settings = self.app.settings_repo.load()
        if settings is None:
            return

        for attr, _, field_type in Settings.FIELDS:
            if field_type == "entry":
                self.entries[attr].delete(0, tk.END)
                self.entries[attr].insert(0, str(getattr(settings, attr)))
            elif field_type == "file":
                self.file_path = settings.logo_path
                if self.file_path:
                    self.file_lbl.config(text=self.file_path.split("/")[-1])
            elif field_type == "folder":
                self.folder_path = settings.download_path
                if self.folder_path:
                    self.folder_lbl.config(text=self.folder_path.split("/")[-1])

    def select_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select Logo File",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")],
        )
        if self.file_path:
            self.file_lbl.config(text=self.file_path.split("/")[-1])

    def select_folder(self):
        self.folder_path = filedialog.askdirectory(title="Select Download Folder")
        if self.folder_path:
            self.folder_lbl.config(text=self.folder_path.split("/")[-1])

    def reset_entry_bg(self, event):
        event.widget.config(bg=DEFAULT_ENTRY_BG)

    def _on_path_hover_enter(self, kind: str):
        if kind == "file" and self.file_path:
            self.file_lbl.config(font=self.path_font_strike)
        elif kind == "folder" and self.folder_path:
            self.folder_lbl.config(font=self.path_font_strike)

    def _on_path_hover_leave(self, kind: str):
        if kind == "file":
            self.file_lbl.config(font=self.path_font)
        elif kind == "folder":
            self.folder_lbl.config(font=self.path_font)

    def _clear_path(self, kind: str):
        if kind == "file" and self.file_path:
            self.file_path = None
            self.file_lbl.config(text="", font=self.path_font)
        elif kind == "folder" and self.folder_path:
            self.folder_path = None
            self.folder_lbl.config(text="", font=self.path_font)

    def validate_entries(self) -> bool:
        error = False
        empty_field = False
        for attr, label, field_type in Settings.FIELDS:
            if field_type != "entry":
                continue

            entry_widget = self.entries[attr]
            value = entry_widget.get().strip()

            if attr == "business_name":
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
            elif attr in ("business_owner", "business_street", "business_city"):
                if value != value.title():
                    value = value.title()
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, value)
                    tk.messagebox.showinfo("Text Formatting",
                                           f"Converted {label} to Title Case")
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
            elif attr == "business_province":
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
            elif attr == "business_postal_code":
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
            elif attr == 'business_email':
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
            elif attr == "hst_number":
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
                else:
                    if not value.isalnum():
                        entry_widget.config(bg=ERROR_ENTRY_BG)
                        tk.messagebox.showerror("Invalid HST Number",
                                                "HST number must only contain letters and digits")
                        error = True
            elif attr == "license_id":
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
            elif attr == "tax_rate":
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
                elif "%" in value:
                    value = value.replace("%", "")
                    try:
                        rate = float(value) / 100
                        entry_widget.delete(0, tk.END)
                        entry_widget.insert(0, str(rate))
                        tk.messagebox.showinfo("Tax Rate Formatting",
                                               "Converted percentage to decimal tax rate")
                    except ValueError:
                        entry_widget.config(bg=ERROR_ENTRY_BG)
                        tk.messagebox.showerror("Invalid Tax Rate",
                                                "Tax rate must be a number between 0 and 1")
                        error = True
                else:
                    try:
                        rate = float(value)
                        if rate < 0 or rate > 1:
                            raise ValueError
                    except ValueError:
                        entry_widget.config(bg=ERROR_ENTRY_BG)
                        tk.messagebox.showerror("Invalid Tax Rate",
                                                "Tax rate must be a number between 0 and 1")
                        error = True
            elif attr == "invoice_number":
                if value == "":
                    entry_widget.config(bg=ERROR_ENTRY_BG)
                    empty_field = True
                else:
                    try:
                        number = int(value)
                        if number < 1:
                            raise ValueError
                    except ValueError:
                        entry_widget.config(bg=ERROR_ENTRY_BG)
                        tk.messagebox.showerror("Invalid Invoice Number",
                                                "Invoice number must be a positive integer")
                        error = True

        if empty_field:
            tk.messagebox.showerror("Empty Fields",
                                    "Please fill in all required fields")
            error = True
        return error

    def can_leave(self) -> bool:
        if self.validate_entries():
            return False
        for attr, label, field_type in Settings.FIELDS:
            if field_type == "entry":
                if self.entries[attr].get() == "":
                    tk.messagebox.showerror("Error", f"{label} is required.")
                    return False

        self._save()
        return True

    def saveandexit(self):
        if self.validate_entries():
            return
        for attr, label, field_type in Settings.FIELDS:
            if field_type == "entry":
                if self.entries[attr].get() == "":
                    tk.messagebox.showerror("Error", f"{label} is required.")
                    return

        self._save()
        self.app.show_frame(PAGE_MAIN)

    def _save(self):
        self.app.settings_repo.save(
            Settings(
                business_name=self.entries["business_name"].get(),
                business_owner=self.entries["business_owner"].get(),
                business_street=self.entries["business_street"].get(),
                business_city=self.entries["business_city"].get(),
                business_province=self.entries["business_province"].get(),
                business_postal_code=self.entries["business_postal_code"].get(),
                business_email=self.entries["business_email"].get(),
                hst_number=self.entries["hst_number"].get(),
                license_id=self.entries["license_id"].get(),
                tax_rate=self.entries["tax_rate"].get(),
                invoice_number=self.entries["invoice_number"].get(),
                logo_path=self.file_path,
                download_path=self.folder_path,
            )
        )
