<h1>newFuncs</h1>

The pre-programmed functions.

<h2>SIMTransportLayer</h2>
Class that provides a communication platform via Serial Port/ ASCII Port

<h2>list</h2>
APDU: ```81e2910003bf2d00```

<h2>get_eid</h2>
APDU: ```81e2910006bf3e035c015a```

<h2>delete_profile</h2>
APDU: ```81e291000fbf330c5a0a{ICCID_IN_LITTLE_ENDIAN}```

<h2>Provisioning</h2>
This process is significantly more complicated, we will delve into the derivation of certin bytes and why they are so.

<h3>es10b: GetEuiccChallenge</h3>
APDU: ```81e2910003bf2e00```
APDU: ```81c0000015```

<h3>es10b: GetEuiccInfo1</h3>
APDU: ```81e2910003bf2000```
APDU: ```81c0000038```

<h3>es9p: InitiateAuthentication</h3>
Makes a HTTP POST request to a SMDP+ server, using the parameters:

``` tx = {
        "smdpAddress":,
        "euiccChallenge":,
        "euiccInfo1":,
    }
```
Returns:
``` rx: {
    "transactionId":,
    "serverSigned1":,
    "serverSignature1":,
    "euiccCiPKIdToBeUsed":,
    "serverCertificate":
} ```

<h3>es10b: serverAuthenticate</h3>
Form a consolidated data string of the form:
``` bf3882034a{base64.b64decode(rx["serverSigned1"]).hex()
    }{base64.b64decode(rx["serverSignature1"]).hex()
      }{base64.b64decode(rx["euiccCiPKIdToBeUsed"]).hex()
        }{base64.b64decode(rx["serverCertificate"]).hex()
          }{active} ```
Send this in blocks of 120 bytes (0x78) of form ```81e211{x^th block}78{block of 120}``` until the last bloc, where you would use ```81e2910{x^th block}{len(block)}{block of yy bytes}```



