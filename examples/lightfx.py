#! /usr/bin/env python3
 
# PFx Brick example script to retrieve basic information about the
# brick including its identidy and configuration settings.

import hid
import time
import pfxbrick.pfxbrick as pfx
from pfxbrick.pfxaction import PFxAction
from pfxbrick.pfx import *

brick = pfx.PFxBrick()
brick.open()
print("Turn lights 1, 2, 3, 4 ON")
a = PFxAction().light_on([1, 2, 3, 4])
brick.test_action(a)
time.sleep(2)
print("Toggle lights 1, 2, 3, 4 OFF")
a = PFxAction().light_off([1, 2, 3, 4])
brick.test_action(a)
time.sleep(2)
print("Toggle strobe lights 1, 4 ON")
a = PFxAction().light_fx([1,4], EVT_LIGHTFX_STROBE_P, [EVT_PERIOD_1S, EVT_DUTYCY_10, EVT_BURST_COUNT_2, EVT_TRANSITION_TOGGLE])
brick.test_action(a)
time.sleep(4)
print("Toggle linear sweep with 8 lights ON")
a = PFxAction().combo_light_fx(EVT_COMBOFX_LIN_SWEEP, [EVT_PERIOD_1S, EVT_FADE_FACTOR_30, EVT_SIZE_8_LIGHTS])
brick.test_action(a)
time.sleep(4)
print("Toggle linear sweep with 8 lights OFF")
a = PFxAction().combo_light_fx(EVT_COMBOFX_LIN_SWEEP, [EVT_PERIOD_1S, EVT_FADE_FACTOR_30, EVT_SIZE_8_LIGHTS])
brick.test_action(a)
brick.close()
