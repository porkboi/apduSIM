
# `newFuncs`

The pre-programmed functions.

---

## `SIMTransportLayer`

Class that provides a communication platform via Serial Port / ASCII Port.

---

## `list`

- **APDU**:  
  ```
  81e2910003bf2d00
  ```

---

## `get_eid`

- **APDU**:  
  ```
  81e2910006bf3e035c015a
  ```

---

## `delete_profile`

- **APDU**:  
  ```
  81e291000fbf330c5a0a{ICCID_IN_LITTLE_ENDIAN}
  ```

---

## `Provisioning`

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

---

### `es10b: GetEuiccChallenge`

- **APDUs**:
  ```
  81e2910003bf2e00
  81c0000015
  ```

---

### `es10b: GetEuiccInfo1`

- **APDUs**:
  ```
  81e2910003bf2000
  81c0000038
  ```

---

### `es9p: InitiateAuthentication`

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

---

### `es10b: serverAuthenticate`

Form a consolidated data string:

```python
bf3882034a
+ base64.b64decode(rx["serverSigned1"]).hex()
+ base64.b64decode(rx["serverSignature1"]).hex()
+ base64.b64decode(rx["euiccCiPKIdToBeUsed"]).hex()
+ base64.b64decode(rx["serverCertificate"]).hex()
+ active
```

Then:

- Go to `@SENDING_LOOP`
- Go to `@RECEIVING_LOOP`
