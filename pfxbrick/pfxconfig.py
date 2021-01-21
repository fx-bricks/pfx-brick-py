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
# PFx Brick configuration data helpers

from pfxbrick import *
import pfxbrick.pfxdict as pd
from pfxbrick.pfxhelpers import set_with_bit


class PFxSettings:
    """
    General settings container class. A member of PFxConfig

    This class contains miscellaneous user preference settings such as
    power saving modes.

    Attributes:
        statusLED (:obj:`int`): status LED mode

        volumeBeep (:obj:`int`): volume beep mode

        autoPowerDown (:obj:`int`): auto power down mode

        lockoutMode (:obj:`int`): IR lockout activation mode

        irAutoOff (:obj:`int`): auto IR disable mode

        bleAutoOff (:obj:`int`): auto BLE disable mode

        bleMotorWhenDisconnect (:obj:`int`): behaviour of motors on BLE disconnect

        bleAdvertPower (:obj:`int`): BLE RF power during advertising

        bleSessionPower (:obj:`int`): BLE RF power during connected session

        notchCount (:obj:`int`): number of motor index speed notches

        notchBounds ([:obj:`int`]): list of monotonic increasing speed notch boundaries
    """

    def __init__(self):
        self.statusLED = 0
        self.volumeBeep = 0
        self.autoPowerDown = 0
        self.lockoutMode = 0
        self.irAutoOff = 0
        self.bleAutoOff = 0
        self.bleMotorWhenDisconnect = 0
        self.bleAdvertPower = 0
        self.bleSessionPower = 0
        self.notchCount = 0
        self.notchBounds = [0, 0, 0, 0, 0, 0, 0]

    def __str__(self):
        sb = []
        sb.append("Status LED            : %s" % (pd.status_led_dict[self.statusLED]))
        sb.append("Volume Beep           : %s" % (pd.volume_beep_dict[self.volumeBeep]))
        sb.append(
            "Auto Power Down       : %s" % (pd.power_save_dict[self.autoPowerDown])
        )
        sb.append("IR Lockout Mode       : %s" % (pd.lockout_dict[self.lockoutMode]))
        sb.append("IR Auto Off           : %s" % (pd.ir_off_dict[self.irAutoOff]))
        sb.append("BLE Auto Off          : %s" % (pd.ble_off_dict[self.bleAutoOff]))
        sb.append(
            "BLE Motor Disconnect  : %s"
            % (pd.ble_motor_dict[self.bleMotorWhenDisconnect])
        )
        sb.append("BLE Advert Power      : %s" % (self.bleAdvertPower))
        sb.append("BLE Session Power     : %s" % (self.bleSessionPower))
        sb.append("Motor sound notches   : %s" % (self.notchCount))
        mb = "".join("{:02X} ".format(x) for x in self.notchBounds)
        sb.append("Motor sound bounds    : %s" % (mb))
        s = "\n".join(sb)
        return s


class PFxMotor:
    """
    Motor settings container class.

    This class contains motor configuration data for one motor channel.

    Attributes:
        invert (:obj:`boolean`): invert the definition of forward/reverse

        torqueComp (:obj:`boolean`): activate low speed torque compensation with low frequency PWM

        tlgMode (:obj:`boolean`): enable LEGO® Power Functions compatible PWM mode

        accel (:obj:`int`): acceleration factor (0 - 15 max)

        decel (:obj:`int`): deceleration factor (0 - 15 max)

        vmin (:obj:`int`): speed curve minimum mapped speed (0 -> vmid-1)

        vmid (:obj:`int`): speed curve midpoint speed (vmin+1 -> vmax-1)

        vmax (:obj:`int`): speed curve maximum mapped speed (vmid+1 -> 255)
    """

    def __init__(self):
        self.invert = False
        self.torqueComp = False
        self.tlgMode = False
        self.accel = 0
        self.decel = 0
        self.vmin = 0
        self.vmid = 128
        self.vmax = 255

    def from_config_byte(self, byte):
        self.invert = set_with_bit(byte, PFX_CFG_MOTOR_INVERT)
        self.torqueComp = set_with_bit(byte, PFX_CFG_MOTOR_TRQCOMP)
        self.tlgMode = set_with_bit(byte, PFX_CFG_MOTOR_TLGMODE)

    def from_speed_bytes(self, msg):
        self.vmin = int(msg[0])
        self.vmid = int(msg[1])
        self.vmax = int(msg[2])
        self.accel = int(msg[3])
        self.decel = int(msg[4])

    def to_config_byte(self):
        v = 0
        if self.invert:
            v |= PFX_CFG_MOTOR_INVERT
        if self.torqueComp:
            v |= PFX_CFG_MOTOR_TRQCOMP
        if self.tlgMode:
            v |= PFX_CFG_MOTOR_TLGMODE
        return v

    def to_speed_bytes(self):
        v = []
        v.append(self.vmin)
        v.append(self.vmid)
        v.append(self.vmax)
        v.append(self.accel)
        v.append(self.decel)
        return v

    def __repr__(self):
        s = "invert=%02X torqueComp=%02X tlgMode=%02X" % (
            self.invert,
            self.torqueComp,
            self.tlgMode,
        )
        s = s + "vmin=%02X vmid=%02X vmax=%02X" % (self.vmin, self.vmid, self.vmax)
        s = "%s(%s)" % ("PFxMotor." + self.__class__.__name__, s)
        return s

    def __str__(self):
        sb = []
        sb.append(
            "  Invert : %s  Torque comp : %s  PF mode : %s"
            % (self.invert, self.torqueComp, self.tlgMode)
        )
        sb.append("  Accel  : %s  Decel : %s" % (self.accel, self.decel))
        sb.append(
            "  vMin   : %s  vMid  : %s  vMax : %s" % (self.vmin, self.vmid, self.vmax)
        )
        s = "\n".join(sb)
        return s


class PFxLights:
    """
    Light settings container class.

    This class contains default startup brightness data for every light channel.
    All brightness values range from 0 (minimum) to 255 (maximum).

    Attributes:
        defaultBrightness (:obj:`int`): default global brightness, if 0, then individual brightness is used

        startupBrightness ([:obj:`int`]): list of 8 individual startup brightness values for each light output

        pfBrightnessA (:obj:`int`): startup brightness of PF channel A (when used for lights)

        pfBrightnessB (:obj:`int`): startup brightness of PF channel B

        pfBrightnessC (:obj:`int`): startup brightness of PF channel C

        pfBrightnessD (:obj:`int`): startup brightness of PF channel D
    """

    def __init__(self):
        self.defaultBrightness = 0
        self.startupBrightness = [0, 0, 0, 0, 0, 0, 0, 0]
        self.pfBrightnessA = 0
        self.pfBrightnessB = 0
        self.pfBrightnessC = 0
        self.pfBrightnessD = 0

    def __repr__(self):
        sb = "".join("{:02X} ".format(x) for x in self.startupBrightness)
        sp = "".join(
            "{:02X} ".format(x)
            for x in [
                self.pfBrightnessA,
                self.pfBrightnessB,
                self.pfBrightnessC,
                self.pfBrightnessD,
            ]
        )
        s = "defaultBrightness=%02X startupBrightness=%s pfBrightness=%s" % (
            self.defaultBrightness,
            sb,
            sp,
        )
        s = "%s(%s)" % ("PFxLights." + self.__class__.__name__, s)
        return s

    def __str__(self):
        sb = []
        sb.append("Default brightness    : %02X" % (self.defaultBrightness))
        sb.append(
            "Startup brightness    : "
            + "".join("{:02X} ".format(x) for x in self.startupBrightness)
        )
        sb.append(
            "PF output brightness  : "
            + "".join(
                "{:02X} ".format(x)
                for x in [
                    self.pfBrightnessA,
                    self.pfBrightnessB,
                    self.pfBrightnessC,
                    self.pfBrightnessD,
                ]
            )
        )
        s = "\n".join(sb)
        return s


class PFxAudio:
    """
    Audio settings container class.

    This class contains audio configuration data such as default volume,
    bass, treble, etc.

    Attributes:
        audioDRC (:obj:`boolean`): auto Dynamic Range Control (True/False)

        bass (:obj:`int`): startup bass EQ (-20 to 20 dB)

        treble (:obj:`int`): startup treble EQ (-20 to 20 dB)

        defaultVolume (:obj:`int`): startup volume (0 min - 255 max)
    """

    def __init__(self):
        self.audioDRC = False
        self.bass = 0
        self.treble = 0
        self.defaultVolume = 0

    def __repr__(self):
        s = "drc=%d bass=%d treble=%d" % (self.audioDRC, self.bass, self.treble)
        s = "%s(%s)" % ("PFxAudio." + self.__class__.__name__, s)
        return s

    def __str__(self):
        os = ""
        if self.audioDRC:
            os = "ON"
        else:
            os = "OFF"
        s = "Audio DRC: %s  Bass: %02X  Treble: %02X" % (os, self.bass, self.treble)
        return s


class PFxConfig:
    """
    Top level configuration data container class.

    This class contains catergorized container classes for groups of related settings.
    To change a configuration setting, simply access the setting value using
    a dotted path type notation, e.g. config.lights.startupBrightness[2] = 100

    Attributes:
        settings (:obj:`PFxSettings`): container for general settings.

        motors ([:obj:`PFxMotor`]): list of 4 containers for motor settings

        lights (:obj:`PFxLights`): container for default brightness settings

        audio (:obj:`PFxAudio`): container for audio related settings
    """

    def __init__(self):
        self.settings = PFxSettings()
        self.motors = [PFxMotor(), PFxMotor(), PFxMotor(), PFxMotor()]
        self.lights = PFxLights()
        self.audio = PFxAudio()

    def from_bytes(self, msg):
        """
        Converts the message string bytes read from the PFx Brick into
        the corresponding data members of this class.
        """
        self.lights.startupBrightness[0] = msg[1]
        self.lights.startupBrightness[1] = msg[2]
        self.lights.startupBrightness[2] = msg[3]
        self.lights.startupBrightness[3] = msg[4]
        self.lights.startupBrightness[4] = msg[5]
        self.lights.startupBrightness[5] = msg[6]
        self.settings.notchCount = msg[7]
        self.settings.notchBounds[0] = msg[8]
        self.settings.notchBounds[1] = msg[9]
        self.settings.notchBounds[2] = msg[10]
        self.settings.notchBounds[3] = msg[11]
        self.settings.notchBounds[4] = msg[12]
        self.settings.notchBounds[5] = msg[13]
        self.settings.notchBounds[6] = msg[14]
        self.settings.irAutoOff = msg[26]
        self.settings.bleAutoOff = msg[27]
        self.settings.bleMotorWhenDisconnect = msg[28]
        self.settings.bleAdvertPower = msg[29]
        self.settings.bleSessionPower = msg[30]
        self.lights.startupBrightness[6] = msg[31]
        self.lights.startupBrightness[7] = msg[32]
        self.lights.pfBrightnessA = msg[33]
        self.lights.pfBrightnessB = msg[34]
        self.audio.bass = msg[35]
        self.audio.treble = msg[36]
        self.settings.statusLED = int(msg[37] & PFX_CFG_STATLED_MASK)
        self.settings.volumeBeep = int(msg[37] & PFX_CFG_VOLBEEP_MASK)
        self.settings.autoPowerDown = int(msg[37] & PFX_CFG_POWERSAVE_MASK)
        self.settings.lockoutMode = int(msg[37] & PFX_CFG_LOCK_MODE_MASK)
        self.audio.audioDRC = int(msg[37] & PFX_CFG_AUDIO_DRC_MASK)
        self.motors[0].from_config_byte(msg[38])
        self.motors[0].from_speed_bytes(msg[39:44])
        self.motors[1].from_config_byte(msg[44])
        self.motors[1].from_speed_bytes(msg[45:50])
        self.motors[2].from_config_byte(msg[50])
        self.motors[2].from_speed_bytes(msg[51:56])
        self.motors[3].from_config_byte(msg[56])
        self.motors[3].from_speed_bytes(msg[57:62])
        self.audio.defaultVolume = msg[62]
        self.lights.defaultBrightness = msg[63]

    def to_bytes(self):
        """
        Converts the data members of this class to the message
        string bytes which can be sent to the PFx Brick.
        """
        msg = []
        msg.append(self.settings.notchCount)
        msg.append(self.settings.notchBounds[0])
        msg.append(self.settings.notchBounds[1])
        msg.append(self.settings.notchBounds[2])
        msg.append(self.settings.notchBounds[3])
        msg.append(self.settings.notchBounds[4])
        msg.append(self.settings.notchBounds[5])
        msg.append(self.settings.notchBounds[6])
        msg.extend([0] * 11)
        msg.append(self.settings.irAutoOff)
        msg.append(self.settings.bleAutoOff)
        msg.append(self.settings.bleMotorWhenDisconnect)
        msg.append(self.settings.bleAdvertPower)
        msg.append(self.settings.bleSessionPower)
        msg.append(self.audio.bass)
        msg.append(self.audio.treble)
        v = 0
        if self.settings.statusLED == PFX_CFG_STATLED_OFF:
            v |= PFX_CFG_STATLED_OFF
        else:
            v |= PFX_CFG_STATLED_ON
        if self.settings.volumeBeep == PFX_CFG_VOLBEEP_ON:
            v |= PFX_CFG_VOLBEEP_ON
        else:
            v |= PFX_CFG_VOLBEEP_OFF
        v |= self.settings.autoPowerDown
        v |= self.settings.lockoutMode
        if self.audio.audioDRC == PFX_CFG_AUDIO_DRC_ON:
            v |= PFX_CFG_AUDIO_DRC_ON
        else:
            v |= PFX_CFG_AUDIO_DRC_OFF
        msg.append(v)
        msg.append(self.motors[0].to_config_byte())
        msg.extend(self.motors[0].to_speed_bytes())
        msg.append(self.motors[1].to_config_byte())
        msg.extend(self.motors[1].to_speed_bytes())
        msg.append(self.motors[2].to_config_byte())
        msg.extend(self.motors[2].to_speed_bytes())
        msg.append(self.motors[3].to_config_byte())
        msg.extend(self.motors[3].to_speed_bytes())
        msg.append(self.audio.defaultVolume)
        msg.append(self.lights.defaultBrightness)
        msg.append(self.lights.startupBrightness[0])
        msg.append(self.lights.startupBrightness[1])
        msg.append(self.lights.startupBrightness[2])
        msg.append(self.lights.startupBrightness[3])
        msg.append(self.lights.startupBrightness[4])
        msg.append(self.lights.startupBrightness[5])
        msg.append(self.lights.startupBrightness[6])
        msg.append(self.lights.startupBrightness[7])
        msg.append(self.lights.pfBrightnessA)
        msg.append(self.lights.pfBrightnessB)
        return msg

    def __str__(self):
        sb = []
        sb.append(str(self.settings))
        sb.append(str(self.lights))
        sb.append(str(self.audio))
        for i, motor in enumerate(self.motors):
            sb.append("Motor Channel %d" % (i))
            sb.append(str(motor))
        s = "\n".join(sb)
        return s
