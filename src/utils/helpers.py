"""
Helper functions for the project are defined here.
"""

import logging
import os
import socket
import sys
import uuid

import requests

from config import CLIENTS_ALLOWLIST, FILE_LOG_PATH, TMP_DIR, resource_path


def get_file_logger(name: str) -> logging.Logger:
    """
    Returns a logger object with the given name and logs to a file.

    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.

    Returns:
        logging.Logger: Logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler = logging.FileHandler(resource_path(FILE_LOG_PATH))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def generateID():
    """
    Generate a unique id for the user.
    """

    return str(uuid.uuid4())


logger = get_file_logger(__name__)


def download_document(urls: list[str]) -> list[str]:
    """
    Descarga documentos desde una lista de URLs y los guarda en TMP_DIR.
    
    :param urls: Lista de URLs de los documentos a descargar.
    :return: Lista de rutas de los archivos descargados.
    """
    paths = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_path = resource_path(f"{TMP_DIR}\\{generateID()}.pdf")

                with open(file_path, "wb") as f:
                    f.write(response.content)

                paths.append(file_path)
            else:
                logger.warning(f"Failed to download PDF from {url} - Status code: {response.status_code}")
        except Exception as e:
            logger.error(f"An error occurred while downloading the PDF - {e}")
    
    return paths
    
async def _download_document(url: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    file_path = resource_path(f"{TMP_DIR}\\{generateID()}.pdf")
                    
                    # Guardar el contenido del archivo de manera asincrónica
                    with open(file_path, "wb") as f:
                        f.write(await response.read())

                    return file_path
                else:
                    print(f"Failed to download PDF from {url} with status code {response.status}")
                    return ""
    except Exception as e:
        logger.error(f"An error occurred while downloading the PDF - {e}")
        return ""


def get_ip_address() -> str:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname_ex(hostname)[2][0]
    return ip_address


def set_ip_address_as_cookie() -> bool:
    """
    This function sets the user IP address as a cookie tn the default browser.
    In the CLIENT_HOST variable, the host address is stored.
    """
    # get my local ip address
    ip = get_ip_address()
    for hots in CLIENTS_ALLOWLIST:
        try:
            response = requests.get(f"http://{hots}")
            if response.status_code == 200:
                response.cookies.set("ip_address", ip, domain=hots)
                return True
        except Exception as e:
            logger.error(
                f"An error occurred while setting the IP address as a cookie - {e}"
            )
