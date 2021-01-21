#! /usr/bin/env python3

# PFx Brick example script to demonstrate motor control

import time
from pfxbrick import *


brick = PFxBrick()
brick.open()

print("Motor channel A forward 50% speed")
brick.set_motor_speed([1], 50)
print("Waiting 3 seconds...")
time.sleep(3)

print("Stop motor A")
brick.stop_motor([1])
time.sleep(1)

print("Motor channel A reverse 33% speed for 2 sec self-timed")
brick.set_motor_speed([1], -33, 2)

brick.close()
