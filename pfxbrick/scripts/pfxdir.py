#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


def main():
    if "-h" in argv:
        print("Usage: pfxdir -h")
        print("  Show the PFx Brick file system directory")
        exit()

    b = PFxBrick()
    r = b.open()
    if not r:
        exit()
    b.refresh_file_dir()
    print(b.filedir)
    b.close()


if __name__ == "__main__":
    main()
