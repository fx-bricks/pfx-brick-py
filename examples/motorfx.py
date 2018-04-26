#! /usr/bin/env python3
 
# PFx Brick example script to demonstrate motor control

import hid
import time
from pfxbrick import PFxBrick, PFxAction
from pfxbrick.pfx import *

brick = PFxBrick()
brick.open()

print("Motor channel A forward 50% speed")
a = PFxAction().set_motor_speed([1], 50)
brick.test_action(a)
print("Waiting 3 seconds...")
time.sleep(3)

print("Stop motor A")
a = PFxAction().stop_motor([1])
brick.test_action(a)
time.sleep(1)

print("Motor channel A reverse 33% speed for 2 sec self-timed")
a = PFxAction().set_motor_speed([1], -33, 2)
brick.test_action(a)

brick.close()
