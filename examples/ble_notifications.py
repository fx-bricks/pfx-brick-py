#! /usr/bin/env python3

# PFx Brick example script to demonstrate using notifications from PFx Brick

import asyncio

from pfxbrick import *


# our callback functions for notification events
def motor_a_stopped():
    print("Motor ch A has stopped")


def motor_a_speed_change(speed):
    print("Motor ch A has changed speed to %d" % (speed))


def audio_file_started(fileid, filename):
    print("Audio playback has started for file %d: %s" % (fileid, filename))


async def brick_session(brickdev):
    brick = PFxBrickBLE(dev_dict=brickdev, debug=False)
    await brick.open()

    # register our notification callback functions
    brick.callback_motora_stop = motor_a_stopped
    brick.callback_motora_speed = motor_a_speed_change
    brick.callback_audio_play = audio_file_started

    # activate our desired PFx Brick notifications
    await brick.set_notifications(
        PFX_NOTIFICATION_AUDIO_PLAY
        | PFX_NOTIFICATION_MOTORA_STOP
        | PFX_NOTIFICATION_MOTORA_CURR_SPD
    )

    # Motor channel A forward 50% speed
    await brick.set_motor_speed([1], -50)
    await asyncio.sleep(3)

    # Stop motor A
    await brick.stop_motor([1])
    await asyncio.sleep(1)

    # Motor channel A reverse 33% speed for 2 sec self-timed
    await brick.set_motor_speed([1], 33, 2)

    await asyncio.sleep(1)
    await brick.play_audio_file(2)
    await asyncio.sleep(2)

    # turn off notifications
    await brick.disable_notifications()

    await brick.close()


loop = asyncio.get_event_loop()
pfxdevs = loop.run_until_complete(ble_device_scanner())
print("Found %d PFx Bricks" % (len(pfxdevs)))
if len(pfxdevs) > 0:
    bricks = loop.run_until_complete(find_ble_pfxbricks(pfxdevs))
    if len(bricks) > 0:
        loop.run_until_complete(brick_session(bricks[0]))
