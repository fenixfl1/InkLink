import signal
import asyncio
import json
import subprocess
import websockets
import requests

from src.utils.printer import (
    get_default_printer,
    print_document,
    get_available_printers,
)
from src.utils.helpers import download_document, generateid, get_file_logger
from src.config.default import (
    TMP_DIR,
    WEBSOCKET_HOST,
    WEBSOCKET_PORT,
)

logger = get_file_logger(__name__, "server.log")


async def handle_websocket(websocket, path):
    try:
        printers = get_available_printers()

        await websocket.send(
            json.dumps(
                {
                    "message": "Connected to the server",
                    "printers": printers,
                    "default": get_default_printer(),
                }
            )
        )

        async for message in websocket:
            data = json.loads(message)
            printer = data.get("printer", None)
            file_path = await download_document(data["url"])

            print_document(file_path, printer)
    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f" Connection closed - {e}")


async def start_server():
    print(f"Starting server at ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    print("Waiting for clients to connect...\n")

    # delete the contnet of the tmp directory (windows)
    subprocess.run(["del", "/Q", f"{TMP_DIR}\\*"], shell=True)

    server = await websockets.serve(handle_websocket, WEBSOCKET_HOST, WEBSOCKET_PORT)

    await server.wait_closed()


asyncio.run(start_server())
