import json
import socket
import subprocess
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

@app.get("/get-port")
async def get_port():
    port = find_free_port()
    print(f"[ENTRY]: Allocated port {port}")
    subprocess.Popen(["python3", "server.py", str(port)])
    return JSONResponse(content={"port":port})