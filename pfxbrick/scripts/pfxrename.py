#! /usr/bin/env python3
"""
pfxrename - renames a file on the PFx Brick
"""
import argparse

from pfxbrick import *


def main():
    parser = argparse.ArgumentParser(
        description="Rename a file on the PFx Brick",
        prefix_chars="-+",
    )
    parser.add_argument(
        "file", metavar="file", type=str, help="file name or file ID to rename"
    )
    parser.add_argument(
        "newname",
        type=str,
        default=None,
        help="new name to assign to file",
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
    b.open()
    b.refresh_file_dir()
    f = str(argsd["file"])
    if f.isnumeric():
        f = int(argsd["file"])
    fid = b.file_id_from_str_or_int(f)
    fn = argsd["newname"]
    b.rename_file(fid, fn)
    print("Renamed file %s to %s" % (str(argsd["file"]), fn))
    b.close()


if __name__ == "__main__":
    main()
