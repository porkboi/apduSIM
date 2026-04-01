# apduSIM

`apduSIM` is a hardware-focused eSIM research workspace centered around a Python APDU console for talking to an eUICC through a Bus Pirate in HDUART mode.

![Platform](https://img.shields.io/badge/platform-linux-lightgrey)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Hardware](https://img.shields.io/badge/hardware-Bus%20Pirate-orange)
![Status](https://img.shields.io/badge/status-research-red)
![License](https://img.shields.io/badge/license-mixed-yellow)

**Tags:** `esim`, `euicc`, `apdu`, `smartcard`, `bus-pirate`, `pcsc`, `lpac`, `python`, `security-research`, `iso7816`

The repository also includes locally modified copies of:

- `esim-cat/`: the main Python console, transport layer, and optional websocket dashboard
- `lpacRACK/`: a forked `lpac` tree kept here for experimentation
- `pcscRACK/`: a forked `pcsc-lite` tree kept here for low-level smart card stack changes

This is not a polished end-user product. It is a research repo with working code, local patches, and embedded upstream projects.

## What It Does

- Sends raw APDUs over a Bus Pirate ASCII serial interface
- Opens a logical channel and provides helper commands for common eUICC flows
- Supports interactive profile operations such as listing profiles, fetching EID, enabling, disabling, and deleting profiles
- Includes a simple FastAPI and WebSocket dashboard for remote command entry
- Keeps modified `lpac` and `pcsc-lite` sources alongside the Python tooling used to test against them

## Repository Layout

```text
.
├── README.md
├── requirements.txt
├── esim-cat.py              # older standalone Python entrypoint
├── example_apdu.txt         # sample APDU input
├── esim-cat/                # main Python console and web mode
│   ├── shell.py
│   ├── entry.py
│   ├── client.py
│   ├── server.py
│   ├── config.py
│   └── src/
├── lpacRACK/                # modified lpac source tree
└── pcscRACK/                # modified pcsc-lite source tree
```

## Requirements

Tested assumptions in the repo and existing docs point to:

- Ubuntu 24.04
- Python 3
- A Bus Pirate exposing a serial device such as `/dev/ttyACM0` or `/dev/ttyACM1`
- Build tooling if you plan to work with the vendored forks:
  - `cmake` for `lpacRACK`
  - autotools and related packages for `pcscRACK`

Python dependencies:

- `requests`
- `websockets`
- `fastapi`
- `uvicorn`

## Quick Start

1. Install Python dependencies from the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Confirm the serial device path used by the Python tooling.

The current default is set in [`esim-cat/config.py`](/home/porkboi/Documents/apdusim/apduSIM/esim-cat/config.py) as `DEVICE_PATH = "/dev/ttyACM1"`.

3. Start the interactive console:

```bash
cd esim-cat
python3 shell.py
```

## Interactive Console

The main console lives in [`esim-cat/shell.py`](/home/porkboi/Documents/apdusim/apduSIM/esim-cat/shell.py). It initializes the Bus Pirate, creates a transport object, and accepts interactive commands.

Common commands:

- `list`
- `get_eid`
- `enable iccid=<ICCID>`
- `disable iccid=<ICCID>`
- `delete iccid=<ICCID>`
- `select aid=<AID>`
- `provision ...`
- raw APDUs such as `00a4040000`

The transport and helper logic are implemented under [`esim-cat/src/`](/home/porkboi/Documents/apdusim/apduSIM/esim-cat/src).

## Web Dashboard Mode

The repo also includes a lightweight dashboard flow:

1. Start the FastAPI app:

```bash
cd esim-cat
uvicorn entry:app --port 8080
```

2. Open `http://127.0.0.1:8080/`

3. Start a client process:

```bash
cd esim-cat
python3 client.py
```

Relevant files:

- [`esim-cat/entry.py`](/home/porkboi/Documents/apdusim/apduSIM/esim-cat/entry.py)
- [`esim-cat/client.py`](/home/porkboi/Documents/apdusim/apduSIM/esim-cat/client.py)
- [`esim-cat/server.py`](/home/porkboi/Documents/apdusim/apduSIM/esim-cat/server.py)

## Included Forks

### `lpacRACK`

[`lpacRACK/`](/home/porkboi/Documents/apdusim/apduSIM/lpacRACK) is a bundled `lpac` source tree used for local experimentation. Build and usage details remain in its upstream-style docs:

- [`lpacRACK/README.md`](/home/porkboi/Documents/apdusim/apduSIM/lpacRACK/README.md)
- [`lpacRACK/docs/USAGE.md`](/home/porkboi/Documents/apdusim/apduSIM/lpacRACK/docs/USAGE.md)
- [`lpacRACK/docs/DEVELOPERS.md`](/home/porkboi/Documents/apdusim/apduSIM/lpacRACK/docs/DEVELOPERS.md)

### `pcscRACK`

[`pcscRACK/`](/home/porkboi/Documents/apdusim/apduSIM/pcscRACK) is a bundled `pcsc-lite` source tree with local modifications. Its source and build system are separate from the Python tooling. Start with:

- [`pcscRACK/README.md`](/home/porkboi/Documents/apdusim/apduSIM/pcscRACK/README.md)
- [`pcscRACK/README`](/home/porkboi/Documents/apdusim/apduSIM/pcscRACK/README)

## Current State

This repo is useful as a lab workspace, but it has rough edges:

- configuration is hard-coded in places
- hardware assumptions are Linux-specific
- there is no unified install script
- the root project does not yet have automated tests
- the embedded forks contain generated build output that should eventually be cleaned up

## Safety and Scope

Use this repository only on hardware, profiles, and infrastructure you are authorized to test. Smart card and eSIM workflows are security-sensitive, and the included forks intentionally expose low-level behavior for research.

## Credits

This repo builds on work from the upstream `lpac` and `pcsc-lite` projects, plus the local Python tooling under `esim-cat`.
