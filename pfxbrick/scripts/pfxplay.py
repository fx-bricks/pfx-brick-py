#! /usr/bin/env python3
"""
pfxplay - play an audio file on the PFx Brick
"""
import argparse

from pfxbrick import *


def main():
    parser = argparse.ArgumentParser(
        description="Play an audio file on the PFx Brick",
        prefix_chars="-+",
    )
    parser.add_argument(
        "file", metavar="file", type=str, help="file name or file ID to play"
    )
    parser.add_argument(
        "-l",
        "--loop",
        action="store_true",
        default=False,
        help="loop playback repeatedly",
    )
    parser.add_argument(
        "-e",
        "--end",
        action="store_true",
        default=False,
        help="end playback",
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
        fd = b.filedir.get_file_dir_entry(fid)
        if fd.is_audio_file():
            if argsd["loop"]:
                b.repeat_audio_file(fid)
            elif argsd["end"]:
                b.stop_audio_file(fid)
            else:
                b.play_audio_file(fid)
        else:
            print("File %s is not an audio file" % (argsd["file"]))
    else:
        print("File %s is not found on the PFx Brick" % (argsd["file"]))
    b.close()


if __name__ == "__main__":
    main()
