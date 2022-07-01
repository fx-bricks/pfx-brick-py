#! /usr/bin/env python3
import math
from sys import argv

from pfxbrick import *

RNOM = 10000
RDIV = 10000
TNOM = 25
BC = 3625

if __name__ == "__main__":
    b = PFxBrick()
    b.open()
    r = b.open()
    if not r:
        exit()

    msg = [0x78]
    res = b.send_raw_icd_command(msg)
    i = 1
    for ch in range(5):
        print(
            "State: %4X  Idx : %d"
            % (uint16_toint(res[i : i + 2]), uint16_toint(res[i + 2 : i + 4]))
        )
        print(
            "Count: %4X  Prev: %4X"
            % (uint16_toint(res[i + 4 : i + 6]), uint16_toint(res[i + 6 : i + 8]))
        )
        i += 8
    adc = uint16_toint(res[i : i + 2])
    print("ADC samp: %4X" % (adc))
    print("ADC2CON1: %4X" % (uint16_toint(res[i + 2 : i + 4])))

    rt = 1023 / adc - 1
    rt = RDIV / rt
    st = rt / RNOM
    st = math.log(st) / BC
    st = st + 1 / (TNOM + 273.15)
    st = 1.0 / st - 273.15
    print("Temp: %.1f ºC" % (st))
    b.close()
