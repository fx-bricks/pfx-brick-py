#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


def main():
    if len(argv) < 2 or "-h" in argv:
        print("Usage: pfxget file dest")
        print("  where <file> is file ID or filename to get")
        print("        <dest> is optional local file path override for copied file")
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
    else:
        fn = fd.name
        if fd.is_audio_file() and not fd.name.lower().endswith(".wav"):
            fn = fn + ".wav"
        if fd.is_script_file() and not fd.name.lower().endswith(".pfx"):
            fn = fn + ".pfx"
    print("Copying file %s as %s from brick..." % (f, fn))
    b.get_file(fid, fn)
    b.close()


if __name__ == "__main__":
    main()
