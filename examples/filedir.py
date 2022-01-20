#! /usr/bin/env python3

# PFx Brick example script to show PFx Brick file directory

import hid

from pfxbrick import PFxBrick

brick = PFxBrick()
brick.open()
brick.refresh_file_dir()
print(brick.filedir)
brick.close()
