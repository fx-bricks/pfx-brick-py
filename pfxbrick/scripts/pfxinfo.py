#! /usr/bin/env python3
import argparse
from datetime import datetime
from rich import print
from rich.console import Console
from rich.table import Table

from pfxbrick import *

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Show information for all attached PFx Bricks"
    )
    parser.add_argument(
        "-c",
        "--config",
        action="store_true",
        default=False,
        help="Show configuration details",
    )
    args = parser.parse_args()
    argsd = vars(args)

    bricks = find_bricks()
    for brick in bricks:
        b = PFxBrick(brick)
        b.open()
        b.get_status()
        icd = b.get_icd_rev()
        name = b.get_name()

        table = Table(show_header=True, header_style="bold blue")
        bid = "[light_slate_blue]%s [bold cyan]%s" % (b.product_id, b.product_desc)
        table.add_column(bid, width=72)
        table.add_row("Serial Number         : [bold cyan]%s" % (b.serial_no))
        table.add_row("ICD Version           : [bold green]%s" % (icd))
        table.add_row(
            "Firmware Version      : [bold green]%s [reset]build [bold green]%s"
            % (b.firmware_ver, b.firmware_build)
        )
        table.add_row("USB vendor ID         : [cyan]0x%04X" % (b.usb_vid))
        table.add_row("USB product ID        : [cyan]0x%04X" % (b.usb_pid))
        table.add_row(
            "Status                : 0x%02X %s" % (b.status, get_status_str(b.status))
        )
        if b.error:
            table.add_row(
                "Errors                : [red]0x%02X %s"
                % (b.error, get_error_str(b.error))
            )
        else:
            table.add_row(
                "Errors                : [green]0x%02X %s"
                % (b.error, get_error_str(b.error))
            )

        table.add_row("Name                  : [bold yellow]%s" % (name))

        console.print(table)
        b.get_current_state()
        b.get_fs_state()

        if argsd["config"]:
            b.get_config()
            console.print(str(b.config))


if __name__ == "__main__":
    main()
