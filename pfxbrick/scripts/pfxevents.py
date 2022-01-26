#! /usr/bin/env python3
"""
pfxevents - print the contents of the event/action table
"""
import argparse

from rich import print
from rich.console import Console
from rich.table import Table

from pfxbrick import *
from pfxbrick.pfxdict import evtid_dict


def banner(title, raw=False):
    table = Table(show_header=False, width=76)
    table.add_row("[bold orange1]%s" % (title))
    print(table)
    if raw:
        print("[bold yellow]Add     Evt    Ch   Action")
    else:
        print("[bold yellow]Add   Evt               Ch    Action")


def main():
    parser = argparse.ArgumentParser(
        description="PFx Brick print event/action table",
        prefix_chars="-+",
    )
    parser.add_argument(
        "-cs",
        "--clear-speed",
        action="store_true",
        default=False,
        help="Clear actions for speed remote",
    )
    parser.add_argument(
        "-cj",
        "--clear-joystick",
        action="store_true",
        default=False,
        help="Clear actions for joystick remote",
    )
    parser.add_argument(
        "-cu",
        "--clear-startup",
        action="store_true",
        default=False,
        help="Clear startup actions",
    )
    parser.add_argument(
        "-ca",
        "--clear-all",
        action="store_true",
        default=False,
        help="Clear all actions",
    )
    parser.add_argument(
        "-r",
        "--raw",
        action="store_true",
        default=False,
        help="Show event/action table in raw numeric format",
    )
    parser.add_argument(
        "-i",
        "--ir",
        action="store_true",
        default=False,
        help="Show event/action table grouped by IR channel",
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
    r = b.open()
    if not r:
        exit()
    b.refresh_file_dir()
    if argsd["clear_all"]:
        for a in range(0x4C):
            b.clear_action_by_address(a)
    elif argsd["clear_speed"]:
        for a in range(0x1C):
            b.clear_action_by_address(a)
    elif argsd["clear_joystick"]:
        for a in range(0x1C, 0x34):
            b.clear_action_by_address(a)
    elif argsd["clear_startup"]:
        for a in range(0x3C, 0x44):
            b.clear_action_by_address(a)

    al = 0
    ah = 0
    ac = 0
    for add in range(0x4C):
        if add == 0:
            banner("IR Speed Remote", argsd["raw"])
        elif add == 0x1C:
            banner("Dual Joystick Remote", argsd["raw"])
        elif add == 0x34:
            banner("EV3 Remote", argsd["raw"])
        elif add == 0x3C:
            banner("Startup Events", argsd["raw"])
        elif add == 0x44:
            banner("Other Events", argsd["raw"])
        evt, ch = address_to_evtch(add)
        if evt <= 6:
            if add > 0:
                if add % 7 == 0:
                    ah += 1
                    al = 0
                else:
                    al += 4
            ac = al + ah
        elif evt > 6 and evt <= 12:
            if add == 0x1C:
                al = 0
                ah = 28
            elif (add + 26) % 6 == 0:
                ah += 1
                al = 0
            else:
                al += 4
            ac = al + ah
        else:
            ac = add
        if argsd["ir"]:
            add = ac
        evt, ch = address_to_evtch(add)
        a = b.get_action_by_address(add)
        if argsd["raw"]:
            fmt = "0x%02X [blue]%2d[/blue] [blue](0x%02X)[/blue] [aquamarine3]%2d[/aquamarine3] : "
            ab = a.to_bytes()
            for i in range(16):
                if ab[i] == 0x00:
                    fmt = fmt + "[black]%02X "
                else:
                    fmt = fmt + "[white]%02X "
                if i == 7:
                    fmt = fmt + " "

            print(fmt % (add, add, evt, ch, *a.to_bytes()))
        else:
            if add < 0x3C:
                es = shorter_str(evtid_dict[evt])
            else:
                es = shorter_str(evtid_dict[add])
            if a.is_empty():
                print(
                    "0x%02X: [bold blue]%-16s[/bold blue] Ch [aquamarine3]%d[/aquamarine3] : ---"
                    % (add, es, ch + 1)
                )
            else:
                vs = shorter_str(a.verbose_line_str(b))
                print(
                    "0x%02X: [bold blue]%-16s[/bold blue] Ch [aquamarine3]%d[/aquamarine3] : %s"
                    % (add, es, ch + 1, vs)
                )

    b.close()


if __name__ == "__main__":
    main()
