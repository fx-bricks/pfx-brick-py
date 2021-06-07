import time
import datetime
import zlib
from datetime import datetime
from rich import print
from rich.console import Console

from pfxbrick import *

console = Console()


def get_file_crc32(fn):
    with open(fn, "rb") as fp:
        fb = fp.read()
    return zlib.crc32(fb) & 0xFFFFFFFF


def flash_read(brick, add, num_bytes):
    rbytes = []
    for x in range(0, num_bytes, 60):
        msg = [PFX_CMD_READ_FLASH]
        msg.extend(uint32_to_bytes(add + x))
        msg.append(60)
        res = brick.send_raw_icd_command(msg)
        rbytes.extend(res[1:61])
    return rbytes[0:num_bytes]


def i2c_write(brick, add, data):
    brick.send_raw_icd_command([PFX_CMD_WRITE_I2C, 0x30, add, data])


def i2c_read(brick, add):
    res = brick.send_raw_icd_command([PFX_CMD_READ_I2C, 0x30, add])
    nbytes = res[1]
    return res[2 : 2 + nbytes]


def test_dac(brick):

    registers = [
        (4, 7),
        (5, 0x94),
        (6, 0x20),
        (7, 0),
        (8, 0),
        (11, 0x88),
        (12, 0x84),
        (13, 0),
        (14, 0x80),
        (15, 0x80),
        (16, 0x08),
        (25, 0x00),
        (26, 0x01),
        (27, 0),
        (30, 0x01),
        (60, 0x19),
        (63, 0xB6),
    ]
    ok = True
    i2c_write(b, 0, 0)
    for reg in registers:
        v = i2c_read(b, reg[0])
        if not v[0] == reg[1]:
            ok = False
    return ok


def test_millisec(brick):
    s1 = brick.get_current_state()
    t1 = s1.millisec_count

    time.sleep(1)
    s2 = brick.get_current_state()
    t2 = s2.millisec_count

    if t2 < t1:
        tdiff = t2 + (0xFFFF - t1) + 1
    else:
        tdiff = t2 - t1
    if abs(tdiff - 1000) < 10:
        return True
    return False


def test_bt_status(brick):
    time.sleep(0.5)
    res = brick.send_raw_icd_command([PFX_CMD_GET_BT_STATUS])
    ok = True
    if res[1] == 0:
        return True
    tests = [(7, 0), (9, 0), (11, 0x00C0), (13, 0x0002)]
    for test in tests:
        if not uint16_toint(res[test[0] : test[0] + 2]) == test[1]:
            console.log(
                "[red]Bluetooth config error. Read %X, expecting %X"
                % (res[test[0] : test[0] + 2], test[1])
            )
            ok = False
    return ok


def test_config(brick):
    r = flash_read(brick, 0xFFF000, 60)
    values = [
        (0, 0x36),
        (1, 0xC0),
        (2, 0xC0),
        (3, 0xC0),
        (4, 0xC0),
        (5, 0xC0),
        (6, 0xC0),
        (7, int(bytes("M", "utf-8")[0])),
        (8, int(bytes("y", "utf-8")[0])),
        (9, int(bytes(" ", "utf-8")[0])),
        (10, int(bytes("P", "utf-8")[0])),
        (11, int(bytes("F", "utf-8")[0])),
        (12, int(bytes("x", "utf-8")[0])),
    ]
    ok = True
    for v in values:
        if not r[v[0]] == v[1]:
            console.log(
                "[red]Readback config error. Read %X, expecting %X at %X"
                % (r[v[0]], v[1], v[0])
            )
            ok = False
    return ok


def test_light_ch(brick, ch):
    ok = True
    brick.light_off(ch)
    brick.light_on(ch)
    st = brick.get_current_state()
    if not st.lights[ch - 1].active:
        ok = False
    if not st.lights[ch - 1].target_level == 0xFF:
        ok = False
    if not st.lights[ch - 1].current_level == 0xFF:
        ok = False

    iprev = 0xFF
    tinit = datetime.now()
    tnow = datetime.now()
    brick.light_fx(
        ch, EVT_LIGHTFX_ON_OFF_TOGGLE, [0, EVT_FADE_TIME_600MS, 0, EVT_TRANSITION_OFF]
    )
    while (tnow - tinit).total_seconds() < 1.0:
        st = brick.get_current_state()
        if st.lights[ch - 1].active:
            ok = False
            console.log("[red]Light channel error: channel %d active" % (ch))
        if not st.lights[ch - 1].target_level == 0x00:
            ok = False
            console.log(
                "[red]Light channel error: channel %d target value=%X, expecting 0"
                % (ch, st.lights[ch - 1].target_level)
            )
        inow = st.lights[ch - 1].current_level
        if inow > iprev:
            ok = False
            console.log(
                "[red]Light channel error: channel %d fade %d not < %d"
                % (ch, inow, iprev)
            )
        time.sleep(0.2)
        tnow = datetime.now()
        iprev = inow
    return ok


def test_combo_light_fx(brick):
    for fx in combo_fx:
        brick.combo_light_fx(fx[1], fx[2])


def check_motor_speed(brick, ch, speed):
    st = brick.get_current_state()
    eq_speed = int((abs(speed) / 100.0) * 63)
    eq_speed = int((eq_speed * 255) / 64)
    eq_pwm = eq_speed
    if speed < 0:
        eq_speed = (~eq_speed + 1) & 0xFF
    ok = True
    if not st.motors[ch - 1].target_speed == eq_speed:
        ok = False
        console.log(
            "[red]Motor channel %d error. target_speed should be %X, read=%X"
            % (ch, eq_speed, st.motors[ch - 1].target_speed)
        )
    if not st.motors[ch - 1].current_speed == eq_speed:
        ok = False
        console.log(
            "[red]Motor channel %d error. current_speed should be %X, read=%X"
            % (ch, eq_speed, st.motors[ch - 1].current_speed)
        )
    if not abs(st.motors[ch - 1].pwm_speed - eq_pwm) < 5:
        ok = False
        console.log(
            "[red]Motor channel %d error. pwm_speed should be %X, read=%X"
            % (ch, eq_pwm, st.motors[ch - 1].pwm_speed)
        )
    return ok


def test_motor_channel(brick, ch, speed):
    brick.stop_motor(ch)
    time.sleep(0.5)
    ok1 = check_motor_speed(brick, ch, 0)
    brick.set_motor_speed(ch, speed)
    time.sleep(1.5)
    ok2 = check_motor_speed(brick, ch, speed)
    brick.stop_motor(ch)
    time.sleep(0.5)
    ok3 = check_motor_speed(brick, ch, 0)
    return ok1 & ok2 & ok3


def test_file_transfer(fn, fid=0):
    crc32 = get_file_crc32(fn)
    console.log("Copying file %s with CRC32=%X" % (fn, crc32))
    b.put_file(fn, fid)
    fcrc = 0
    while fcrc == 0:
        time.sleep(1)
        b.refresh_file_dir()
        f0 = b.filedir.get_file_dir_entry(fid)
        fcrc = f0.crc32
    test_result("Copied file directory %s CRC32=%X" % (fn, f0.crc32), f0.crc32 == crc32)
    console.log("Getting file %s with CRC32=%X" % (fn, crc32))
    fnr = fn + ".rx"
    b.get_file(fid, fnr)
    read_crc32 = get_file_crc32(fnr)
    test_result("Read back file %s CRC32=%X" % (fnr, read_crc32), crc32 == read_crc32)


def test_result(desc, result):
    if result:
        res = ":green_circle:"
    else:
        res = ":red_circle:"
    console.log(res, ":", desc)


combo_fx = [
    ("Linear Sweep R-L", EVT_COMBOFX_LIN_SWEEP, [2, 6, 0, 1], 0xFF),
    ("Linear Sweep L-R", EVT_COMBOFX_LIN_SWEEP, [2, 6, 0, 2], 0xFF),
    ("Bargraph Sweep R-L", EVT_COMBOFX_BARGRAPH, [4, 3, 0, 1], 0xFF),
    ("Bargraph Sweep L-R", EVT_COMBOFX_BARGRAPH, [4, 3, 0, 2], 0xFF),
    ("Knight Rider", EVT_COMBOFX_KNIGHTRIDER, [6, 6, 0, 0], 0xFF),
    ("Twinsonic Flashers", EVT_COMBOFX_EMCY_TWSONIC, [2, 1, 2, 0], 0x3F),
    ("Whelen Flashers", EVT_COMBOFX_EMCY_WHELEN, [10, 2, 2, 0], 0x3F),
    ("Times Square", EVT_COMBOFX_TIMES_SQ, [1, 10, 0, 0], 0xFF),
    ("Noise", EVT_COMBOFX_NOISE, [1, 9, 0, 0], 0xFF),
    ("Twinkling Stars", EVT_COMBOFX_TWINKLE_STAR, [8, 15, 0, 0], 0xFF),
    ("Traffic Lights", EVT_COMBOFX_TRAFFIC_SIG, [4, 6, 2, 0], 0xFF),
    ("Alternating Flashers", EVT_COMBOFX_ALT_FLASH, [4, 9, 6, 255], 0xFF),
    ("Lava Lamp", EVT_COMBOFX_LAVA_LAMP, [4, 0, 0, 0], 0xFF),
    ("Runway", EVT_COMBOFX_RUNWAY, [0, 0, 0, 0], 0xFF),
]

from rich.table import Table

console = Console()

b = PFxBrick()
b.open()
b.get_status()
icd = b.get_icd_rev()
name = b.get_name()

table = Table(show_header=True, header_style="bold blue")
bid = "[light_slate_blue]%s [bold cyan]%s" % (b.product_id, b.product_desc)
table.add_column(bid, width=72)
table.add_row("Serial Number         : [bold cyan]%s" % (b.serial_no))
table.add_row("ICD Version           : [bold green]%s" % (icd))
table.add_row(
    "Firmware Version      : [bold green]%s [reset]build [bold green]%s"
    % (b.firmware_ver, b.firmware_build)
)
table.add_row("USB vendor ID         : [cyan]0x%04X" % (b.usb_vid))
table.add_row("USB product ID        : [cyan]0x%04X" % (b.usb_pid))
table.add_row(
    "Status                : 0x%02X %s" % (b.status, get_status_str(b.status))
)
if b.error:
    table.add_row(
        "Errors                : [red]0x%02X %s" % (b.error, get_error_str(b.error))
    )
else:
    table.add_row(
        "Errors                : [green]0x%02X %s" % (b.error, get_error_str(b.error))
    )

table.add_row("Name                  : [bold yellow]%s" % (name))
console.print(table)

print(b.get_current_state())
print(b.get_fs_state())
print(b.get_bt_state())

table = Table(show_header=False, width=76)
table.add_row("[bold orange1]Testing")
console.print(table)

with console.status("Testing...") as status:
    res = test_config(b)
    test_result("Configuration flash test", res)
    res = test_dac(b)
    test_result("DAC register test", res)

    res = test_millisec(b)
    test_result("Millisec timer test", res)

    res = test_bt_status(b)
    test_result("Bluetooth configuration", res)

    res = test_motor_channel(b, 1, 50)
    test_result("Motor channel A +50", res)
    res = test_motor_channel(b, 1, -50)
    test_result("Motor channel A -50", res)

    res = test_motor_channel(b, 2, 75)
    test_result("Motor channel B +75", res)
    res = test_motor_channel(b, 2, -75)
    test_result("Motor channel B -75", res)

    for ch in range(1, 9):
        res = test_light_ch(b, ch)
        test_result("Light channel %d test" % (ch), res)

    for fx in combo_fx:
        b.combo_light_fx(fx[1], fx[2])
        time.sleep(1.5)
        st = b.get_current_state()
        test_result(fx[0], st.lightmask == fx[3])
        if not st.lightmask == fx[3]:
            console.log(
                "[red]Combo light fx %s output channels=0x%02X, expected 0x%02X"
                % (fx[0], st.lightmask, fx[3])
            )
        b.light_off(list(range(1, 9)))

files = [
    (0, "sin150Hz.wav", 0x0000, 0x000204CE, 0x0000002C),
    (1, "pink6dB.wav", 0x0000, 0x000204CE, 0x0000002C),
    (2, "yamanote16pcm22k.wav", 0x0000, 0x00054A80, 0x0000002C),
]

for file in files:
    test_file_transfer(file[1], file[0])

b.refresh_file_dir()
for file in files:
    f = b.filedir.get_file_dir_entry(file[0])
    test_result(
        "File %s attributes=%X" % (file[1], f.attributes), f.attributes == file[2]
    )
    test_result("File %s UserData1=%X" % (file[1], f.userData1), f.userData1 == file[3])
    test_result("File %s UserData2=%X" % (file[1], f.userData2), f.userData2 == file[4])

b.close()
# b.play_audio_file(7)
# time.sleep(5)
# print("Seeking...")
# Fs = 22050
# bps = 2
# # 30 sec seek
# offs = int(30 * Fs * bps)
# b0 = (offs >> 24) & 0xFF
# b1 = (offs >> 16) & 0xFF
# b2 = (offs >> 8) & 0xFF
# b3 = offs & 0xFF
# res = b.send_raw_icd_command([0x44, 0x06, b0, b1, b2, b3])
# time.sleep(5)

# print("Seeking...")
# offs = int(60 * Fs * bps)
# b0 = (offs >> 24) & 0xFF
# b1 = (offs >> 16) & 0xFF
# b2 = (offs >> 8) & 0xFF
# b3 = offs & 0xFF
# res = b.send_raw_icd_command([0x44, 0x06, b0, b1, b2, b3])
# time.sleep(5)
# b.stop_audio_file(7)
