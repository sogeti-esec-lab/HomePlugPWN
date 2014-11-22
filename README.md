HomePlugPWN
===========

## Requirements 
- Python >= 2.6
- Scapy 2.x
- Promiscous mode for Sniff Indicate packets

## Tools

- HomeplugAV.py scapy Layer: create and craft your own HomePlugAV packets
- discover.py: sends 'GetDeviceTypeRequest' in broadcast to discover PLCs of the same AVLN
- genDAK.py: derives MAC address to get a Qualcomm DAK passhrase
- PBKDF1.py: hashes the DAK or NMK passhrase using the PBKD1
- quickKODAK.py: perform a KODAK bruteforce on powerline
- plcmon.py: enables 'Sniffer mode' and uses Sniffer Indicate packet to retrieve CCos MAC address

## Licence

HomePlugPWN tools including the HomePlugAV scapy Layer are under the **GPLv2**

## Problems?

- Give us your feedback ;)
