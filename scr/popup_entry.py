import tkinter as tk
from tkinter import ttk


class PopupEntry(ttk.Entry):
    def __init__(self, master=None, values=None, max_rows=8, font="TkDefaultFont", command=None, **kwargs):
        super().__init__(master, font=font, **kwargs)
        self.values = list(values or [])
        self.max_rows = max_rows
        self.filtered = []
        self.command = command

        self.popup = tk.Toplevel(self)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)
        self.frame = ttk.Frame(self.popup)
        self.frame.pack(fill="both", expand=True)
        self.listbox = tk.Listbox(self.frame, activestyle="dotbox", font=font)
        self.vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.vsb.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
        self.popup.withdraw()

        self.bind("<FocusIn>", self._on_focus_in, add="+")
        self.bind("<KeyRelease>", self._on_keyrelease, add="+")
        self.bind("<Down>", self._on_down, add="+")
        self.bind("<Up>", self._on_up, add="+")
        self.bind("<Return>", self._on_return, add="+")
        self.bind("<Tab>", self._on_tab, add="+")
        self.bind("<Escape>", lambda e: self.hide_popup(), add="+")
        self.listbox.bind("<ButtonRelease-1>", self._on_listbox_click, add="+")
        self.bind_all("<Button-1>", self._on_global_click, add="+")
        self.winfo_toplevel().bind("<Configure>", lambda e: self._reposition_popup())
        self.bind("<Destroy>", lambda e: self.popup.destroy(), add="+")

    def get_value(self) -> str:
        """Return the current text inside the entry."""
        return self.get()

    def show_popup(self):
        if not self.filtered:
            self.hide_popup()
            return
        self.listbox.delete(0, "end")
        for item in self.filtered:
            self.listbox.insert("end", item)
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set(0)
        self.listbox.activate(0)

        rows = min(len(self.filtered), self.max_rows)
        self.listbox.configure(height=rows)

        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.popup.update_idletasks()
        width = self.winfo_width()
        height = self.listbox.winfo_reqheight()
        self.popup.geometry(f"{width}x{height}+{x}+{y}")
        self.popup.deiconify()

        self.focus_set()
        self.icursor("end")

    def hide_popup(self):
        try:
            self.popup.withdraw()
        except Exception:
            pass

    def _reposition_popup(self):
        if self.popup.state() == "withdrawn":
            return
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.popup.geometry(f"+{x}+{y}")

    def update_filter(self):
        typed = self.get()
        if typed == "":
            self.filtered = list(self.values)
        else:
            q = typed.lower()
            self.filtered = [v for v in self.values if q in v.lower()]

    def _on_focus_in(self, event=None):
        self.icursor("end")
        self.update_filter()
        if self.filtered:
            self.show_popup()

    def _on_keyrelease(self, event):
        if self.command:
            self.command()
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return
        self.update_filter()
        if self.filtered:
            self.show_popup()
        else:
            self.hide_popup()

    def _on_down(self, event):
        if self.popup.state() != "withdrawn":
            size = self.listbox.size()
            if size == 0:
                return "break"
            sel = self.listbox.curselection()
            idx = sel[0] if sel else -1
            idx = min(size - 1, idx + 1)
            self.listbox.selection_clear(0, "end")
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
            self.listbox.see(idx)
            self.focus_set()
            self.icursor("end")
            return "break"
        else:
            self.update_filter()
            if self.filtered:
                self.show_popup()
            return "break"

    def _on_up(self, event):
        if self.popup.state() != "withdrawn":
            size = self.listbox.size()
            if size == 0:
                return "break"
            sel = self.listbox.curselection()
            idx = sel[0] if sel else 0
            idx = max(0, idx - 1)
            self.listbox.selection_clear(0, "end")
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
            self.listbox.see(idx)
            self.focus_set()
            self.icursor("end")
            return "break"

    def _on_return(self, event):
        self._select_current(move_focus=True)
        return "break"

    def _on_tab(self, event):
        self._select_current(move_focus=False)

    def _on_listbox_click(self, event):
        idx = self.listbox.nearest(event.y)
        if 0 <= idx < self.listbox.size():
            val = self.listbox.get(idx)
            self._set_entry(val)
        self.hide_popup()
        self._focus_next_widget()

    def _on_global_click(self, event):
        try:
            clicked_toplevel = event.widget.winfo_toplevel()
        except Exception:
            clicked_toplevel = None
        if self.popup.winfo_viewable():
            if event.widget is self:
                return
            if clicked_toplevel is self.popup:
                return
            self.hide_popup()

    def _select_current(self, move_focus=True):
        if self.listbox.size():
            sel = self.listbox.curselection()
            if sel:
                val = self.listbox.get(sel[0])
            else:
                val = self.listbox.get(0)
            self._set_entry(val)
        self.hide_popup()
        if move_focus:
            self._focus_next_widget()

    def _set_entry(self, text):
        self.delete(0, "end")
        self.insert(0, text)
        self.icursor("end")
        if self.command:
            self.command()

    def _focus_next_widget(self):
        try:
            self.winfo_toplevel().focus_set()
        except Exception:
            pass
