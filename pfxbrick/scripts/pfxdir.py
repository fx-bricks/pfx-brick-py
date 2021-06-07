#! /usr/bin/env python3
from sys import argv

from pfxbrick import *


if __name__ == "__main__":
    b = PFxBrick()
    r = b.open()
    if not r:
        exit()
    b.refresh_file_dir()
    print(b.filedir)
    b.close()
