#! /usr/bin/env python3
 
# PFx Brick example script to show PFx Brick file directory

import hid
from pfxbrick import PFxBrick
from sys import argv

if len(argv) < 3:
    print("Usage: ./filecopy.py <filename> <id>")
    print("  where <filename> is the local file to copy")
    print("        <id> is the unique file ID to assign the file on the PFx Brick")
else:
    brick = PFxBrick()
    brick.open()

    fn = argv[1]
    fid = int(argv[2])
    print("Copying %s to brick with id %d..." % (fn, fid))
    brick.put_file(fid, fn)
    brick.refresh_file_dir()
    print(brick.filedir)

    brick.close()