import asyncio
import socket
import sys
import threading
import time
import servicemanager
import win32event
import win32service
import win32serviceutil

from config import SERVICE_DISPLAY_NAME, SERVICE_NAME, SERVICE_DESCRIPTION
from utils.helpers import get_file_logger, post_service_update
from server import start_server

logger = get_file_logger(__name__)


class InkLinkService(win32serviceutil.ServiceFramework):
    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = SERVICE_DISPLAY_NAME
    _svc_description_ = SERVICE_DESCRIPTION

    def __init__(self, args) -> None:
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(120)
        self.is_alive = True
        self.server_thread: threading.Thread = None

    @classmethod
    def parse_command_line(cls):
        try:
            if len(sys.argv) == 1:
                servicemanager.Initialize()
                servicemanager.PrepareToHostSingle(cls)
                servicemanager.StartServiceCtrlDispatcher()
            else:
                win32serviceutil.HandleCommandLine(
                    cls, customOptionHandler=post_service_update
                )

        except Exception as e:
            print(f"An error occurred while starting the service - {e}.")
            logger.error(f"An error occurred while starting the service - {e}")

    def SvcStop(self) -> None:
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False
        if self.server_thread and self.server_thread.is_alive():
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.server_thread.join()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self) -> None:
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        self.server_thread = threading.Thread(target=self.main)
        self.server_thread.start()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def __start_asyncio_thead(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(start_server())
        self.loop.run_forever()

    def main(self) -> None:
        try:
            self.server_thread = threading.Thread(target=self.__start_asyncio_thead)
            self.server_thread.start()

            while self.is_alive:
                time.sleep(5)
        except Exception as e:
            self.is_alive = False
            self.server_thread.join()
            logger.error(f"An error occurred while running the service - {e}")
