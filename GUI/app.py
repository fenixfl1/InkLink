from tkinter import Tk as TkRoot
from tkinter.ttk import Style as TkStyle
from GUI.screen.add_printe import PrinterScreen
from GUI.widget import *
from utils.printer import PrinterUtilities


class App(TkRoot):
    def __init__(self):
        super().__init__()
        self.printer = PrinterUtilities()

        self.geometry("300x300")
        self.title("Printer GUI")
        self.configure_styles()

        MainMenu(
            self, menu_items=[{"text": "Add Printer", "command": self.printer_screen}]
        )

        PrinterScreen(self, data=self.printer.get_printer_list())

    def configure_styles(self):
        self.style = TkStyle()
        self.style.configure("Button.TButton", font=("Arial", 12))
        self.style.configure("Button.TButtonHover", font=("Arial", 12, "underline"))
        self.style.configure("Button.TButtonActive", font=("Arial", 12, "overstrike"))
        self.style.configure("ComboBox.TCombobox", font=("Arial", 12))
        self.style.configure("ComboBox.TComboboxHover", font=("Arial", 12, "underline"))
        self.style.configure(
            "ComboBox.TComboboxActive", font=("Arial", 12, "overstrike")
        )

    def show_selected_printer(self):
        selected_printer = self.combobox.get()
        print(f"Selected printer: {selected_printer}")

    def printer_screen(self):
        self.printer_screen = PrinterScreen(self, data=self.printer.get_printer_list())
        self.printer_screen.grind(
            row=0, column=0, columnspan=2, rowspan=2, sticky="nsew"
        )
