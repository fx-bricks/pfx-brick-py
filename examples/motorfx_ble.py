#! /usr/bin/env python3

# PFx Brick example script to demonstrate motor control

import asyncio

from pfxbrick import *


async def brick_session(brickdev):
    brick = PFxBrickBLE(dev_dict=brickdev)
    await brick.open()

    print("Motor channel A forward 50% speed")
    await brick.set_motor_speed([1], 50)
    print("Waiting 3 seconds...")
    await asyncio.sleep(3)

    print("Stop motor A")
    await brick.stop_motor([1])
    await asyncio.sleep(1)

    print("Motor channel A reverse 33% speed for 2 sec self-timed")
    await brick.set_motor_speed([1], -33, 2)

    await brick.close()


loop = asyncio.get_event_loop()
pfxdevs = loop.run_until_complete(ble_device_scanner())
print("Found %d PFx Bricks" % (len(pfxdevs)))
if len(pfxdevs) > 0:
    bricks = loop.run_until_complete(find_ble_pfxbricks(pfxdevs))
    loop.run_until_complete(brick_session(bricks[0]))
