#! /usr/bin/env python3

# PFx Brick example script to demonstrate multiple scripted actions


import random
import time

from pfxbrick import *

brick = PFxBrick()
brick.open()

max_speed = 100
audiofile = "yamanote16pcm22k"

# start looped audio playback and set volume
brick.repeat_audio_file(audiofile)
brick.set_volume(75)

# ramp up the motor speed gradually to max_speed
for x in range(max_speed):
    brick.set_motor_speed([1], x)
    # show a random light pattern
    y = random.randint(1, 8)
    brick.light_toggle([y])
    time.sleep(0.1)

# ramp down the motor speed gradually to 0%

for x in range(max_speed):
    brick.set_motor_speed([1], max_speed - x - 1)
    # show a random light pattern
    y = random.randint(1, 8)
    brick.light_toggle([y])
    time.sleep(0.1)

# stop motor and turn off audio and lights
brick.stop_motor([1])
brick.stop_audio_file(audiofile)
brick.light_off([ch for ch in range(1, 9)])

brick.close()
