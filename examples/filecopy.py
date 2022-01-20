#! /usr/bin/env python3

# PFx Brick example script to show PFx Brick file directory

from sys import argv

import hid

from pfxbrick import PFxBrick

if len(argv) < 3:
    print("Usage: ./filecopy.py <filename> [id]")
    print("  where <filename> is the local file to copy")
    print(
        "        <id> is an optional unique file ID to assign the file on the PFx Brick"
    )
    print("             if not specified, it is automatically determined")
else:
    brick = PFxBrick()
    brick.open()

    fn = argv[1]
    if len(argv) > 2:
        fid = int(argv[2])
    else:
        brick.refresh_file_dir()
        fid = brick.filedir.find_available_file_id()
    print("Copying %s to brick with id %d..." % (fn, fid))
    brick.put_file(fid, fn)
    brick.refresh_file_dir()
    print(brick.filedir)

    brick.close()
