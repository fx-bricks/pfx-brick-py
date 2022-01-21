#! /usr/bin/env python3
"""
pfxrun - run a script file on the PFx Brick
"""
import argparse

from pfxbrick import *


def main():
    parser = argparse.ArgumentParser(
        description="Run a script file on the PFx Brick",
        prefix_chars="-+",
    )
    parser.add_argument(
        "file", metavar="file", type=str, help="file name or file ID of script"
    )
    parser.add_argument(
        "-e",
        "--end",
        action="store_true",
        default=False,
        help="end script execution",
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
    if argsd["end"]:
        b.stop_script()
        print("Script execution stopped")
        exit()
    f = str(argsd["file"])
    if f.isnumeric():
        f = int(argsd["file"])
    fid = b.file_id_from_str_or_int(f)
    if fid < 0xFF:
        b.run_script(fid)
        print("Running script file %s" % (argsd["file"]))
    else:
        print("File %s is not found on the PFx Brick" % (argsd["file"]))
    b.close()


if __name__ == "__main__":
    main()
