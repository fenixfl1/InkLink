import subprocess
import os
import win32print
import asyncio

from utils.helpers import get_file_logger


logger = get_file_logger(__name__)


class PrinterUtilities:
    def __init__(self):
        self.__printer_name = self.get_default_printer()

    def set_printer_name(self, printer_name):
        self.__printer_name = printer_name

    def get_printer_name(self):
        return self.__printer_name

    async def print_file(self, file_path: str, printer_name: str = None, *print_args):
        try:
            # get the default printer or the printer name passed as argument
            printer_name = printer_name or win32print.GetDefaultPrinter()

            command = f'-print-to /D:"{printer_name}" {file_path}'

            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                logger.error(
                    f"An error occurred while printing the document - {stderr}"
                )
                raise subprocess.CalledProcessError(process.returncode, command)

            logger.info(f"Print job completed successfully: {stdout.decode()}")
        except subprocess.CalledProcessError as e:
            logger.error(f"An error occurred while printing the document - {e}")
        finally:
            pass
            # subprocess.run(["del", "/Q", PDF_VIEWER_TEMP_FOLDER], shell=True)

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
