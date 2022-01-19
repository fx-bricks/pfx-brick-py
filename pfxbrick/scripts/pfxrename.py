#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


def main():
    if len(argv) < 3 or "-h" in argv:
        print("Usage: pfxrename file newname")
        print("  where <file> is file ID or filename to change")
        print("        <newname> is the new desired filename")
        exit()
    b = PFxBrick()
    r = b.open()
    if not r:
        exit()
    b.open()
    b.refresh_file_dir()
    f = str(argv[1])
    if f.isnumeric():
        f = int(argv[1])
    fid = b.file_id_from_str_or_int(f)
    fd = b.filedir.get_file_dir_entry(fid)
    if len(argv) == 3:
        fn = argv[2]
        b.rename_file(fid, fn)
        print("Renamed file %s to %s" % (str(argv[1]), fn))
    b.refresh_file_dir()
    print(b.filedir)
    b.close()


if __name__ == "__main__":
    main()
