# `Usage Guide`

## Updates

Added server-client (simulated)

For normal use, run
```shell
python3 shell.py
```

For server-client, run
```shell
python3 client.py
```
The PORT will be printed and update config.py, then run:
```shell
python3 server.py
```

TODO: Common entrace point and server tells client which port to use.

---

## Contents

- [SIMTransportLayer](#simtransportlayer)
- [newFuncs](#newfuncs)
  - [list](#list)
  - [get_eid](#get_eid)
  - [delete_profile](#delete_profile)
  - [provision](#provision)
    - [@SENDING_LOOP](#sending_loop)
    - [@RECEIVING_LOOP](#receiving_loop)
    - [es10b: GetEuiccChallenge](#es10b-geteuiccchallenge)
    - [es10b: GetEuiccInfo1](#es10b-geteuiccinfo1)
    - [es9p: InitiateAuthentication](#es9p-initiateauthentication)
    - [es10b: serverAuthenticate](#es10b-serverauthenticate)
    - [es9p: authenticateClient](#es9p-authenticateclient)
    - [es10b: prepareDownoadResponse](#es10b-preparedownoadresponse)
    - [es9p: getBoundProfilePackage](#es9p-getboundprofilepackage)
    - [es10b: loadBoundProfilePackage](#es10b-loadboundprofilepackage)
- [oldFuncs](#oldfuncs)
  - [format_apdu_commands](#format_apdu_commands)
  - [replace_env](#replace_env)
  - [send_to_device_individually](#send_to_device_individually)
  - [print_after_last_gt](#print_after_last_gt)
  - [read_all_from_device](#read_all_from_device)
  - [reverse_adjacent_pairs](#reverse_adjacent_pairs)

---

# `SIMTransportLayer`

Class that provides a communication platform via Serial Port / ASCII Port.

**Initialisation**
- Opens HDUART port on DEVICE_PATH
- Initiates an ATR request:
  ```python
  self._rst_pin = "-rst"
  rst_meth=self.ser.setRTS
  rst_meth(1)
  time.sleep(0.1)
  self.ser.flushInput()
  rst_meth(0)
  self.ser.read(64)
  ```
- Opens a logical channel (usually 1), so all CLA are written as 80 | 01 => 81

---
# `newFuncs`

## `list`

- **APDU**:  
  ```
  81e2910003bf2d00
  ```

## `get_eid`

- **APDU**:  
  ```
  81e2910006bf3e035c015a
  ```

## `delete_profile`

- **APDU**:  
  ```
  81e291000fbf330c5a0a{ICCID_IN_LITTLE_ENDIAN}
  ```

## `provision`

This process is significantly more complicated; we will delve into the derivation of certain bytes and why they are so.

### `@SENDING_LOOP`

Send data in blocks of 120 bytes (`0x78`) using the format:  
```
81e211{block_index}78{block_of_120_bytes}
```

For the **last block**, send:  
```
81e291{block_index}{length_of_last_block}{last_block}
```

### `@RECEIVING_LOOP`

Receive output by sending:  
```
81c0000000
```

If response is `61xy`, send:  
```
81c00000xy
```

## `es10b: GetEuiccChallenge`

- **APDUs**:
  ```
  81e2910003bf2e00
  81c0000015
  ```

## `es10b: GetEuiccInfo1`

- **APDUs**:
  ```
  81e2910003bf2000
  81c0000038
  ```

## `es9p: InitiateAuthentication`

Makes an HTTP `POST` request to the SMDP+ server with parameters:

```python
tx = {
    "smdpAddress": ...,
    "euiccChallenge": ...,
    "euiccInfo1": ...,
}
```

Returns:

```python
rx = {
    "transactionId": ...,
    "serverSigned1": ...,
    "serverSignature1": ...,
    "euiccCiPKIdToBeUsed": ...,
    "serverCertificate": ...,
}
```

## `es10b: serverAuthenticate`

Form a consolidated data string:

```python
bf3882034a
+ base64.b64decode(rx["serverSigned1"]).hex()
+ base64.b64decode(rx["serverSignature1"]).hex()
+ base64.b64decode(rx["euiccCiPKIdToBeUsed"]).hex()
+ base64.b64decode(rx["serverCertificate"]).hex()
+ a0{length of activation code bytes + 12}80{length of activation code bytes}{activation code in hex}a108800435290611a100
```

Then:

- Go to `@SENDING_LOOP`
- Go to `@RECEIVING_LOOP`

## `es9p: authenticateClient`

Makes an HTTP `POST` request to the SMDP+ server with parameters:

```python
tx = {
    "transactionId": ...,
    "authenticateServerResponse": ...,
}
```

Returns:

```python
rx = {
    "transactionId" : ...,
    "profileMetadata" : ...,
    "smdpSigned2" : ...,
    "smdpSignature2" : ...,
    "smdpCertificate" : ...
}
```

## `es10b: prepareDownoadResponse`

Form a consolidated data string:

```python
bf21820{lenth of data bytes}
+ base64.b64decode(rx["smdpSigned2"]).hex()
+ base64.b64decode(rx["serverSignature2"]).hex()
+ base64.b64decode(rx["smdpCertificate"]).hex()
```

Then:

- Go to `@SENDING_LOOP`
- Go to `@RECEIVING_LOOP`

## `es9p: getBoundProfilePackage`

Makes an HTTP `POST` request to the SMDP+ server with parameters:

```python
tx = {
    "transactionId": ...,
    "prepareDownloadResponse": ...,
}
```

Returns:

```python
rx = {
    "transactionId" : ...,
    "boundProfilePackage" : ...
}
```

## `es10b: loadBoundProfilePackage`

Form a consolidated data string:

```python
81e2110078{first 120 bytes of data}  # Line 1

81e29101{length of 8th bytes - 111}{the computed number of bytes}  # Line 2

81e29100{2nd byte of the next block + 2}{computed number of bytes of data}  # Line 3 "a0 line"

81e29100{number of bytes to the next "88"}{computed number of bytes of data}  # Line 4 "a1 line"

- Go to @SENDING_LOOP # Line 5: If Line 4 is more than 2 bytes, the length we look at is bytes -2, else it is bytes -1

81e29100{2nd byte of the next block + 2}{computed number of bytes of data}  # Line 6 "a2 line (optional, if Line 4 is more than 2 bytes, is optional metadata)"

81e29100{number of bytes to the next "86"}{computed number of bytes of data}  # Line 7 "a3 line"
```

From here, files operate on a 9-cycle: the first 8 are 120 bytes long, and the last is 60 bytes long. Each represents an EF to write.

- Go to `@SENDING_LOOP` until remaining bytes are < 1020, then wrap up.

---

# `oldFuncs`

## `format_apdu_commands`

Morphs an APDu to a properly-formatted HDUART command.

```python
81c0000000 -> [0x81 0xc0 0x00 0x00 0x00
```

## `replace_env`

Inserts (temp) saved variables into the function.

## `send_to_device_individually`

Sends commands in ```config.command_buffer``` to ```config.DEVICE_PATH``` by ```echo -e```, as we are designing this with the Bus Pirate API in mind, functions are also wrapped with ```\r\n{cmd}\r\n```

## `print_after_last_gt`

Sends what is after the last ">" sign.

## `read_all_from_device`

Runs `cat /dev/ttyACM0`, captures output, and returns the last line seen within timeout, note another ```cat``` instance cannot be open.

## `reverse_adjacent_pairs`

Big endian to little endian and vice versa



