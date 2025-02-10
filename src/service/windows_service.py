import asyncio
import os
import shutil
import socket
import win32serviceutil
import servicemanager
import win32event
import win32service
import time

from src.server import start_server
from src.utils.helpers import get_file_logger

logger = get_file_logger(__name__)


class WindowsService(win32serviceutil.ServiceFramework):
    _svc_name_ = "InkLInkService"
    _svc_display_name_ = "InkLink Service"
    _svc_description_ = "FiBanking plugin for printing documents"

    def __init__(self, args) -> None:
        # win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True
        socket.setdefaulttimeout(60)

    def SvcStop(self) -> None:
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self) -> None:
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        self.main()

    async def main(self) -> None:
        while self.is_alive:
            try:
                asyncio.create_task(start_server())
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"An error occurred while starting the service - {e}")
                break

    @staticmethod
    def install() -> None:
        """
        Install the service
        """
        try:
            win32serviceutil.InstallService(
                pythonClassString=f"{WindowsService.__module__}.{WindowsService.__name__}",
                serviceName=WindowsService._svc_name_,
                displayName=WindowsService._svc_display_name_,
                startType=win32service.SERVICE_AUTO_START,
            )
            print(f"{WindowsService._svc_display_name_} installed successfully")
        except Exception as e:
            print(f"An error occurred while installing the service - {e}")

        # Copy required files with appropriate permissions
        try:
            src_exe = (
                r"D:\Projects\InkLink\env\Lib\site-packages\win32\pythonservice.exe"
            )
            dest_exe = r"D:\Projects\InkLink\env\pythonservice.exe"
            if not os.path.exists(dest_exe):
                shutil.copy(src_exe, dest_exe)
                print(f"Copied {src_exe} to {dest_exe}")

            src_dll = r"D:\Projects\InkLink\env\Lib\site-packages\pywin32_system32\pywintypes312.dll"
            dest_dll = (
                r"C:\ProgramData\pywintypes312.dll"  # Usa un directorio accesible
            )
            if not os.path.exists(dest_dll):
                shutil.copy(src_dll, dest_dll)
                print(f"Copied {src_dll} to {dest_dll}")

        except PermissionError as e:
            print(f"Permission error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def remove() -> None:
        """
        Remove the service
        """
        try:
            win32serviceutil.RemoveService(WindowsService._svc_name_)
            print(f"{WindowsService._svc_display_name_} removed successfully")
        except Exception as e:
            logger.error(f"An error occurred while removing the service: {e}")
            print(f"An error occurred while removing the service: {e}")

    @staticmethod
    def start() -> None:
        """
        Start the service
        """
        win32serviceutil.StartService(WindowsService._svc_name_)
        print(f"{WindowsService._svc_display_name_} started successfully")

    @staticmethod
    def stop() -> None:
        """
        Stop the service
        """
        win32serviceutil.StopService(WindowsService._svc_name_)
        print(f"{WindowsService._svc_display_name_} stopped successfully")

    @staticmethod
    def restart() -> None:
        """
        Restart the service
        """
        win32serviceutil.RestartService(WindowsService._svc_name_)
        print(f"{WindowsService._svc_display_name_} restarted successfully")

    @staticmethod
    def status() -> None:
        """
        Get the status of the service
        """
        print("*" * 75)
        print(
            f"{WindowsService._svc_display_name_} status: {win32serviceutil.QueryServiceStatus(WindowsService._svc_name_)[1]}"
        )
        print("*" * 75)

    @staticmethod
    def help() -> None:
        print(
            """
            Usage: manage.py <command>
            
            Commands:
                install - Install the service
                remove - Remove the service
                start - Start the service
                stop - Stop the service
                restart - Restart the service
            """
        )
