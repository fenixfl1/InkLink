"""
This is a snippet from the Table.py file in the widget folder. This file contains the Table class, which is a subclass of the QTableWidget class from the PyQt5 library. The Table class is used to create a table widget that displays data in a tabular format.
"""

from tkinter.ttk import Treeview, Scrollbar


class Table(Treeview):
    def __init__(self, master, columns=None, data=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(expand=True, fill="both")

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.columns = columns
        self.data_source = data

        if self.columns:
            self.set_columns(self.columns)

        if self.data_source:
            self.set_data_source(self.data_source)

    def set_columns(self, columns):
        self.columns = columns
        self["columns"] = columns
        self["show"] = "headings"

        for column in columns:
            self.heading(column, text=column)
            self.column(column, width=100, anchor="center")

    def set_data_source(self, data_source):
        self.data_source = data_source
        self.delete(*self.get_children())
        for row in data_source:
            self.insert("", "end", values=row)
