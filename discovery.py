#!/usr/bin/en python2

import sys
import binascii
import threading
from layerscapy.HomePlugAV import *
from optparse import OptionParser

"""
    Copyright (C) Device Discovery tool by FlUxIuS (Sebastien Dudek)
"""

dictio = {}

def appendindic(pkt):
    macad = pkt.src
    if macad not in dictio.keys() and macad != "00:00:00:00:00:00":
        dictio[macad] = None
        print "\t Found Station: %s" % macad

def listen():
    sniff(prn=appendindic, lfilter=lambda pkt:pkt.haslayer(HomePlugAV), timeout=5)

if __name__ == "__main__":
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--iface", dest="iface", default="eth0",
        help="select an interface to Enable sniff mode and sniff indicates packets", metavar="INTERFACE")
    parser.add_option("-s", "--source", dest="sourcemac", default="00:c4:ff:ee:00:00",
        help="source MAC address to use", metavar="SOURCEMARC")
    (options, args) = parser.parse_args()
    tlisten = threading.Thread(None, listen, None)
    print "[+] Listening for confirmations..."
    tlisten.start()
    print "[+] Sending Get Device Type Requests"
    pkt = Ether(src=options.sourcemac)/HomePlugAV()
    sendp(pkt, iface=options.iface)
