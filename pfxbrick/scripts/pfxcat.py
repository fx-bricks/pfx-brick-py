#! /usr/bin/env python3
"""
pfxcat - print the contens of a file on the PFx Brick
"""
import argparse
import tempfile
from sys import argv

from pfxbrick import *

TMP_FILE = tempfile.gettempdir() + os.sep + "pfxdump.dat"


def main():
    parser = argparse.ArgumentParser(
        description="PFx Brick print file contents",
        prefix_chars="-+",
    )
    parser.add_argument(
        "file", metavar="file", type=str, help="file name or file ID to show contents"
    )
    parser.add_argument(
        "-s",
        "--serialno",
        default=None,
        help="Specify PFx Brick with serial number (if more than one connected)",
    )
    args = parser.parse_args()
    argsd = vars(args)

    b = get_one_pfxbrick(argsd["serialno"])
    r = b.open()
    if not r:
        exit()
    b.refresh_file_dir()
    f = argsd["file"]
    if f.isnumeric():
        fid = int(f)
    else:
        fid = b.file_id_from_str_or_int(f)
    as_bytes = True if len(argv) == 3 else False
    fd = b.filedir.get_file_dir_entry(fid)
    if fd is not None:
        fs_copy_file_from(
            b, fd, TMP_FILE, show_progress=False, as_bytes=as_bytes, to_console=True
        )
        os.remove(TMP_FILE)
    else:
        print("File %s not found" % (argv[1]))
    b.close()


if __name__ == "__main__":
    main()
