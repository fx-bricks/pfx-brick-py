#! /usr/bin/env python3
"""
PFx Brick example script to retrieve basic information about the
brick including its identity and configuration settings.

This example shows how you can start a session with a PFx Brick
directly without scanning if you already know its Bluetooth
UUID / address. The Bluetooth hardware address is operating system
dependent and must be provided in a UUID form that is compatible with your OS.

for Windows and Linux this is typically in the form of "24:71:89:cc:09:05"
and on macOS it is in the form of "B9EA5233-37EF-4DD6-87A8-2A875E821C46"
"""

import asyncio

from pfxbrick import *


async def brick_session(uuid):
    brick = PFxBrickBLE(uuid=uuid)
    await brick.open()
    print("PFx Brick Status / Identity")
    print("===========================")
    print("PFx Brick ICD version : %s" % (await brick.get_icd_rev()))
    await brick.get_name()
    print("PFx Brick name        : %s" % (brick.name))
    await brick.get_status()
    brick.print_status()
    print("PFx Brick Configuration")
    print("=======================")
    await brick.get_config()
    brick.print_config()
    r = await brick.get_rssi()
    print("RSSI = %s" % (r))
    await brick.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(brick_session("059930E2-BE75-48A4-B193-3AD3F67246E4"))
