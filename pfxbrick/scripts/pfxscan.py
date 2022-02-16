#! /usr/bin/env python3
"""
pfxscan - scan for advertising Bluetooth PFx Bricks
"""
import argparse
import asyncio
from datetime import datetime

from rich import print
from rich.console import Console
from rich.table import Table

from pfxbrick import *

console = Console()


async def brick_session(uuid, timeout=15):
    b = PFxBrickBLE(uuid=uuid)
    await b.open(timeout=timeout)
    icd = await b.get_icd_rev()
    await b.get_status()

    if b.status == 0x00:
        name = await b.get_name()
    else:
        name = "Service Mode"
    table = Table(show_header=True, header_style="bold blue")
    bid = "[light_slate_blue]%s [bold cyan]%s" % (b.product_id, b.product_desc)
    table.add_column(bid, width=72)
    table.add_row("Bluetooth UUID        : [bold orange3]%s" % (uuid))
    table.add_row("Serial Number         : [bold cyan]%s" % (b.serial_no))
    table.add_row("ICD Version           : [bold green]%s" % (icd))
    table.add_row(
        "Firmware Version      : [bold green]%s [reset]build [bold green]%s"
        % (b.firmware_ver, b.firmware_build)
    )
    table.add_row(
        "Status                : 0x%02X %s" % (b.status, get_status_str(b.status))
    )
    if b.error:
        table.add_row(
            "Errors                : [red]0x%02X %s" % (b.error, get_error_str(b.error))
        )
    else:
        table.add_row(
            "Errors                : [green]0x%02X %s"
            % (b.error, get_error_str(b.error))
        )
    table.add_row("Name                  : [bold yellow]%s" % (name))
    r = await b.get_rssi()
    table.add_row("RSSI                  : %s dBm" % (r))
    console.print(table)
    await b.close()


def main():
    parser = argparse.ArgumentParser(
        description="Scan for PFx Bricks advertising on Bluetooth"
    )
    parser.add_argument(
        "-s",
        "--scantime",
        default=10,
        help="Time interval (seconds) to scan for advertising PFx Bricks, default=10",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        default=15,
        help="Timeout interval (seconds) to wait while connecting to a PFx Brick, default=15",
    )
    args = parser.parse_args()
    argsd = vars(args)

    loop = asyncio.get_event_loop()
    pfxdevs = []
    with console.status("Scanning...") as status:
        pfxdevs = loop.run_until_complete(
            ble_device_scanner(
                scan_timeout=float(argsd["scantime"]), silent=True, filters=["16 MB"]
            )
        )
    print("Found %d PFx Bricks" % (len(pfxdevs)))
    if len(pfxdevs) > 0:
        for d in pfxdevs:
            with console.status(
                "Connecting to [bold orange3]%s[/]..." % (d.address)
            ) as status:
                loop.run_until_complete(
                    brick_session(d.address, timeout=float(argsd["timeout"]))
                )


if __name__ == "__main__":
    main()
