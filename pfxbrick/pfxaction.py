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

    def _init_ch(self, ch):
        self.lightOutputMask = ch_to_mask(ch)

    def light_on(self, ch):
        """
        Populates an action to turn on selected light outputs.
        
        :param ch: a list of light channels (1-8)
        :returns: self (PFxAction class)        
        """
        self._init_ch(ch)
        self.lightFxId = EVT_LIGHTFX_ON_OFF_TOGGLE
        self.lightParam4 = EVT_TRANSITION_ON
        return self
        
    def light_off(self, ch):
        """
        Populates an action to turn off selected light outputs.
        
        :param ch: a list of light channels (1-8)
        :returns: self (PFxAction class)        
        """
        self._init_ch(ch)
        self.lightFxId = EVT_LIGHTFX_ON_OFF_TOGGLE
        self.lightParam4 = EVT_TRANSITION_OFF
        return self
        
    def light_toggle(self, ch):
        """
        Populates an action to toggle the state of selected light outputs.
        
        :param ch: a list of light channels (1-8)
        :returns: self (PFxAction class)        
        """
        self._init_ch(ch)
        self.lightFxId = EVT_LIGHTFX_ON_OFF_TOGGLE
        self.lightParam4 = EVT_TRANSITION_TOGGLE
        return self
        
    def combo_light_fx(self, fx, param=[0, 0, 0, 0, 0]):
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
        self._init_ch(ch)
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