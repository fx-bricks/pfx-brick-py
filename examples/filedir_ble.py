#! /usr/bin/env python3

# PFx Brick example script to show PFx Brick file directory

import asyncio

from pfxbrick import *


async def brick_session(brickdev):
    brick = PFxBrickBLE(dev_dict=brickdev)
    await brick.open()
    print("Connected.  Getting file directory...")
    await brick.refresh_file_dir()
    print(brick.filedir)
    await brick.close()


loop = asyncio.new_event_loop()
pfxdevs = loop.run_until_complete(ble_device_scanner())
print("Found %d PFx Bricks" % (len(pfxdevs)))
if len(pfxdevs) > 0:
    bricks = loop.run_until_complete(find_ble_pfxbricks(pfxdevs))
    if len(bricks) > 0:
        loop.run_until_complete(brick_session(bricks[0]))
