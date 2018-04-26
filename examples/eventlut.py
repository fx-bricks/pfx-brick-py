#! /usr/bin/env python3
 
# PFx Brick example script to show access to the event/action LUT

import hid
import time
import copy
from pfxbrick import PFxBrick, PFxAction, find_bricks
from pfxbrick.pfx import *

brick = PFxBrick()
brick.open()

left_button_ch1 = brick.get_action(EVT_ID_8879_LEFT_BUTTON, 0)
print("Get action for Left Button Ch 1 on Speed Remote...")
print(left_button_ch1)

print("Add a light effect to this action...")
new_left_action = copy.copy(left_button_ch1)
new_left_action.light_on([1,2,3,4])
print(new_left_action)

print("Save new action back to brick...")
brick.set_action(EVT_ID_8879_LEFT_BUTTON, 0, new_left_action)
print(brick.get_action(EVT_ID_8879_LEFT_BUTTON, 0))
time.sleep(1)

print("Restore the original action without the change...")
brick.set_action(EVT_ID_8879_LEFT_BUTTON, 0, left_button_ch1)
print(brick.get_action(EVT_ID_8879_LEFT_BUTTON, 0))

brick.close()
