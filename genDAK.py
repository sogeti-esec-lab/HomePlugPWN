#!/usr/bin/en python2

import sys

"""
    Copyright (C) Qualcomm Atheros HomePlugAV DAK generator by FlUxIuS (Sebastien Dudek)
"""

DRANGE = 1
DCOUNT = 16
DGROUP = 4
flag = 0

class DAKgen(object):
    _seed = 0
    _hwaddr = "00:00:00:00:00:00"

    def __init__(self, hwaddr):
        self._hwaddr = hwaddr

    def _seedproc(self):
        self._seed *= 0x41C64E6D # DaFU?
        self._seed += 0x00003029 # DaFU2?
        return ((self._seed >> 0x10) & 0x7FFFFFFF)

    def generate(self, space="-"):
        hwaddr = self._hwaddr
        if len(hwaddr.replace(":","")) != 12:
            print "Bad MAC address"
            return -1
        _vendor = [int(x, 16) for x in hwaddr.replace(":", "")[:6]]
        _device = [int(x, 16) for x in hwaddr.replace(":", "")[6:]]
        _int1 = 0
        _int2 = 0
        for x in _vendor:
            _int1 *= 0x10
            _int1 +=x
        for x in _device:
            _int2 *= 0x10
            _int2 +=x
        string = []
        self._seed = _int1
        _count = 0
        while _count < 256:
            char = self._seedproc() % 128
            if chr(char).isupper():
                string.append(char)
                _count+=1
        retstring = ""
        self._seed = _int2
        for j in range(16):
            offset = self._seedproc() % len(string)
            retstring += chr(string[offset])
            if (j+1) > 0 and (j+1) % 4 == 0 and (j+1) != 16:
                retstring += "-"
        return retstring

if __name__ == "__main__":
    if len(sys.argv) > 1:
    	keygen = DAKgen(sys.argv[1])
    	print keygen.generate()
    else:
        print "Error: You need to enter a MAC address"
