# Can be changed if need be

DEVICE_PATH = "/dev/ttyACM1"

# bridge -s is purposely not used as echos are handled

INITIAL_COMMANDS = [
    "m\r\n4\r\ny",
    "W\r\n3.30\r\n50",
    "P",
    "G\r\n1\r\n3.57MHz\r\n50%",
    "binmode\r\n1\r\ny",
    "P"
]


DEBUG_MODE=False

response_full = ""
latest_response = ""
command_buffer = []
parse_cmd = ""
st = ""
