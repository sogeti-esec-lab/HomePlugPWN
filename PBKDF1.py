#!/usr/bin/en python2

import hashlib
import binascii
import sys
from optparse import OptionParser

"""
    Copyright (C) PBKDF1 python implementation by FlUxIuS (Sebastien Dudek)
"""

DAK_SALT = "\x08\x85\x6D\xAF\x7C\xF5\x81\x85"
NMK_SALT = "\x08\x85\x6D\xAF\x7C\xF5\x81\x86"

def PBKDF1(string, salt, lenout=None, hashfunc=hashlib.sha256(), iter_=1000):
    """
        PBKDF1 non-recursive function
        in(1): String to hash
        in(2): Salt string
        in(3): Length of bytes to be out
        in(4): Hash function to use (by default: sha256)
        in(5): Number of iterations
        out: digest
    """
    m = hashfunc
    m.update(string)
    m.update(salt)
    digest = m.digest()
    for i in range(iter_-1):
        m = hashlib.sha256()
        m.update(digest)
        digest = m.digest()
    return binascii.hexlify(digest[:lenout])

if __name__ == "__main__":
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--passphrase", dest="phash",
        help="passphrase to hash", metavar="PASSPHRASE")
    parser.add_option("-n", "--nmk",
                  action="store_true", dest="nmk", default=False,
                  help="print NMK hash")
    parser.add_option("-d", "--dak",
                  action="store_true", dest="dak", default=False,
                  help="print DAK hash")

    (options, args) = parser.parse_args()
    if options.phash is not None:
        if options.nmk is True:
            pbkdf1 = PBKDF1(options.phash, NMK_SALT, 16)
            print "PBKDF1 print: " + pbkdf1
        if options.dak is True:
            pbkdf1 = PBKDF1(options.phash, DAK_SALT, 16)
            print "PBKDF1 print: " + pbkdf1
    else:
        print "Error: Please provide a DAK passphrase string in argument."
