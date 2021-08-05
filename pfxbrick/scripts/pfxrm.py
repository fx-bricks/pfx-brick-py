#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


if __name__ == "__main__":
    if len(argv) < 2 or argv[1] == "-h":
        print("Usage: pfxrm.py file")
        print("  where file is file ID or filename to remove")
        exit()
    b = PFxBrick()
    b.open()
    r = b.open()
    if not r:
        exit()
    b.refresh_file_dir()
    f = str(argv[1])
    if f.isnumeric():
        f = int(argv[1])
    fid = b.file_id_from_str_or_int(f)
    if fid < 0xFF:
        b.remove_file(fid)
    else:
        print("File %s is not found on the PFx Brick" % (argv[1]))
    b.close()
