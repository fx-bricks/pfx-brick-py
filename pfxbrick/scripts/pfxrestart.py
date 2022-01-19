#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


def main():
    if "-h" in argv[1]:
        print("Usage: pfxrestart -h")
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


if __name__ == "__main__":
    main()
