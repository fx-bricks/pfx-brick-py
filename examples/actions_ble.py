#! /usr/bin/env python3

# PFx Brick example script to demonstrate multiple scripted actions


import asyncio
import random
from pfxbrick import *


async def brick_session(brickdev):
    brick = PFxBrickBLE(dev_dict=brickdev, debug=False)
    await brick.open()
    max_speed = 50
    audiofile = "yamanote16pcm22k"

    # start looped audio playback and set volume
    await brick.repeat_audio_file(audiofile)
    await brick.set_volume(75)

    # ramp up the motor speed gradually to max_speed
    for x in range(max_speed):
        await brick.set_motor_speed([1], x)
        # show a random light pattern
        y = random.randint(1, 8)
        await brick.light_toggle([y])
        await asyncio.sleep(0.1)

    # ramp down the motor speed gradually to 0%

    for x in range(max_speed):
        await brick.set_motor_speed([1], max_speed - x - 1)
        # show a random light pattern
        y = random.randint(1, 8)
        await brick.light_toggle([y])
        await asyncio.sleep(0.1)

    # stop motor and turn off audio and lights
    await brick.stop_motor([1])
    await brick.stop_audio_file(audiofile)
    await brick.light_off([ch for ch in range(1, 9)])

    await brick.close()


loop = asyncio.get_event_loop()
pfxdevs = loop.run_until_complete(ble_device_scanner())
print("Found %d PFx Bricks" % (len(pfxdevs)))
if len(pfxdevs) > 0:
    bricks = loop.run_until_complete(find_ble_pfxbricks(pfxdevs))
    loop.run_until_complete(brick_session(bricks[0]))
