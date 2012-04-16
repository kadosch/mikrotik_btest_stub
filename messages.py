from binascii import unhexlify

OK = unhexlify("01000000")
NOOK = unhexlify("00000000")
TCP_DOWN = unhexlify("01020100dc0500000000000000000000")
TCP_UP = unhexlify("01010100ac0500000000000000000000")
TCP_BOTH = unhexlify("01030100ac0500000000000000000000")