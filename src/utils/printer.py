import os
import win32print
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas

from src.utils.helpers import get_file_logger

logger = get_file_logger(__name__, "printer.log")


def find_available_printers() -> list:
    try:
        return [
            printer[2]
            for printer in win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL, None, 1
            )
        ]
    except Exception as e:
        logger.error(f"An error occurred while fetching the available printers - {e}")
        return []


def verify_printer_status() -> bool:
    # validate if the printer is available
    if not find_available_printers():
        print("No printer available")
        return False

    return True


def print_document(pdf_path, printer_name=None):
    try:
        hprinter = win32print.OpenPrinter(printer_name)
        try:
            hjob = win32print.StartDocPrinter(hprinter, 1, (pdf_path, None, "RAW"))
            try:
                win32print.StartPagePrinter(hprinter)

                # Use PyPDF2 to read the PDF content
                with open(pdf_path, "rb") as pdf_file:
                    reader = PdfReader(pdf_file)
                    num_pages = len(reader.pages)
                    pdf_content = ""
                    for page_num in range(num_pages):
                        page = reader.pages[page_num]
                        pdf_content += page.extract_text()

                # Use reportlab to render the PDF content before printing
                c = canvas.Canvas(os.devnull)
                c.drawString(100, 100, pdf_content)
                c.showPage()
                c.save()

                win32print.WritePrinter(hprinter, open(pdf_path, "r").read())
                win32print.EndPagePrinter(hprinter)
            finally:
                win32print.EndDocPrinter(hprinter)
        finally:
            win32print.ClosePrinter(hprinter)
    except Exception as e:
        logger.error(f"failing to print the document - {e}")
