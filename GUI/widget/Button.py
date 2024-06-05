import tkinter as ttk
from tkinter import PhotoImage


class Button(ttk.Button):

    def __init__(
        self,
        master=None,
        image_path="GUI/assets/img/button.png",
        width=10,
        height=None,
        **kwargs,
    ):
        if image_path:
            self.image = PhotoImage(file=image_path)
            if width and height:
                self.image = self.image.subsample(width=width, height=height)
        else:
            self.image = None

        ttk.Button.__init__(
            self,
            master,
            image=self.image,
            borderwidth=0,
            relief="flat",
            **kwargs,
        )

        # self.style = ttk.Style()
        # self.style.map(
        #     "Borderless.TButton",
        #     background=[("hover", "lightblue"), ("active", "yellow")],
        #     relief=[("pressed", "flat"), ("!disabled", "flat")],
        #     bordercolor=[
        #         ("focus", "lightblue")
        #     ],  # Set border color to match the background color
        # )
        # self.config(style="Borderless.TButton")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        # self.style.map("Borderless.TButton", background=[("hover", "lightblue")])
        pass

    def on_leave(self, event):
        # self.style.map("Borderless.TButton", background=[("hover", "white")])
        pass

    def on_click(self, event):
        # self.style.map("Borderless.TButton", background=[("active", "yellow")])
        self.after(100, self.on_leave, event)
        self.invoke()
