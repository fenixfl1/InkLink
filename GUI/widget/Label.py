from tkinter import ttk


class Label(ttk.Label):
    def __init__(self, master, **kwargs):
        ttk.Label.__init__(self, master, **kwargs)
        self.pack()
        self.style = ttk.Style()  # Crear una instancia de ttk.Style()
        self.style.map(
            "Label.TLabel",
            background=[("hover", "lightblue"), ("active", "yellow")],
        )
        self.config(style="Label.TLabel")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        self.style.map("Label.TLabel", background=[("hover", "lightblue")])

    def on_leave(self, event):
        self.style.map("Label.TLabel", background=[("hover", "white")])

    def on_click(self, event):
        self.style.map("Label.TLabel", background=[("active", "yellow")])
        self.after(100, self.on_leave, event)
        self.invoke()
