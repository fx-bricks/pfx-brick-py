#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


def main():
    if len(argv) < 2 or "-h" in argv:
        print("Usage: pfxplay file")
        print("  where <file> is file ID or filename of audio file to playback")
        exit()
    b = PFxBrick()
    b.open()
    r = b.open()
    if not r:
        exit()
    b.refresh_file_dir()
    f = str(argv[1])
    if f.isnumeric():
        f = int(argv[1])
    fid = b.file_id_from_str_or_int(f)
    if fid < 0xFF:
        fd = b.filedir.get_file_dir_entry(fid)
        if fd.is_audio_file():
            b.play_audio_file(fid)
        else:
            print("File %s is not an audio file" % (argv[1]))
    else:
        print("File %s is not found on the PFx Brick" % (argv[1]))
    b.close()


if __name__ == "__main__":
    main()
