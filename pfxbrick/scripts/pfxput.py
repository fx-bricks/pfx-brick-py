#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: pfxput file id")
        print("  where file is the local file to copy")
        print("        id is an optional file ID to use instead of next available ID")
        exit()
    b = PFxBrick()
    b.open()
    r = b.open()
    if not r:
        exit()
    b.refresh_file_dir()
    if len(argv) == 3:
        fid = int(argv[2])
    else:
        fid = b.filedir.find_available_file_id()
    fn = argv[1]
    print("Copying file %s to PFx Brick..." % (fn))
    b.put_file(fn, fid)
    if fn.lower().endswith(".pfx"):
        res = b.send_raw_icd_command(
            [PFX_CMD_FILE_DIR, PFX_DIR_REQ_SET_ATTR_ID, fid, 0x30, 0x80]
        )
    b.close()
