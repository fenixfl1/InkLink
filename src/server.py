import asyncio
import json
import websockets

from src.utils.printer import (
    get_default_printer,
    print_document,
    get_available_printers,
)
from src.utils.helpers import download_document, get_file_logger
from config import (
    WEBSOCKET_HOST,
    WEBSOCKET_PORT,
)

logger = get_file_logger(__name__)


async def handle_websocket(websocket, path):
    print("Client connected")

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
            file_path = download_document(data["url"])

            print_document(file_path, printer)
    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f" Connection closed - {e}")


async def start_server():
    print(f"Starting server at ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    print("Waiting for clients to connect...\n")

    server = await websockets.serve(handle_websocket, WEBSOCKET_HOST, WEBSOCKET_PORT)

    await server.wait_closed()

