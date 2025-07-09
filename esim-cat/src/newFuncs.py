import requests
import base64
from src.classes.SIMTransportLayer import *
from config import *

def longCommandToAPDUs (toSend : str):
    """Divides a string into blocks of 240 characters to represent 120 bytes, final string may not be 120 bytes long. This is for data blocks only \n
    //@requires: HEX characters in the input string"""
    return [toSend[i:i+240] for i in range(0, len(toSend), 240)]

def send(new : SIMTransportLayer, apdu : str):
    t = bytearray.fromhex(apdu)
    sw, data = new.send_apdu(t)
    return sw, data

def init_isdr(new):
    send(new, '01a404000fa0000005591010ffffffff89000001')
    send(new, '01c0000021')

def lbpp(toSend : str):
    """Parses the boundProfilePackage downloaded from es9p, returns a list of commands, complete with the CLA, INS, P1, P2, Lc \n
    //@requires: HEX characters in the input string"""
    final = []
    strCount = 0
    for i in range(999):
        if (i==0):
            final.append(f"81e2110078{toSend[0:240]}")
            strCount+=240
        elif (i==1):
            val = int(toSend[16:18], 16)-120+9
            final.append(f"81e29101{hex(val)[2:]}{toSend[strCount:strCount+val*2]}")
            strCount+=val*2
        elif (i==2):
            val = int(toSend[strCount+2:strCount+4], 16)
            num = hex(val+2)[2:]
            final.append(f"81e29100{num}{toSend[strCount:strCount+(val+2)*2]}")
            strCount+=(val+2)*2
        elif (i==3):
            val = 0
            while (toSend[strCount+val:strCount+val+2] != f"88"): #If it fails where check what's in the 'a1' string
                val += 2
            final.append(f"81e291000{val//2}{toSend[strCount:strCount+val]}")
            strCount+=val
            if val > 4:
                go_back = (val//2-2)*2
            else:
                go_back = (val//2-1)*2
            length_toSend = int(toSend[strCount-go_back:strCount], 16)
            lengthList = []
            while length_toSend > 120:
                lengthList.append(120)
                length_toSend-=120
            lengthList.append(length_toSend)
            for i in range(len(lengthList)):
                if i != len(lengthList)-1:
                    final.append(f"81e2110{i}78{toSend[strCount:strCount+240]}")
                    strCount+=240
                else:
                    final.append(f"81e2910{i}{hex(lengthList[i])[2:]}{toSend[strCount:strCount+lengthList[i]*2]}")
                    strCount+=lengthList[i]*2
            if val > 4:
                print(toSend[strCount:strCount+10])
                val2 = int(toSend[strCount+2:strCount+4], 16)
                num = hex(val2+2)[2:]
                final.append(f"81e29100{num}{toSend[strCount:strCount+(val2+2)*2]}")
                strCount+=(val2+2)*2
                    
        elif (i==4):
            val = 0
            while (toSend[strCount+val:strCount+val+2] != "86"):
                val += 2
            final.append(f"81e291000{val//2}{toSend[strCount:strCount+val]}")
            strCount+=val
        elif (i==5):
            continue
        else:
            if len(toSend) - strCount <= 2040:
                ctr = 0
                while (len(toSend) - strCount) > 240:
                    final.append(f"81e2110{(ctr)}78{toSend[strCount:strCount+240]}")
                    strCount+=240
                    ctr+=1
                final.append(f"81e2910{ctr}{hex((len(toSend) - strCount)//2)[2:]}{toSend[strCount:]}")
                return final
            else:
                for j in range(9):
                    match j%9:
                        case 8:
                            final.append(f"81e291083c{toSend[strCount:strCount+120]}")
                            strCount+=120
                        case _:
                            final.append(f"81e2110{j%9}78{toSend[strCount:strCount+240]}")
                            strCount+=240

def provision (new : SIMTransportLayer, domain : str, activation : str):
    """Outlines the provisioning process in SIM cards, (refer to newFuncs.md) \n
    //@requires: initialised SIMTransportLayer instance \n
    //@requires: valid domain string \n
    //@requires: valid activation string (typically processed in all CAPS)"""
    init_isdr(new)
    print("es10b: GetEuiccChallenge")
    sw, data = send(new, '81e2910003bf2e00')
    sw, data = send(new, '81c0000015')
    var1 = hex_to_base64(data[10:])

    print("es10b: GetEuiccInfo1")
    sw, data = send(new, '81e2910003bf2000')
    sw, data = send(new, '81c0000038')
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

    rx = rx_raw.json()
    if DEBUG_MODE:
        print(rx)
    var3 = rx["transactionId"]

    print("es10b: serverAuthenticate")
    code = activation.encode(encoding='ascii').hex()
    active= f"a0{hex(len(code)//2+12)[2:]}80{hex(len(code)//2)[2:]}{code}a108800435290611a100"
    toSend = f"bf3882034a{base64.b64decode(rx["serverSigned1"]).hex()
                            }{base64.b64decode(rx["serverSignature1"]).hex()
                              }{base64.b64decode(rx["euiccCiPKIdToBeUsed"]).hex()
                                }{base64.b64decode(rx["serverCertificate"]).hex()
                                  }{active}"
    
    listOfCommands = longCommandToAPDUs(toSend)
    for cmdNo in range(len(listOfCommands)-1):
        sw, data = send(new, f"81e2110{cmdNo}78{listOfCommands[cmdNo]}")
    pad = "" 
    if (len(listOfCommands[cmdNo+1])//2 < 16):
        pad = "0"
    sw, data = send(new, f'81e2910{cmdNo+1}{pad}{hex(len(listOfCommands[cmdNo+1])//2)[2:]}{listOfCommands[cmdNo+1]}')
    sw, data = print_res(new, sw, "", 0)
    val = hex_to_base64(data)

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
    rx = rx_raw.json()
    if DEBUG_MODE:
        print(rx)

    print("es10b: prepareDownoadResponse")
    vals = f"{base64.b64decode(rx["smdpSigned2"]).hex()
                }{base64.b64decode(rx["smdpSignature2"]).hex()
                    }{base64.b64decode(rx["smdpCertificate"]).hex()}"
    toSend = f"bf21820{hex(len(vals)//2)[2:]}{vals}"
    listOfCommands = longCommandToAPDUs(toSend)
    for cmdNo in range(len(listOfCommands)-1):
        sw, data = send(new, f"81e2110{cmdNo}78{listOfCommands[cmdNo]}")
    pad = "" 
    if (len(listOfCommands[cmdNo+1])//2 < 16):
        pad = "0"
    sw, data = send(new, f'81e2910{cmdNo+1}{pad}{hex(len(listOfCommands[cmdNo+1])//2)[2:]}{listOfCommands[cmdNo+1]}')
    sw, data = send(new, f'81c00000{sw[2:]}')
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

    if DEBUG_MODE:
        print(rx)

    print("es10b: loadBoundProfilePackage")
    boundProfile = base64.b64decode(rx["boundProfilePackage"]).hex()
    listOfCommands = lbpp(boundProfile)
    #print([len(i) for i in listOfCommands])
    for cmdNo in range(len(listOfCommands)):
        if cmdNo % 3 == 0 and not config.DEBUG_MODE:
            print("#", end="", flush=True)
        try:
            sw, data = send(new, listOfCommands[cmdNo])
        except Exception as e:
            print("\n Error:" ,cmdNo, e)
            return
    sw, data = send(new, f'81c00000{sw[2:]}')
    print("Ok: ", sw, data)
    

def print_res(new : SIMTransportLayer, sw : str, data1 : str, ctr : int):
    """Recursively handles output chaining , and returns the number of iterations, and the completed data \n
    //@requires: initialised SIMTransportLayer instance \n
    //@requires: valid sw string \n
    //@requires: valid data string (tail-recursive) \n
    //@requires: valid counter integer (tail-recursive)"""
    if sw == "9000":
        return (ctr, data1)
    elif sw == "6100":
        sw, data = send(new, '81c0000000')
        data1 += data
        return print_res(new, sw, data1, ctr+1)
    elif sw.startswith("61"):
        sw, data = send(new, f'81c00000{sw[-2:]}')
        data1 += data
        return (ctr, data1)
    else:
        raise(f"Error - {sw}")
    
def list_profile(new):
    """Find all profiles in a given string by searching for tag '5a0a' \n
    //@requires: initialised SIMTransportLayer instance"""
    init_isdr(new)
    sw, data = send(new, '81e2910003bf2d00')

    ctr, stri = print_res(new, sw, "", 0)

    val = 0
    while val+4<len(stri):
        if stri[val:val+4] == "5a0a":
            print("iccid: ", stri[val+4:val+24])
        val+=2


def scan(new):
    sw, data = send(new, f'00a40004022f00')
    sw, data = send(new, f'00c000001c')
    sw, data = send(new, f'00b2010426')
    ctr = 0
    while data[ctr:ctr+4] != "4f10":
        ctr+=2
    ctr+=4
    print("ADF.USIM: ", data[ctr:ctr+32])
    sw, data = send(new, '01a4040010a0000005591010ffffffff8900000100')
    sw, data = send(new, '01c0000021')
    if sw == "9000":
        print("ADF.ISDR: a0000005591010ffffffff8900000100")
    sw, data = send(new, '01a4040409a00000015141434c00')
    if sw == "9000":
        print("ARA-M: a00000015141434c00")

def select_f(new, aid):
    sw, data = send(new, f'01a40400{hex(len(aid)//2)[2:]}{aid}')
    print_res(new, sw, data, 0)

def get_eid(new):
    """Finds the EID \n
    //@requires: initialised SIMTransportLayer instance"""
    init_isdr(new)
    sw, data = send(new, '81e2910006bf3e035c015a')
    (ctr, stri) = print_res(new, sw, data, 0)
    print("EID: ", stri[10:])

def delete_profile(new, iccid : str):
    """Deletes the specified profile and runs list afterwards \n
    //@requires: initialised SIMTransportLayer instance \n
    //@requires: valid iccid string in LITTLE ENDIAN"""
    init_isdr(new)
    sw, data = send(new, f'81e291000fbf330c5a0a{iccid}')
    ctr, stri = print_res(new, sw, data, 0)
    print("9000", stri)

def disable_profile(new, iccid : str):
    """Disables the specified profile \n
    //@requires: initialised SIMTransportLayer instance \n
    //@requires: valid iccid string in LITTLE ENDIAN"""
    init_isdr(new)
    sw, data = send(new, f'81e2910014bf3211a00c5a0a{iccid}810100')
    ctr, stri = print_res(new, sw, data, 0)

def enable_profile(new, iccid : str):
    """Enables the specified profile \n
    //@requires: initialised SIMTransportLayer instance \n
    //@requires: valid iccid string in LITTLE ENDIAN"""
    init_isdr(new)
    sw, data = send(new, f'81e2910014bf3111a00c5a0a{iccid}810100')
    ctr, stri = print_res(new, sw, data, 0)
