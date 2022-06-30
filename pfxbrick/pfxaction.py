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

import pfxbrick.pfxdict as pd
from pfxbrick.pfx import *
from pfxbrick.pfxhelpers import *


class PFxAction:
    """
    Action data structure class.

    This class reflects the 16 byte data structure used internally
    by the PFx Brick to execute a composite action of motor, lighting,
    and sound effects.

    Attributes:
        command (:obj:`int`): Command byte

        motorActionId (:obj:`int`): Motor action ID and motor channel mask byte

        motorParam1 (:obj:`int`): Motor parameter 1

        motorParam2 (:obj:`int`): Motor parameter 2

        lightFxId (:obj:`int`): Light Fx ID byte

        lightOutputMask (:obj:`int`): Light channel output mask

        lightPFOutputMask (:obj:`int`): Light channel on PF output mask

        lightParam1 (:obj:`int`): Lighting parameter 1

        lightParam2 (:obj:`int`): Lighting parameter 2

        lightParam3 (:obj:`int`): Lighting parameter 3

        lightParam4 (:obj:`int`): Lighting parameter 4

        lightParam5 (:obj:`int`): Lighting parameter 5

        soundFxId (:obj:`int`): Sound Fx ID byte

        soundFileId (:obj:`int`): Sound file ID

        soundParam1 (:obj:`int`): Sound parameter 1

        soundParam2 (:obj:`int`): Sound parameter 2

    """

    def __init__(self):
        self.command = 0
        self.motorActionId = 0
        self.motorParam1 = 0
        self.motorParam2 = 0
        self.lightFxId = 0
        self.lightOutputMask = 0
        self.lightPFOutputMask = 0
        self.lightParam1 = 0
        self.lightParam2 = 0
        self.lightParam3 = 0
        self.lightParam4 = 0
        self.lightParam5 = 0
        self.soundFxId = 0
        self.soundFileId = 0
        self.soundParam1 = 0
        self.soundParam2 = 0

        self.fileIDstr = None

    def __eq__(self, other):
        """Dunder method for equality"""
        for k, v in self.__dict__.items():
            if k not in other.__dict__:
                return False
            if not v == other.__dict__[k]:
                return False
        return True

    def all_off(self):
        """
        Populates an action to turn off all motors, lights, and sound.
        """
        self.clear()
        self.command = EVT_COMMAND_ALL_OFF
        return self

    def set_motor_speed(self, ch, speed, duration=None):
        """
        Populates an action to set the speed of specified motor channel(s).
        The motor speed is specified between -100% and +100% where negative
        values are in the reverse direction and positive values are in
        the forward direction.

        :param ch: [:obj:`int`] a list of motor channels (1-4)
        :param speed: :obj:`int` desired motor speed (-100 to +100)
        :param duration: :obj:`float` optional duration (in seconds) to run motor, runs indefinitely if not specified
        :returns: :obj:`PFxAction` self

        If the duration value is specified, it represents the desired motor
        run time in seconds. Note that this value will be rounded to the
        nearest fixed interval of the DURATION parameter as defined in the ICD
        ranging between 16 fixed values from 0.5 sec to 5 min.
        """
        sf = float(speed)
        if sf > 100.0:
            sf = 100.0
        if sf < -100.0:
            sf = -100.0
        sf = (sf / 100.0) * 63.0
        s = int(abs(sf)) & EVT_MOTOR_SPEED_HIRES_MASK
        s |= EVT_MOTOR_SPEED_HIRES
        if speed < 0:
            s |= EVT_MOTOR_SPEED_HIRES_REV
        self.motorParam1 = s

        m = ch_to_mask(listify(ch)) & EVT_MOTOR_OUTPUT_MASK
        if duration is not None:
            m |= EVT_MOTOR_SET_SPD_TIMED
            self.motorParam2 = duration_to_fixed_value(duration)
        else:
            m |= EVT_MOTOR_SET_SPD
        self.motorActionId = m
        return self

    def stop_motor(self, ch, estop=True):
        """
        Populates an action to stop the specifed motor channel(s).

        :param ch: [:obj:`int`] a list of motor channels (1-4)
        :param estop: :obj:`boolean` specifies emergency/instant stop
        :returns: :obj:`PFxAction` self
        """
        m = ch_to_mask(listify(ch)) & EVT_MOTOR_OUTPUT_MASK
        if not estop:
            m |= EVT_MOTOR_STOP
        self.motorActionId = m
        return self

    def change_dir(self, ch):
        """
        Populates an action to change direction in specifed motor channel(s).

        :param ch: [:obj:`int`] a list of motor channels (1-4)
        :returns: :obj:`PFxAction` self
        """
        m = ch_to_mask(listify(ch)) & EVT_MOTOR_OUTPUT_MASK
        m |= EVT_MOTOR_CHANGE_DIR
        self.motorActionId = m
        return self

    def increase_speed(self, ch, step=1, bidir=False):
        """
        Populates an action to increase speed in specifed motor channel(s).

        :param ch: [:obj:`int`] a list of motor channels (1-4)
        :returns: :obj:`PFxAction` self
        """
        m = ch_to_mask(listify(ch)) & EVT_MOTOR_OUTPUT_MASK
        m |= EVT_MOTOR_INC_SPD_BI if bidir else EVT_MOTOR_INC_SPD
        self.motorActionId = m
        self.motorParam1 = step
        return self

    def decrease_speed(self, ch, step=1, bidir=False):
        """
        Populates an action to increase speed in specifed motor channel(s).

        :param ch: [:obj:`int`] a list of motor channels (1-4)
        :returns: :obj:`PFxAction` self
        """
        m = ch_to_mask(listify(ch)) & EVT_MOTOR_OUTPUT_MASK
        m |= EVT_MOTOR_DEC_SPD_BI if bidir else EVT_MOTOR_DEC_SPD
        self.motorActionId = m
        self.motorParam1 = step
        return self

    def light_on(self, ch):
        """
        Populates an action to turn on selected light outputs.

        :param ch: [:obj:`int`] a list of light channels (1-8)
        :returns: :obj:`PFxAction` self
        """
        self.lightOutputMask = ch_to_mask(listify(ch))
        self.lightFxId = EVT_LIGHTFX_ON_OFF_TOGGLE
        self.lightParam4 = EVT_TRANSITION_ON
        return self

    def light_off(self, ch):
        """
        Populates an action to turn off selected light outputs.

        :param ch: [:obj:`int`] a list of light channels (1-8)
        :returns: :obj:`PFxAction` self
        """
        self.lightOutputMask = ch_to_mask(listify(ch))
        self.lightFxId = EVT_LIGHTFX_ON_OFF_TOGGLE
        self.lightParam4 = EVT_TRANSITION_OFF
        return self

    def light_toggle(self, ch):
        """
        Populates an action to toggle the state of selected light outputs.

        :param ch: [:obj:`int`] a list of light channels (1-8)
        :returns: :obj:`PFxAction` self
        """
        self.lightOutputMask = ch_to_mask(listify(ch))
        self.lightFxId = EVT_LIGHTFX_ON_OFF_TOGGLE
        self.lightParam4 = EVT_TRANSITION_TOGGLE
        return self

    def set_brightness(self, ch, brightness):
        """
        Populates an action to set the brightness of selected light outputs.

        :param ch: [:obj:`int`] a list of light channels (1-8)
        :param brightness: :obj:`int` brightness (0 - 255 max)
        :returns: :obj:`PFxAction` self
        """
        x = brightness
        if x > 255:
            x = 255
        if x < 0:
            x = 0
        self.lightOutputMask = ch_to_mask(listify(ch))
        self.lightFxId = EVT_LIGHTFX_SET_BRIGHT
        self.lightParam1 = x
        return self

    def combo_light_fx(self, fx, param=[0, 0, 0, 0, 0]):
        """
        Populates an action with a user specified combination light effect
        and associated parameters.

        :param fx: :obj:`int` desired light effect
        :param param: [:obj:`int`] a list of up to 5 light parameters
        :returns: :obj:`PFxAction` self
        """
        return self.light_fx([], fx | EVT_LIGHT_COMBO_MASK, param)

    def light_fx(self, ch, fx, param=[0, 0, 0, 0, 0]):
        """
        Populates an action with a user specified light effect and
        associated parameters.

        :param ch: [:obj:`int`] a list of light channels (1-8)
        :param fx: :obj:`int` desired light effect
        :param param: [:obj:`int`] a list of up to 5 light parameters
        :returns: :obj:`PFxAction` self

        The details of specifying the light **fx** and **param** items
        is described in detail in the ICD document. The **pfx.py**
        file contains convenient pre-defined constants for all of
        the light effect types and parameter values.

        An example of using this method is as follows::

            p = [EVT_PERIOD_1S, EVT_DUTYCY_10, EVT_BURST_COUNT_2, EVT_TRANSITION_TOGGLE]
            a = PFxAction().light_fx([1,4], EVT_LIGHTFX_STROBE_P, p)

        This specifies a strobe light effect on channels 1 and 4 with
        a 1 second period, 10% duty cycle, two light pulses and with
        a toggle activation.
        """
        self.lightOutputMask = ch_to_mask(listify(ch))
        self.lightFxId = fx
        for i, p in enumerate(param):
            if i == 0:
                self.lightParam1 = p
            elif i == 1:
                self.lightParam2 = p
            elif i == 2:
                self.lightParam3 = p
            elif i == 3:
                self.lightParam4 = p
            elif i == 4:
                self.lightParam5 = p
        return self

    def sound_fx(self, fx, param=[0, 0], fileID=None):
        """
        Populates an action with a user specified sound effect and
        associated parameters.

        :param fx: :obj:`int` desired sound action
        :param param: [:obj:`int`] a list of up to 2 sound parameters
        :param fileID: :obj:`int` file ID of an audio file in the file system
        :returns: :obj:`PFxAction` self

        The details of specifying the sound **fx** and **param** items
        is described in detail in the ICD document. The **pfx.py**
        file contains convenient pre-defined constants for all of
        the sound effect types and parameter values.

        An example of using this method is as follows::

            p = [EVT_SOUND_DUR_10S]
            a = PFxAction().sound_fx(EVT_SOUND_PLAY_DUR, p, 5)

        This specifies an action to playback an audio file with ID=5
        for a fixed duration of 10 seconds.
        """
        self.soundFxId = fx
        if fileID is not None:
            if isinstance(fileID, int):
                self.soundFileId = fileID
            else:
                self.fileIDstr = fileID
        for i, p in enumerate(param):
            if i == 0:
                self.soundParam1 = p
            elif i == 1:
                self.soundParam2 = p
        return self

    def play_audio_file(self, fileID):
        """
        Populates an action to play an audio file once.

        :param fileID: :obj:`int` file ID of an audio file in the file system
        :returns: :obj:`PFxAction` self

        This is a convenience wrapper for the sound_fx method.
        """
        return self.sound_fx(EVT_SOUND_PLAY_ONCE, [EVT_SOUND_TOGGLE], fileID)

    def stop_audio_file(self, fileID):
        """
        Populates an action to stop playback of an audio file.

        :param fileID: :obj:`int` file ID of an audio file in the file system
        :returns: :obj:`PFxAction` self

        This is a convenience wrapper for the sound_fx method.
        """
        return self.sound_fx(EVT_SOUND_STOP, [], fileID)

    def repeat_audio_file(self, fileID):
        """
        Populates an action for repeated playback of an audio file.

        :param fileID: :obj:`int` file ID of an audio file in the file system
        :returns: :obj:`PFxAction` self

        This is a convenience wrapper for the sound_fx method.
        """
        return self.sound_fx(EVT_SOUND_PLAY_CONT, [], fileID)

    def set_volume(self, volume):
        """
        Populates an action to set the audio volume.

        :param volume: :obj:`int` desired audio volume (0 - 100%)
        :returns: :obj:`PFxAction` self

        This is a convenience wrapper for the sound_fx method.
        """
        vf = float(volume)
        if vf > 100.0:
            vf = 100.0
        if vf < 0.0:
            vf = 0.0
        vf = (vf / 100.0) * 255.0
        v = int(vf)
        return self.sound_fx(EVT_SOUND_SET_VOL, [0, v])

    def is_empty(self):
        """Determines if the action is clear/undefined"""
        if self.command > 0:
            return False
        if self.motorActionId > 0:
            return False
        if self.motorParam1 > 0:
            return False
        if self.motorParam2 > 0:
            return False
        if self.lightFxId > 0:
            return False
        if self.lightOutputMask > 0:
            return False
        if self.lightPFOutputMask > 0:
            return False
        if self.lightParam1 > 0:
            return False
        if self.lightParam2 > 0:
            return False
        if self.lightParam3 > 0:
            return False
        if self.lightParam4 > 0:
            return False
        if self.lightParam5 > 0:
            return False
        if self.soundFxId > 0:
            return False
        if self.soundFileId > 0:
            return False
        if self.soundParam1 > 0:
            return False
        if self.soundParam2 > 0:
            return False
        return True

    def clear(self):
        """
        Sets all the action data in this class to zero.
        """
        self.command = 0
        self.motorActionId = 0
        self.motorParam1 = 0
        self.motorParam2 = 0
        self.lightFxId = 0
        self.lightOutputMask = 0
        self.lightPFOutputMask = 0
        self.lightParam1 = 0
        self.lightParam2 = 0
        self.lightParam3 = 0
        self.lightParam4 = 0
        self.lightParam5 = 0
        self.soundFxId = 0
        self.soundFileId = 0
        self.soundParam1 = 0
        self.soundParam2 = 0

    def from_bytes(self, msg):
        """
        Converts the message string bytes read from the PFx Brick into
        the corresponding data members of this class.
        """
        self.command = msg[1]
        self.motorActionId = msg[2]
        self.motorParam1 = msg[3]
        self.motorParam2 = msg[4]
        self.lightFxId = msg[5]
        self.lightOutputMask = msg[6]
        self.lightPFOutputMask = msg[7]
        self.lightParam1 = msg[8]
        self.lightParam2 = msg[9]
        self.lightParam3 = msg[10]
        self.lightParam4 = msg[11]
        self.lightParam5 = msg[12]
        self.soundFxId = msg[13]
        self.soundFileId = msg[14]
        self.soundParam1 = msg[15]
        self.soundParam2 = msg[16]

    def to_bytes(self):
        """
        Converts the data members of this class to the message
        string bytes which can be sent to the PFx Brick.
        """
        msg = []
        msg.append(self.command)
        msg.append(self.motorActionId)
        msg.append(self.motorParam1)
        msg.append(self.motorParam2)
        msg.append(self.lightFxId)
        msg.append(self.lightOutputMask)
        msg.append(self.lightPFOutputMask)
        msg.append(self.lightParam1)
        msg.append(self.lightParam2)
        msg.append(self.lightParam3)
        msg.append(self.lightParam4)
        msg.append(self.lightParam5)
        msg.append(self.soundFxId)
        msg.append(self.soundFileId)
        msg.append(self.soundParam1)
        msg.append(self.soundParam2)
        return msg

    def to_event_script_str(self, evtID, ch=None):
        """
        PFx script language representation.

        Converts an action to a PFx script representation with the keywork 'event' and the
        action encapsulated in curly braces.  The event can be specified either with an
        event ID / IR channel pair or by the address (specified with evtID=address and ch not used)

        :param evtID: :obj:`int` event id or address of action
        :param ch: :obj:`int` IR channel of event (0-3) or None if evtID=address
        :returns: :obj:`str` string representation of event/action
        """
        if ch is None:
            evs = "0x%02X" % evtID
        else:
            if evtID == EVT_ID_8879_TWO_BUTTONS:
                evs = "ir speed ch %d button" % (ch + 1)
            elif evtID == EVT_ID_8879_LEFT_BUTTON:
                evs = "ir speed ch %d left button" % (ch + 1)
            elif evtID == EVT_ID_8879_RIGHT_BUTTON:
                evs = "ir speed ch %d right button" % (ch + 1)
            elif evtID == EVT_ID_8879_LEFT_INC:
                evs = "ir speed ch %d left up" % (ch + 1)
            elif evtID == EVT_ID_8879_LEFT_DEC:
                evs = "ir speed ch %d left down" % (ch + 1)
            elif evtID == EVT_ID_8879_RIGHT_INC:
                evs = "ir speed ch %d right up" % (ch + 1)
            elif evtID == EVT_ID_8879_RIGHT_DEC:
                evs = "ir speed ch %d right down" % (ch + 1)
            elif evtID == EVT_ID_8885_LEFT_FWD:
                evs = "ir joy ch %d left up" % (ch + 1)
            elif evtID == EVT_ID_8885_LEFT_REV:
                evs = "ir joy ch %d left down" % (ch + 1)
            elif evtID == EVT_ID_8885_RIGHT_FWD:
                evs = "ir joy ch %d right up" % (ch + 1)
            elif evtID == EVT_ID_8885_RIGHT_REV:
                evs = "ir joy ch %d right down" % (ch + 1)
            elif evtID == EVT_ID_8885_LEFT_CTROFF:
                evs = "ir joy ch %d left" % (ch + 1)
            elif evtID == EVT_ID_8885_RIGHT_CTROFF:
                evs = "ir joy ch %d right" % (ch + 1)
            elif evtID == EVT_ID_STARTUP_EVENT:
                evs = "startup %d" % (ch + 1)
            elif evtID == EVT_ID_STARTUP_EVENT2:
                evs = "startup %d" % (ch + 5)
        s = []
        s.append("event %s {" % (evs))
        s.append("%s" % (self.to_script_str(indent="  ")))
        s.append("}")
        return "\n".join(s)

    def to_script_str(self, indent=""):
        """
        PFx script language representation.

        Converts an action to a PFx script representation.

        :returns: :obj:`str` string representation of event/action
        """
        s = []
        if self.motorActionId & EVT_MOTOR_OUTPUT_MASK:
            ms = motor_mask_to_script_str(self.motorActionId & EVT_MOTOR_OUTPUT_MASK)
            mid = (self.motorActionId & EVT_MOTOR_ACTION_ID_MASK) >> 4
            s.append(
                "%smotor %s fx 0x%01X %d %d"
                % (indent, ms, mid, self.motorParam1, self.motorParam2)
            )
        if self.lightFxId & EVT_LIGHT_COMBO_MASK:
            s.append(
                "%slight all fx 0x%02X %d %d %d %d %d"
                % (
                    indent,
                    self.lightFxId & EVT_LIGHT_ID_MASK,
                    self.lightParam1,
                    self.lightParam2,
                    self.lightParam3,
                    self.lightParam4,
                    self.lightParam5,
                )
            )
        elif self.lightFxId & EVT_LIGHT_ID_MASK:
            lc = lightch_mask_to_script_str(self.lightOutputMask)
            s.append(
                "%slight %s fx 0x%02X %d %d %d %d %d"
                % (
                    indent,
                    lc,
                    self.lightFxId & EVT_LIGHT_ID_MASK,
                    self.lightParam1,
                    self.lightParam2,
                    self.lightParam3,
                    self.lightParam4,
                    self.lightParam5,
                )
            )
        if self.soundFxId:
            if self.fileIDstr is not None:
                # action specified with a string based filename
                s.append(
                    '%ssound fx 0x%02X "%s" %d %d'
                    % (
                        indent,
                        self.soundFxId,
                        self.fileIDstr,
                        self.soundParam1,
                        self.soundParam2,
                    )
                )
            else:
                # action specified with numeric fileID
                s.append(
                    "%ssound fx 0x%02X %d %d %d"
                    % (
                        indent,
                        self.soundFxId,
                        self.soundFileId,
                        self.soundParam1,
                        self.soundParam2,
                    )
                )
        if len(s) == 0:
            s.append("# cleared action")
        return "\n".join(s)

    def verbose_line_str(self, brick):
        """
        Human readable string of action object in single line.

        :param brick: :obj:`PFxBrick` reference to a PFx Brick in order to query filename
        """
        s = []
        if self.command > 0:
            s.append("Cmd: %s" % shorter_str(pd.command_dict[self.command]))
        if self.motorActionId & EVT_MOTOR_OUTPUT_MASK:
            x = pd.motor_action_dict[self.motorActionId & EVT_MOTOR_ACTION_ID_MASK]
            s.append("%s%s" % (motor_ch_str(self.motorActionId), shorter_str(x)))
        if self.lightFxId & EVT_LIGHT_COMBO_MASK:
            sf = pd.combo_lightfx_dict[self.lightFxId & EVT_LIGHT_ID_MASK]
            s.append("Combo light: %s" % (shorter_str(sf)))
        elif self.lightFxId & EVT_LIGHT_ID_MASK:
            sf = pd.ind_lightfx_dict[self.lightFxId & EVT_LIGHT_ID_MASK]
            sc = light_ch_str(self.lightOutputMask)
            s.append("Light %s %s" % (sc, sf))
        if self.soundFxId:
            x = pd.soundfx_dict[self.soundFxId]
            if self.soundFileId:
                fn = brick.filedir.get_filename(self.soundFileId)
                s.append('Sound %s "%s" (%d)' % (x, fn, self.soundFileId))
            else:
                s.append("Sound %s" % (x))
        return " ".join(s)

    def __str__(self):
        """
        Convenient human readable string of the action data structure. This allows
        a :py:class:`PFxAction` object to be used with :obj:`str` and :obj:`print` methods.
        """
        sb = []
        sb.append(
            "Command           : [%02X] %s"
            % (self.command, pd.command_dict[self.command])
        )
        if self.motorActionId & EVT_MOTOR_OUTPUT_MASK == 0:
            sb.append("Motor Action ID   : [%02X] None" % (self.motorActionId))
        else:
            sb.append(
                "Motor Action ID   : [%02X] %s %s"
                % (
                    self.motorActionId,
                    pd.motor_action_dict[self.motorActionId & EVT_MOTOR_ACTION_ID_MASK],
                    motor_ch_str(self.motorActionId),
                )
            )
        sb.append("Motor Param 1     : [%02X]" % (self.motorParam1))
        sb.append("Motor Param 2     : [%02X]" % (self.motorParam2))
        sf = ""
        if self.lightFxId & EVT_LIGHT_COMBO_MASK:
            sf = pd.combo_lightfx_dict[self.lightFxId & EVT_LIGHT_ID_MASK]
        else:
            sf = pd.ind_lightfx_dict[self.lightFxId & EVT_LIGHT_ID_MASK]
        sb.append("Light Fx ID       : [%02X] %s" % (self.lightFxId, sf))
        sb.append(
            "Light Output Mask : [%02X] %s"
            % (self.lightOutputMask, light_ch_str(self.lightOutputMask))
        )
        sb.append("Light PF Out Mask : [%02X]" % (self.lightPFOutputMask))
        sb.append("Light Param 1     : [%02X]" % (self.lightParam1))
        sb.append("Light Param 2     : [%02X]" % (self.lightParam2))
        sb.append("Light Param 3     : [%02X]" % (self.lightParam3))
        sb.append("Light Param 4     : [%02X]" % (self.lightParam4))
        sb.append("Light Param 5     : [%02X]" % (self.lightParam5))
        sb.append("Sound Fx ID       : [%02X]" % (self.soundFxId))
        sb.append("Sound File ID     : [%02X]" % (self.soundFileId))
        sb.append("Sound Param 1     : [%02X]" % (self.soundParam1))
        sb.append("Sound Param 2     : [%02X]" % (self.soundParam2))
        s = "\n".join(sb)
        return s
