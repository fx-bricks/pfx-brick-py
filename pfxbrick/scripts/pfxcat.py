#! /usr/bin/env python3
import tempfile
from sys import argv

from pfxbrick import *

TMP_FILE = tempfile.gettempdir() + os.sep + "pfxdump.dat"


def main():
    if len(argv) < 2 or "-h" in argv:
        print("Usage: pfxcat file -h")
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
        fid = int(f)
    else:
        fid = b.file_id_from_str_or_int(f)
    as_bytes = True if len(argv) == 3 else False
    fd = b.filedir.get_file_dir_entry(fid)
    if fd is not None:
        fs_copy_file_from(
            b.dev, fd, TMP_FILE, show_progress=False, as_bytes=as_bytes, to_console=True
        )
        os.remove(TMP_FILE)
    else:
        print("File %s not found" % (argv[1]))
    b.close()


if __name__ == "__main__":
    main()
