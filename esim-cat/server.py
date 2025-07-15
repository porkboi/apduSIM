import asyncio
import tkinter as tk
from tkinter import ttk, scrolledtext
import websockets
import threading
import sys

PORT = int(sys.argv[1])

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)

    async def send_command(self, command: str) -> str:
        try:
            if self.websocket is None or not getattr(self.websocket, "open", False):
                await self.connect()
            await self.websocket.send(command)
            response = await self.websocket.recv()
            return response
        except Exception as e:
            return f"[ERROR] {e}"

class App(tk.Tk):
    def __init__(self, ws_client):
        super().__init__()
        self.title("apduSIM Dashboard")
        self.geometry("600x400")
        self.ws_client = ws_client

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Command (as plain text, e.g., get_eid or APDU):").pack(pady=5)

        self.command_entry = ttk.Entry(self, width=70)
        self.command_entry.pack(pady=5)

        self.send_button = ttk.Button(self, text="Send", command=self.on_send)
        self.send_button.pack(pady=5)

        self.output_box = scrolledtext.ScrolledText(self, width=70, height=20, state="disabled")
        self.output_box.pack(pady=10)

    def log_output(self, message: str):
        self.output_box.config(state="normal")
        self.output_box.insert(tk.END, f"{message}\n")
        self.output_box.config(state="disabled")
        self.output_box.see(tk.END)

    def on_send(self):
        command = self.command_entry.get().strip()
        if not command:
            self.log_output("❌ Empty command")
            return
        threading.Thread(target=self.send_async, args=(command,), daemon=True).start()

    def send_async(self, command: str):
        response = asyncio.run(self.ws_client.send_command(command))
        self.log_output(f"🟢 Sent: {command}")
        self.log_output(f"📥 Response: {response}")
        print(f"[Console] Sent: {command}")
        print(f"[Console] Received: {response}")

if __name__ == "__main__":
    print("Port: ", PORT)
    WS_SERVER = f"ws://localhost:{PORT}"
    client = WebSocketClient(WS_SERVER)
    app = App(client)
    app.mainloop()
