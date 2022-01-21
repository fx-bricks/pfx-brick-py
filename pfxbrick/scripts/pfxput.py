#! /usr/bin/env python3
import argparse

from pfxbrick import *


def full_path(file):
    """Returns the fully expanded path of a file"""
    if "~" in str(file):
        return os.path.expanduser(file)
    return os.path.expanduser(os.path.abspath(file))


def split_path(file):
    """Returns a tuple containing a file's (directory, name.ext)"""
    if os.path.isdir(file):
        return full_path(file), None
    return os.path.split(full_path(file))


def main():
    parser = argparse.ArgumentParser(
        description="copy a file to the PFx Brick from host computer",
        prefix_chars="-+",
    )
    parser.add_argument(
        "file", metavar="file", type=str, help="is the local filename to copy"
    )
    parser.add_argument(
        "dest",
        type=str,
        default=None,
        nargs="?",
        help="is optional file ID instead of next available ID",
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

    ff = full_path(argsd["file"])
    _, fn = split_path(ff)
    if argsd["dest"] is not None:
        fid = int(argsd["dest"])
        if b.filedir.has_file(fid):
            print("Replacing file %d on PFx Brick..." % (fid))
        else:
            print("Copying file %s as %d to PFx Brick..." % (fn, fid))

    else:
        if b.filedir.has_file(fn):
            fid = b.file_id_from_str_or_int(fn)
            print("Replacing file %s on PFx Brick..." % (fn))
        else:
            fid = b.filedir.find_available_file_id()
            print("Copying file %s to PFx Brick..." % (fn))

    b.put_file(ff, fid)
    if fn.lower().endswith(".pfx"):
        res = b.send_raw_icd_command(
            [PFX_CMD_FILE_DIR, PFX_DIR_REQ_SET_ATTR_ID, fid, 0x30, 0x80]
        )
    b.close()


if __name__ == "__main__":
    main()
