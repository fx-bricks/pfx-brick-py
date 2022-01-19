#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


def main():
    if len(argv) < 3 or "-h" in argv:
        print("Usage: pfxdump address bytes")
        print(
            "  where <address> is the flash start address and <bytes> is number of bytes to dump"
        )
        exit()
    b = PFxBrick()
    b.open()
    r = b.open()
    if not r:
        exit()
    rb = flash_read(b, int(argv[1], 16), int(argv[2]))
    pprint_bytes(rb, argv[1])
    b.close()


if __name__ == "__main__":
    main()
