#! /usr/bin/env python3
 
# PFx Brick example script to retrieve basic information about the
# brick including its identity and configuration settings.

import hid
from pfxbrick import PFxBrick, find_bricks

n = find_bricks(True)
print('%d PFx Bricks found' % (n))

if n > 0:
    brick = PFxBrick()
    res = brick.open()
    if not res:
        print("Unable to open session to PFx Brick")
    else:
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
        brick.close()
