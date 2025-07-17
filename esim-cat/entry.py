import json
import socket
import subprocess
import websockets
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import config
import asyncio
import threading
import time

app = FastAPI()
websock = set()

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

@app.get("/get-port")
async def get_port():
    PORT = find_free_port()
    print(f"[ENTRY]: Allocated port {PORT}")
    subprocess.Popen(["python3", "server.py", str(PORT)])
    time.sleep(1)
    return JSONResponse(content={"port":PORT})