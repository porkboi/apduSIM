import re
import json
import asyncio
import threading
import socket
import websockets
from src.oldFuncs import *
from src.newFuncs import *
import config
import sys
import requests

websock = set()

class WSStdoutRedirector:
    def __init__(self, terminal=sys.__stdout__):
        self.terminal = terminal
        self.buffer = ""
    
    def write(self, message):
        self.terminal.write(message)
        self.buffer += message
    
    def flush(self):
        self.terminal.flush()

    def flush_output(self):
        if self.buffer:
            for wb in websock.copy():
                try:
                    
                    asyncio.run_coroutine_threadsafe(wb.send(self.buffer), config.event_loop)
                except Exception:
                    websock.discard(wb)
            self.buffer=""

# WebSocket command queue

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

# WebSocket handler
async def ws_handler(websocket):
    try:
        websock.add(websocket)
        async for message in websocket:
            print(f"[WebSocket] Received: {message}")
            config.ws_command_queue.put(message)
            #await websocket.send(f"Command '{message}' received.")
    except websockets.exceptions.ConnectionClosed:
        print("[WebSocket] Client disconnected.")
        websock.discard(websocket)

# WebSocket server loop
async def ws_server():
    async with websockets.serve(ws_handler, "0.0.0.0", config.PORT):
        await asyncio.Future()  # Run forever

def open_port():
    config.event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(config.event_loop)
    config.event_loop.run_until_complete(ws_server())
    config.event_loop.run_forever()

# Load empty JSON if not existing
with open("dict.json", "w") as f:
    json.dump({}, f, indent=2)
with open("dict.json", "r") as f:
    d = json.load(f)

def get_dynamic_port():
    try:
        response = requests.get("http://localhost:8000/get-port")
        return response.json()["port"]
    except Exception:
        raise ValueError

def main():
    config.command_buffer = [f"{cmd}" for cmd in INITIAL_COMMANDS]
    print("Initial commands added. Enter APDU commands or use WebSocket")
    config.command_buffer.append("bridge")
    listOfCmds = []
    send_to_device_individually(config.command_buffer)
    config.command_buffer=[]
    new = SIMTransportLayer()
    pre = "> "
    while True:
        user_input = ""
        if config.SERVER:
            if not config.ws_command_queue.empty():
                user_input = config.ws_command_queue.get()
                print(f"[WebSocket Command] >> {user_input}")
                sys.stdout = WSStdoutRedirector()
            else:
                continue
        else:
            user_input = input(pre).strip().lower()
            sys.stdout = sys.__stdout__

        if user_input == "d":
            config.DEBUG_MODE = True
        elif user_input == "runOld":
            print(f"\nSending each command to {config.DEVICE_PATH}...\n")
            send_to_device_individually(config.command_buffer)
            print("Reading response from device...")
            if config.parse_cmd == "GET.EID":
                try:
                    sol = print_after_last_gt(response_full)
                    new_sol = sol[33:-10]
                    lst = new_sol.split(" 0x")
                    print(f"EID:{"".join(lst)}")
                except Exception as e:
                    print(f"Error parsing GET.EID: {e}")
            elif config.parse_cmd == "GET.ICCID":
                try:
                    sol = print_after_last_gt(response_full).split(" 0x")[13:23]
                    new_sol = [s[::-1] for s in sol]
                    val1 = "".join(new_sol)
                    print(f"ICCID 1: {val1}")
                    if val1.isnumeric():
                        user_input2 = input("Save this as iccid1? Y/n > ").strip().lower()
                        if user_input2 == "y":
                            add_to_json("iccid1", val1)
                    try:
                        sol2 = print_after_last_gt(response_full).split(" 0x")[13 + 140:23 + 140]
                        new_sol2 = [s[::-1] for s in sol2]
                        val2 = "".join(new_sol2)
                        print(f"ICCID 2: {val2}")
                        if val2.isnumeric():
                            user_input2 = input("Save this as iccid2? Y/n > ").strip().lower()
                            if user_input2 == "y":
                                add_to_json("iccid2", val2)
                    except Exception as e:
                        print(f"Error parsing ICCID 2: {e}")
                except Exception as e:
                    print(f"Error parsing GET.ICCID 1: {e}")
                    break
            else:
                print(f"Device Response: {print_after_last_gt(response_full)}")
            config.command_buffer = []
            config.parse_cmd = ""

        elif user_input == "run":
            for cmdNo in range(len(listOfCmds)):
                try:
                    apdu = listOfCmds[cmdNo]
                    t = bytearray.fromhex(apdu)
                    sw, data = new.send_apdu(t)
                    print_res(new, sw, data, 0)
                except Exception:
                    print(cmdNo)
                    break

        elif user_input == "exit":
            print("Exiting without sending.")
            break

        elif user_input == "list":
            list_profile(new)
            sys.stdout.flush()
            sys.stdout.flush_output()

        elif user_input == "get_eid":
            get_eid(new)
            sys.stdout.flush()
            sys.stdout.flush_output()

        elif user_input.startswith("delete"):
            match = re.search(r'iccid=([0-9A-Za-z]+)', user_input)
            if match:
                iccid = match.group(1)
                delete_profile(new, iccid)
                print("Left:")
                list_profile(new)
            else:
                print("iccid missing. Hint: include iccid=")

        elif user_input.startswith("enable"):
            match = re.search(r'iccid=([0-9A-Za-z]+)', user_input)
            if match:
                iccid = match.group(1)
                enable_profile(new, iccid)
                print(f"Active: {iccid}, Disabled Previous")
            else:
                print("iccid missing. Hint: include iccid=")

        elif user_input.startswith("disable"):
            match = re.search(r'iccid=([0-9A-Za-z]+)', user_input)
            if match:
                iccid = match.group(1)
                disable_profile(new, iccid)
                print(f"Disabled: {iccid}")
            else:
                print("iccid missing. Hint: include iccid=")

        elif user_input == "r":
            scan(new)
            sys.stdout.flush()
            sys.stdout.flush_output()

        elif user_input.startswith("select"):
            match pre:
                case "> ":
                    match = re.search(r'aid=([0-9A-Za-z]+)', user_input)
                    if match:
                        aid = match.group(1)
                        select_f(new, aid)
                        match aid:
                            case "a0000005591010ffffffff8900000100":
                                pre = "> (ADF.ISD-R) "
                            case "a0000000871002ffffffff8903050001":
                                pre = "> (ADF.USIM) "
                            case "a0000005591010ffffffff8900000200":
                                pre = "> (ADF.ECASD) "
                    else:
                        print("AID missing. Hint: include aid=")
                case "> (ADF.ISD-R) ":
                    match = re.search(r'method=([0-9A-Za-z]+)', user_input)
                    if match:
                        method = match.group(1)
                        print(method)
                        match method:
                            case "listnotifs":
                                sw, data = send(new, "81e2910003bf2800")
                                print_res(new, sw, data, 0)
                            case "geteim":
                                sw, data = send(new, "81e2910003bf5500")
                                print_res(new, sw, data, 0)
                            case "getcerts":
                                sw, data = send(new, "81e2910003bf5600")
                                print_res(new, sw, data, 0)
                            case _:
                                print("You can use: listnotifs, geteim, getcerts")
                    else:
                        print("Method missing. Hint: include method=")

        elif user_input == "ar":
            config.command_buffer.append("ar")
            print("Buffered special 'ar' command.")

        elif user_input.startswith("provision"):
            match = re.search(r'\$(.*?)\$', user_input)
            if match:
                domain = match.group(1)
                match2 = re.search(r'\$([^$]+)$', user_input)
                if match2:
                    activation = match2.group(1).upper()
                    provision(new, domain, activation)
                else:
                    print("Poorly formed activation code.")
            else:
                print("No activation code, Hint: include ac=")

        elif user_input.startswith("parse="):
            config.parse_cmd = user_input[6:].upper()
            print(f"Set parse command to: {config.parse_cmd}")

        elif user_input == "":
            continue
        else:
            try:
                hex_string, repeat = parse_input_line(user_input)
                listOfCmds.extend([hex_string]*repeat)
                print(f"Buffered {repeat}x: {hex_string}")
            except ValueError as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    print("Finding Server...")
    config.PORT = get_dynamic_port()

    threading.Thread(target=open_port, daemon=True).start()
    time.sleep(1)
    #threading.Thread(target=runApp, daemon=True).start()
    main()
