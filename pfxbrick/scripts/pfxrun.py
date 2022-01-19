#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


def main():
    if len(argv) < 2 or "-h" in argv:
        print("Usage: pfxrun.py file [-s]")
        print("  where <file> is file ID or filename of script file to run")
        print("  -s optionally stops script execution")
        exit()
    b = PFxBrick()
    b.open()
    r = b.open()
    if not r:
        exit()
    b.refresh_file_dir()
    f = str(argv[1])
    if f == "-s":
        b.stop_script()
        print("Script execution stopped")
        exit()
    if f.isnumeric():
        f = int(argv[1])
    fid = b.file_id_from_str_or_int(f)
    if fid < 0xFF:
        b.run_script(fid)
        print("Running script file %s" % (argv[1]))
    else:
        print("File %s is not found on the PFx Brick" % (argv[1]))
    b.close()


if __name__ == "__main__":
    main()
