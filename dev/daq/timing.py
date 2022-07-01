#! /usr/bin/env python3
import math
import time
from sys import argv

from pfxbrick import *

RNOM = 10000
RDIV = 10000
TNOM = 25
BC = 3625

last_idx = [0, 0, 0, 0]


def print_timings(idx, times):
    global last_idx
    # ts = sorted(zip(idx, times))
    ts = [[i, j] for i, j in zip(idx, times)]
    curr_idx = [ts[0][0], ts[1][0], ts[2][0], ts[3][0]]
    # print(curr_idx)
    # for t in ts:
    #     print("%d : %d" % (t[0], t[1]))
    # print("%d %d" % (ts[1][1], ts[0][1]))
    # print("%d %d" % (ts[3][1], ts[2][1]))
    # print(curr_idx)
    # is_ready = True
    # for c, l in zip(curr_idx, last_idx):
    #     if abs(c - l) < 2:
    #         is_ready = False
    # if is_ready:
    # last_idx = curr_idx.copy()
    i1 = ts[1][0] - ts[0][0]
    i2 = ts[3][0] - ts[2][0]
    d1 = ts[1][1] - ts[0][1]
    d2 = ts[3][1] - ts[2][1]
    v1 = 0.128 / (d1 / 1000)
    v2 = 0.128 / (d2 / 1000)
    k1 = v1 * 3.6 * 40
    k2 = v2 * 3.6 * 40
    if abs(i1) == 1 and abs(i2) == 1:
        print("diff1: %d ms  %.3f m/s  %.1f kph (scale)" % (d1, v1, k1))
        print("diff2: %d ms  %.3f m/s  %.1f kph (scale)" % (d2, v2, k2))


def get_timings(b):
    msg = [0x78]
    res = b.send_raw_icd_command(msg)
    i = 1
    times = []
    idx = []
    for ch in range(4):
        idx.append(uint16_toint(res[i + 2 : i + 4]))
        times.append(uint16_toint(res[i + 4 : i + 6]))
        print(
            "State: %4X  Idx : %d"
            % (uint16_toint(res[i : i + 2]), uint16_toint(res[i + 2 : i + 4]))
        )
        print(
            "Count: %4X  Prev: %4X"
            % (uint16_toint(res[i + 4 : i + 6]), uint16_toint(res[i + 6 : i + 8]))
        )
        i += 8
    # print(times)
    return idx, times


if __name__ == "__main__":
    b = PFxBrick()
    b.open()
    r = b.open()
    if not r:
        exit()

    while True:
        idx, times = get_timings(b)
        print_timings(idx, times)
        time.sleep(0.5)

    b.close()
