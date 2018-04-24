#! /usr/bin/env python3
 
# PFx Brick example script to retrieve basic information about the
# brick including its identidy and configuration settings.

import hid
import pfxbrick as pfx

brick = pfx.PFxBrick()
brick.open()
brick.get_status()
brick.print_status()
brick.get_config()
brick.print_config()
brick.get_name()
print(brick.name)
brick.close()
