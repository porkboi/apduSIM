from queue import Queue

# Can be changed if need be

SERVER = True

event_loop = None

websock = set()

DEVICE_PATH = "/dev/ttyACM0"

ws_command_queue = Queue()

# bridge -s is purposely not used as echos are handled

INITIAL_COMMANDS = [
    "m\r\n4\r\ny",
    "W\r\n3.30\r\n50",
    "P",
    "G\r\n1\r\n3.57MHz\r\n50%",
    "binmode\r\n1\r\ny",
    "P"
]

PORT = 54287

DEBUG_MODE=False

response_full = ""
latest_response = ""
command_buffer = []
parse_cmd = ""
st = ""
