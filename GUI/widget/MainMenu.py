"""
This file contains the siderbar menu items for the application. Each menu item is a dictionary with the following keys:
- text: The text to display for the menu item.
- icon: The icon to display for the menu item.
- command: The function to call when the menu item is clicked.
- active: A boolean value indicating whether the menu item is active or not.
"""

from tkinter import PhotoImage
from tkinter.ttk import Style
from tkinter import ttk

from GUI.widget import Button, Label


class MainMenu(ttk.Frame):
    def __init__(self, master, menu_items, **kwargs):
        ttk.Frame.__init__(self, master, style="MainMenu.TFrame", **kwargs)
        self.pack(side="left", fill="y")
        self.menu_items = menu_items

        # set the background color of the frame
        style = Style()
        style.configure("MainMenu.TFrame", background="#69b1ff")

        self.style = ttk.Style()
        self.style.configure(
            "Borderless.TButton", borderwidth=0, relief="flat", font=("Arial", 12)
        )

        self.buttons = []
        for item in menu_items:
            button = Button(
                self,
                text=item["text"],
                # style="Borderless.TButton",
                command=item["command"],
                state="normal" if item.get("active", True) else "disabled",
            )
            button.pack(fill="x", padx=15, pady=5)
            self.buttons.append(button)
            if "icon" in item:
                icon = PhotoImage(file=item["icon"])
                button.config(image=icon, compound="left")
                button.image = icon

    def set_active(self, index):
        for i, button in enumerate(self.buttons):
            if i == index:
                button.config(state="normal")
            else:
                button.config(state="disabled")
