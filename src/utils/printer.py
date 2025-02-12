import win32print
from PyPDF2 import PdfReader
import subprocess
import asyncio

from config import PDF_VIEWER_PATH, PDF_VIEWER_TEMP_FOLDER, resource_path
from src.utils.helpers import get_file_logger

logger = get_file_logger(__name__)


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


async def print_document(pdf_paths: list[str], printer_name: str = None):
    """
    Imprime documentos PDF usando el visor de PDF especificado.
    
    :param pdf_paths: Lista de rutas de los archivos PDF a imprimir.
    :param printer_name: Nombre de la impresora (opcional, usa la predeterminada si no se proporciona).
    :return: Diccionario con el estado y mensaje de la impresión.
    """
    try:
        # get the default printer or the printer name passed as argument
        printer_name = printer_name or win32print.GetDefaultPrinter()
        
        tasks = []
        for path in pdf_paths:
            task = asyncio.create_subprocess_exec(
                PDF_VIEWER_PATH,
                "-print-to",
                printer_name,
                path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            tasks.append(task)
            
        processes = await asyncio.gather(*tasks, return_exceptions=True)
        errors = []
        
        for process in processes:
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_message = f"Error Occurred while printing: {stderr.decode()}"
                logger.error(error_message)
                errors.append(error_message)
                
        if errors:
            return {"status": "error", "message": "Algunos documentos no se imprimieron", "details": errors}
        
        return {"status": "success", "message": "Printing completed"}
    
    except subprocess.CalledProcessError as e:
        error_message = f"An error occurred while printing the document - {e}"
        logger.error(error_message)
        return {"status": "error", "message": error_message}
    # finally:
    #     try:
    #         subprocess.run(["del", "/Q", f'{PDF_VIEWER_TEMP_FOLDER}'], shell=True)
    #     except Exception as e:
    #         logger.error(f"Failed to delete temporary folder: {e}")
