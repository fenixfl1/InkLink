import signal
import asyncio
import json
import subprocess
import websockets
import requests

from src.utils.printer import print_document
from src.utils.helpers import generateid, get_file_logger
from src.config.default import (
    DEFAULT_PRINTER,
    ROOT_DIR,
    TMP_DIR,
    WEBSOCKET_HOST,
    WEBSOCKET_PORT,
)

logger = get_file_logger(__name__, "server.log")


async def download_and_print_pdf(url: str, file_name: str = None):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = f"{TMP_DIR}\\{file_name}"

            with open(file_path, "wb") as f:
                f.write(response.content)

            print_document(file_path, DEFAULT_PRINTER)
        else:
            print(f"Failed to download PDF from {url}")
    except Exception as e:
        logger.error(f"An error occurred while downloading the PDF - {e}")


async def handle_websocket(websocket, path):
    print(f"Client connected")
    try:
        async for message in websocket:
            data = json.loads(message)
            rp_name = f"{data.get('rp_name', f'{generateid()}')}.pdf"
            await download_and_print_pdf(data["url"], rp_name)
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
