# system modules
import math
import os.path
import sys

import pytest

# my modules
from pfxbrick import *
from pfxbrick.pfxhelpers import *


def test_pfxbrick_init():
    b = PFxBrick()
    assert not b.is_open
    assert b.dev is None


def test_find_bricks():
    bricks = find_bricks(show_list=False)
    assert len(bricks) == 0 or len(bricks) == 1


def test_config():
    c1 = PFxConfig()
    c2 = PFxConfig()
    assert c1 == c2
    c1.settings.notchCount = 7
    assert not c1 == c2
    c2.settings.notchCount = 7
    assert c1 == c2

    c1.motors[0].invert = True
    c2.motors[1].invert = True
    assert not c1 == c2
    c1.motors[1].invert = True
    c2.motors[0].invert = True
    assert c1 == c2

    c1.settings.notchBounds[0] = 1
    c1.settings.notchBounds[1] = 2
    c1.settings.notchBounds[2] = 4
    c1.settings.notchBounds[3] = 8
    assert not c1 == c2
    c2.settings.notchBounds[0] = 1
    c2.settings.notchBounds[1] = 2
    c2.settings.notchBounds[2] = 4
    c2.settings.notchBounds[3] = 8
    assert c1 == c2


def test_helpers():
    b1 = bounds_from_notchcount(4)
    assert b1 == [64, 128, 191]
    n1 = notch_ranges_from_bounds(b1)
    assert n1 == [(0, 32, 64), (64, 96, 128), (128, 160, 191), (191, 223, 255)]
    s1 = notch_from_speed(10, b1)
    s2 = notch_from_speed(165, b1)
    s3 = notch_from_speed(192, b1)
    assert s1 == 0
    assert s2 == 2
    assert s3 == 3


def test_conversions():
    s1 = "speed ch 2 right up"
    e1 = script_ir_mask_to_address(s1)
    assert e1 == EVT_8879_RIGHT_INC + 1
    s2 = "joy ch 1 left down"
    e2 = script_ir_mask_to_address(s2)
    assert e2 == EVT_8885_LEFT_REV + 0
    s3 = "speed ch 3 left button"
    e3 = script_ir_mask_to_address(s3)
    assert e3 == EVT_8879_LEFT_BUTTON + 2
