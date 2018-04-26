#! /usr/bin/env python3
 
# PFx Brick example script to demonstrate multiple scripted actions

import hid
import time
import random
from pfxbrick import PFxBrick, PFxAction
from pfxbrick.pfx import *

brick = PFxBrick()
brick.open()

audiofile = 2
max_speed = 100

# start looped audio playback and set volume
brick.test_action(PFxAction().repeat_audio_file(audiofile))
brick.test_action(PFxAction().set_volume(75))

# ramp up the motor speed gradually to max_speed
for x in range(max_speed):
    brick.test_action(PFxAction().set_motor_speed([1], x))
    # show a random light pattern
    y = random.randint(1,8)
    brick.test_action(PFxAction().light_toggle([y]))
    time.sleep(0.1)

# ramp down the motor speed gradually to 0%

for x in range(max_speed):
    brick.test_action(PFxAction().set_motor_speed([1], max_speed-x-1))
    # show a random light pattern
    y = random.randint(1,8)
    brick.test_action(PFxAction().light_toggle([y]))
    time.sleep(0.1)

# stop motor and turn off audio and lights
brick.test_action(PFxAction().stop_motor([1]))
brick.test_action(PFxAction().stop_audio_file(audiofile))
brick.test_action(PFxAction().light_off(range(1,9))

brick.close()
