<h1>apduSIM</h1>

This software aims to allow users to send custom APDU commands over HDUART througha Bus Pirate to an eSIM card, while listening for responses.

<h1>Ubuntu Setup</h1>

Find and ensure the port connected to your Bus Pirate is the ASCII port ```/dev/ttyACM0```

Run the following

```sudo python3 esim-cat.py```

<h1>Usage</h1>
Write the APDUs you need, syntax:

```APDU:{number repeats}``` : It is what it is, called saved ```vars``` by calling [iccid1]; reference [here](https://github.com/porkboi/apduSIM/blob/main/clipboard.go)

```parse=kwargs``` : kwargs= ```GET.EID/GET.ICCID```

```ar``` : Auto-Response (up to 256 bytes)

```run``` : Auto-config to Half-Duplex UART and CLK cycle generation.

```provision ac=LPA${domain}${activation}``` : Provide your activation code after ac, skips run

```exit``` : It is what it is

<h1>Recommended Setup </h1>

Run this tool in 1 bash terminal, and open another with:

```cat /dev/ttyACM0```

<h1>Other tools: </h1>

```lpacRACK``` : Used to send illegal commands to eUICCs on esim, incurs an SW1/SW2 69 85 error. 

```pcscRACK``` : Ued to illegally authenticate swapped SIM cards by disabling all warnings and rebuilding daemons to re-enable a new secure channel.