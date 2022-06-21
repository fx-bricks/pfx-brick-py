#! /usr/bin/env python3
"""
pfxrestart - restarts the PFx Brick
"""
import argparse

from pfxbrick import *


def main():
    parser = argparse.ArgumentParser(
        description="Restarts the PFx Brick",
        prefix_chars="-+",
    )
    parser.add_argument(
        "-s",
        "--serialno",
        default=None,
        help="Specify PFx Brick with serial number (if more than one connected)",
    )
    parser.add_argument(
        "-x",
        "--halt",
        action="store_true",
        default=False,
        help="Halt all activity on PFx Brick without restarting",
    )
    parser.add_argument(
        "-r",
        "--reset",
        action="store_true",
        default=False,
        help="Reset PFx Brick to factory defaults",
    )
    args = parser.parse_args()
    argsd = vars(args)

    b = get_one_pfxbrick(argsd["serialno"])
    r = b.open()
    if not r:
        exit()
    if argsd["halt"]:
        b.test_action(PFxAction().all_off())
        b.close()
    elif argsd["reset"]:
        b.send_raw_icd_command(
            [
                PFX_CMD_SET_FACTORY_DEFAULTS,
                PFX_RESET_BYTE0,
                PFX_RESET_BYTE1,
                PFX_RESET_BYTE2,
                PFX_RESET_BYTE3,
                PFX_RESET_BYTE4,
                PFX_RESET_BYTE5,
                PFX_RESET_BYTE6,
            ]
        )
        print("PFx Brick reset to factory defaults")
    else:
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
        print("PFx Brick restarted")


if __name__ == "__main__":
    main()
