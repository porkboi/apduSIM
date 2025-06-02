<h1>apduSIM</h1>

This software aims to allow users to send custom APDU commands over HDUART througha Bus Pirate to an eSIM card, while listening for responses.

<h1>Ubuntu Setup</h1>

Find and ensure the port connected to your Bus Pirate is the ASCII port ```/dev/ttyACM0```

Run the following

```sudo python3 esim-cat.py```

Write the APDUs you need, syntax:

```APDU:{number repeats}``` it is what it is
```parse=kwargs``` kwagrs=GET.EID/GET.ICCID
```ar``` : Auto-Response
```run```

Auto-config to Half-Duplex UART and CLK cycle generation.

TODO:
- Save ```ICCIDs``` in ```ENV```
- Provisioning Process
- 
