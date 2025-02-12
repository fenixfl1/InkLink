import asyncio
import json
import websockets
import time

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

clients = {}

async def handle_websocket(websocket, path):
    client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    clients[client_id] = websocket
    
    print(f"Cliente {client_id} conectado.")
    
    message_id = f"print-{int(time.time() * 1000)}"
    
    try:
        printers = get_available_printers()

        await websocket.send(
            json.dumps(
                {
                    "message": "Connected to the server",
                    "messageId": message_id,
                    "printers": {
                        "default": get_default_printer(),
                        "options": printers,
                    }
                }
            )
        )

        async for message in websocket:
            try:
                data = json.loads(message)
                printer = data.get("printer", None)
                
                file_paths = download_document(data["url"])

                result = await print_document(file_paths, printer)
                
                result["messageId"] = data.get("messageId", message_id)
            
                await websocket.send(json.dumps(result))
            except Exception as e:
                logger.error(e)
                await websocket.send(json.dumps({"status": "error", "message": str(e)}))
    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f" Connection closed - {e}")
        await websocket.send(json.dumps({"status": "error", "message": str(e)}))


async def start_server():
    print(f"Starting server at ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
    print("Waiting for clients to connect...\n")

    server = await websockets.serve(handle_websocket, WEBSOCKET_HOST, WEBSOCKET_PORT)

    await server.wait_closed()

