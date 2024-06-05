import logging
import os
import sys
import uuid
import requests

from config import ROOT_DIR
from config.default import FILE_LOGGER_HANDLER, TMP_DIR


def resource_path(relative_path):
    """
    This function is used to get the absolute path of the file in the
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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
    logger.addHandler(FILE_LOGGER_HANDLER)
    return logger


logger = get_file_logger(__name__)


def download_document(url: str) -> str:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = resource_path(f"{TMP_DIR}\\{generateid()}.pdf")

            with open(file_path, "wb") as f:
                f.write(response.content)

            return file_path
        else:
            print(f"Failed to download PDF from {url}")
    except Exception as e:
        logger.error(f"An error occurred while downloading the PDF - {e}")
        return ""


def generateid():
    """
    Generate a unique id for the user.
    """
    return str(uuid.uuid4())


def post_service_update(*args):
    import win32api, win32con, win32profile, pywintypes
    from contextlib import closing

    env_reg_key = "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment"
    hkey = win32api.RegOpenKeyEx(
        win32con.HKEY_LOCAL_MACHINE, env_reg_key, 0, win32con.KEY_ALL_ACCESS
    )

    with closing(hkey):
        system_path = win32api.RegQueryValueEx(hkey, "path")[0]
        system_path = win32profile.ExpandEnvironmentStringsForUser(None, system_path)
        system_path_list = system_path.split(os.pathsep)

        core_dll_file = win32api.GetModuleFileName(sys.dllhandle)
        core_dll_name = os.path.basename(core_dll_file)

        for search_path_dir in system_path_list:
            try:
                dll_path = win32api.SearchPath(
                    resource_path(search_path_dir), core_dll_name
                )[0]
                print(f"System python DLL: {dll_path}")
                break
            except pywintypes.error as ex:
                if ex.args[1] != "SearchPath":
                    raise
                continue
        else:
            print("*** WARNING ***".center(80))
            print(
                f"Your current Python DLL ({core_dll_name}) is not in your SYSTEM PATH"
            )
            print("The service is likely to not launch correctly.")

    from win32serviceutil import LocatePythonServiceExe

    pythonservice_exe = LocatePythonServiceExe()
    pywintypes_dll_file = pywintypes.__spec__.origin

    pythonservice_path = os.path.dirname(pythonservice_exe)
    pywintypes_dll_name = os.path.basename(pywintypes_dll_file)

    try:
        return win32api.SearchPath(pythonservice_path, pywintypes_dll_name)[0]
    except pywintypes.error as ex:
        if ex.args[1] != "SearchPath":
            raise
        print("*** WARNING ***")
        print(
            f"{pywintypes_dll_name} is not is the same directory as pythonservice.exe"
        )
        print(f'Copy "{pywintypes_dll_file}" to "{pythonservice_path}"')
        print("The service is likely to not launch correctly.")
