import socket
import win32serviceutil
import servicemanager
import win32event
import win32service
import time

from src.server import start_server
from src.utils.helpers import get_file_logger

logger = get_file_logger(__name__, "windows_service.log")


class WindowsService(win32serviceutil.ServiceFramework):
    _svc_name_ = "InkLInkService"
    _svc_display_name_ = "InkLink Service"

    def __init__(self, args: socket.Iterable[str]) -> None:
        win32serviceutil.ServiceFramework.__init__(self, args)
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

    def main(self) -> None:
        while True:
            try:
                if self.is_alive:
                    start_server()
                else:
                    break
                time.sleep(5)
            except Exception as e:
                logger.error(f"An error occurred while starting the service - {e}")
                break
