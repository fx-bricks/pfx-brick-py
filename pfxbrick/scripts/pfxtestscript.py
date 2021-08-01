import copy
import datetime
import time
from rich import print
from toolbox import *
from pfxbrick import *

TMP_FILE = "~/tmp/test_script.txt"


def copy_script_file(brick, text):
    file = full_path(TMP_FILE)
    fp, fn = split_path(file)
    brick.refresh_file_dir()
    fileID = brick.filedir.find_available_file_id()
    with open(file, "wb") as f:
        for line in text.splitlines():
            f.write("%s\n" % (line))
    crc32 = get_file_crc32(file)
    print("Copying file %s with CRC32=0x%08X" % (file, crc32))
    brick.put_file(file, fileID)
    fcrc = 0
    while fcrc == 0:
        time.sleep(1)
        brick.refresh_file_dir()
        f0 = brick.filedir.get_file_dir_entry(fileID)
        fcrc = f0.crc32
    test_result(
        "Copied file directory %s CRC32=0x%08X" % (file, f0.crc32), f0.crc32 == crc32
    )


TEST_SCRIPT_LIGHTS = """
# Test Lights
light all off
wait 0.2
light [1] on
wait 0.2
light all off
wait 0.2

light [2, 3] flash 0.5 1.0
wait 3.0
light [2, 3] off
"""


def test_script_lights(brick):
    return True


TEST_SCRIPT_VARS = """
# Test vars
set $A = 1.0
set $B = 1.5
light all off
light [4] on
wait $A
light [4] off
wait $B
light [4] on
wait 0.5
light [4] off
"""
