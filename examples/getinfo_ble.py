#! /usr/bin/env python3

# PFx Brick example script to retrieve basic information about the
# brick including its identity and configuration settings.

import asyncio

from pfxbrick import *


async def brick_session(brickdev):
    brick = PFxBrickBLE(dev_dict=brickdev)
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


loop = asyncio.new_event_loop()
pfxdevs = loop.run_until_complete(ble_device_scanner(filters=["16 MB"]))

print("Found %d PFx Bricks" % (len(pfxdevs)))
if len(pfxdevs) > 0:
    bricks = loop.run_until_complete(find_ble_pfxbricks(pfxdevs))
    if len(bricks) > 0:
        loop.run_until_complete(brick_session(bricks[0]))
