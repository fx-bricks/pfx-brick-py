#! /usr/bin/env python3

# PFx Brick example script to retrieve basic information about the
# brick including its identidy and configuration settings.

import asyncio
from math import sin

from pfxbrick import *


async def brick_session(brickdev):
    brick = PFxBrickBLE(brickdev)
    await brick.open()
    print("Set lights 1, 2, 3, 4 ON")
    await brick.light_on([1, 2, 3, 4])
    await asyncio.sleep(2)

    for x in range(100):
        b = int(sin(6.28 * x * 0.1) * 127 + 128)
        await brick.set_brightness([1, 2, 3, 4], b)

    print("Set lights 1, 2, 3, 4 OFF")
    await brick.light_off([1, 2, 3, 4])
    await asyncio.sleep(2)

    print("Set strobe lights 1, 4 ON")
    a = PFxAction().light_fx(
        [1, 4],
        EVT_LIGHTFX_STROBE_P,
        [EVT_PERIOD_1S, EVT_DUTYCY_10, EVT_BURST_COUNT_2, EVT_TRANSITION_TOGGLE],
    )
    await brick.test_action(a)
    await asyncio.sleep(3)

    print("Toggle linear sweep with 8 lights ON")
    await brick.combo_light_fx(
        EVT_COMBOFX_LIN_SWEEP, [EVT_PERIOD_1S, EVT_FADE_FACTOR_30, EVT_SIZE_8_LIGHTS]
    )
    await asyncio.sleep(3)

    print("Toggle linear sweep with 8 lights OFF")
    await brick.combo_light_fx(
        EVT_COMBOFX_LIN_SWEEP, [EVT_PERIOD_1S, EVT_FADE_FACTOR_30, EVT_SIZE_8_LIGHTS]
    )
    await brick.close()


loop = asyncio.new_event_loop()
pfxdevs = loop.run_until_complete(ble_device_scanner())
print("Found %d PFx Bricks" % (len(pfxdevs)))
if len(pfxdevs) > 0:
    bricks = loop.run_until_complete(find_ble_pfxbricks(pfxdevs))
    if len(bricks) > 0:
        loop.run_until_complete(brick_session(bricks[0]))
