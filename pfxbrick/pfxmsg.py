#! /usr/bin/env python3

# PFx Brick message helpers

import hid
from pfxbrick.pfx import *

def usb_transaction(hdev, send):
    hdev.write(send)
    res = hdev.read(64)
    if res:
        if res[0] == send[0] | 0x80:
            return res
        else:
            print("Error reading valid response from PFx Brick")
    return 0

def cmd_get_icd_rev(hdev, silent=False):
    msg = [PFX_CMD_GET_ICD_REV, PFX_GET_ICD_BYTE0, PFX_GET_ICD_BYTE1, PFX_GET_ICD_BYTE2, int(silent)]
    return usb_transaction(hdev, msg)

def cmd_get_status(hdev):
    msg = [PFX_CMD_GET_STATUS, PFX_STATUS_BYTE0, PFX_STATUS_BYTE1, PFX_STATUS_BYTE2, PFX_STATUS_BYTE3, PFX_STATUS_BYTE4, PFX_STATUS_BYTE5, PFX_STATUS_BYTE6]
    return usb_transaction(hdev, msg)
        
def cmd_get_config(hdev):
    msg = [PFX_CMD_GET_CONFIG]        
    return usb_transaction(hdev, msg)

def cmd_get_name(hdev):
    msg = [PFX_CMD_GET_NAME]
    return usb_transaction(hdev, msg)
    
def cmd_set_name(hdev, name):
    msg = [PFX_CMD_SET_NAME]
    mb = bytes(name, "utf-8")
    for x in mb:
        msg.append(int(x))
    return usb_transaction(hdev, msg)

def cmd_get_event_action(hdev, evtID, ch):
    msg = [PFX_CMD_GET_EVENT_ACTION, evtID, ch]
    return usb_transaction(hdev, msg)


