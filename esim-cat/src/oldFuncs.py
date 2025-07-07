import subprocess
import re
import os
import fcntl
import json
import config

response_full = config.response_full

def format_apdu_command(hex_string : str):
    """Changes hex string into an APDU format \n
    //@requires: HEX characters in the input string"""
    if len(hex_string) % 2 != 0:
        raise ValueError("APDU command must have even number of hex digits.")
    bytes_list = [f"0x{hex_string[i:i+2]}" for i in range(0, len(hex_string), 2)]
    return f"[{' '.join(bytes_list)}"

#ChatGPTed function
def replace_env(match):
    """Loads dictionary and finds the saved variable \n
    //@requires: Valid regex match"""
    with open("dict.json", "r") as f:
        d = json.load(f)
        key = match.group(1)
        return d[key]

def parse_input_line(line : str):
    """Parses the input line for 2nd depth functions \n
    //@requires: Valid str input"""
    match = re.fullmatch(r"([0-9a-fA-F\[\]a-zA-Z0-9]+)(?::\{(\d+)\})?", line.strip())
    if not match:
        raise ValueError("Invalid input format.")
    hex_part = match.group(1)
    if re.search(r"\[.*?\]", hex_part.lower()):
        hex_part = re.sub(r'\[(.*?)\]', replace_env, hex_part.lower())
    repeat = int(match.group(2)) if match.group(2) else 1
    return hex_part.lower(), repeat

def send_to_device_individually(commands, long=False, xxd=False):
    """Sends APDU to eSIM via Linux echo -e \n
    //@requires: Valid list of HEX commands \n
    //@requires \forall cmd in commands, len(cmd) < 100 bytes """
    global response_full
    global d
    global st

    with open("dict.json", "r") as f:
        d = json.load(f)

    for cmd in commands:
        # If the command is the special "ar", resolve it dynamically
        if cmd == "ar":

            print(f"Received from device: {st}")

            match = re.search(r'0x61[\s,;:-]*0x([0-9a-fA-F]{2}).*?', st, re.DOTALL)

            if match:
                ab_hex = match.group(1).upper()
                cmd = f"00C00000{ab_hex}"
                print(f"Resolved 'ar' to command: {cmd}")
                full_cmd = f"\r\n{format_apdu_command(cmd)}\r\n"
                if not xxd:
                    subprocess.run(["bash", "-c", f"echo -e '{full_cmd}' > {config.DEVICE_PATH}"])
                else:
                    subprocess.run(["bash", "-c", f"echo -e '{full_cmd}' | xxd -r -p > {config.DEVICE_PATH}"])
                #time.sleep(0.1)  # Allow processing time

                # Read and accumulate response
                st = read_all_from_device()
                response_full += st
            else:
                print("Warning: Could not resolve 'ar' — no 0x61 AB pattern found.")
                continue  # Skip sending if unresolved
        else:
        # Wrap command in CRLF as required by Bus Pirate
            full_cmd = f"\r\n{cmd}\r\n"
            if not xxd:
                subprocess.run(["bash", "-c", f"echo -e '{full_cmd}' > {config.DEVICE_PATH}"])
            else:
                subprocess.run(["bash", "-c", f"echo -e '{full_cmd}' | xxd -r -p > {config.DEVICE_PATH}"])

            # Read and accumulate response
            st = read_all_from_device()
            response_full += st


def print_after_last_gt(s):
    """Prints output in cat after the last '>' \n
    //@requires: HEX characters in the input string"""
    # Find the index of the last ">"
    last_index = s.rfind(">")
    if last_index != -1 and last_index + 1 < len(s):
        # Print everything after the last ">"
        return s[last_index + 1:]
    else:
        # If ">" is not found or nothing follows it
        return ''

def read_all_from_device(timeout_sec=0.5):
    """Runs `cat /dev/ttyACM0`, captures output, and returns the last line seen within timeout.
    //@requires: None"""
    try:
        with open(config.DEVICE_PATH, "rb", buffering=0) as tty:
            # Set non-blocking mode
            fd = tty.fileno()
            flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

            import time
            start_time = time.time()
            buffer = bytearray()

            while time.time() - start_time < timeout_sec:
                try:
                    data = tty.read(1024)
                    if data:
                        buffer.extend(data)
                    else:
                        time.sleep(0.0)
                except BlockingIOError:
                    time.sleep(0.0)
            return buffer.decode("utf-8", errors="replace")

    except Exception as e:
        return f"Error: {e}"

def reverse_adjacent_pairs(n):
    """ChatGPTed function to reverse pairs, aka convert little endian to big endian \n
    //@requires: HEX characters in the input string"""
    s = str(n)
    result = []

    # Step through two characters at a time
    for i in range(0, len(s) - 1, 2):
        result.append(s[i+1])
        result.append(s[i])

    # If there's an odd digit left at the end, append it as-is
    if len(s) % 2 != 0:
        result.append(s[-1])

    return int(''.join(result))

def add_to_json(key, val):
    with open("dict.json", "r") as f:
        data = json.load(f)
        if not isinstance(data, dict):
            data = {}
        val1 = reverse_adjacent_pairs(val)
        data[key] = str(val1)
    try:
        with open("dict.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"Added {key}:{val}")
    except Exception as e:
        print("Error adding to dict")