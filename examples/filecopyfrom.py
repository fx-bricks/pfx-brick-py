#! /usr/bin/env python3

# PFx Brick example script to show copying a file from the PFx Brick

import hid
from pfxbrick import PFxBrick
from sys import argv

brick = PFxBrick()
brick.open()

if len(argv) < 2:
    print("Usage: ./filecopyfrom.py <id> [filename]")
    print("  where <id> is file ID to copy or a string filename")
    print("  where [filename] optional override filename when copied")
else:
    fn = ""
    fid = int(argv[1])
    brick.refresh_file_dir()
    fid = brick.file_id_from_str_or_int()
    f = brick.filedir.get_file_dir_entry(fid)
    if len(argv) == 3:
        fn = argv[2]
    else:
        fn = f.name
    print("Copying file id %d as %s from brick..." % (fid, fn))
    brick.get_file(fid, fn)

    brick.close()
