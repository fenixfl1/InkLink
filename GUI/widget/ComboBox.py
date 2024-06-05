from tkinter import ttk


class ComboBox(ttk.Combobox):
    def __init__(self, master, **kwargs):
        ttk.Combobox.__init__(self, master, **kwargs)
        self.pack()
        self.style = ttk.Style()  # Crear una instancia de ttk.Style()
        self.style.map(
            "ComboBox.TCombobox",
            background=[("hover", "lightblue"), ("active", "yellow")],
        )
        self.config(style="ComboBox.TCombobox")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

        # set the default width and height of the combobox
        self.width = 20
        self.height = 50

    def on_enter(self, event):
        self.style.map("ComboBox.TCombobox", background=[("hover", "lightblue")])

    def on_leave(self, event):
        self.style.map("ComboBox.TCombobox", background=[("hover", "white")])

    def on_click(self, event):
        self.style.map("ComboBox.TCombobox", background=[("active", "yellow")])
        self.after(100, self.on_leave, event)
        self.invoke()
