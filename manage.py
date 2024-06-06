import win32serviceutil
import sys
import asyncio

from service.windows_service import InkLinkService
from utils.helpers import post_service_update
from server import start_server

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            win32serviceutil.HandleCommandLine(
                InkLinkService, customOptionHandler=post_service_update
            )
        else:
            asyncio.run(start_server())
    except KeyboardInterrupt as e:
        print("Service has been stopped by the user. Exiting...")
