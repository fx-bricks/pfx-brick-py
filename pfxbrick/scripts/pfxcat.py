#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


if __name__ == "__main__":
    if len(argv) < 2 or argv[1] == "-h":
        print("Usage: pfxcat.py file -h")
        print("  where file is file ID or filename to dump")
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
    as_bytes = True if len(argv) == 3 else False
    f = b.filedir.get_file_dir_entry(fid)
    fs_copy_file_from(b.dev, f, show_progress=False, as_bytes=as_bytes, to_console=True)
    b.close()
