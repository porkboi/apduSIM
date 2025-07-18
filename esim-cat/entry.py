import json
import socket
import subprocess
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
import asyncio
import threading
import time
import os

app = FastAPI()
allocated_ports = set()
websockets = set()

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

@app.get("/")
async def dashboard():
    # Read usage instructions from README.md
    readme = "list, get_eid, provision ac=, enable/disable iccid="
    return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head>
    <title>APDU SIM Dashboard</title>
    <style>
        body {{ display: flex; font-family: sans-serif; margin: 0; }}
        #sidebar {{
            width: 300px; background: #f4f4f4; padding: 1em; height: 100vh; overflow-y: auto;
            border-right: 1px solid #ccc;
        }}
        #main {{ flex: 1; padding: 2em; }}
        #ports {{ margin-bottom: 2em; }}
        .port-item {{ cursor: pointer; padding: 0.5em; border-radius: 4px; }}
        .port-item.selected {{ background: #d0eaff; }}
        #usage {{ font-size: 0.9em; background: #fffbe6; padding: 1em; border-radius: 6px; }}
        #output {{ border: 1px solid #ccc; min-height: 100px; margin-bottom: 1em; padding: 1em; background: #fafafa; white-space: pre-wrap; }}
        #input-bar {{ width: 100%; padding: 0.5em; font-size: 1em; }}
        #send-btn {{ padding: 0.5em 1em; font-size: 1em; margin-left: 0.5em; }}
    </style>
</head>
<body>
    <div id="sidebar">
        <h3>Ports</h3>
        <div id="ports"></div>
        <h3>How to use</h3>
        <div id="usage">{readme}</div>
    </div>
    <div id="main">
        <div id="output"></div>
        <div style="display: flex;">
            <input id="input-bar" placeholder="Type command..." />
            <button id="send-btn">Send</button>
        </div>
    </div>
    <script>
        let ws = new WebSocket(`ws://${{location.host}}/ws`);
        let ports = [];
        let selectedPort = null;
        let backendWS = null;
        let output = document.getElementById("output");

        ws.onmessage = (event) => {{
            let msg = JSON.parse(event.data);
            if(msg.type === "ports") {{
                ports = msg.ports;
                renderPorts();
            }}
        }};

        function renderPorts() {{
            let el = document.getElementById("ports");
            el.innerHTML = "";
            ports.forEach(port => {{
                let div = document.createElement("div");
                div.textContent = port;
                div.className = "port-item" + (port === selectedPort ? " selected" : "");
                div.onclick = () => selectPort(port);
                el.appendChild(div);
            }});
        }}

        function logOutput(msg) {{
            output.textContent += msg + "\\n";
            output.scrollTop = output.scrollHeight;
        }}

        function selectPort(port) {{
            if (port !== selectedPort) {{
                if (backendWS) {{
                    backendWS.close();
                    backendWS = null;
                }}
                selectedPort = port;
                renderPorts();
                logOutput("🔌 Connecting to backend for port " + port + "...");
                backendWS = new WebSocket(`ws://localhost:${{port}}`);
                backendWS.onopen = () => {{
                    logOutput("🟢 Connected to backend for port " + port);
                }};
            }}
            backendWS.onmessage = (event) => {{
                logOutput("📥 " + event.data);
            }};
            backendWS.onclose = () => {{
                logOutput("🔴 Disconnected from backend for port " + port);
            }};
            backendWS.onerror = (e) => {{
                logOutput("❌ Backend connection error.");
            }};
        }}

        function sendCommand() {{
            let cmd = document.getElementById("input-bar").value.trim();
            if (!cmd) return;
            if (!backendWS || backendWS.readyState !== 1) {{
                logOutput("❌ Not connected to backend for any port.");
                return;
            }}
            backendWS.send(cmd);
            logOutput("> " + cmd);
            document.getElementById("input-bar").value = "";
        }}

        document.getElementById("input-bar").addEventListener("keydown", function(e) {{
            if(e.key === "Enter") {{
                sendCommand();
            }}
        }});
        document.getElementById("send-btn").onclick = sendCommand;
    </script>
</body>
</html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websockets.add(websocket)
    try:
        # Send current ports on connect
        await websocket.send_json({"type": "ports", "ports": sorted(allocated_ports)})
        while True:
            data = await websocket.receive_text()
            # Here you could handle commands sent from the frontend
            # For now, just echo
            # await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Disconnected")
        websockets.remove(websocket)

@app.get("/get-port")
async def get_port():
    PORT = find_free_port()
    allocated_ports.add(PORT)
    subprocess.Popen(["python3", "server.py", str(PORT)])
    # Notify all websockets
    for ws in list(websockets):
        try:
            await ws.send_json({"type": "ports", "ports": sorted(allocated_ports)})
        except Exception:
            websockets.discard(ws)
    time.sleep(1)
    return JSONResponse(content={"port":PORT})