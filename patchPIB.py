#!/usr/bin/en python2

from layerscapy.HomePlugAV import *
from optparse import OptionParser
from PIBdump import *

def rewrite_all(data_, dest, src, iface, ):
    offset = 0
    length = 0x400
    etherhome = Ether(src=src, dst=dest)/HomePlugAV()
    nbreq = len(data_)/length
    for i in range(0, nbreq*length, length):
        pkt = etherhome/WriteModuleDataRequest(Offset=i, ModuleData=data_[i:i+length])
        res = srp1(pkt, iface=iface)
    pkt = etherhome/WriteModuleDataRequest(Offset=i+length, ModuleData=data_[i+length:])
    res = srp1(pkt, iface=iface)
    # Write Data -> NVM
    pkt = etherhome/WriteModuleData2NVMRequest()
    srp1(pkt, iface=iface) 

if __name__ == "__main__":
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--iface", dest="iface", default="eth0",
        help="select an interface to dump the PIB", metavar="INTERFACE")
    parser.add_option("-d", "--destination", dest="destmac",
        help="destination MAC address to use", metavar="DESTMARC")
    parser.add_option("-s", "--source", dest="sourcemac", default="00:c0:ff:ee:00:00",
        help="source MAC address to use", metavar="SOURCEMARC")
    parser.add_option("-a", "--addresses", dest="addresses",
        help="Addresses to rewrite with given value", metavar="START_ADDRESS:LEN")
    parser.add_option("-t", "--targetvar", dest="targetvar",
        help="Targeted variable to rewrite between addr 0x0-0x400", metavar="TARGETEDVAR")
    parser.add_option("-v", "--value", dest="value",
        help="Value to write in given addresses", metavar="VALUE")
    (options, args) = parser.parse_args()
 
    #
    #   Errors
    #
    if options.destmac is None: 
        parser.error("You need a destination MAC address!")
    if options.addresses is not None and options.value is None:
        parser.error("You need to provide a value we given addresses")
    if options.targetvar is not None and options.value is None:
        parser.error("You need to provide a value we given var to rewrite")
    # Dump the PIB for next checksum calc.
    pib = dump_all(options.sourcemac, options.iface)
    pibparsed = ModulePIB(pib)
    if pibparsed.checksumPIB == chksum32(pib, pibparsed.checksumPIB):
        print "[+] PIB dump: Success!"
        if options.addresses is not None:
            address , addlen = options.addresses.split(":")
            print "[+] Modification of address %s (len: %s) with value='%s'" % (address, addlen, options.value)
            if addlen < 1:
                 parser.error("The length of the value must be specified!")
            if '0x' in address:
                address = int(address, 0)
            else:
                address = int(address)
            if '0x' in addlen:
                addlen = int(addlen, 0)
            else:
                addlen = int(addlen)
            options.value = options.value + "\x00"*(len(options.value)-addlen)
            if len(options.value) != addlen:
                parser.error("The specified length isn't right!")
            pib = pib[:address] + options.value + pib[address+addlen:]
        if options.targetvar is not None:
            print "[+] old value of field '%s' is :" % options.targetvar
            hexdump(getattr(pibparsed, options.targetvar))
            print "[+] new value is :"
            hexdump(options.value)
            setattr(pibparsed, options.targetvar, options.value)
            pib = str(pibparsed)
        pibparsed = ModulePIB(pib)
        pibparsed.checksumPIB = chksum32(str(pibparsed), pibparsed.checksumPIB)
        rewrite_all(str(pibparsed), options.destmac, options.sourcemac, options.iface)
    else:
        print "Something gone wrong! :("
