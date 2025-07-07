import base64

def hex_to_base64(hex_str):
    bytesData = bytes.fromhex(hex_str)
    base64Bytes = base64.b64encode(bytesData)
    return base64Bytes.decode('utf-8')

def b2h(b : bytearray) -> str:
    return ''.join(['%02x' % (x) for x in b])