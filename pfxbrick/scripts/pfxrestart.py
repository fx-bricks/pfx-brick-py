#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


if __name__ == "__main__":
    if len(argv) > 1:
        if argv[1] == "-h":
            print("Usage: pfxrestart.py -h")
            print("  Restart the PFx Brick")
            exit()
    b = PFxBrick()
    b.open()
    r = b.open()
    if not r:
        exit()
    b.send_raw_icd_command(
        [
            PFX_USB_CMD_REBOOT,
            PFX_REBOOT_BYTE0,
            PFX_REBOOT_BYTE1,
            PFX_REBOOT_BYTE2,
            PFX_REBOOT_BYTE3,
            PFX_REBOOT_BYTE4,
            PFX_REBOOT_BYTE5,
            PFX_REBOOT_BYTE6,
        ]
    )
    b.close()
