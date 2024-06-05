from tkinter.ttk import Frame

from GUI.widget import Label, Button, ComboBox, Table


class PrinterScreen(Frame):
    def __init__(self, master, data=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.pack()
        self.title = Label(self, text="Add Printer", font=("Arial", 20))
        self.title.pack()
        self.printer_name_label = Label(self, text="Printer Name")
        self.printer_name_label.pack()
        self.printer_name_entry = ComboBox(self)
        self.printer_name_entry.pack()
        self.printer_name_entry.focus_set()
        self.printer_name_entry.bind("<Return>", self.add_printer)
        self.add_printer_button = Button(
            self,
            text="Add Printer",
            command=self.add_printer,
        )
        self.add_printer_button.pack()

        self.printer_table = Table(self, columns=["Printer Name"], data=data)
        self.printer_table.pack(expand=True, fill="both")

    def add_printer(self, event=None):
        print("Printer added")
        self.printer_name_entry.delete(0, "end")
        self.printer_name_entry.focus_set()

    def printer_list(self, printer_list):
        """
        Show the list of printers in a table
        """
        table = Table(self, columns=["Printer Name"], data_source=printer_list)
