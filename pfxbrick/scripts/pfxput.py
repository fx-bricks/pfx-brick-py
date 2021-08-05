#! /usr/bin/env python3
from sys import argv
from toolbox import *
from pfxbrick import *


if __name__ == "__main__":
    if len(argv) < 2 or argv[1] == "-h":
        print("Usage: pfxput.py file id")
        print("  where file is the local file to copy")
        print("        id is an optional file ID to use instead of next available ID")
        exit()
    b = PFxBrick()
    b.open()
    r = b.open()
    if not r:
        exit()
    b.refresh_file_dir()

    ff = full_path(argv[1])
    fp, fn = split_path(ff)
    if len(argv) == 3:
        fid = int(argv[2])
        if b.filedir.has_file(fid):
            print("Replacing file %d on PFx Brick..." % (fid))
            b.remove_file(fid)
        else:
            print("Copying file %s as %d to PFx Brick..." % (fn, fid))

    else:
        fid = b.filedir.find_available_file_id()
        if b.filedir.has_file(fn):
            fod = b.file_id_from_str_or_int(fn)
            print("Replacing file %s on PFx Brick..." % (fn))
            b.remove_file(fod)
            fid = fod
        else:
            print("Copying file %s to PFx Brick..." % (fn))

    b.put_file(ff, fid)
    if fn.lower().endswith(".pfx"):
        res = b.send_raw_icd_command(
            [PFX_CMD_FILE_DIR, PFX_DIR_REQ_SET_ATTR_ID, fid, 0x30, 0x80]
        )
    b.close()
