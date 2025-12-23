import tkinter as tk
from tkinter import ttk
import sys


class ScrollableFrame(tk.Frame):
    def __init__(self, master, max_height: int = 250):
        super().__init__(master)

        self.max_height = max_height
        self._last_canvas_height = None
        self._last_req_height = None

        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        self.inner = tk.Frame(canvas)

        def _on_inner_configure(_=None):
            try:
                canvas.configure(scrollregion=canvas.bbox("all"))

                req_w = self.inner.winfo_reqwidth()
                canvas.config(width=req_w)

                req_h = self.inner.winfo_reqheight()

                if req_h == self._last_req_height:
                    return
                self._last_req_height = req_h

                if self.max_height is None:
                    desired_h = req_h
                else:
                    desired_h = min(req_h, self.max_height)

                if desired_h != self._last_canvas_height:
                    self._last_canvas_height = desired_h
                    canvas.config(height=desired_h)
                    self.config(height=desired_h)

            except tk.TclError:
                pass

        self.inner.bind("<Configure>", _on_inner_configure)

        def _on_mousewheel(event):
            if hasattr(event, 'delta') and event.delta:
                try:
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                except (TypeError, ValueError):
                    canvas.yview_scroll(int(-1 * event.delta), "units")
            elif hasattr(event, 'num'):
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")

        def _bind_mousewheel(_=None):
            if sys.platform.startswith('linux'):
                # X11
                self.inner.bind_all('<Button-4>', _on_mousewheel)
                self.inner.bind_all('<Button-5>', _on_mousewheel)
            else:
                self.inner.bind_all('<MouseWheel>', _on_mousewheel)

        def _unbind_mousewheel(_=None):
            if sys.platform.startswith('linux'):
                self.inner.unbind_all('<Button-4>')
                self.inner.unbind_all('<Button-5>')
            else:
                self.inner.unbind_all('<MouseWheel>')

        self.inner.bind('<Enter>', _bind_mousewheel)
        self.inner.bind('<Leave>', _unbind_mousewheel)

        self._window = canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="x", expand=True)
        scrollbar.pack(side="right", fill="y")
