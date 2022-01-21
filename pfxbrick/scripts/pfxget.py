#! /usr/bin/env python3
import argparse

from pfxbrick import *


def main():
    parser = argparse.ArgumentParser(
        description="copy a file from the PFx Brick to host computer",
        prefix_chars="-+",
    )
    parser.add_argument(
        "file", metavar="file", type=str, help="is file ID or filename to copy"
    )
    parser.add_argument(
        "dest",
        type=str,
        default=None,
        nargs="?",
        help="is optional local file path override for copied file",
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
    fd = b.filedir.get_file_dir_entry(fid)
    if argsd["dest"] is not None:
        fn = argsd["dest"]
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
