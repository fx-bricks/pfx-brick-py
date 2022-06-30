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

import zlib

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


def pprint_bytes(x, address=None):
    def append_ascii(x, a, b):
        s = []
        for i in range(a, b):
            if i < len(x):
                ch = "." if x[i] > 127 else x[i]
                ch = "." if x[i] < 32 else x[i]
                s.append("%c" % (ch))
        return "".join(s)

    s = []
    if address is not None:
        if isinstance(address, str):
            a = int(address, 16)
        else:
            a = address
        ads = "%06X " % (a)
    else:
        ads = ""
    s.append("%s " % (ads))
    for i, b in enumerate(x):
        s.append("%02X " % (b))
        if (i + 1) % 8 == 0 and i > 0:
            s.append(" ")
        if (i + 1) % 16 == 0 and i > 0:
            s.append(" ")
            s.extend(append_ascii(x, i - 15, i + 1))
            if address is not None:
                a += 16
                ads = "%06X " % (a)
            else:
                ads = ""
            s.append("\n")
            s.append("%s " % (ads))
    nb = len(x) % 16
    if nb:
        for i in range(16 - nb + 1):
            s.append("   ")
        s.extend(append_ascii(x, len(x) - nb, len(x) + 1))
    else:
        s.pop()
    print("".join(s))


def listify(x):
    if isinstance(x, list):
        return x
    return [x]


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


def uint16_to_bytes(v):
    x = []
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


def ver_to_bytes(ver):
    major, minor = 0, 0
    vs = ver.split(".")
    major = int(vs[0]) & 0x0F
    vm = "%2s" % (vs[1])
    minor = (int(vm[0]) & 0x0F) << 4
    minor |= int(vm[1]) & 0x0F
    return major, minor


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


def motor_mask_to_script_str(x):
    s = []
    s.append("[")
    if x & EVT_MOTOR_OUTPUT_A:
        s.append("A, ")
    if x & EVT_MOTOR_OUTPUT_B:
        s.append("B, ")
    if x & EVT_MOTOR_OUTPUT_C:
        s.append("C, ")
    if x & EVT_MOTOR_OUTPUT_D:
        s.append("D ")
    s = "".join(s)
    s = s.rstrip().rstrip(",")
    s = s + "]"
    return s


def lightch_mask_to_script_str(x):
    s = []
    s.append("[")
    for i in range(8):
        if x & (1 << i):
            s.append("%d, " % (i + 1))
    s = "".join(s)
    s = s.rstrip().rstrip(",")
    s = s + "]"
    return s


IR_MASK_SPEED = 0x01
IR_MASK_JOY = 0x02
IR_MASK_LEFT = 0x04
IR_MASK_RIGHT = 0x08
IR_MASK_BUTTON = 0x10
IR_MASK_UP = 0x20
IR_MASK_DOWN = 0x40


def ir_mask_to_event_id(x):
    if x == (IR_MASK_SPEED | IR_MASK_BUTTON):
        return EVT_8879_TWO_BUTTONS
    elif x == (IR_MASK_SPEED | IR_MASK_LEFT | IR_MASK_BUTTON):
        return EVT_8879_LEFT_BUTTON
    elif x == (IR_MASK_SPEED | IR_MASK_RIGHT | IR_MASK_BUTTON):
        return EVT_8879_RIGHT_BUTTON
    elif x == (IR_MASK_SPEED | IR_MASK_LEFT | IR_MASK_UP):
        return EVT_8879_LEFT_INC
    elif x == (IR_MASK_SPEED | IR_MASK_LEFT | IR_MASK_DOWN):
        return EVT_8879_LEFT_DEC
    elif x == (IR_MASK_SPEED | IR_MASK_RIGHT | IR_MASK_UP):
        return EVT_8879_RIGHT_INC
    elif x == (IR_MASK_SPEED | IR_MASK_RIGHT | IR_MASK_DOWN):
        return EVT_8879_RIGHT_DEC
    elif x == (IR_MASK_JOY | IR_MASK_LEFT | IR_MASK_UP):
        return EVT_8885_LEFT_FWD
    elif x == (IR_MASK_JOY | IR_MASK_LEFT | IR_MASK_DOWN):
        return EVT_8885_LEFT_REV
    elif x == (IR_MASK_JOY | IR_MASK_RIGHT | IR_MASK_UP):
        return EVT_8885_RIGHT_FWD
    elif x == (IR_MASK_JOY | IR_MASK_RIGHT | IR_MASK_DOWN):
        return EVT_8885_RIGHT_REV
    elif x == (IR_MASK_JOY | IR_MASK_LEFT):
        return EVT_8885_LEFT_CTROFF
    elif x == (IR_MASK_JOY | IR_MASK_RIGHT):
        return EVT_8885_RIGHT_CTROFF
    return 0


def script_ir_mask_to_address(x):
    """Converts IR mask specification from a script to a event LUT address."""
    mask = 0
    add = 0
    xs = x.split()
    for i, e in enumerate(xs):
        if "speed" in e:
            mask |= IR_MASK_SPEED
        elif "joy" in e:
            mask |= IR_MASK_JOY
        elif "left" in e:
            mask |= IR_MASK_LEFT
        elif "right" in e:
            mask |= IR_MASK_RIGHT
        elif "up" in e:
            mask |= IR_MASK_UP
        elif "down" in e:
            mask |= IR_MASK_DOWN
        elif "button" in e:
            mask |= IR_MASK_BUTTON
        elif "ch" in e:
            if (i + 1) < len(xs):
                add += int(xs[i + 1]) - 1
    add += ir_mask_to_event_id(mask)
    return add


def script_ir_mask_to_evtch(x):
    return address_to_evtch(script_ir_mask_to_address(x))


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


def get_file_crc32(fn):
    """Returns the CRC32 over the bytes of specified file on the local file system."""
    with open(fn, "rb") as fp:
        fb = fp.read()
    return zlib.crc32(fb) & 0xFFFFFFFF


def bounds_from_notchcount(count):
    """Returns the boundaries between a desired number of power notch levels.

    The power range between 0 to 255 can be subdivided into a desired number
    of notch levels (up to 8 levels).  For example, 2 notch levels would
    return a list with one bound of 128.  4 levels would return a list of
    [64, 128, 192], etc.
    """
    bounds = [round((x + 1) / count * 255) for x in range(count - 1)]
    return bounds


def notch_ranges_from_bounds(bounds):
    """Returns a list of tuples containing the min, mid, max power levels
    based on a list of notch boundary values.
    """
    ranges = []
    count = len(bounds) + 1
    for i in range(count):
        if i == 0:
            mid_speed = bounds[0] / 2
            lower, upper = 0, bounds[0]
        elif i == count - 1:
            mid_speed = bounds[i - 1] + (255 - bounds[i - 1]) / 2
            lower, upper = bounds[i - 1], 255
        else:
            mid_speed = bounds[i - 1] + (bounds[i] - bounds[i - 1]) / 2
            lower, upper = bounds[i - 1], bounds[i]
        ranges.append((lower, round(mid_speed), upper))
    return ranges


def notch_from_speed(speed, bounds):
    """Returns the notch index for a given speed value within a specified list of bounds."""
    ranges = notch_ranges_from_bounds(bounds)
    for i, r in enumerate(ranges):
        if speed >= r[0] and speed < r[2]:
            return i


def safe_unicode_str(text):
    """Trys to decode a byte stream as UTF-8 with a safe fallback to raw ascii."""
    try:
        sn = bytes(text).decode("utf-8")
    except UnicodeDecodeError:
        sn = []
        for b in text:
            if b >= 0x20 and b <= 127:
                sn.append(str(b))
        sn = "".join(sn)
    sn = sn.rstrip("\0")
    return sn


def is_version_less_than(ver, other):
    """ "Determines if a version number is less than another version number string"""
    sv = ver.split(".")
    ov = other.split(".")
    sv_major = int(sv[0])
    if len(sv) > 1:
        sv_minor = int(sv[1])
    ov_major = int(ov[0])
    if len(ov) > 1:
        ov_minor = int(ov[1])
    if sv_major < ov_major:
        return True
    if sv_major == ov_major:
        if sv_minor < ov_minor:
            return True
    return False


def pprint_diff(x, y, address=None):
    from rich import print

    def append_ascii(x, a, b):
        s = []
        for i in range(a, b):
            if i < len(x):
                ch = "." if x[i] > 127 else x[i]
                ch = "." if x[i] < 32 else x[i]
                s.append("%c" % (ch))
        return "".join(s)

    s = []
    if address is not None:
        if isinstance(address, str):
            a = int(address, 16)
        else:
            a = address
        ads = "%06X " % (a)
    else:
        ads = ""
    s.append("%s " % (ads))
    for i, (b, by) in enumerate(zip(x, y)):
        if b == by:
            s.append("[bold black]%02X|%02X[/] " % (b, by))
        else:
            s.append("[bold red]%02X|%02X[/] " % (b, by))

        if (i + 1) % 8 == 0 and i > 0:
            s.append(" ")
        if (i + 1) % 16 == 0 and i > 0:
            s.append(" ")
            s.extend(append_ascii(x, i - 15, i + 1))
            if address is not None:
                a += 16
                ads = "%06X " % (a)
            else:
                ads = ""
            s.append("\n")
            s.append("%s " % (ads))
    nb = len(x) % 16
    if nb:
        for i in range(16 - nb + 1):
            s.append("   ")
        s.extend(append_ascii(x, len(x) - nb, len(x) + 1))
    else:
        s.pop()
    print("".join(s))


def get_one_pfxbrick(serial_no=None):
    """Returns only one instance of a PFx Brick if one or more are connected.
    If only one is connected, then a PFxBrick object is returned for it.
    If more than one is connected, a warning to select using serial number is shown.
    """
    from pfxbrick.pfxbrick import PFxBrick, find_bricks

    b = None
    bricks = find_bricks()
    if len(bricks) > 1 and serial_no is None:
        print(
            "More than one PFx Brick is attached.  Please specify brick serial number with the -s argument."
        )
        print("Currently attached PFx Bricks:")
        for brick in bricks:
            b = PFxBrick(brick)
            r = b.open()
            b.get_status()
            name = b.get_name()
            print(
                "[light_slate_blue]%-4s[/] [bold cyan]%-24s[/] Serial no: [bold cyan]%-9s[/] Name: [bold yellow]%s[/]"
                % (b.product_id, b.product_desc, b.serial_no, name)
            )
            b.close()
        exit()
    if serial_no is not None and len(bricks) > 1:
        b = PFxBrick(serial_no=serial_no)
    else:
        b = PFxBrick()
    return b


def shorter_str(s):
    """Replaces words in a string that are found in the helper dictionaries
    in pfxdict.py  with shorter versions for a more compact description."""
    tokens = [
        "Increase Inc",
        "Decrease Dec",
        "Emergency Emcy",
        "Oscillate Osc",
        "Direction Dir",
        "Brightness Bright",
        "positive +",
        "negative -",
        "Modulated Mod",
        "Alternating Alt",
        "Style ",
        "Left L",
        "Right R",
        "Joystick Joy",
        "Event Evt",
        "Centre Ctr",
        "Flashers Flash",
    ]
    for t in tokens:
        ts = t.split()
        if len(ts) < 2:
            s = s.replace(ts[0], "")
        else:
            s = s.replace(ts[0], ts[1])
    return s
