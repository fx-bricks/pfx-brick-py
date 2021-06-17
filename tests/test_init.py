# system modules
import math, os.path
import sys
import pytest

# my modules
from pfxbrick import *


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
