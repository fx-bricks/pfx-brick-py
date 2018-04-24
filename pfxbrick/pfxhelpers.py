#! /usr/bin/env python3

# PFx Brick data helpers

from pfx import *

def set_with_bit(byte, mask):
    if (byte & mask) == mask:
        return True
    else:
        return False


def get_status_str(x):
    s = ''
    if x in status_dict:
        s = status_dict[x]
    return s


def get_error_str(x):
    s = 'None'
    if x in err_dict:
        s = err_dict[x]
    return s
    
def uint16_tostr(msb, lsb):
    res = "".join("{:02X}".format(x) for x in [msb, lsb])
    return res

def uint32_tostr(msb, b1, b2, lsb):
    res = "".join("{:02X}".format(x) for x in [msb, b1, b2, lsb])
    return res

