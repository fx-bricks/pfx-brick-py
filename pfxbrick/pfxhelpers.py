#! /usr/bin/env python3

# PFx Brick data helpers

import pfxbrick.pfxdict as pd


def set_with_bit(byte, mask):
    if (byte & mask) == mask:
        return True
    else:
        return False


def get_status_str(x):
    s = ''
    if x in pd.status_dict:
        s = pd.status_dict[x]
    return s


def get_error_str(x):
    s = 'None'
    if x in pd.err_dict:
        s = pd.err_dict[x]
    return s

def uint16_toint(bytes):
    res = (int(bytes[0] & 0xFF) << 8) | (int(bytes[1]) & 0xFF)
    return res

def uint32_toint(bytes):
    res = (int(bytes[0] & 0xFF) << 24) | (int(bytes[1] & 0xFF) << 16) | (int(bytes[2] & 0xFF) << 8) | (int(bytes[3]) & 0xFF)
    return res
    
def uint16_tostr(msb, lsb):
    res = "".join("{:02X}".format(x) for x in [msb, lsb])
    return res

def uint32_tostr(msb, b1, b2, lsb):
    res = "".join("{:02X}".format(x) for x in [msb, b1, b2, lsb])
    return res

def uint16_tover(msb, lsb):
    res = '%02X.%02X' % (msb, lsb)
    return res
    
def motor_ch_str(x):
    s = []
    if x & EVT_MOTOR_OUTPUT_MASK:
        s.append('Motor Ch ')
        if x & EVT_MOTOR_OUTPUT_A:
            s.append('A ')
        if x & EVT_MOTOR_OUTPUT_B:
            s.append('B ')
        if x & EVT_MOTOR_OUTPUT_C:
            s.append('C ')
        if x & EVT_MOTOR_OUTPUT_D:
            s.append('D ')
    s = ''.join(s)
    return s

def light_ch_str(x):
    s = []
    if x:
        s.append('Ch')
        for i in range(8):
            m = 1 << i
            if (x & m):
                s.append(str(i+1))
    else:
        s.append('None')
    s = ' '.join(s)
    return s

def ch_to_mask(ch):
    mask = 0
    for c in ch:
        if c < 1 or c > 8:
            print("Channel out of range")
        else:
            mask = mask | (1 << (c-1))
    return mask
