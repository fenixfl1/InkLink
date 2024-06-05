import json
import websockets

from config import WEBSOCKET_HOST, WEBSOCKET_PORT
from config.default import CONFIT_PATH
from utils.helpers import get_file_logger
from utils.printer import PrinterUtilities

logger = get_file_logger(__name__)


printer = PrinterUtilities()


async def error_handler(websocket, path, error):
    event = {"type": "error", "message": str(error)}
    await websocket.send(json.dumps(event))
    logger.error(f"Error in connection from {path}: {error}")


async def websocket_handler(websocket, path):
    print(f"New connection from {websocket.remote_address[0]}")

    try:
        event = {
            "type": "notification",
            "message": "Connection established!",
            "printers": printer.get_printer_list(),
        }
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
                    if "data" not in data or not isinstance(data["data"], dict):
                        raise ValueError("Invalid data format")
                    event = {
                        "type": "printing",
                        "message": "Printing document...",
                    }
                    await websocket.send(json.dumps(event))
                case "command":
                    event = {
                        "type": "notification",
                        "message": "Command received!",
                    }
                    await websocket.send(json.dumps(event))
                case _:
                    raise ValueError(
                        f"Invalid data type: {data['type']}. Supported types are: ping, status, printing, command"
                    )
    except Exception as e:
        await error_handler(websocket, path, e)


async def start_server():
    print(f"Starting server at ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    print(f"\nReading configuración from {CONFIT_PATH}")
    print("Waiting for connections...")

    server = await websockets.serve(websocket_handler, WEBSOCKET_HOST, WEBSOCKET_PORT)

    await server.wait_closed()
