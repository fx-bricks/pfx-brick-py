#! /usr/bin/env python3
 
# PFx Brick configuration data helpers
 
from pfxbrick.pfx import *
import pfxbrick.pfxdict as pd
from pfxbrick.pfxhelpers import set_with_bit
 
class PFxSettings:
 
    def __init__(self):
        self.statusLED = 0
        self.volumeBeep = False
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
        sb.append('Status LED            : %s' % (pd.status_led_dict[self.statusLED]))
        sb.append('Volume Beep           : %s' % (pd.volume_beep_dict[self.volumeBeep]))
        sb.append('Auto Power Down       : %s' % (pd.power_save_dict[self.autoPowerDown]))
        sb.append('IR Lockout Mode       : %s' % (pd.lockout_dict[self.lockoutMode]))
        sb.append('IR Auto Off           : %s' % (pd.ir_off_dict[self.irAutoOff]))
        sb.append('BLE Auto Off          : %s' % (pd.ble_off_dict[self.bleAutoOff]))
        sb.append('BLE Motor Disconnect  : %s' % (pd.ble_motor_dict[self.bleMotorWhenDisconnect]))
        sb.append('BLE Advert Power      : %s' % (self.bleAdvertPower))
        sb.append('BLE Session Power     : %s' % (self.bleSessionPower))
        sb.append('Motor sound notches   : %s' % (self.notchCount))
        mb = "".join("{:02X} ".format(x) for x in self.notchBounds)
        sb.append('Motor sound bounds    : %s' % (mb))
        s = '\n'.join(sb)
        return s
 
class PFxMotor:
 
    def __init__(self):
        self.invert = False
        self.torqueComp = False
        self.tlgMode = False
        self.accel = 0
        self.decel = 0
        self.vmin = 0
        self.vmid = 128
        self.vmax = 255
         
    def parse_config_byte(self, byte):
        self.invert = set_with_bit(byte, PFX_CFG_MOTOR_INVERT)
        self.torqueComp = set_with_bit(byte, PFX_CFG_MOTOR_TRQCOMP)
        self.tlgMode = set_with_bit(byte, PFX_CFG_MOTOR_TLGMODE)
 
    def parse_speed_bytes(self, msg):
        self.vmin = int(msg[0])
        self.vmid = int(msg[1])
        self.vmax = int(msg[2])
        self.accel = int(msg[3])
        self.decel = int(msg[4])
 
    def __repr__(self):
        s = 'invert=%02X torqueComp=%02X tlgMode=%02X' % (self.invert, self.torqueComp, self.tlgMode)
        s = s + 'vmin=%02X vmid=%02X vmax=%02X' % (self.vmin, self.vmid, self.vmax)
        s = "%s(%s)" % ('PFxMotor.' + self.__class__.__name__, s)
        return s
 
    def __str__(self):
        sb = []
        sb.append('  Invert : %s  Torque comp : %s  PF mode : %s' % (self.invert, self.torqueComp, self.tlgMode))
        sb.append('  Accel  : %s  Decel : %s' % (self.accel, self.decel))
        sb.append('  vMin   : %s  vMid  : %s  vMax : %s' % (self.vmin, self.vmid, self.vmax))
        s = '\n'.join(sb)
        return s
 
 
class PFxLights:
 
    def __init__(self):
        self.defaultBrightness = 0
        self.startupBrightness = [0, 0, 0, 0, 0, 0, 0, 0]
        self.pfBrightnessA = 0              
        self.pfBrightnessB = 0              
        self.pfBrightnessC = 0              
        self.pfBrightnessD = 0              
 
 
    def __repr__(self):
        sb = "".join("{:02X} ".format(x) for x in self.startupBrightness)
        sp = "".join("{:02X} ".format(x) for x in [self.pfBrightnessA, self.pfBrightnessB, self.pfBrightnessC, self.pfBrightnessD])
        s = 'defaultBrightness=%02X startupBrightness=%s pfBrightness=%s' % (self.defaultBrightness, sb, sp)
        s = "%s(%s)" % ('PFxLights.' + self.__class__.__name__, s)
        return s
 
    def __str__(self):
        sb = []
        sb.append('Default brightness    : %02X' % (self.defaultBrightness))
        sb.append('Startup brightness    : ' + "".join("{:02X} ".format(x) for x in self.startupBrightness))
        sb.append('PF output brightness  : ' + "".join("{:02X} ".format(x) for x in [self.pfBrightnessA, self.pfBrightnessB, self.pfBrightnessC, self.pfBrightnessD]))
        s = '\n'.join(sb)
        return s
         
class PFxAudio:
     
    def __init__(self):
        self.audioDRC = False
        self.bass = 0
        self.treble = 0
        self.defaultVolume = 0   
         
    def __repr__(self):
        s = 'drc=%d bass=%d treble=%d' % (self.audioDRC, self.bass, self.treble)
        s = "%s(%s)" % ('PFxAudio.' + self.__class__.__name__, s)
        return s
         
    def __str__(self):
        os = ''
        if self.audioDRC:
            os = 'ON'
        else:
            os = 'OFF'
        s = 'Audio DRC: %s  Bass: %02X  Treble: %02X' % (os, self.bass, self.treble)
        return s        
 
class PFxConfig:
     
    def __init__(self):
        self.settings = PFxSettings()
        self.motors = [PFxMotor(), PFxMotor(), PFxMotor(), PFxMotor()]
        self.lights = PFxLights()
        self.audio = PFxAudio()
         
    def read_from_brick(self, msg):
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
        self.settings.btAutoOff = msg[27]
        self.settings.btMotorWhenDisconnect = msg[28]
        self.settings.btAdvertPower = msg[29]
        self.settings.btSessionPower = msg[30]
        self.lights.startupBrightness[6] = msg[31]
        self.lights.startupBrightness[7] = msg[32]
        self.lights.pfBrightnessA = msg[33]
        self.lights.pfBrightnessB = msg[34]
        self.audio.bass = msg[35]
        self.audio.treble = msg[36]
        self.settings.statusLED = int(msg[37] & PFX_CFG_STATLED_MASK)
        self.settings.volumeBeep = set_with_bit(msg[37], PFX_CFG_VOLBEEP_MASK)
        self.settings.autoPowerDown = int(msg[37] & PFX_CFG_POWERSAVE_MASK)
        self.settings.lockoutMode = int(msg[37] & PFX_CFG_LOCK_MODE_MASK)
        self.audio.audioDRC = set_with_bit(msg[37], PFX_CFG_AUDIO_DRC_MASK)
        self.motors[0].parse_config_byte(msg[38])
        self.motors[0].parse_speed_bytes(msg[39:44])
        self.motors[1].parse_config_byte(msg[44])
        self.motors[1].parse_speed_bytes(msg[45:50])
        self.motors[2].parse_config_byte(msg[50])
        self.motors[2].parse_speed_bytes(msg[51:56])
        self.motors[3].parse_config_byte(msg[56])
        self.motors[3].parse_speed_bytes(msg[57:62])
        self.audio.defaultVolume = msg[62]
        self.lights.defaultBrightness = msg[63]
         
    def __str__(self):
        sb = []
        sb.append(str(self.settings))
        sb.append(str(self.lights))
        sb.append(str(self.audio))
        for i,motor in enumerate(self.motors):
            sb.append('Motor Channel %d' % (i))
            sb.append(str(motor))
        s = '\n'.join(sb)
        return s
        