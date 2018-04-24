#! /usr/bin/env python3
 
# PFx Brick example script to show PFx Brick file directory

import hid
import pfxbrick.pfxbrick as pfx
from pfxbrick.pfx import *

brick = pfx.PFxBrick()
brick.open()
brick.refresh_file_dir()
print(brick.filedir)
brick.close()
