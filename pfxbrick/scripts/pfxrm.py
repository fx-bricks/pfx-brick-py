#! /usr/bin/env python3
"""
pfxrm - remove a file on the PFx Brick
"""
import argparse

from pfxbrick import *


def main():
    parser = argparse.ArgumentParser(
        description="remove a file from the PFx Brick",
        prefix_chars="-+",
    )
    parser.add_argument(
        "file", metavar="file", type=str, help="file name or file ID to remove"
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
    f = str(argsd["file"])
    if f.isnumeric():
        f = int(argsd["file"])
    fid = b.file_id_from_str_or_int(f)
    if fid < 0xFF:
        b.remove_file(fid)
    else:
        print("File %s is not found on the PFx Brick" % (argsd["file"]))
    b.close()


if __name__ == "__main__":
    main()
