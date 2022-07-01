# system modules
import copy
import math
import os.path
import sys

import pytest

# my modules
from pfxbrick import *
from pfxbrick.pfx import *


def test_pfxaction_init():
    a = PFxAction()
    assert a is not None
    assert type(a) == PFxAction


def test_clear():
    a = PFxAction()
    a.command = 0x01
    a.motorActionId = 0x02
    a.motorParam1 = 0x03
    a.motorParam2 = 0x04
    a.lightFxId = 0x05
    a.soundFxId = 0x06
    assert a.command == 0x01
    assert a.motorActionId == 0x02
    assert a.motorParam1 == 0x03
    assert a.motorParam2 == 0x04
    assert a.lightFxId == 0x05
    assert a.soundFxId == 0x06
    a.clear()
    assert a.command == 0x00
    assert a.motorActionId == 0x00
    assert a.motorParam1 == 0x00
    assert a.motorParam2 == 0x00
    assert a.lightFxId == 0x00
    assert a.soundFxId == 0x00


def test_set_motor():
    a = PFxAction()
    a.set_motor_speed(1, 50)
    assert a.motorParam1 == 0x9F
    assert a.motorActionId == EVT_MOTOR_SET_SPD | 0x01


def test_stop_motor():
    a = PFxAction()
    a.stop_motor([1, 2])
    assert a.motorActionId == EVT_MOTOR_ESTOP | 0x03


def test_light_on():
    a = PFxAction()
    a.light_on([1, 8])
    assert a.lightFxId == EVT_LIGHTFX_ON_OFF_TOGGLE
    assert a.lightOutputMask == 0x81
    assert a.lightParam4 == EVT_TRANSITION_ON


def test_equality():
    a1 = PFxAction()
    a2 = PFxAction()
    assert a1.is_empty()
    assert a1 == a2
    a1.lightFxId = 5
    assert not a1 == a2
    assert not a1.is_empty()
    a2.lightFxId = 5
    assert a1 == a2
    a3 = copy.copy(a1)
    assert a1 == a3
    a3.soundFxId = 3
    assert not a1 == a3


def test_script_str():
    a1 = PFxAction()
    a1.set_motor_speed([1, 2], 50)
    assert a1.motorParam1 == 0x9F
    assert a1.motorActionId == EVT_MOTOR_SET_SPD | 0x03
    s1 = a1.to_event_script_str(0x3C)
    assert "event 0x3C" in s1
    assert "motor [a, b]" in s1
    assert "fx 0x7 159 0" in s1

    a2 = PFxAction()
    a2.light_on([1, 8])
    s2 = a2.to_event_script_str(0x40)
    assert "event 0x40" in s2
    assert "light [1, 8]" in s2
    assert "fx 0x01 0 0 0 1 0" in s2
