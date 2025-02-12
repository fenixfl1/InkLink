import win32serviceutil

from src.service.windows_service import WindowsService


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(WindowsService)

    WindowsService.install()
    WindowsService.start()
    print("Service installed and started successfully")
