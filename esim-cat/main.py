import re
import json
from src.oldFuncs import *
from src.newFuncs import *
import config

with open("dict.json", "w") as f:
    json.dump({}, f, indent=2)

with open("dict.json", "r") as f:
    d = json.load(f)

# DEBUG MODE is disabled by default
def main():  
    config.command_buffer = [f"{cmd}" for cmd in INITIAL_COMMANDS]
    print("Initial commands added. \nEnter APDU commands (hex or hex:{n}) \n'parse=**' which could be GET.EID \n'ar' to auto-respond \n'runOld' to send \n'exit' to quit.")
    print("You can alo use the pre-programmed APDUs: \n'list' \n'delete iccid=***' \n'provision ac=***' \n'get_eid'")
    print("'d' to enable debug mode")
    listOfCmds = []
    send_to_device_individually(config.command_buffer)
    config.command_buffer=[]
    new = SIMTransportLayer()
    while True:
        user_input = input("> ").strip().lower()
        
        if user_input == "d":
            config.DEBUG_MODE = True
        elif user_input == "runOld":
            print(f"\nSending each command to {config.DEVICE_PATH}...\n")
            send_to_device_individually(config.command_buffer)
            print("Reading response from device...")
            #response = print_after_last_gt(read_all_from_device())
            if config.parse_cmd == "GET.EID":
                try:
                    sol = print_after_last_gt(response_full)
                    new_sol = sol[33:-10]
                    lst = new_sol.split(" 0x")          
                    print(f"EID: {"".join(lst)}")
                except Exception as e:
                    print(f"Error parsing GET.EID: {e}")
            elif config.parse_cmd == "GET.ICCID":
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
            config.command_buffer = []
            config.parse_cmd = ""
            #break

        elif user_input == "run":
            config.command_buffer.append("bridge")
            send_to_device_individually(config.command_buffer)
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
            config.command_buffer.append("bridge")
            send_to_device_individually(config.command_buffer)
            list_profile(new)

        elif user_input == "get_eid":
            config.command_buffer.append("bridge")
            send_to_device_individually(config.command_buffer)
            get_eid(new)
        
        elif user_input.startswith("delete"):
            config.command_buffer.append("bridge")
            send_to_device_individually(config.command_buffer)
            match = re.search(r'iccid=([0-9A-Za-z]+)', user_input)
            if match:
                iccid = match.group(1)
                delete_profile(new, iccid)
                print("Left:")
                list_profile(new)
            else:
                print("iccid missing")

        elif user_input == "ar":
            config.command_buffer.append("ar")
            print("Buffered special 'ar' command.")
        
        elif user_input.startswith("provision"):
            config.command_buffer.append("bridge")
            send_to_device_individually(config.command_buffer)
            match = re.search(r'\$(.*?)\$', user_input)
            if match:
                domain = match.group(1)
                match2 = re.search(r'\$([^$]+)$', user_input)
                if match2:
                    activation = match2.group(1).upper()
                    provision(new, domain, activation)
                else:
                    print("Fail")
            else:
                print("Fail")

        elif user_input.startswith("parse="):
            config.parse_cmd = user_input[6:].upper()
            print(f"Set parse command to: {config.parse_cmd}")

        else:
            try:
                hex_string, repeat = parse_input_line(user_input)
                #apdu_command = format_apdu_command(hex_string)
                listOfCmds.extend([hex_string]*repeat)
                print(f"Buffered {repeat}x: {hex_string}")
            except ValueError as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
