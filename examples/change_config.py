#! /usr/bin/env python3
 
# PFx Brick example script to showing modification to the
# brick configuration settings.

import hid
from pfxbrick import PFxBrick, find_bricks
from pfxbrick.pfx import *

bricks = find_bricks()
print('%d PFx Bricks found' % (len(bricks)))

if bricks:
    brick = PFxBrick()
    res = brick.open()
    if not res:
        print("Unable to open session to PFx Brick")
    else:
        print('PFx Brick Configuration')
        print('=======================')
        brick.get_config()
        brick.print_config()

        print("Change the volume beep setting...")
        if brick.config.settings.volumeBeep == PFX_CFG_VOLBEEP_ON:
            brick.config.settings.volumeBeep = PFX_CFG_VOLBEEP_OFF
        else:
            brick.config.settings.volumeBeep = PFX_CFG_VOLBEEP_ON
        brick.set_config()

        print('PFx Brick Updated Configuration')
        print('===============================')
        brick.get_config()
        brick.print_config()

        brick.close()
