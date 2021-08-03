from pfxbrick.pfx import *

###############################################################################

TEST_SCRIPT_LIGHTS = """
# Test Lights
light all off
wait 0.5
light [1] on
wait 0.5
light all off
wait 0.5

light [2, 3] flash 0.4 0.6
wait 2.5
light [2, 3] off
"""
TEST_SCRIPT_LIGHTS_RESULTS = [
    (0, 0.5, 255),
    (0, 0.5, 0),
    (1, 0.5, 255),
    (2, 0.5, 255),
    (1, 0.4, 0),
    (2, 0.4, 0),
    (1, 0.6, 255),
    (2, 0.6, 255),
    (1, 0.4, 0),
    (2, 0.4, 0),
    (1, 0.6, 255),
    (2, 0.6, 255),
    (1, 0.4, 0),
    (2, 0.4, 0),
]

###############################################################################

TEST_SCRIPT_VARS = """
# Test vars
set $A = 1.0
set $B = 1.5
light all off
wait 0.5
light [4] on
wait $A
light [4] off
wait $B
light [4] on
wait 0.5
light [4] off
"""
TEST_SCRIPT_VARS_RESULTS = [
    (3, 0.5, 255),
    (3, 1, 0),
    (3, 1.5, 255),
    (3, 0.5, 0),
]

###############################################################################

TEST_SCRIPT_CONFIG = """
# Test setting configuration
light all off
wait 0.5

set config nc = 5
set config bass = 3
set config treble = -5
set config acc thr = 42
set config volume = 80
set config motor a acc = 14
set config motor b decel = 4
set config rate thr = 88
set config nb 3 = 0x90
set config bright 5 = 55
set config motor a invert = 0
set config motor b invert = 1
set config motor a v0 = 10
set config motor a v1 = 33
set config motor a v2 = 99

wait 1
"""

###############################################################################

TEST_SCRIPT_REPEAT = """
# Looping test
set $A = 0.2
set $B = 0.4
set $C = 0.6
light all off
wait 0.5
repeat 3 {
  repeat 2 {
    light [1] on
    wait $A
    light [1] off
    wait $A
  }
  light [2] on
  wait $B
  light [2] off
  wait $C
}
light all off
"""
TEST_SCRIPT_REPEAT_RESULTS = [
    (0, 0.5, 255),
    (0, 0.2, 0),
    (0, 0.2, 255),
    (0, 0.2, 0),
    (1, 0.2, 255),
    (1, 0.4, 0),
    (0, 0.6, 255),
    (0, 0.2, 0),
    (0, 0.2, 255),
    (0, 0.2, 0),
    (1, 0.2, 255),
    (1, 0.4, 0),
    (0, 0.6, 255),
    (0, 0.2, 0),
    (0, 0.2, 255),
    (0, 0.2, 0),
    (1, 0.2, 255),
    (1, 0.5, 0),
]

###############################################################################

TEST_SCRIPT_EVENTS = """
# Test event setting
light all off
wait 0.5

event startup 4 {
  ir off
}
event button long {
  sound play 5
}
event ir joy ch 3 right up {
  sound stop all
}
event ble disconnect {
  sound fx 6 7 3 0
}
event button down {
  sound play 9 repeat
  light 7 on
}
# set EVT_BUTTON_UP with its address at 0x47
event 0x47 {
  light [5] fx 11 [1, 6]
}

event 0x51 {
  motor b stop
}
event 0x52 {
  motor a speed 64
}
event 0x53 {
  motor 1 servo -45
}

wait 1
"""

TEST_SCRIPT_EVENTS_TESTS = [
    (EVT_STARTUP_EVENT4, "EVT_STARTUP_EVENT4"),
    (EVT_BUTTON_LONGPRESS, "EVT_BUTTON_LONGPRESS"),
    (EVT_8885_RIGHT_FWD | 0x02, "EVT_8885_RIGHT_FWD"),
    (EVT_BLE_DISCONNECT, "EVT_BLE_DISCONNECT"),
    (EVT_BUTTON_DOWN, "EVT_BUTTON_DOWN"),
    (EVT_BUTTON_UP, "EVT_BUTTON_UP"),
    (0x51, "0x51 motor b stop"),
    (0x52, "0x52 motor a speed 64"),
    (0x53, "0x53 motor 1 servo -45"),
]

###############################################################################
