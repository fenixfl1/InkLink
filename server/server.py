import json
import websockets
import asyncio

from config import WEBSOCKET_HOST, WEBSOCKET_PORT
from config.default import CONFIT_PATH
from utils.helpers import download_document, get_file_logger
from utils.printer import PrinterUtilities

logger = get_file_logger(__name__)


printer = PrinterUtilities()


async def error_handler(websocket, path, error):
    event = {"type": "error", "message": str(error)}
    await websocket.send(json.dumps(event))
    logger.error(f"Error in connection from {path}: {error}")


async def handle_printing(
    data: dict[str, str], websocket: websockets.WebSocketServerProtocol
):
    if not data or not isinstance(data, dict):
        raise ValueError("Invalid data format")
    if not data["url"]:
        raise ValueError("Url not found in data")
    if not data["printer"]:
        raise ValueError("Printer not found in data")

    url = data["url"]
    copies = data.get("copies", 1)
    printer_name = data["printer"]

    file_path = await download_document(url)

    await printer.print_file(file_path, printer_name)

    await websocket.send(
        json.dumps(
            {
                "type": "notification",
                "message": "Printing completed successfully!",
            }
        )
    )


async def websocket_handler(websocket: websockets.WebSocketServerProtocol, path: str):
    print(f"New connection from {websocket.remote_address[0]}")

    try:
        event = {"type": "notification", "message": "Connection established!"}

        await websocket.send(json.dumps(event))

        async for message in websocket:
            data = json.loads(message)

            if "type" not in data:
                raise ValueError("Invalid message format. Type is missing")

            match data["type"]:
                case "ping":
                    event["type"] = "pong"
                    event["message"] = "Pong!"
                    await websocket.send(json.dumps(event))
                case "status":
                    event = {
                        "type": "status",
                        "message": "Printer is ready!",
                    }
                    await websocket.send(json.dumps(event))
                case "printing":
                    await handle_printing(data, websocket)
                case "command":
                    event = {
                        "type": "notification",
                        "message": "Command received!",
                    }
                    await websocket.send(json.dumps(event))
                case _:
                    raise ValueError(f"Invalid data type: {data['type']}.")
    except Exception as e:
        await error_handler(websocket, path, e)


async def start_server():
    print(f"Starting server at ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    print(f"\nReading configuración from {CONFIT_PATH}")
    print("Waiting for connections...")

    server = await websockets.serve(websocket_handler, WEBSOCKET_HOST, WEBSOCKET_PORT)

    await server.wait_closed()
