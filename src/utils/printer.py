import win32print
from PyPDF2 import PdfReader
import subprocess

from src.config.default import PDF_VIEWER_PATH, PDF_VIEWER_TEMP_FOLDER
from src.utils.helpers import get_file_logger

logger = get_file_logger(__name__, "printer.log")


def get_available_printers() -> list:
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


def get_default_printer() -> str:
    try:
        return win32print.GetDefaultPrinter()
    except Exception as e:
        logger.error(f"An error occurred while fetching the default printer - {e}")
        return ""


def verify_printer_status() -> bool:
    # validate if the printer is available
    if not get_available_printers():
        print("No printer available")
        return False

    return True


def print_document(pdf_path, printer_name=None):
    try:
        # get the default printer or the printer name passed as argument
        printer_name = printer_name or win32print.GetDefaultPrinter()

        subprocess.Popen(
            [
                PDF_VIEWER_PATH,
                "-print-to",
                printer_name,
                pdf_path,
            ],
            shell=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while printing the document - {e}")
    finally:
        subprocess.run(["del", "/Q", PDF_VIEWER_TEMP_FOLDER], shell=True)
