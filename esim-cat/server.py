import asyncio
import websockets
import threading
import sys
import config

websock = set()
PORT = int(sys.argv[1])

# WebSocket handler
async def ws_handler(websocket):
    websock.add(websocket)
    try:
        async for message in websocket:
            print(f"[SERVER] Received {message}")
            for client in websock.copy():
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        print(f"[WebSocket] {PORT} Client disconnected.")
    finally:
        websock.discard(websocket)

# WebSocket server loop
async def ws_server():
    async with websockets.serve(ws_handler, "0.0.0.0", PORT):
        await asyncio.Future()  # Run forever

def open_port():
    config.event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(config.event_loop)
    config.event_loop.run_until_complete(ws_server())
    config.event_loop.run_forever()

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)

    async def send_command(self, command: str) -> str:
        try:
            print(self.uri)
            if self.websocket is None or not getattr(self.websocket, "open", False):
                await self.connect()
            print(self.websocket)
            await self.websocket.send(command)
            print(f"[CONSOLE] Sent: {command}")
            response = await self.websocket.recv()
            return response
        except Exception as e:
            return f"[ERROR] {e}"

if __name__ == "__main__":
    print("Port: ", PORT)
    open_port()
