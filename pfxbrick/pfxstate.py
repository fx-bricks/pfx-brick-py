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
# PFx Brick internal state helpers

from pfxbrick import *


class PFxMotorState:
    def __init__(self):
        self.dir = "Forward"
        self.target_speed = 0
        self.current_speed = 0
        self.pwm_speed = 0

    def __str__(self):
        return "Dir: %7s Target speed: 0x%02X  Current: 0x%02X  PWM: 0x%02X" % (
            self.dir,
            self.target_speed,
            self.current_speed,
            self.pwm_speed,
        )

    def from_bytes(self, msg):
        self.dir = "Reverse" if (msg[0] & 0x01) else "Forward"
        self.target_speed = msg[1]
        self.current_speed = msg[2]
        self.pwm_speed = msg[3]


class PFxLightState:
    def __init__(self):
        self.active = False
        self.target_level = 0
        self.current_level = 0

    def __str__(self):
        return "Active: %5s Target level: 0x%02X  Current level: 0x%02X" % (
            self.active,
            self.target_level,
            self.current_level,
        )


class PFxAudioChannel:
    def __init__(self):
        self.mode = 0
        self.file_id = PFX_FILE_INVALID_ID

    def __str__(self):
        return "Mode: %d Current file: %3d" % (self.mode, self.file_id)


class PFxBTState:
    def __init__(self):
        self.sleep = 0
        self.state = 0
        self.flags = 0
        self.error = 0
        self.features = 0
        self.services = 0
        self.auth = 0
        self.tx_count = 0
        self.rx_count = 0
        self.msg_len = 0
        self.msg_prefix = []

    def __str__(self):
        s = []
        s.append(
            "Sleep: %d State: 0x%04X  Flags: 0x%04X  Err: 0x%04X"
            % (self.sleep, self.state, self.flags, self.error)
        )
        s.append(
            "BLE Feautures: 0x%04X  Services: 0x%04X  Auth: 0x%04X"
            % (self.features, self.services, self.auth)
        )
        s.append("Tx Count: %d  Rx Count: %d" % (self.tx_count, self.rx_count))
        mb = " ".join(["0x%02X" % (x) for x in self.msg_prefix])
        s.append("Last message len: %d <%s>" % (self.msg_len, mb))
        return "\n".join(s)

    def from_bytes(self, msg):
        msg = msg[1:]
        self.sleep = msg[1]
        self.state = uint16_toint(msg[2:4])
        self.flags = uint16_toint(msg[4:6])
        self.error = uint16_toint(msg[6:8])
        self.features = uint16_toint(msg[8:10])
        self.services = uint16_toint(msg[10:12])
        self.auth = uint16_toint(msg[12:14])
        self.tx_count = uint16_toint(msg[14:16])
        self.rx_count = uint16_toint(msg[16:18])
        self.msg_len = msg[19]
        self.msg_prefix = msg[20:28]


class PFxFSState:
    def __init__(self):
        self.file_count = 0
        self.open_files = 0
        self.task_state = 0
        self.flags = 0
        self.erase_sector = 0
        self.init_timemout = 0
        self.auto_sync_dir = 0
        self.auto_sync_map = 0
        self.sector_capacity = 0
        self.free_sectors = 0
        self.empty_sectors = 0

    def __str__(self):
        s = []
        s.append(
            "State: 0x%02X  Flags: 0x%02X  Files: %d  Open: %d"
            % (self.task_state, self.flags, self.file_count, self.open_files)
        )
        s.append(
            "Erase: 0x%04X  InitTime: 0x%04X  SyncDir: 0x%04X  SyncMap: 0x%04X"
            % (
                self.erase_sector,
                self.init_timemout,
                self.auto_sync_dir,
                self.auto_sync_map,
            )
        )
        s.append(
            "Sector Capacity: 0x%04X  Free: 0x%04X  Empty: 0x%04X"
            % (self.sector_capacity, self.free_sectors, self.empty_sectors)
        )
        return "\n".join(s)

    def from_bytes(self, msg):
        self.file_count = msg[1]
        self.open_files = msg[18]
        self.task_state = msg[2]
        self.flags = msg[3]
        self.erase_sector = uint16_toint(msg[4:6])
        self.init_timemout = uint16_toint(msg[6:8])
        self.auto_sync_dir = uint16_toint(msg[8:10])
        self.auto_sync_map = uint16_toint(msg[10:12])
        self.sector_capacity = uint16_toint(msg[12:14])
        self.free_sectors = uint16_toint(msg[14:16])
        self.empty_sectors = uint16_toint(msg[16:18])


class PFxState:
    """
    PFx Brick internal data state container class.

    This class is used to store internal state data obtained with the `PFX_CMD_GET_CURRENT_STATE`
    ICD command.  This internal state data can be useful for monitoring, debugging, and
    for building apps which can use this data for enhanced feedback of the PFx Brick runtime
    state and behaviour.

    Attributes:
        brightness (:obj:`int`): current global brightness value

        volume (:obj:`int`): current audio volume level

        millisec_count (:obj:`int`): PFx Brick millisecond counter value

        slow_count (:obj:`int`): PFx Brick 1 second counter value

        status_latch1 (:obj:`int`): PFx Brick status latch 1 bit flag state

        status_latch2 (:obj:`int`): PFx Brick status latch 2 bit flag state

        audio_peak (:obj:`int`): current audio peak level based on current playback

        audio_notch (:obj:`int`): current motor notch value for indexed audio playback

        fs_state (:obj:`int`): PFx Brick file system state flags

        script_state (:obj:`int`): PFx Brick script engine state

        script_line (:obj:`int`): current running script line pointer

        motors ([:obj:`PFxMotorState`]): motor channel runtime state container class

        lights ([:obj:`PFxLightState`]): light channel runtime state container class

        audio_ch ([:obj:`PFxAudioChannel`]): audio channel runtime state container class

    """

    def __init__(self):
        self.brightness = 0
        self.volume = 0
        self.motors = [PFxMotorState() for ch in range(PFX_MOTOR_CHANNELS)]
        self.lights = [PFxLightState() for ch in range(PFX_LIGHT_CHANNELS)]
        self.audio_ch = [PFxAudioChannel() for ch in range(PFX_AUDIO_CHANNELS)]
        self.lightmask = 0
        self.millisec_count = 0
        self.slow_count = 0
        self.status_latch1 = 0
        self.status_latch2 = 0
        self.audio_peak = 0
        self.audio_notch = 0
        self.fs_state = 0
        self.script_state = 0
        self.script_line = 0
        self.motor_ptr = 0
        self.motor_pwm_ptr = 0
        self.motor_rate_ptr = 0
        self.trig_change_dir_state = 0
        self.trig_set_off_state = 0
        self.trig_rapid_accel_state = 0
        self.trig_rapid_decel_state = 0
        self.trig_brake_state = 0
        self.filesys = PFxFSState()
        self.bt = PFxBTState()

    def from_bytes(self, msg):
        """
        Converts the message string bytes read from the PFx Brick into
        the corresponding data members of this class.
        """
        self.brightness = msg[1]
        self.volume = msg[2]
        for ch, idx in zip(self.motors, [3, 7]):
            ch.from_bytes(msg[idx : idx + 4])
        self.motor_ptr = msg[11]
        self.motor_pwm_ptr = msg[12]
        self.motor_rate_ptr = msg[13]
        self.trig_change_dir_state = msg[14]
        self.trig_set_off_state = msg[15]
        self.trig_rapid_accel_state = msg[16]
        self.trig_rapid_decel_state = msg[17]
        self.trig_brake_state = msg[18]
        self.lightmask = msg[19]
        for i, ch in enumerate(self.lights):
            ch.target_level = msg[21 + i]
            ch.current_level = msg[33 + i]
            if i > 7:
                mask = 1 << (i - 8)
                ch.active = True if (msg[20] & mask) else False
            else:
                mask = 1 << i
                ch.active = True if (msg[19] & mask) else False
        for ch, idx in zip(self.audio_ch, [45, 47, 49, 51]):
            ch.mode = msg[idx]
            ch.file_id = msg[idx + 1]
        self.millisec_count = uint16_toint(msg[53:55])
        self.slow_count = uint16_toint(msg[55:57])
        self.status_latch1 = msg[57]
        self.status_latch2 = msg[58]
        self.audio_peak = msg[60]
        self.audio_notch = msg[61]
        self.fs_state = msg[59]
        self.script_state = msg[62]
        self.script_line = msg[63]

    def __str__(self):
        s = []
        s.append("Brightness: %3d  Volume: %3d" % (self.brightness, self.volume))
        s.append(
            "Slow count: %4X  Millisec count: %4X"
            % (self.slow_count, self.millisec_count)
        )
        s.append(
            "File system: %2X Script exec: %2X Script line: %3d"
            % (self.fs_state, self.script_state, self.script_line)
        )
        s.append(
            "Status 1: %2X  Status 2: %2X" % (self.status_latch1, self.status_latch2)
        )
        for i, ch in enumerate(self.motors):
            s.append("Motor Ch %d : %s" % (i + 1, str(ch)))
        for i, ch in enumerate(self.lights):
            s.append("Light Ch %2d : %s" % (i + 1, str(ch)))
        for i, ch in enumerate(self.audio_ch):
            s.append("Audio Ch %d : %s" % (i + 1, str(ch)))
        s.append(
            "Audio Peak: %3d  Audio notch: %d" % (self.audio_peak, self.audio_notch)
        )
        return "\n".join(s)
