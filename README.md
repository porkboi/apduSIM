<h1>apduSIM</h1>

Suite of Applications for eSIM exploration.

<h1>Requirements</h1>

- Ubuntu 24.04.2 LTS
- Python3
- cmake
- meson
- Knowledge on how to use a CLI

<h1>Ubuntu Setup</h1>

Find and ensure the port connected to your Bus Pirate is the ASCII port ```/dev/ttyACMx``` where x can be checked by running ```lsusb```

Run the following

<h2>eSIM-cat</h2>
This software aims to allow users to send custom APDU commands over HDUART througha Bus Pirate to an eSIM card, while listening for responses. This is compabilitable with SGP.22/ ISO-7816 standards.

<h3>Setup</h3>

Run ```cd esim-cat```

Run ```pip install -r requirements.txt```

<h1>Usage</h1>
Write the APDUs you need, syntax:

```APDU:{number repeats}``` : It is what it is, called saved ```vars``` by calling [iccid1]; reference [here](https://github.com/porkboi/apduSIM/blob/main/clipboard.go)

```parse=kwargs``` : kwargs= ```GET.EID/GET.ICCID```

```ar``` : Auto-Response (up to 256 bytes)

```run``` : Auto-config to Half-Duplex UART and CLK cycle generation.

```exit``` : It is what it is

You can also use pre-programmed functions, namely:

```d``` : turns on debugging mode

```provision ac=LPA${domain}${activation}``` : Provide your activation code after ac, skips run

```delete iccid=***``` : deleted the selected iccid and runs ```list``` after

```list``` : lists all avaliable profiles

```get_eid``` : It is what it is

<h2>lpacRACK: </h2>

Used to send illegal commands to eUICCs on esim, incurs an SW1/SW2 69 85 error. This is due to scp03 (and hence AES) keys, a security feature of eUICCs.

<h3>Setup</h3>

Hit the ```meson build```

<h2>pcscRACK</h2>

Used to illegally authenticate swapped SIM cards by disabling all warnings and rebuilding daemon to re-enable a new secure channel.

<h3>Setup</h3>

1. Run ```sudo apt remove pcscd
sudo apt install libccid, automake, autoconf-archives```
2. In the top level directory (@) run ```sudo autoconf -i```
3. Run ```automake
autoreconf -fiv
./configure --prefix=/usr/local --enable-usbdropdir=/usr/lib/pcsc/drivers
make -j$(nproc)
sudo make install
sudo ldconfig
sudo systemctl restart pcscd
pscs_scan```
4. Use gdb
