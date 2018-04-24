#! /usr/bin/env python3
 
# PFx Brick example script to retrieve basic information about the
# brick including its identidy and configuration settings.

import hid
import pfxbrick.pfxbrick as pfx
from pfxbrick.pfxaction import PFxAction
from pfxbrick.pfx import *

brick = pfx.PFxBrick()
brick.open()
print('PFx Brick Status / Identity')
print('===========================')
print('PFx Brick ICD version : %s' %(brick.get_icd_rev()))
brick.get_name()
print('PFx Brick name        : %s' %(brick.name))
brick.get_status()
brick.print_status()
print('PFx Brick Configuration')
print('=======================')
brick.get_config()
brick.print_config()
#a = PFxAction().light_toggle([1, 2, 3, 4])
# a = PFxAction().light_fx([1,4], EVT_LIGHTFX_STROBE_P, [EVT_PERIOD_1S, EVT_DUTYCY_10, EVT_BURST_COUNT_2, EVT_TRANSITION_TOGGLE])
# a = PFxAction().combo_light_fx(EVT_COMBOFX_LIN_SWEEP, [EVT_PERIOD_1S, EVT_FADE_FACTOR_30, EVT_SIZE_8_LIGHTS])
# brick.test_action(a)
brick.close()
