import subprocess
import re
import os
import fcntl
import json
import requests
import base64
import re
import certifi
import ast

DEVICE_PATH = "/dev/ttyACM0"
INITIAL_COMMANDS = [
    "m",
    "4\r\ny",
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

def read_all_from_device(timeout_sec=0.5):
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

def longCommandToAPDUs (toSend : str):
    return [toSend[i:i+240] for i in range(0, len(toSend), 240)]

def lbpp(toSend : str):
    final = []
    strCount = 0
    for i in range(227):
        if (i==0):
            final.append(f"00e2110078{toSend[0:240]}")
            strCount+=240
        elif (i==1):
            final.append(f"00e2910141{toSend[240:370]}")
            strCount+=130
        elif (i==2):
            final.append(f"00e291001c{toSend[370:426]}")
            strCount+=(426-370)
        elif (i==3):
            final.append(f"00e2910003{toSend[426:432]}")
            strCount+=6
        elif (i==4):
            final.append(f"00e2110078{toSend[432:672]}")
            strCount+=(672-432)
        elif (i==5):
            final.append(f"00e291014f{toSend[672:830]}")
            strCount+=(830-672)
        elif (i==6):
            final.append(f"00e291004c{toSend[830:982]}")
            strCount+=(982-830)
        elif (i==7):
            final.append(f"00e2910004{toSend[982:990]}")
            strCount+=8
        elif (i==225):
            final.append(f"00e2910143{toSend[-134:]}")
            strCount+=134
        elif (i==224):
            final.append(f"00e2110078{toSend[-374:-134]}")
            strCount+=240
        elif (i==226):
            final.append(f"00c00000b9")
        else:
            match (i+1)%9:
                case 8:
                    final.append(f"00e291083c{toSend[strCount:strCount+120]}")
                    strCount+=120
                case _:
                    final.append(f"00e2110{(i+1)%9}78{toSend[strCount:strCount+240]}")
                    strCount+=240
                
def hex_to_base64(hex_str):
    bytesData = bytes.fromhex(hex_str)
    base64Bytes = base64.b64encode(bytesData)
    return base64Bytes.decode('utf-8')

def provision (domain : str, activation : str):
    global command_buffer
    global response_full

    hex_string, repeat = "00a404000fa0000005591010ffffffff89000001", 7
    apdu_command = format_apdu_command(hex_string)
    command_buffer.extend([f"{apdu_command}"] * repeat)
    print(f"Buffered {repeat}x: {apdu_command}")

    #return
    command_buffer.extend([f"{format_apdu_command("00c0000021")}"])
    print(f"\nSending each command to {DEVICE_PATH}...\n")
    send_to_device_individually(command_buffer)
    command_buffer=[]
    print("Reading response from device...")

    #euiccchallenge
    command_buffer.extend([f"{format_apdu_command("00e2910003bf2e00")}"])
    command_buffer.extend([f"{format_apdu_command("00c0000015")}"])
    print(f"\nSending each command to {DEVICE_PATH}...\n")
    send_to_device_individually(command_buffer)
    command_buffer=[]
    #res1 = read_all_from_device()
    print("Reading response from device...")
    data1 = re.sub(r'\s+0x', '', print_after_last_gt(response_full)).strip()
    data2 = data1[5:-5]
    data3 = data2[2:]
    #print(data3)
    var1 = hex_to_base64(data3[:-1])

    #euiccinfo1
    command_buffer.extend([f"{format_apdu_command("00e2910003bf2000")}"])
    command_buffer.extend([f"{format_apdu_command("00c0000038")}"])
    print(f"\nSending each command to {DEVICE_PATH}...\n")
    send_to_device_individually(command_buffer)
    command_buffer=[]
    print("Reading response from device...")
    #res2 = read_all_from_device(timeout_sec=5)
    data1 = re.sub(r'\s+0x', '', print_after_last_gt(response_full)).strip()
    #print(data1)
    data2 = data1[5:-4]
    data3 = data2[2:]
    #print(data3)
    var2 = hex_to_base64(data3)

    #es9p_initiate_authentication
    tx = {
        "smdpAddress":domain,
        "euiccChallenge":var1,
        "euiccInfo1":var2,
    }
    rx_raw = requests.post(url=f"https://{domain}/gsma/rsp2/es9plus/initiateAuthentication", 
                        headers={
                            "User-Agent": "gsma-rsp-lpad",
                            "X-Admin-Protocol": "gsma/rsp/v2.2.0",
                            "Content-Type": "application/json",
                        },
                        json=tx, 
                        verify='certificate.pem')
    '''rx: {
        "transactionId":var3,
        "serverSigned1":var4,
        "serverSignature1":var5,
        "euiccCiPKIdToBeUsed":var6,
        "serverCertificate":var7
    } '''

    rx = rx_raw.json()
    print(rx)
    #es10b
    toSend = f"bf3882034a{base64.b64decode(rx["serverSigned1"]).hex()
                            }{base64.b64decode(rx["serverSignature1"]).hex()
                              }{base64.b64decode(rx["euiccCiPKIdToBeUsed"]).hex()
                                }{base64.b64decode(rx["serverCertificate"]).hex()
                                  }{base64.b64decode(activation).hex()}"
    print("Sending es10b")
    listOfCommands = longCommandToAPDUs(toSend)
    #print(listOfCommands)
    command_buffer=[]
    print("Reading response from device...")
    for cmdNo in range(len(listOfCommands)):
        command_buffer.extend([format_apdu_command(f"00e2110{cmdNo}78{listOfCommands[cmdNo]}")])
    command_buffer.extend([f"{format_apdu_command("00e29107070435290611a100")}"])
    command_buffer.extend([f"{format_apdu_command("00c0000000")}"])
    print(f"\nSending each command to {DEVICE_PATH}...\n")
    send_to_device_individually(command_buffer)
    command_buffer=[]
    print("Reading response from device...")
    var8 = ""
    print(response_full)
    res = print_after_last_gt(response_full)
    while re.search(r'\b?61\s?00\b?', res) :
        res_clean = re.sub(r'\s+', '', re.sub(r'\b?61\s?00\b?', '', res)).strip()
        var8 += res_clean
        command_buffer.extend([f"{format_apdu_command("00c0000000")}"])
        print(f"\nSending each command to {DEVICE_PATH}...\n")
        send_to_device_individually(command_buffer)
        print("Reading response from device...")
        res = print_after_last_gt(response_full)
    match = re.search(r'\b?61\s?([0-9A-Fa-f]{2})', res)
    res_clean = re.sub(r'\s+', '', re.sub(r'\b?61\s?([0-9A-Fa-f]{2})', '', res)).strip()
    var8 += res_clean
    command_buffer.extend([f"{format_apdu_command(f"00c00000{match.group(1)}")}"])
    print(f"\nSending each command to {DEVICE_PATH}...\n")
    send_to_device_individually(command_buffer)
    command_buffer=[]
    print("Reading response from device...")
    res = print_after_last_gt(response_full)
    res_clean = re.sub(r'\s+', '', re.sub(r'\b90\s?00\b', '', res)).strip()
    var8 += res_clean
    var8 = base64.b64encode(var8)
    print(var8) # string manipulation here

    #es9p_authenticate_client
    tx = {
        "transactionId":rx.transactionId,
        "euiccInfo1":var8
    }
    rx = requests.post(url=f"https://{domain}/gsma/rsp2/es9plus/authenticateClient", data=str(tx), verify=certifi.where())
    '''rx: {
        "transactionId" : var3,
        "profileMetadata" : var9,
        "smdpSigned2" : var10,
        "smdpSignature2" : var11,
        "smdpCertificate" : var12
    } '''

    #es10b
    toSend = f"bf218202d5{base64.b64decode(rx.smdpSigned2).hex()
                            }{base64.b64decode(rx.smdpSignature2).hex()
                                }{base64.b64decode(rx.smdpCertificate).hex()}"
    listOfCommands = longCommandToAPDUs(toSend)
    for cmdNo in range(len(listOfCommands)):
        command_buffer.extend([format_apdu_command(f"00e2110{cmdNo}78{listOfCommands[cmdNo]}")])
    command_buffer.extend([f"{format_apdu_command("00e291060aa31bc405191353b0cfad")}"])
    command_buffer.extend([f"{format_apdu_command("00c00000a2")}"])
    print(f"\nSending each command to {DEVICE_PATH}...\n")
    send_to_device_individually(command_buffer)
    command_buffer=[]
    print("Reading response from device...")
    var13 = ""
    res = print_after_last_gt(response_full)
    res_clean = re.sub(r'\s+', '', re.sub(r'\b90\s?00\b', '', res)).strip()
    var13 += res_clean
    var13 = base64.b64encode(var13)
    print(var13) # string manipulation here

    #es9p_get_bound_package
    tx = {
        "transactionId":rx.transactionId,
        "prepareDownloadResponse":var13
    }
    rx = requests.post(url=f"https://{domain}/gsma/rsp2/es9plus/getBoundProfilePackage", json=tx.json())
    '''rx: {
        "transactionId" : var3,
        "boundProfilePackage" : var14
    } '''

    #es10b_load_bound_profile_package
    toSend = f"{base64.b64decode(rx.boundProfilePackage).hex()}"
    listOfCommands = lbpp(toSend)
    for cmd in listOfCommands:
        command_buffer.extend([format_apdu_command(cmd)])
    print(f"\nSending each command to {DEVICE_PATH}...\n")
    send_to_device_individually(command_buffer)
    command_buffer=[]
    print("Reading response from device...")
    res = print_after_last_gt(response_full)
    print(res)

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
        
        elif user_input.startswith("provision"):
            match = re.search(r'\$(.*?)\$', user_input)
            if match:
                domain = match.group(1)
                match2 = re.search(r'\$([^$]+)$', user_input)
                if match2:
                    activation = match2.group(1)
                    provision(domain, activation)
                else:
                    print("Fail")
            else:
                print("Fail")

            

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