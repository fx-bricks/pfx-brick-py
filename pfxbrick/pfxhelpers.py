#! /usr/bin/env python3
#
# Copyright (C) 2018  Fx Bricks Inc.
# This file is part of the pfxbrick python module.
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# PFx Brick data helpers

import pfxbrick.pfxdict as pd
from pfxbrick.pfx import *


def set_with_bit(byte, mask):
    if (byte & mask) == mask:
        return True
    else:
        return False


def get_status_str(x):
    s = ""
    if x in pd.status_dict:
        s = pd.status_dict[x]
    return s


def get_error_str(x):
    s = "None"
    if x in pd.err_dict:
        s = pd.err_dict[x]
    return s


def uint16_toint(bytes):
    res = (int(bytes[0] & 0xFF) << 8) | (int(bytes[1]) & 0xFF)
    return res


def uint32_to_bytes(v):
    x = []
    x.append((v >> 24) & 0xFF)
    x.append((v >> 16) & 0xFF)
    x.append((v >> 8) & 0xFF)
    x.append(v & 0xFF)
    return x


def uint32_toint(bytes):
    res = (
        (int(bytes[0] & 0xFF) << 24)
        | (int(bytes[1] & 0xFF) << 16)
        | (int(bytes[2] & 0xFF) << 8)
        | (int(bytes[3]) & 0xFF)
    )
    return res


def uint16_tostr(msb, lsb):
    res = "".join("{:02X}".format(x) for x in [msb, lsb])
    return res


def uint32_tostr(msb, b1, b2, lsb):
    res = "".join("{:02X}".format(x) for x in [msb, b1, b2, lsb])
    return res


def uint16_tover(msb, lsb):
    res = "%02X.%02X" % (msb, lsb)
    return res


def int8_toint(val):
    if val & 0x80:
        return -((~val & 0x7F) + 1)
    return val & 0x7F


def motor_ch_str(x):
    s = []
    if x & EVT_MOTOR_OUTPUT_MASK:
        s.append("Motor Ch ")
        if x & EVT_MOTOR_OUTPUT_A:
            s.append("A ")
        if x & EVT_MOTOR_OUTPUT_B:
            s.append("B ")
        if x & EVT_MOTOR_OUTPUT_C:
            s.append("C ")
        if x & EVT_MOTOR_OUTPUT_D:
            s.append("D ")
    s = "".join(s)
    return s


def light_ch_str(x):
    s = []
    if x:
        s.append("Ch")
        for i in range(8):
            m = 1 << i
            if x & m:
                s.append(str(i + 1))
    else:
        s.append("None")
    s = " ".join(s)
    return s


def ch_to_mask(ch):
    mask = 0
    if isinstance(ch, list):
        channels = ch
    else:
        channels = [ch]
    for c in channels:
        if c < 1 or c > 8:
            print("Channel out of range")
        else:
            mask = mask | (1 << (c - 1))
    return mask


def address_to_evtch(address):
    evt = (address & EVT_EVENT_ID_MASK) >> 2
    ch = address & EVT_EVENT_CH_MASK
    return evt, ch


def evtch_to_address(evt, ch):
    address = ch & EVT_EVENT_CH_MASK
    address |= (evt << 2) & EVT_EVENT_ID_MASK
    return address


def period_param(period):
    x = float(period)
    if x < 0.250:
        return EVT_PERIOD_100MS
    elif x < 0.50:
        return EVT_PERIOD_250MS
    elif x < 0.75:
        return EVT_PERIOD_500MS
    elif x < 1.0:
        return EVT_PERIOD_750MS
    elif x < 1.25:
        return EVT_PERIOD_1S
    elif x < 1.50:
        return EVT_PERIOD_1_25S
    elif x < 1.75:
        return EVT_PERIOD_1_5S
    elif x < 2.0:
        return EVT_PERIOD_1_75S
    elif x < 2.5:
        return EVT_PERIOD_2S
    elif x < 3.0:
        return EVT_PERIOD_2_5S
    elif x < 4.0:
        return EVT_PERIOD_3S
    elif x < 5.0:
        return EVT_PERIOD_4S
    elif x < 8.0:
        return EVT_PERIOD_5S
    elif x < 10.0:
        return EVT_PERIOD_8S
    elif x < 20.0:
        return EVT_PERIOD_10S
    else:
        return EVT_PERIOD_20S


def period2_param(period):
    x = float(period)
    if x < 0.1:
        return EVT_PERIOD2_50MS
    elif x < 0.2:
        return EVT_PERIOD2_100MS
    elif x < 0.3:
        return EVT_PERIOD2_200MS
    elif x < 0.4:
        return EVT_PERIOD2_300MS
    elif x < 0.5:
        return EVT_PERIOD2_400MS
    elif x < 0.6:
        return EVT_PERIOD2_500MS
    elif x < 0.7:
        return EVT_PERIOD2_600MS
    elif x < 0.8:
        return EVT_PERIOD2_700MS
    elif x < 0.9:
        return EVT_PERIOD2_800MS
    elif x < 1.0:
        return EVT_PERIOD2_900MS
    elif x < 1.25:
        return EVT_PERIOD2_1S
    elif x < 1.5:
        return EVT_PERIOD2_1_25S
    elif x < 1.75:
        return EVT_PERIOD2_1_5S
    elif x < 2.0:
        return EVT_PERIOD2_1_75S
    elif x < 3.0:
        return EVT_PERIOD2_2S
    else:
        return EVT_PERIOD2_3S


def duty_cycle_param(duty_cycle):
    x = float(duty_cycle)
    if x < 0.02:
        return EVT_DUTYCY_1
    elif x < 0.05:
        return EVT_DUTYCY_2
    elif x < 0.1:
        return EVT_DUTYCY_5
    elif x < 0.15:
        return EVT_DUTYCY_10
    elif x < 0.2:
        return EVT_DUTYCY_15
    elif x < 0.25:
        return EVT_DUTYCY_20
    elif x < 0.3:
        return EVT_DUTYCY_25
    elif x < 0.4:
        return EVT_DUTYCY_30
    elif x < 0.5:
        return EVT_DUTYCY_40
    elif x < 0.6:
        return EVT_DUTYCY_50
    elif x < 0.7:
        return EVT_DUTYCY_60
    elif x < 0.75:
        return EVT_DUTYCY_70
    elif x < 0.8:
        return EVT_DUTYCY_75
    elif x < 0.85:
        return EVT_DUTYCY_80
    elif x < 0.9:
        return EVT_DUTYCY_85
    elif x < 0.95:
        return EVT_DUTYCY_90
    elif x < 0.98:
        return EVT_DUTYCY_95
    elif x < 0.99:
        return EVT_DUTYCY_98
    else:
        return EVT_DUTYCY_99


def duration_to_fixed_value(duration):
    x = float(duration)
    if x < 1.0:
        return EVT_SOUND_DUR_500MS
    elif x < 1.5:
        return EVT_SOUND_DUR_1S
    elif x < 2.0:
        return EVT_SOUND_DUR_1_5S
    elif x < 3.0:
        return EVT_SOUND_DUR_2S
    elif x < 4.0:
        return EVT_SOUND_DUR_3S
    elif x < 5.0:
        return EVT_SOUND_DUR_4S
    elif x < 10.0:
        return EVT_SOUND_DUR_5S
    elif x < 15.0:
        return EVT_SOUND_DUR_10S
    elif x < 20.0:
        return EVT_SOUND_DUR_15S
    elif x < 30.0:
        return EVT_SOUND_DUR_20S
    elif x < 45.0:
        return EVT_SOUND_DUR_30S
    elif x < 60.0:
        return EVT_SOUND_DUR_45S
    elif x < 90.0:
        return EVT_SOUND_DUR_60S
    elif x < 120.0:
        return EVT_SOUND_DUR_90S
    elif x < 300.0:
        return EVT_SOUND_DUR_2M
    else:
        return EVT_SOUND_DUR_5M


def printProgressBar(
    iteration, total, prefix="", suffix="", decimals=1, length=100, fill="█"
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end="\r")
    # Print New Line on Complete
    if iteration == total:
        print()
