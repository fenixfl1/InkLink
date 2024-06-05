import subprocess
import os
import win32print

from utils.helpers import get_file_logger


logger = get_file_logger(__name__)


class PrinterUtilities:
    def __init__(self):
        self.__printer_name = self.get_default_printer()

    def set_printer_name(self, printer_name):
        self.__printer_name = printer_name

    def get_printer_name(self):
        return self.__printer_name

    def print_file(self, file_path: str, printer_name: str = None):
        try:
            if printer_name:
                self.set_printer_name(printer_name)

            if not self.get_printer_name():
                raise ValueError("Printer name is not set")

            if not os.path.exists(file_path):
                raise FileNotFoundError("File not found")

            # print the file using win32print module
            hPrinter = win32print.OpenPrinter(self.get_printer_name())
            try:
                hJob = win32print.StartDocPrinter(
                    hPrinter, 1, ("test of raw data", None, "RAW")
                )
                try:
                    win32print.StartPagePrinter(hPrinter)
                    with open(file_path, "rb") as f:
                        win32print.WritePrinter(hPrinter, f.read())
                    win32print.EndPagePrinter(hPrinter)
                finally:
                    win32print.EndDocPrinter(hPrinter)
            finally:
                win32print.ClosePrinter(hPrinter)
        except Exception as e:
            logger.error(f"An error occurred while printing the file - {e}")
        finally:
            pass

    def get_printer_list(self) -> list[str]:
        try:
            return [
                printer[2]
                for printer in win32print.EnumPrinters(
                    win32print.PRINTER_ENUM_LOCAL, None, 1
                )
            ]
        except Exception as e:
            logger.error(
                f"An error occurred while fetching the available printers - {e}"
            )
            return []

    def get_default_printer(self) -> str:
        try:
            return win32print.GetDefaultPrinter()
        except Exception as e:
            logger.error(f"An error occurred while fetching the default printer - {e}")
            return None
