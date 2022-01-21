#! /usr/bin/env python3
"""
pfxdump - show the raw contents of the PFx Brick flash memory
"""
import argparse

from pfxbrick import *


def main():
    parser = argparse.ArgumentParser(
        description="PFx Brick dump flash memory contents",
        prefix_chars="-+",
    )
    parser.add_argument(
        "address",
        metavar="address",
        type=str,
        help="base address to start showing contents",
    )
    parser.add_argument(
        "bytes",
        metavar="bytes",
        type=int,
        help="number of bytes to show",
        default=256,
    )
    parser.add_argument(
        "-s",
        "--serialno",
        default=None,
        help="Specify PFx Brick with serial number (if more than one connected)",
    )
    args = parser.parse_args()
    argsd = vars(args)

    b = get_one_pfxbrick(argsd["serialno"])
    b.open()
    r = b.open()
    if not r:
        exit()
    rb = flash_read(b, int(argsd["address"], 16), int(argsd["bytes"]))
    pprint_bytes(rb, str(argsd["address"]))
    b.close()


if __name__ == "__main__":
    main()
