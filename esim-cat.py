import subprocess
import re
import os
import fcntl
import json

DEVICE_PATH = "/dev/ttyACM0"
INITIAL_COMMANDS = [
    "m",
    "4",
    "y",
    "W\r\n3.30\r\n50",
    "P",
    "G\r\n1\r\n3.57MHz\r\n50%",
    "binmode\r\n1\r\ny",
    "P"
]

response_full = ""
latest_response = ""
command_buffer = []
parse_cmd = ""
st = ""
with open("dict.json", "w") as f:
    json.dump({}, f, indent=2)

with open("dict.json", "r") as f:
    d = json.load(f)

def format_apdu_command(hex_string):
    if len(hex_string) % 2 != 0:
        raise ValueError("APDU command must have even number of hex digits.")
    bytes_list = [f"0x{hex_string[i:i+2]}" for i in range(0, len(hex_string), 2)]
    return f"[{' '.join(bytes_list)}"

#ChatGPTed function
def replace_env(match):
    with open("dict.json", "r") as f:
        d = json.load(f)
        key = match.group(1)
        return d[key]

def parse_input_line(line):
    match = re.fullmatch(r"([0-9a-fA-F\[\]a-zA-Z0-9]+)(?::\{(\d+)\})?", line.strip())
    if not match:
        raise ValueError("Invalid input format.")
    hex_part = match.group(1)
    if re.search(r"\[.*?\]", hex_part.lower()):
        hex_part = re.sub(r'\[(.*?)\]', replace_env, hex_part.lower())
    repeat = int(match.group(2)) if match.group(2) else 1
    return hex_part.lower(), repeat

def send_to_device_individually(commands):
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
                subprocess.run(["bash", "-c", f"echo -e '{full_cmd}' > {DEVICE_PATH}"])
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
            subprocess.run(["bash", "-c", f"echo -e '{full_cmd}' > {DEVICE_PATH}"])
            #time.sleep(0.1)  # Allow processing time

            # Read and accumulate response
            st = read_all_from_device()
            response_full += st


def print_after_last_gt(s):
    # Find the index of the last ">"
    last_index = s.rfind(">")
    if last_index != -1 and last_index + 1 < len(s):
        # Print everything after the last ">"
        return s[last_index + 1:]
    else:
        # If ">" is not found or nothing follows it
        return ''

def read_all_from_device(timeout_sec=5):
    """Runs `cat /dev/ttyACM0`, captures output, and returns the last line seen within timeout."""
    try:
        with open("/dev/ttyACM0", "rb", buffering=0) as tty:
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

def main():
    global command_buffer
    global parse_cmd

    command_buffer = [f"{cmd}" for cmd in INITIAL_COMMANDS]
    print("Initial commands added. \nEnter APDU commands (hex or hex:{n}) \n'parse=**' which could be GET.EID \n'ar' to auto-respond \n'run' to send \n'exit' to quit.")

    while True:
        user_input = input("> ").strip().lower()

        if user_input == "run":
            print(f"\nSending each command to {DEVICE_PATH}...\n")
            send_to_device_individually(command_buffer)
            print("Reading response from device...")
            #response = print_after_last_gt(read_all_from_device())
            if parse_cmd == "GET.EID":
                try:
                    sol = print_after_last_gt(response_full)
                    new_sol = sol[33:-10]
                    lst = new_sol.split(" 0x")          
                    print(f"EID: {"".join(lst)}")
                except Exception as e:
                    print(f"Error parsing GET.EID: {e}")
            elif parse_cmd == "GET.ICCID":
                #counter = 1
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
                            if user_input2 == "Y":
                                add_to_json("iccid2", val2)
                    except Exception as e:
                        print(f"Error parsing ICCID 2: {e}")
                except Exception as e:
                    print(f"Error parsing GET.ICCID 1: {e}")
                    break
            else:
                print(f"Device Response: {print_after_last_gt(response_full)}")
            command_buffer = []
            parse_cmd = ""
            #break

        elif user_input == "exit":
            print("Exiting without sending.")
            break
        
        elif user_input == "ar":
            command_buffer.append("ar")
            print("Buffered special 'ar' command.")
        
        elif user_input.startswith("parse="):
            parse_cmd = user_input[6:].upper()
            print(f"Set parse command to: {parse_cmd}")

        else:
            try:
                hex_string, repeat = parse_input_line(user_input)
                apdu_command = format_apdu_command(hex_string)
                command_buffer.extend([f"{apdu_command}"] * repeat)
                print(f"Buffered {repeat}x: {apdu_command}")
            except ValueError as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
