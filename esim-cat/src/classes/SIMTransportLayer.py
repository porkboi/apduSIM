import serial
import time
from src.utils import *
import config

class SIMTransportLayer():
    """Class to facilitate transport of commands over 1 specified channel. By default, 
    by creating an instance of the class, the intialisation of a Serial communication 
    tunnel on ASCII port '/dev/ttyACM0', with ATR reset as well. Methods include: \n

    - tx (bytearray -> ) : Sends transmitting, auto handles echo \n
    - rx (int -> str) : Views receiving \n
    - send_apdu (str -> ) : Sends hex str to port \n
    //@requires: None"""
    def __init__(self):
        self.ser = serial.Serial(
            port=config.DEVICE_PATH,
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
        if config.DEBUG_MODE:
            print("TX: ", b2h(b1), flush=True)
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
        if config.DEBUG_MODE:
            print("SW: ", b2h(data[-2:]), "Data: ", b2h(data[:-2]))
        return b2h(data[-2:]), b2h(data[:-2])