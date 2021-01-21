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
# PFx Brick dictionary lookup helpers

from pfxbrick.pfx import *

status_dict = {
    PFX_STATUS_NORMAL: "Normal",
    PFX_STATUS_NORMAL_PENDING: "Normal, upgrade pending",
    PFX_STATUS_SERVICE: "Service",
    PFX_STATUS_SERVICE_PENDING: "Service, upgrade pending",
    PFX_STATUS_SERVICE_BUSY: "Service, busy",
}

err_dict = {
    PFX_ERR_VERIFY_FAIL: "Verify failed",
    PFX_ERR_TRANSFER_FILE_EXISTS: "File exists",
    PFX_ERR_TRANSFER_TOO_BIG: "File too big",
    PFX_ERR_TRANSFER_INVALID: "Transfer request invalid",
    PFX_ERR_TRANSFER_FILE_NOT_FOUND: "File not found",
    PFX_ERR_TRANSFER_ERROR: "Transfer error",
    PFX_ERR_TRANSFER_CRC_MISMATCH: "CRC mismatch",
    PFX_ERR_TRANSFER_BUSY_WAIT: "Busy, try again",
    PFX_ERR_TRANSFER_LUT_FULL: "LUT full",
    PFX_ERR_TRANSFER_COMPLETE: "Transfer complete",
    PFX_ERR_UPGRADE_FAIL: "Upgrade failed",
    PFX_ERR_FILE_SYSTEM_ERR: "File system error",
    PFX_ERR_FILE_INVALID: "File is invalid",
    PFX_ERR_FILE_OUT_OF_RANGE: "File access is out of range",
    PFX_ERR_FILE_READ_ONLY: "File is read only",
    PFX_ERR_FILE_TOO_BIG: "File is too big",
    PFX_ERR_FILE_NOT_FOUND: "File not found",
    PFX_ERR_FILE_NOT_UNIQUE: "File ID is not unique",
    PFX_ERR_FILE_LOCKED_BUSY: "File system is locked or busy",
    PFX_ERR_FILE_SYSTEM_FULL: "File system is full",
    PFX_ERR_FILE_SYSTEM_TIMEOUT: "File system operation timed out",
    PFX_ERR_FILE_INVALID_ADDRESS: "File system accessed invalid address",
    PFX_ERR_FILE_NEXT_SECTOR: "File system error reading next sector",
    PFX_ERR_FILE_ACCESS_DENIED: "File system access denied",
    PFX_ERR_BLE_FAULT: "Bluetooth fault",
    PFX_ERR_SPKR_SHORTCIR_FAULT: "Short circuit on speaker output",
    PFX_ERR_DAC_OVERTEMP_FAULT: "Overtemperature reported by DAC",
    PFX_ERR_TRAP_BROWNOUT_RST: "Brown-out reset trap",
    PFX_ERR_TRAP_CONFLICT: "Reset trap conflict",
    PFX_ERR_TRAP_ILLEGAL_OPCODE: "Reset trap due to illegal OP code",
    PFX_ERR_TRAP_CONFIG_MISMATCH: "Reset trap due to configuration mismatch",
}


def get_err_str(err):
    if err in err_dict:
        return err_dict[err]
    else:
        return "Unknown error"


status_led_dict = {
    PFX_CFG_STATLED_OFF: "Normally OFF, blink with activity",
    PFX_CFG_STATLED_ON: "Normally ON, blink with activity",
}

volume_beep_dict = {PFX_CFG_VOLBEEP_ON: "ON", PFX_CFG_VOLBEEP_OFF: "OFF"}

power_save_dict = {
    PFX_CFG_POWERSAVE_OFF: "OFF",
    PFX_CFG_POWERSAVE_30M: "30 min",
    PFX_CFG_POWERSAVE_60M: "60 min",
    PFX_CFG_POWERSAVE_3HR: "3 hrs",
}

lockout_dict = {
    PFX_CFG_LOCKOUT_INH: "Inhibit",
    PFX_CFG_LOCKOUT_CH1: "Toggle from ch 1",
    PFX_CFG_LOCKOUT_ALLCH: "Toggle from any ch",
}

ir_off_dict = {
    PFX_CFG_IRAUTO_OFF_NEVER: "Never",
    PFX_CFG_IRAUTO_OFF_1MIN: "After 1 min",
    PFX_CFG_IRAUTO_OFF_5MIN: "After 5 min",
    PFX_CFG_IRAUTO_OFF_IMMEDIATE: "Immediately",
}

ble_off_dict = {
    PFX_CFG_BLEAUTO_OFF_NEVER: "Never",
    PFX_CFG_BLEAUTO_OFF_1MIN: "After 1 min",
    PFX_CFG_BLEAUTO_OFF_5MIN: "After 5 min",
    PFX_CFG_BLEAUTO_OFF_IMMEDIATE: "Immediately",
}

ble_motor_dict = {
    PFX_CFG_BLE_MOTOR_CONTINUE: "Continue operation",
    PFX_CFG_BLE_MOTOR_STOP: "Stop motors",
}

command_dict = {
    EVT_COMMAND_NONE: "None",
    EVT_COMMAND_ALL_OFF: "All OFF",
    EVT_COMMAND_IR_LOCKOUT_ON: "IR Lockout ON",
    EVT_COMMAND_IR_LOCKOUT_OFF: "IR Lockout OFF",
    EVT_COMMAND_IR_LOCK_TOGGLE: "Toggle IR Lockout",
    EVT_COMMAND_ALL_MOTORS_OFF: "All Motors OFF",
    EVT_COMMAND_ALL_LIGHTS_OFF: "All Lights OFF",
    EVT_COMMAND_ALL_AUDIO_OFF: "All Audio OFF",
    EVT_COMMAND_RESTART: "Restart",
    EVT_COMMAND_RUN_SCRIPT: "Run Script",
}

motor_action_dict = {
    EVT_MOTOR_ESTOP: "Emergency Stop",
    EVT_MOTOR_STOP: "Stop",
    EVT_MOTOR_INC_SPD: "Increase Speed",
    EVT_MOTOR_DEC_SPD: "Decrease Speed",
    EVT_MOTOR_INC_SPD_BI: "Increase Speed (bi-dir)",
    EVT_MOTOR_DEC_SPD_BI: "Decrease Speed (bi-dir)",
    EVT_MOTOR_CHANGE_DIR: "Change Direction",
    EVT_MOTOR_SET_SPD: "Set Speed",
    EVT_MOTOR_SET_SPD_TIMED: "Set Speed with Duration",
    EVT_MOTOR_OSCILLATE: "Oscillate",
    EVT_MOTOR_OSCILLATE_BIDIR: "Oscillate (bi-dir)",
    EVT_MOTOR_OSCILLATE_BIDIR_WAIT: "Oscillate (bi-dir) with wait",
    EVT_MOTOR_RANDOM: "Random",
    EVT_MOTOR_RANDOM_BIDIR: "Random (bi-dir)",
    EVT_MOTOR_SOUND_MODULATED: "Sound Modulated",
}

ind_lightfx_dict = {
    EVT_LIGHTFX_NONE: "None",
    EVT_LIGHTFX_ON_OFF_TOGGLE: "On/Off",
    EVT_LIGHTFX_INC_BRIGHT: "Increase Brightness",
    EVT_LIGHTFX_DEC_BRIGHT: "Decrease Brightness",
    EVT_LIGHTFX_SET_BRIGHT: "Set Brightness",
    EVT_LIGHTFX_FLASH50_P: "Flash 50%, positive",
    EVT_LIGHTFX_FLASH50_N: "Flash 50%, negative",
    EVT_LIGHTFX_STROBE_P: "Strobe Flasher, positive",
    EVT_LIGHTFX_STROBE_N: "Strobe Flasher, negative",
    EVT_LIGHTFX_GYRALITE_P: "Gyralite, postive",
    EVT_LIGHTFX_GYRALITE_N: "Gyralite, negative",
    EVT_LIGHTFX_FLICKER: "Flicker",
    EVT_LIGHTFX_RAND_BLINK: "Random Blink",
    EVT_LIGHTFX_PHOTON_TORP: "Photon Torpedo",
    EVT_LIGHTFX_LASER_PULSE: "Laser Pulse",
    EVT_LIGHTFX_ENGINE_GLOW: "Engine Glow",
    EVT_LIGHTFX_LIGHTHOUSE: "Light House",
    EVT_LIGHTFX_BROKEN_LIGHT: "Broken Light",
    EVT_LIGHTFX_STATUS_IND: "Status Indicator",
    EVT_LIGHTFX_SOUND_MOD: "Sound Modulated",
    EVT_LIGHTFX_MOTOR_MOD: "Motor Modulated",
}

combo_lightfx_dict = {
    EVT_COMBOFX_NONE: "None",
    EVT_COMBOFX_LIN_SWEEP: "Linear Sweep",
    EVT_COMBOFX_BARGRAPH: "Bargraph",
    EVT_COMBOFX_KNIGHTRIDER: "Knight Rider",
    EVT_COMBOFX_EMCY_TWSONIC: "Twinsonic Style Flashers",
    EVT_COMBOFX_EMCY_WHELEN: "Strobe Style Flashers",
    EVT_COMBOFX_TIMES_SQ: "Times Square",
    EVT_COMBOFX_NOISE: "Noise",
    EVT_COMBOFX_TWINKLE_STAR: "Twinkling Stars",
    EVT_COMBOFX_TRAFFIC_SIG: "Traffic Lights",
    EVT_COMBOFX_SOUND_BAR: "Sound Bar",
    EVT_COMBOFX_ALT_FLASH: "Alternating Flashers",
    EVT_COMBOFX_LAVA_LAMP: "Lava Lamp",
    EVT_COMBOFX_LASER_CANNON: "Laser Cannon",
    EVT_COMBOFX_DRAGSTER: "Dragster Starter",
    EVT_COMBOFX_RUNWAY: "Airport Runway",
    EVT_COMBOFX_FORMULA1: "Formula 1 Lights",
}

evtid_dict = {
    EVT_ID_8879_TWO_BUTTONS: "Left + Right Button",
    EVT_ID_8879_LEFT_BUTTON: "Left Button",
    EVT_ID_8879_RIGHT_BUTTON: "Right Button",
    EVT_ID_8879_LEFT_INC: "Left Wheel Inc",
    EVT_ID_8879_LEFT_DEC: "Left Wheel Dec",
    EVT_ID_8879_RIGHT_INC: "Right Wheel Inc",
    EVT_ID_8879_RIGHT_DEC: "Rigth Wheel Dec",
    EVT_ID_8885_LEFT_FWD: "Left Joystick Fwd",
    EVT_ID_8885_LEFT_REV: "Left Joystick Rev",
    EVT_ID_8885_RIGHT_FWD: "Right Joystick Fwd",
    EVT_ID_8885_RIGHT_REV: "Right Joystick Rev",
    EVT_ID_8885_LEFT_CTROFF: "Left Joystick Centre",
    EVT_ID_8885_RIGHT_CTROFF: "Right Joystick Centre",
    EVT_ID_EV3_BEACON: "EV3 Beacon",
    EVT_ID_TEST_EVENT: "Test Event",
    EVT_ID_STARTUP_EVENT: "Startup Events 1-4",
    EVT_ID_STARTUP_EVENT2: "Startup Events 5-8",
    EVT_ID_RCTRAIN_UP: "RC Train Up",
    EVT_ID_RCTRAIN_DOWN: "RC Train Down",
    EVT_ID_RCTRAIN_STOP: "RC Train Stop",
    EVT_ID_RCTRAIN_HORN: "RC Train Horn",
}
