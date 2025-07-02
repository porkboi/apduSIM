import subprocess
import re
import os
import fcntl
import json
import requests
import base64
import re
import certifi
import serial
import time

DEVICE_PATH = "/dev/ttyACM0"
INITIAL_COMMANDS = [
    "m\r\n4\r\ny",
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

def send_to_device_individually(commands, long=False, xxd=False):
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
                    subprocess.run(["bash", "-c", f"echo -e '{full_cmd}' > {DEVICE_PATH}"])
                else:
                    subprocess.run(["bash", "-c", f"echo -e '{full_cmd}' | xxd -r -p > {DEVICE_PATH}"])
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
                subprocess.run(["bash", "-c", f"echo -e '{full_cmd}' > {DEVICE_PATH}"])
            else:
                subprocess.run(["bash", "-c", f"echo -e '{full_cmd}' | xxd -r -p > {DEVICE_PATH}"])

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
            final.append(f"81e2110078{toSend[0:240]}")
            strCount+=240
        elif (i==1):
            final.append(f"81e2910141{toSend[240:370]}")
            strCount+=130
        elif (i==2):
            final.append(f"81e291001c{toSend[370:426]}")
            strCount+=(426-370)
        elif (i==3):
            final.append(f"81e2910003{toSend[426:432]}")
            strCount+=6
        elif (i==4):
            final.append(f"81e2110078{toSend[432:672]}")
            strCount+=(672-432)
        elif (i==5):
            final.append(f"81e291014f{toSend[672:830]}")
            strCount+=(830-672)
        elif (i==6):
            final.append(f"81e291004c{toSend[830:982]}")
            strCount+=(982-830)
        elif (i==7):
            final.append(f"81e2910004{toSend[982:990]}")
            strCount+=8
        elif (i==225):
            final.append(f"81e2910143{toSend[-134:]}")
            strCount+=134
        elif (i==224):
            final.append(f"81e2110078{toSend[-374:-134]}")
            strCount+=240
        elif (i==226):
            final.append(f"81c00000b9")
        else:
            match (i+1)%9:
                case 8:
                    final.append(f"81e291083c{toSend[strCount:strCount+120]}")
                    strCount+=120
                case _:
                    final.append(f"81e2110{(i+1)%9}78{toSend[strCount:strCount+240]}")
                    strCount+=240
    return final
                
def hex_to_base64(hex_str):
    bytesData = bytes.fromhex(hex_str)
    base64Bytes = base64.b64encode(bytesData)
    return base64Bytes.decode('utf-8')

def b2h(b : bytearray) -> str:
    return ''.join(['%02x' % (x) for x in b])

def int2hex(num : int):
    match num:
        case 10:
            return "a"
        case 11:
            return "b"
        case 12:
            return "c"
        case 13:
            return "d"
        case 14:
            return "e"
        case 15:
            return "f"
        case _:
            match num//16:
                case 0:
                    return str(num)
                case _:
                    return int2hex(num//16) + int2hex(num%16)

class SIMTransportLayer():
    def __init__(self):
        self.ser = serial.Serial(
            port="/dev/ttyACM0",
            parity=serial.PARITY_EVEN,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_TWO,
            timeout=1,
            xonxoff=0,
            rtscts=0,
            baudrate=9600
        )
        self._rst_pin = "-rst"
        rst_meth=self.ser.setRTS
        rst_meth(1)
        time.sleep(0.1)
        self.ser.flushInput()
        rst_meth(0)
        self.ser.read(64)
    
    def tx(self, b : bytearray):
        #print(b)
        self.ser.write(b)
        #self.ser.flush()
        r = self.ser.read(len(b))
        #print(r)
        if r != b: return
    
    def rx(self, len=1):
        return self.ser.read(len)
    
    def send_apdu(self, b1 : bytearray):
        dataSize = b1[4]
        #print(b1[:5])
        self.tx(b1[:5])
        while True:
            b = self.rx()
            #print(b)
            if ord(b) == b1[1]:
                break
            if b != b'\x60':
                sw1 = b
                sw2 = self.rx()
                nil = self.rx()
                if sw2 and not nil:
                    print(sw1, sw2)
                    return
                print("Error")
        if len(b1) > 5:
            #print(b2h(b1[5:]))
            self.tx(b1[5:])
        
        if (dataSize == 0): dataSize = 256
        toGet = dataSize - len(b1) + 7
        data = bytes(0)
        while len(data) < toGet:
            b = self.rx()
            if (toGet == 2) and (b == b'\x60'):
                continue
            if not b:
                break
            data += b
        
        self.ser.flushInput()
        self.ser.flushOutput()

        if len(data) < 2:
            return None, None
        #print(b2h(data[-2:]), b2h(data[:-2]))
        return b2h(data[-2:]), b2h(data[:-2])

def provision (domain : str, activation : str):
    global command_buffer
    command_buffer.extend(["bridge"])
    send_to_device_individually(command_buffer)
    command_buffer=[]
    new = SIMTransportLayer()

    apdu = '0070000001'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '01a404000fa0000005591010ffffffff89000001'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '01c0000021'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    print("es10b: GetEuiccChallenge")
    apdu = '81e2910003bf2e00'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '81c0000015'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)
    var1 = hex_to_base64(data[10:])

    print("es10b: GetEuiccInfo1")
    apdu = '81e2910003bf2000'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '81c0000038'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)
    var2 = hex_to_base64(data)

    print("es9p: initiateAuthentication")
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
    var3 = rx["transactionId"]

    print("es10b: serverAuthenticate")
    active= f"a0248018{activation.encode(encoding='ascii').hex()}a10880"
    toSend = f"bf3882034a{base64.b64decode(rx["serverSigned1"]).hex()
                            }{base64.b64decode(rx["serverSignature1"]).hex()
                              }{base64.b64decode(rx["euiccCiPKIdToBeUsed"]).hex()
                                }{base64.b64decode(rx["serverCertificate"]).hex()
                                  }{active}"
    
    listOfCommands = longCommandToAPDUs(toSend)
    #print([len(i) for i in listOfCommands])
    for cmdNo in range(len(listOfCommands)):
        apdu = f"81e2110{cmdNo}78{listOfCommands[cmdNo]}"
        t = bytearray.fromhex(apdu)
        sw, data = new.send_apdu(t)
    apdu = '81e29107070435290611a100'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)
    
    apdu = '81c0000000'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)
    var8 = ""
    while sw=="6100":
        var8+=data
        apdu = '81c0000000'
        t = bytearray.fromhex(apdu)
        sw, data = new.send_apdu(t)
    var8+=data
    apdu = f'81c00000{sw[-2:]}'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)
    var8+=data
    val = hex_to_base64(var8)

    print("es9p: authenticateClient")
    tx = {
        "transactionId": var3,
        "authenticateServerResponse": val,
    }
    rx_raw = requests.post(url=f"https://{domain}/gsma/rsp2/es9plus/authenticateClient", 
                        headers={
                            "User-Agent": "gsma-rsp-lpad",
                            "X-Admin-Protocol": "gsma/rsp/v2.2.0",
                            "Content-Type": "application/json",
                        },
                        json=tx, 
                        verify='certificate.pem')
    '''rx: {
        "transactionId" : var3,
        "profileMetadata" : var9,
        "smdpSigned2" : var10,
        "smdpSignature2" : var11,
        "smdpCertificate" : var12
    } '''
    rx = rx_raw.json()
    #print(rx)

    print("es10b: prepareDownoadResponse")
    toSend = f"bf218202d5{base64.b64decode(rx["smdpSigned2"]).hex()
                            }{base64.b64decode(rx["smdpSignature2"]).hex()
                                }{base64.b64decode(rx["smdpCertificate"]).hex()}"
    listOfCommands = longCommandToAPDUs(toSend)
    #print([len(i) for i in listOfCommands])
    for cmdNo in range(len(listOfCommands)-1):
        apdu = f"81e2110{cmdNo}78{listOfCommands[cmdNo]}"
        t = bytearray.fromhex(apdu)
        sw, data = new.send_apdu(t)
    apdu = '81e291060aa31bc405191353b0cfad'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '81c00000a2'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)
    var13 = hex_to_base64(data)

    print("es9p: getBoundProfilePackage")
    tx = {
        "transactionId": var3,
        "prepareDownloadResponse": var13,
    }
    rx_raw = requests.post(url=f"https://{domain}/gsma/rsp2/es9plus/getBoundProfilePackage", 
                        headers={
                            "User-Agent": "gsma-rsp-lpad",
                            "X-Admin-Protocol": "gsma/rsp/v2.2.0",
                            "Content-Type": "application/json",
                        },
                        json=tx, 
                        verify='certificate.pem')
    rx = rx_raw.json()

    print("es10b: loadBoundProfilePackage")
    boundProfile = base64.b64decode(rx["boundProfilePackage"]).hex()
    listOfCommands = lbpp(boundProfile)
    #print([len(i) for i in listOfCommands])
    for cmdNo in range(len(listOfCommands)):
        if cmdNo % 3 == 0:
            print("#", end="", flush=True)
        try:
            apdu = listOfCommands[cmdNo]
            t = bytearray.fromhex(apdu)
            sw, data = new.send_apdu(t)
        except Exception:
            print(cmdNo)
            break
    print("\nOk: ", sw, data)

def print_res(new : SIMTransportLayer, sw : str, data1 : str, ctr : int):
    #print(sw)
    if sw == "9000":
        return (ctr, data1)
    elif sw == "6100":
        apdu = '81c0000000'
        t = bytearray.fromhex(apdu)
        sw, data = new.send_apdu(t)
        data1 += data
        return print_res(new, sw, data1, ctr+1)
    elif sw.startswith("61"):
        apdu = f'81c00000{sw[-2:]}'
        t = bytearray.fromhex(apdu)
        sw, data = new.send_apdu(t)
        data1 += data
        #print(ctr, data1)
        return (ctr, data1)
    else:
        raise(f"Error - {sw}")
    
def list_profile():
    global command_buffer
    command_buffer.extend(["bridge"])
    send_to_device_individually(command_buffer)
    command_buffer=[]
    new = SIMTransportLayer()
    #time.sleep(3)

    apdu = '0070000001'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '01a404000fa0000005591010ffffffff89000001'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '01c0000021'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '81e2910003bf2d00'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    ctr, stri = print_res(new, sw, "", 0)

    if ctr != 0:
        print(stri[20:48])
        print("Count next")
    else:
        print(stri[20:48])

def get_eid():
    global command_buffer
    command_buffer.extend(["bridge"])
    send_to_device_individually(command_buffer)
    command_buffer=[]
    new = SIMTransportLayer()

    apdu = '0070000001'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '01a404000fa0000005591010ffffffff89000001'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '01c0000021'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '81e2910006bf3e035c015a'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    (ctr, stri) = print_res(new, sw, data, 0)

def delete_profile(iccid : str):
    global command_buffer
    command_buffer.extend(["bridge"])
    send_to_device_individually(command_buffer)
    command_buffer=[]
    new = SIMTransportLayer()

    apdu = '0070000001'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '01a404000fa0000005591010ffffffff89000001'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    apdu = '01c0000021'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    print(iccid[8:])
    apdu = f'81e291000fbf330c5a0a{iccid[8:]}'
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)

    ctr, stri = print_res(new, sw, data, 0)

def main():
    global command_buffer
    global parse_cmd

    command_buffer = [f"{cmd}" for cmd in INITIAL_COMMANDS]
    print("Initial commands added. \nEnter APDU commands (hex or hex:{n}) \n'parse=**' which could be GET.EID \n'ar' to auto-respond \n'run' to send \n'exit' to quit.")
    listOfCmds = []
    while True:
        user_input = input("> ").strip().lower()

        if user_input == "runOld":
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

        elif user_input == "run":
            new = SIMTransportLayer()
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
            list_profile()

        elif user_input == "get_eid":
            get_eid()
        
        elif user_input.startswith("delete"):
            match = re.search(r'iccid=([0-9A-Za-z]+)', user_input)
            if match:
                iccid = match.group(1)
                delete_profile(iccid)
            else:
                print("iccid missing")

        elif user_input == "ar":
            command_buffer.append("ar")
            print("Buffered special 'ar' command.")
        
        elif user_input.startswith("provision"):
            match = re.search(r'\$(.*?)\$', user_input)
            if match:
                domain = match.group(1)
                match2 = re.search(r'\$([^$]+)$', user_input)
                if match2:
                    activation = match2.group(1).upper()
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
                #apdu_command = format_apdu_command(hex_string)
                command_buffer.extend(["bridge"])
                listOfCmds.extend([hex_string]*repeat)
                print(f"Buffered {repeat}x: {hex_string}")
            except ValueError as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()