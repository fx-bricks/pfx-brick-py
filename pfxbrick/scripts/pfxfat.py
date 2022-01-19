#! /usr/bin/env python3
from sys import argv

from rich import print
from pfxbrick import *


def main():
    if len(argv) > 1 or "-h" in argv:
        print("Usage: pfxfat -h")
        print("  Shows the PFx Brick file allocation table")
        exit()

    b = PFxBrick()
    b.open()
    r = b.open()
    if not r:
        exit()
    rb = flash_read(b, 0xFFC000, 8192)
    b.close()
    x = []
    for i in range(0, len(rb) - 1, 2):
        x.append(rb[i + 1])
        x.append(rb[i])

    a = 0
    s = []
    ads = "[bold white]%06X[/] " % (a)
    s.append("%s " % (ads))
    for i, b in enumerate(x):
        if (i % 2) == 0:
            if x[i] == 0xFF and x[i + 1] == 0xFF:
                cs = "[bold red]"
            elif x[i] == 0xFF and x[i + 1] == 0xFE:
                cs = "[bold magenta]"
            elif x[i] == 0xFF and x[i + 1] == 0xF3:
                cs = "[green]"
            elif x[i] == 0xFF and x[i + 1] == 0xF1:
                cs = "[bold orange3]"
            elif x[i] == 0xFF and x[i + 1] == 0xF7:
                cs = "[bold yellow]"
            elif i > 1:
                if abs(int(x[i + 1]) - int(x[i - 1])) > 1:
                    cs = "[bold cyan]"
                else:
                    cs = "[bold white]"
            else:
                cs = "[bold white]"
        s.append("%s%02X[/]" % (cs, b))
        if (i + 1) % 2 == 0 and i > 0:
            s.append(" ")
        if (i + 1) % 16 == 0 and i > 0:
            s.append(" ")
        if (i + 1) % 32 == 0 and i > 0:
            a += 16
            ads = "[bold white]%06X[/] " % (a)
            s.append("\n")
            s.append("%s " % (ads))
    nb = len(x) % 32
    if nb:
        for i in range(32 - nb + 1):
            s.append("   ")
    else:
        s.pop()
    print("".join(s))


if __name__ == "__main__":
    main()
