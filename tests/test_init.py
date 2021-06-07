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
    assert len(bricks) == 0
