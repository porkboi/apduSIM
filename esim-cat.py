import subprocess
import re
import time
import select
import os

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

command_buffer = []

def format_apdu_command(hex_string):
    if len(hex_string) % 2 != 0:
        raise ValueError("APDU command must have even number of hex digits.")
    bytes_list = [f"0x{hex_string[i:i+2]}" for i in range(0, len(hex_string), 2)]
    return f"[{' '.join(bytes_list)}"

def parse_input_line(line):
    match = re.fullmatch(r"([0-9a-fA-F]+)(?::\{(\d+)\})?", line.strip())
    if not match:
        raise ValueError("Invalid input format.")
    hex_part = match.group(1)
    repeat = int(match.group(2)) if match.group(2) else 1
    return hex_part.lower(), repeat

def send_to_device_individually(commands):
    for cmd in commands:
        # Wrap command in CRLF as required by Bus Pirate
        full_cmd = f"\r\n{cmd}\r\n"
        subprocess.run(["bash", "-c", f"echo -e '{full_cmd}' > {DEVICE_PATH}"])
        time.sleep(0.2)  # Optional delay to allow processing time

def read_all_from_device():
    """Runs `cat /dev/ttyACM0`, captures output, and returns the last line seen within timeout."""
    subprocess.run(["cat", DEVICE_PATH, ">", "output.txt"])
    with open("output.txt", "r") as f:
        lines = f.readlines()
    if lines:
        return lines[-1].strip()
    return "Empty"

def main():
    global command_buffer

    command_buffer = [f"{cmd}" for cmd in INITIAL_COMMANDS]
    print("Initial commands added. Enter APDU commands (hex or hex:{n}), or 'run' to send, or 'exit':")

    while True:
        user_input = input("> ").strip().lower()

        if user_input == "run":
            print(f"\nSending each command to {DEVICE_PATH}...\n")
            send_to_device_individually(command_buffer)
            print("Reading response from device...")
            response = read_all_from_device()
            print(f"Device Response: {response}")
            break

        elif user_input == "exit":
            print("Exiting without sending.")
            break

        elif re.match(r"^[0-9a-f]+(?::\{\d+\})?$", user_input):
            try:
                hex_string, repeat = parse_input_line(user_input)
                apdu_command = format_apdu_command(hex_string)
                command_buffer.extend([f"{apdu_command}"] * repeat)
                print(f"Buffered {repeat}x: {apdu_command}")
            except ValueError as e:
                print(f"Error: {e}")
        else:
            print("Invalid input. Enter a hex string, hex:{n}, or 'run'.")

if __name__ == "__main__":
    main()
