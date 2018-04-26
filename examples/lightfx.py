#! /usr/bin/env python3
 
# PFx Brick example script to retrieve basic information about the
# brick including its identidy and configuration settings.

import hid
import time
from math import sin
from pfxbrick import PFxBrick, PFxAction
from pfxbrick.pfx import *

brick = PFxBrick()
brick.open()
print("Set lights 1, 2, 3, 4 ON")
a = PFxAction().light_on([1, 2, 3, 4])
brick.test_action(a)
time.sleep(2)

for x in range(100):
    b = int(sin(6.28 * x * 0.1) * 127 + 128)
    brick.test_action(PFxAction().set_brightness([1,2,3,4], b))
    time.sleep(0.050)

print("Set lights 1, 2, 3, 4 OFF")
a = PFxAction().light_off([1, 2, 3, 4])
brick.test_action(a)
time.sleep(2)

print("Set strobe lights 1, 4 ON")
a = PFxAction().light_fx([1,4], EVT_LIGHTFX_STROBE_P, [EVT_PERIOD_1S, EVT_DUTYCY_10, EVT_BURST_COUNT_2, EVT_TRANSITION_TOGGLE])
brick.test_action(a)
time.sleep(3)

print("Toggle linear sweep with 8 lights ON")
a = PFxAction().combo_light_fx(EVT_COMBOFX_LIN_SWEEP, [EVT_PERIOD_1S, EVT_FADE_FACTOR_30, EVT_SIZE_8_LIGHTS])
brick.test_action(a)
time.sleep(3)

print("Toggle linear sweep with 8 lights OFF")
a = PFxAction().combo_light_fx(EVT_COMBOFX_LIN_SWEEP, [EVT_PERIOD_1S, EVT_FADE_FACTOR_30, EVT_SIZE_8_LIGHTS])
brick.test_action(a)
brick.close()
