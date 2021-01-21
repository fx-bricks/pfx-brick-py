#! /usr/bin/env python3

# PFx Brick example script to show access to the event/action LUT
# by showing startup events

import hid
import time
import copy
from pfxbrick import *

brick = PFxBrick()
brick.open()

events = [
    EVT_STARTUP_EVENT1,
    EVT_STARTUP_EVENT2,
    EVT_STARTUP_EVENT3,
    EVT_STARTUP_EVENT4,
]
for event in events:
    evt, ch = address_to_evtch(event)
    print("%s %d at LUT address %02X" % (evtid_dict[evt], ch + 1, event))
    print(brick.get_action_by_address(event))
brick.close()
