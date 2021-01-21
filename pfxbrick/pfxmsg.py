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
# PFx Brick message helpers


import hid
import platform
from pfxbrick import *


def usb_transaction(hdev, msg):
    # enforce non-numbered report pre-pending and report length
    # This ensures consistent operation on Windows, macOS, etc.
    # since Windows insists on matched report length/buffer size
    # and for all non-numbered reports to start with 0
    msglen = len(msg)
    buf = [0]
    buf.extend(msg)
    buf.extend([0] * (64 - msglen))
    hdev.write(buf)
    res = hdev.read(64)
    if res:
        if res[0] == msg[0] | 0x80:
            return res
        else:
            raise InvalidResponseException()
    return 0


def msg_transaction(hdev, msg):
    if isinstance(hdev, hid.device):
        return usb_transaction(hdev, msg)
    else:
        return hdev.ble_transaction(msg)


def cmd_get_icd_rev(hdev, silent=False):
    msg = [
        PFX_CMD_GET_ICD_REV,
        PFX_GET_ICD_BYTE0,
        PFX_GET_ICD_BYTE1,
        PFX_GET_ICD_BYTE2,
        int(silent),
    ]
    return msg_transaction(hdev, msg)


def cmd_get_status(hdev):
    msg = [
        PFX_CMD_GET_STATUS,
        PFX_STATUS_BYTE0,
        PFX_STATUS_BYTE1,
        PFX_STATUS_BYTE2,
        PFX_STATUS_BYTE3,
        PFX_STATUS_BYTE4,
        PFX_STATUS_BYTE5,
        PFX_STATUS_BYTE6,
    ]
    return msg_transaction(hdev, msg)


def cmd_get_config(hdev):
    msg = [PFX_CMD_GET_CONFIG]
    return msg_transaction(hdev, msg)


def cmd_set_config(hdev, cfgbytes):
    msg = [PFX_CMD_SET_CONFIG]
    msg.extend(cfgbytes)
    return msg_transaction(hdev, msg)


def cmd_get_name(hdev):
    msg = [PFX_CMD_GET_NAME]
    return msg_transaction(hdev, msg)


def cmd_set_name(hdev, name):
    msg = [PFX_CMD_SET_NAME]
    mb = bytes(name, "utf-8")
    for x in mb:
        msg.append(x)
    for i in range(PFX_NAME_MAX - len(mb)):
        msg.append(0)
    return msg_transaction(hdev, msg)


def cmd_get_event_action(hdev, evtID, ch):
    msg = [PFX_CMD_GET_EVENT_ACTION, evtID, ch]
    return msg_transaction(hdev, msg)


def cmd_set_event_action(hdev, evtID, ch, action):
    msg = [PFX_CMD_SET_EVENT_ACTION, evtID, ch]
    msg.extend(action)
    return msg_transaction(hdev, msg)


def cmd_test_action(hdev, action):
    msg = [PFX_CMD_TEST_ACTION]
    msg.extend(action)
    return msg_transaction(hdev, msg)


def cmd_get_dir_entry(hdev, idx):
    msg = [PFX_CMD_FILE_DIR, PFX_DIR_REQ_GET_DIR_ENTRY_IDX, idx]
    return msg_transaction(hdev, msg)


def cmd_get_num_files(hdev):
    msg = [PFX_CMD_FILE_DIR, PFX_DIR_REQ_GET_FILE_COUNT]
    return msg_transaction(hdev, msg)


def cmd_get_free_space(hdev):
    msg = [PFX_CMD_FILE_DIR, PFX_DIR_REQ_GET_FREE_SPACE]
    return msg_transaction(hdev, msg)


def cmd_set_factory_defaults(hdev):
    msg = [
        PFX_CMD_SET_FACTORY_DEFAULTS,
        PFX_RESET_BYTE0,
        PFX_RESET_BYTE1,
        PFX_RESET_BYTE2,
        PFX_RESET_BYTE3,
        PFX_RESET_BYTE4,
        PFX_RESET_BYTE5,
        PFX_RESET_BYTE6,
    ]
    return msg_transaction(hdev, msg)


def cmd_set_notifications(hdev, flags):
    msg = [PFX_CMD_SET_NOTIFICATIONS, flags]
    return msg_transaction(hdev, msg)


def cmd_run_script(hdev, fileid):
    msg = [PFX_CMD_RUN_SCRIPT, fileid]
    return msg_transaction(hdev, msg)


def cmd_file_dir(hdev, req, params=None):
    msg = [PFX_CMD_FILE_DIR, req]
    if params is not None:
        msg.extend(params)
    return msg_transaction(hdev, msg)


def cmd_get_current_state(hdev):
    msg = [PFX_CMD_GET_CURRENT_STATE]
    return msg_transaction(hdev, msg)
