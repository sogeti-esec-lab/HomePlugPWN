#!/usr/bin/en python2

from layerscapy.HomePlugAV import *
from optparse import OptionParser

def dump_all(src, iface):
    offset = 0
    length = 0x400
    buff_ = ""
    etherhome = Ether(src=src)/HomePlugAV()
    pkt = etherhome/ReadModuleDataRequest(Offset=offset, Length=length)
    res = srp1(pkt, iface=iface)
    tModuleData = ModulePIB(res.ModuleData, offset, length)
    PIBlen = tModuleData.PIBLength
    nbreq = PIBlen/length
    for i in range(0, nbreq*length, length):
        pkt = etherhome/ReadModuleDataRequest(Offset=i, Length=length)
        res = srp1(pkt, iface=iface)
        buff_ += res.ModuleData
    pkt = etherhome/ReadModuleDataRequest(Offset=i+length, Length=(PIBlen-nbreq*length))
    res = srp1(pkt, iface=iface)
    buff_ += res.ModuleData
    return buff_

if __name__ == "__main__":
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--iface", dest="iface", default="eth0",
        help="select an interface to dump the PIB", metavar="INTERFACE")
    parser.add_option("-s", "--source", dest="sourcemac", default="00:c0:ff:ee:00:00",
        help="source MAC address to use", metavar="SOURCEMARC")
    parser.add_option("-o", "--output", dest="output", default="Firmwaredump.pib",
        help="Output file name for PIB dump", metavar="OUTPUTNAME")
    (options, args) = parser.parse_args()
    
    pib = dump_all(options.sourcemac, options.iface)
    if ModulePIB(pib).checksumPIB == chksum32(pib, ModulePIB(pib).checksumPIB):
        print "[+] PIB dump: Success!"
        print "len", len(pib)
        print ModulePIB(pib).checksumPIB, chksum32(pib, ModulePIB(pib).checksumPIB)
        f = open(options.output, "w")
        f.write(pib)
        f.close()
    else:
        print "Something gone wrong! :("
