#! /usr/bin/env python3

# PFx Brick configuration data helpers

from pfxbrick.pfx import *
import pfxbrick.pfxdict as pd
from pfxbrick.pfxhelpers import *


class PFxAction:
    """
    Action data structure class.
    
    This class reflects the 16 byte data structure used internally
    by the PFx Brick to execute a composite action of motor, lighting,
    and sound effects.
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

    def set_motor_speed(self, ch, speed, duration=None):
        """
        Populates an action to set the speed of specified motor channel(s).
        The motor speed is specified between -100% and +100% where negative
        values are in the reverse direction and positive values are in
        the forward direction.
        
        :param ch: a list of motor channels (1-4)
        :param speed: desired motor speed (-100 to +100)
        :param duration: optional duration (in seconds) to run motor, runs indefinitely if not specified
        :returns: self (PFxAction class)        
        
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
        
        m = (ch_to_mask(ch) & EVT_MOTOR_OUTPUT_MASK)
        if duration is not None:
            m |= EVT_MOTOR_SET_SPD_TIMED
            self.motorParam2 = duration_to_fixed_value(duration)
        else:
            m |= EVT_MOTOR_SET_SPD
        self.motorActionId = m
        return self

    def stop_motor(self, ch):
        """
        Populates an action to stop the specifed motor channel(s).

        :param ch: a list of motor channels (1-4)
        :returns: self (PFxAction class)        
        """
        m = (ch_to_mask(ch) & EVT_MOTOR_OUTPUT_MASK)
        m |= EVT_MOTOR_ESTOP
        self.motorActionId = m
        return self
        
    def light_on(self, ch):
        """
        Populates an action to turn on selected light outputs.
        
        :param ch: a list of light channels (1-8)
        :returns: self (PFxAction class)        
        """
        self.lightOutputMask = ch_to_mask(ch)
        self.lightFxId = EVT_LIGHTFX_ON_OFF_TOGGLE
        self.lightParam4 = EVT_TRANSITION_ON
        return self
        
    def light_off(self, ch):
        """
        Populates an action to turn off selected light outputs.
        
        :param ch: a list of light channels (1-8)
        :returns: self (PFxAction class)        
        """
        self.lightOutputMask = ch_to_mask(ch)
        self.lightFxId = EVT_LIGHTFX_ON_OFF_TOGGLE
        self.lightParam4 = EVT_TRANSITION_OFF
        return self
        
    def light_toggle(self, ch):
        """
        Populates an action to toggle the state of selected light outputs.
        
        :param ch: a list of light channels (1-8)
        :returns: self (PFxAction class)        
        """
        self.lightOutputMask = ch_to_mask(ch)
        self.lightFxId = EVT_LIGHTFX_ON_OFF_TOGGLE
        self.lightParam4 = EVT_TRANSITION_TOGGLE
        return self
        
    def combo_light_fx(self, fx, param=[0, 0, 0, 0, 0]):
        """
        Populates an action with a user specified combination light effect
        and associated parameters.
        
        :param fx: desired light effect
        :param param: a list of up to 5 light parameters
        :returns: self (PFxAction class)
        """
        return self.light_fx([], fx | EVT_LIGHT_COMBO_MASK, param)
    
    def light_fx(self, ch, fx, param=[0, 0, 0, 0, 0]):
        """
        Populates an action with a user specified light effect and
        associated parameters.
        
        :param ch: a list of light channels (1-8)
        :param fx: desired light effect
        :param param: a list of up to 5 light parameters
        :returns: self (PFxAction class)
        
        The details of specifying the light *fx* and *param* items
        is described in detail in the ICD document. The *pfx.py* 
        file contains convenient pre-defined constants for all of
        the light effect types and parameter values.
        
        An example of using this method is as follows::
        
            p = [EVT_PERIOD_1S, EVT_DUTYCY_10, EVT_BURST_COUNT_2, EVT_TRANSITION_TOGGLE]
            a = PFxAction().light_fx([1,4], EVT_LIGHTFX_STROBE_P, p)
        
        This specifies a strobe light effect on channels 1 and 4 with
        a 1 second period, 10%% duty cycle, two light pulses and with
        a toggle activation.
        """
        self.lightOutputMask = ch_to_mask(ch)
        self.lightFxId = fx
        for i,p in enumerate(param):
            if i==0:
                self.lightParam1 = p
            elif i==1:
                self.lightParam2 = p
            elif i==2:
                self.lightParam3 = p
            elif i==3:
                self.lightParam4 = p
            elif i==4:
                self.lightParam5 = p
        return self            
        
    def sound_fx(self, fx, param=[0, 0], fileID=None):
        """
        Populates an action with a user specified sound effect and
        associated parameters.
        
        :param fx: desired sound action
        :param param: a list of up to 2 sound parameters
        :param fileID: file ID of an audio file in the file system
        :returns: self (PFxAction class)
        
        The details of specifying the sound *fx* and *param* items
        is described in detail in the ICD document. The *pfx.py* 
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
            self.soundFileId = fileID
        for i,p in enumerate(param):
            if i==0:
                self.soundParam1 = p
            elif i==1:
                self.soundParam2 = p
        return self

    def play_audio_file(self, fileID):
        """
        Populates an action to play an audio file once.
        
        :param fileID: file ID of an audio file in the file system
        :returns: self (PFxAction class)
        
        This is a convenience wrapper for the sound_fx method.
        """
        return self.sound_fx(EVT_SOUND_PLAY_ONCE, [EVT_SOUND_TOGGLE], fileID)

    def stop_audio_file(self, fileID):
        """
        Populates an action to stop playback of an audio file.
        
        :param fileID: file ID of an audio file in the file system
        :returns: self (PFxAction class)
        
        This is a convenience wrapper for the sound_fx method.
        """
        return self.sound_fx(EVT_SOUND_STOP, [], fileID)

    def repeat_audio_file(self, fileID):
        """
        Populates an action for repeated playback of an audio file.
        
        :param fileID: file ID of an audio file in the file system
        :returns: self (PFxAction class)
        
        This is a convenience wrapper for the sound_fx method.
        """
        return self.sound_fx(EVT_SOUND_PLAY_CONT, [], fileID)

    def set_volume(self, volume):
        """
        Populates an action to set the audio volume.
        
        :param volume: desired audio volume (0 - 100%)
        :returns: self (PFxAction class)
        
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

    def __str__(self):
        sb = []
        sb.append('Command           : [%02X] %s' % (self.command, pd.command_dict[self.command]))
        if self.motorActionId & EVT_MOTOR_OUTPUT_MASK == 0:
            sb.append('Motor Action ID   : [%02X] None' % (self.motorActionId))
        else:
            sb.append('Motor Action ID   : [%02X] %s %s' % (self.motorActionId, pd.motor_action_dict[self.motorActionId & EVT_MOTOR_ACTION_ID_MASK], motor_ch_str(self.motorActionId)))
        sb.append('Motor Param 1     : [%02X]' % (self.motorParam1))
        sb.append('Motor Param 2     : [%02X]' % (self.motorParam1))
        sf = ''
        if self.lightFxId & EVT_LIGHT_COMBO_MASK:
            sf = pd.combo_lightfx_dict[self.lightFxId & EVT_LIGHT_ID_MASK]
        else:
            sf = pd.ind_lightfx_dict[self.lightFxId & EVT_LIGHT_ID_MASK]
        sb.append('Light Fx ID       : [%02X] %s' % (self.lightFxId, sf))
        sb.append('Light Output Mask : [%02X] %s' % (self.lightOutputMask, light_ch_str(self.lightOutputMask)))
        sb.append('Light PF Out Mask : [%02X]' % (self.lightPFOutputMask))
        sb.append('Light Param 1     : [%02X]' % (self.lightParam1))
        sb.append('Light Param 2     : [%02X]' % (self.lightParam2))
        sb.append('Light Param 3     : [%02X]' % (self.lightParam3))
        sb.append('Light Param 4     : [%02X]' % (self.lightParam4))
        sb.append('Light Param 5     : [%02X]' % (self.lightParam5))
        sb.append('Sound Fx ID       : [%02X]' % (self.soundFxId))
        sb.append('Sound File ID     : [%02X]' % (self.soundFileId))
        sb.append('Sound Param 1     : [%02X]' % (self.soundParam1))
        sb.append('Sound Param 2     : [%02X]' % (self.soundParam2))
        s = '\n'.join(sb)
        return s
        
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