import win32serviceutil

from service.windows_service import InkLinkService
from utils.helpers import post_service_update

if __name__ == "__main__":
    try:
        win32serviceutil.HandleCommandLine(
            InkLinkService, customOptionHandler=post_service_update
        )
    except KeyboardInterrupt as e:
        print("Service has been stopped by the user. Exiting...")
