import argparse
import base64
import copy
import time
import datetime
import random
import tempfile
import zlib
from datetime import datetime
from rich import print
from rich.console import Console
from rich.table import Table

from pfxbrick.pfxtesthelpers import *
from pfxbrick.pfxtestdata import *
from pfxbrick import *

console = Console()


TMP_FILE = tempfile.gettempdir() + os.sep + "test_script.txt"


def full_path(file):
    """Returns the fully expanded path of a file"""
    if "~" in str(file):
        return os.path.expanduser(file)
    return os.path.expanduser(os.path.abspath(file))


def split_path(file):
    """Returns a tuple containing a file's (directory, name.ext)"""
    if os.path.isdir(file):
        return full_path(file), None
    return os.path.split(full_path(file))


def copy_script_file(brick, text):
    file = full_path(TMP_FILE)
    fp, fn = split_path(file)
    brick.refresh_file_dir()
    fileID = brick.filedir.find_available_file_id()
    with open(file, "w") as f:
        for line in text.splitlines():
            f.write("%s\n" % (line))
    crc32 = get_file_crc32(file)
    console.log("Copying file [cyan]%s[/] with CRC32=0x%08X" % (fn, crc32))
    brick.put_file(file, fileID)
    fcrc = 0
    while fcrc == 0:
        time.sleep(1)
        brick.refresh_file_dir()
        f0 = brick.filedir.get_file_dir_entry(fileID)
        fcrc = f0.crc32
    test_result(
        "Copied file [cyan]%s[/] CRC32=0x%08X" % (fn, f0.crc32), f0.crc32 == crc32
    )
    return fileID


def event_recorder(brick, interval, duration):
    time.sleep(interval)
    events = []
    tinit = datetime.now()
    tnow = datetime.now()
    tprev = tnow
    state_now = brick.get_current_state()
    prev_state = copy.deepcopy(state_now)
    while (tnow - tinit).total_seconds() < duration:
        time.sleep(interval)
        tnow = datetime.now()
        state_now = brick.get_current_state()
        tdiff = (tnow - tprev).total_seconds()
        for ch in range(8):
            if state_now.lights[ch].target_level != prev_state.lights[ch].target_level:
                event = (ch, tdiff, state_now.lights[ch].target_level)
                events.append(event)
                tprev = tnow
        prev_state = copy.deepcopy(state_now)
    return events


def check_results(events, results, tolerance=0.175):
    # print(events, results)
    if not len(results) == len(events):
        print(events, results)
        print("[red]%s is not %s" % (len(results), len(events)))
        return False
    for event, result in zip(events, results):
        if not event[0] == result[0]:
            print(events, results)
            print("[red]%s is not %s" % (event[0], result[0]))
            return False
        if not abs(event[1] - result[1]) < tolerance:
            print(events, results)
            print("[red]%s is not %s" % (event[1], result[1]))
            return False
        if not event[2] == result[2]:
            print(events, results)
            print("[red]%s is not %s" % (event[2], result[2]))
            return False
    return True


###############################################################################


def do_test_script_lights(brick, fid):
    brick.run_script(fid)
    events = event_recorder(brick, 0.1, 5)
    brick.stop_script()
    return check_results(events, TEST_SCRIPT_LIGHTS_RESULTS)


###############################################################################


def do_test_script_vars(brick, fid):
    brick.run_script(fid)
    events = event_recorder(brick, 0.1, 5.0)
    brick.stop_script()
    return check_results(events, TEST_SCRIPT_VARS_RESULTS)


###############################################################################


def do_test_script_config(brick, fid):
    old_settings = snapshot_config(brick)
    brick.run_script(fid)
    time.sleep(2)
    brick.stop_script()
    brick.get_config()
    new_settings = [
        (brick.config.settings.notchCount, 5),
        (brick.config.settings.rapidAccelThr, 42),
        (brick.config.audio.bass, 3),
        (brick.config.audio.treble, 251),
        (brick.config.audio.defaultVolume, 80),
        (brick.config.motors[0].accel, 14),
        (brick.config.motors[1].decel, 4),
        (brick.config.settings.brakeDecelThr, 88),
        (brick.config.settings.notchBounds[2], 0x90),
        (brick.config.lights.startupBrightness[4], 55),
        (brick.config.motors[0].invert, False),
        (brick.config.motors[1].invert, True),
        (brick.config.motors[0].vmin, 10),
        (brick.config.motors[0].vmid, 33),
        (brick.config.motors[0].vmax, 99),
    ]
    ok = True
    for setting in new_settings:
        if not setting[0] == setting[1]:
            test_result(
                "Read back %s should be %s" % (setting[0], setting[1]),
                (setting[0] == setting[1]),
            )
            ok = False
    test_result("Set configuration values from script", ok)
    restore_config(brick, old_settings)
    return ok


###############################################################################


def do_test_script_repeat(brick, fid):
    brick.run_script(fid)
    events = event_recorder(brick, 0.1, 6.5)
    brick.stop_script()
    return check_results(events, TEST_SCRIPT_REPEAT_RESULTS)


###############################################################################


def do_test_script_events(brick, fid):
    ok = True
    copies = []
    for test in TEST_SCRIPT_EVENTS_TESTS:
        ainit = brick.get_action_by_address(test[0])
        copies.append(ainit)
    brick.run_script(fid)
    time.sleep(2)
    brick.stop_script()
    for test, ainit in zip(TEST_SCRIPT_EVENTS_TESTS, copies):
        achange = brick.get_action_by_address(test[0])
        if test[0] == EVT_STARTUP_EVENT4:
            result = achange.command == EVT_COMMAND_IR_LOCKOUT_ON
        elif test[0] == EVT_BUTTON_LONGPRESS:
            result = (achange.soundFxId == EVT_SOUND_PLAY_ONCE) and (
                achange.soundFileId == 5
            )
        elif test[0] == EVT_8885_RIGHT_FWD | 0x02:
            result = achange.command == EVT_COMMAND_ALL_AUDIO_OFF
        elif test[0] == EVT_BLE_DISCONNECT:
            result = (
                (achange.soundFxId == EVT_SOUND_PLAY_NTIMES)
                and (achange.soundFileId == 7)
                and (achange.soundParam1 == 3)
                and (achange.soundParam2 == 0)
            )
        elif test[0] == EVT_BUTTON_DOWN:
            result = (
                (achange.soundFxId == EVT_SOUND_PLAY_CONT)
                and (achange.soundFileId == 9)
                and (achange.lightFxId == EVT_LIGHTFX_ON_OFF_TOGGLE)
                and (achange.lightOutputMask == 0x40)
            )
        elif test[0] == EVT_BUTTON_UP:
            result = (
                (achange.lightFxId == EVT_LIGHTFX_FLICKER)
                and (achange.lightParam1 == 1)
                and (achange.lightParam2 == 6)
            )
        elif test[0] == 0x51:
            result = (
                achange.motorActionId & EVT_MOTOR_ACTION_ID_MASK
            ) == EVT_MOTOR_STOP
        elif test[0] == 0x52:
            result = (
                (
                    (achange.motorActionId & EVT_MOTOR_ACTION_ID_MASK)
                    == EVT_MOTOR_SET_SPD
                )
                and (achange.motorParam1 == 144)
                and (achange.motorParam2 == 0)
            )
        elif test[0] == 0x53:
            result = (
                (achange.motorActionId & EVT_MOTOR_ACTION_ID_MASK)
                == EVT_MOTOR_SET_SERVO
            ) and (achange.motorParam1 == 0x3)
        if not result:
            test_result(
                "Scripted startup event did not make correct change to %s" % (test[1]),
                result,
            )
            ok = False
    for test, ainit in zip(TEST_SCRIPT_EVENTS_TESTS, copies):
        brick.set_action_by_address(test[0], ainit)
    time.sleep(2)
    for test, ainit in zip(TEST_SCRIPT_EVENTS_TESTS, copies):
        arestore = brick.get_action_by_address(test[0])
        result = ainit == arestore
        if not result:
            ok = False
            test_result(
                "Scripted startup event did not restore to %s" % (test[1]), result
            )
    return ok


###############################################################################

SCRIPT_TESTS = [
    (TEST_SCRIPT_LIGHTS, do_test_script_lights, "Lighting"),
    (TEST_SCRIPT_VARS, do_test_script_vars, "Variables"),
    (TEST_SCRIPT_REPEAT, do_test_script_repeat, "Repeat Loops"),
    (TEST_SCRIPT_EVENTS, do_test_script_events, "Events"),
    (TEST_SCRIPT_CONFIG, do_test_script_config, "Configuration"),
]


def test_scripts(brick):
    for test in SCRIPT_TESTS:
        fid = copy_script_file(brick, test[0])
        time.sleep(0.2)
        result = test[1](brick, fid)
        test_result("Executed test script [cyan]%s[/]" % (test[2]), result)
        brick.remove_file(fid)
        time.sleep(1)
        os.remove(TMP_FILE)


def snapshot_config(brick):
    brick.get_config()
    backup_config = copy.deepcopy(brick.config)
    return backup_config


def restore_config(brick, config):
    if config is not None:
        brick.config = copy.deepcopy(config)
        brick.set_config()
        console.log("Writing back original configuration values...")
        time.sleep(3)


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
    i2c_write(brick, 0, 0)
    for reg in registers:
        v = i2c_read(brick, reg[0])
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
    console.log("[red]Millisec timer test error %d ms instead of 1000 ms" % (tdiff))
    return False


def test_sec(brick):
    test_count = 0
    ok = False
    while test_count < 3 and not ok:
        s1 = brick.get_current_state()
        t1 = s1.slow_count
        time.sleep(3)
        s2 = brick.get_current_state()
        t2 = s2.slow_count

        if t2 < t1:
            tdiff = t2 + (0xFFFF - t1) + 1
        else:
            tdiff = t2 - t1
        if abs(tdiff - 3) < 1:
            ok = True
        test_count += 1
    if not ok:
        console.log("[red]Second timer test error %d sec instead of 3 sec" % (tdiff))
    return ok


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
    ok = True
    backup_config = snapshot_config(brick)
    brick.config.audio.bass = 0x03
    brick.config.lights.defaultBrightness = 0x40
    brick.config.lights.startupBrightness[5] = 0x55
    brick.config.settings.notchBounds[6] = 0xF0
    brick.set_config()
    console.log("Writing new configuration test values...")
    time.sleep(3)
    brick.get_config()
    test_values = [
        (brick.config.audio.bass, 0x03),
        (brick.config.lights.defaultBrightness, 0x40),
        (brick.config.lights.startupBrightness[5], 0x55),
        (brick.config.settings.notchBounds[6], 0xF0),
    ]
    for v in test_values:
        if v[0] != v[1]:
            console.log(
                "[red]Readback config error. Read %X, expecting %X" % (v[0], v[1])
            )
            ok = False
    restore_config(brick, backup_config)
    test_values = [
        (brick.config.audio.bass, backup_config.audio.bass),
        (brick.config.lights.defaultBrightness, backup_config.lights.defaultBrightness),
        (
            brick.config.lights.startupBrightness[5],
            backup_config.lights.startupBrightness[5],
        ),
        (brick.config.settings.notchBounds[6], backup_config.settings.notchBounds[6]),
    ]
    for v in test_values:
        if v[0] != v[1]:
            console.log(
                "[red]Readback config error. Read %X, expecting %X" % (v[0], v[1])
            )
            ok = False
    return ok


def test_light_ch(brick, ch):
    ok = True
    brick.light_off(ch)
    time.sleep(0.2)
    brick.light_on(ch)
    time.sleep(0.2)
    st = brick.get_current_state()
    if not st.lights[ch - 1].active:
        console.log("[red]Light channel error: channel %d not active" % (ch))
        ok = False
    if not st.lights[ch - 1].target_level == 0xFF:
        console.log(
            "[red]Light channel error: channel %d wrong target level 0x%02X"
            % (ch, st.lights[ch - 1].target_level)
        )
        ok = False
    if not st.lights[ch - 1].current_level == 0xFF:
        console.log(
            "[red]Light channel error: channel %d wrong current level 0x%02X"
            % (ch, st.lights[ch - 1].current_level)
        )
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


def test_button_events(brick, testtime=10):
    console.log("Waiting %d sec for button events..." % (testtime))
    elapsed = 0
    bstate = False
    nevents = 0
    while elapsed < testtime:
        time.sleep(0.2)
        elapsed += 0.2
        st = brick.get_current_state()
        if not bstate and st.status_latch2 & EVT_SOURCE2_BUTTON:
            test_result("Button press down detected at %.1f sec" % (elapsed), True)
            nevents += 1
            bstate = True
        elif bstate and not st.status_latch2 & EVT_SOURCE2_BUTTON:
            test_result("Button release up detected at %.1f sec" % (elapsed), True)
            bstate = False
            nevents += 1
    console.log("Detected %d button events" % (nevents))


def test_audio_playback(brick, fileid):
    brick.get_config()
    st = brick.get_current_state()
    old_vol = st.volume
    brick.set_volume(30)
    brick.play_audio_file(fileid)
    brick.refresh_file_dir()
    fd = brick.filedir.get_file_dir_entry(fileid)
    if fd is None:
        console.log("[red]Audio file %d does not exist" % (fileid))
        return False
    test_result("File %d is an audio file" % (fileid), fd.is_audio_file())
    sr = 22050
    ws = 2
    if (fd.attributes & PFX_WAV_ATTR_SAMPLE_RATE_MASK) == PFX_WAV_ATTR_SAMPLE_RATE_11K:
        sr = 11025
    if (fd.attributes & PFX_WAV_ATTR_QUANTIZATION_MASK) == PFX_WAV_ATTR_QUANTIZATION_8:
        ws = 1
    file_dur = fd.userData1 * 1.0 / sr / ws
    time.sleep(0.1)
    st = brick.get_current_state()
    test_result(
        "Audio channel %d is active in mode %d" % (0, EVT_SOUND_PLAY_ONCE),
        st.audio_ch[0].mode == EVT_SOUND_PLAY_ONCE,
    )
    test_result(
        "Audio channel %d reports file 0x%02X" % (0, st.audio_ch[0].file_id),
        fileid == st.audio_ch[0].file_id,
    )
    test_result("Audio peak values 0x%02X > 0" % (st.audio_peak), st.audio_peak > 0)
    console.log(
        "Waiting %.1f sec for file %d to finish playing..." % (file_dur, fileid)
    )
    time.sleep(file_dur)
    st = brick.get_current_state()
    test_result(
        "Audio channel %d is not active in mode %d" % (0, 0), st.audio_ch[0].mode == 0
    )
    test_result(
        "Audio channel %d reports file 0x%02X" % (0, st.audio_ch[0].file_id),
        st.audio_ch[0].file_id == 0xFF,
    )
    brick.set_volume(old_vol / 255 * 100)


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


def test_file_transfer(fdata, fid=0, fn="test_data.wav"):
    bindata = base64.b64decode(fdata)
    with open(fn, "wb") as f:
        f.write(bindata)
    crc32 = get_file_crc32(fn)
    console.log("Copying file %s with CRC32=0x%08X" % (fn, crc32))
    b.put_file(fn, fid)
    fcrc = 0
    while fcrc == 0:
        time.sleep(1)
        b.refresh_file_dir()
        f0 = b.filedir.get_file_dir_entry(fid)
        fcrc = f0.crc32
    test_result(
        "Copied file directory %s CRC32=0x%08X" % (fn, f0.crc32), f0.crc32 == crc32
    )
    console.log("Getting file %s with CRC32=0x%08X" % (fn, crc32))
    fnr = fn + ".rx"
    b.get_file(fid, fnr)
    read_crc32 = get_file_crc32(fnr)
    test_result(
        "Read back file %s CRC32=0x%08X" % (fnr, read_crc32), crc32 == read_crc32
    )
    os.remove(fn)
    os.remove(fnr)


def test_banner(title):
    table = Table(show_header=False, width=76)
    table.add_row("[bold orange1]%s" % (title))
    console.print(table)


def test_result(desc, result):
    if result:
        res = ":white_check_mark:"
    else:
        res = ":cross_mark:"
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
    ("Runway", EVT_COMBOFX_RUNWAY, [2, 2, 2, 0], 0xFF),
    ("Dragster", EVT_COMBOFX_DRAGSTER, [0, 2, 0, 0], 0xFF),
    ("F1", EVT_COMBOFX_FORMULA1, [0, 0, 0, 0], 0x7F),
]


def main():
    parser = argparse.ArgumentParser(
        description="PFx Brick self test.  Most tests are run by default but individual tests can be omitted using  command line arguments.",
        prefix_chars="-+",
    )
    parser.add_argument(
        "-c",
        "--config",
        action="store_false",
        default=True,
        help="Omit config flash test",
    )
    parser.add_argument(
        "+b",
        "--button",
        action="store_true",
        default=False,
        help="Include button press test",
    )
    parser.add_argument(
        "-l",
        "--lights",
        action="store_false",
        default=True,
        help="Omit light channel test",
    )
    parser.add_argument(
        "-lc",
        "--combo",
        action="store_false",
        default=True,
        help="Omit combo light effects test",
    )
    parser.add_argument(
        "-m",
        "--motors",
        action="store_false",
        default=True,
        help="Omit motor channel test",
    )
    parser.add_argument(
        "-f",
        "--files",
        action="store_false",
        default=True,
        help="Omit file transfer test",
    )
    parser.add_argument(
        "-a",
        "--audio",
        action="store_false",
        default=True,
        help="Omit audio playback test",
    )
    parser.add_argument(
        "+sc",
        "--scripts",
        action="store_true",
        default=False,
        help="Include script execution test",
    )
    parser.add_argument(
        "-t",
        "--time",
        action="store_false",
        default=1.0,
        help="Dwell time for each combo light effect test",
    )
    parser.add_argument(
        "-s",
        "--serialno",
        default=None,
        help="Perform test on PFx Brick with specified serial number",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Show verbose details of PFx Brick",
    )
    args = parser.parse_args()
    argsd = vars(args)

    bricks = find_bricks()
    if len(bricks) > 1 and argsd["serialno"] is None:
        print(
            "More than one PFx Brick is attached.  Please specify brick serial number with the -s argument."
        )
        print("Currently attached PFx Bricks:")
        for brick in bricks:
            b = PFxBrick(brick)
            r = b.open()
            b.get_status()
            name = b.get_name()
            print(
                "[light_slate_blue]%-4s[/] [bold cyan]%-24s[/] Serial no: [bold cyan]%-9s[/] Name: [bold yellow]%s[/]"
                % (b.product_id, b.product_desc, b.serial_no, name)
            )
            b.close()
        exit()
    if argsd["serialno"] is not None and len(bricks) > 1:
        b = PFxBrick(argsd["serialno"])
    else:
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
            "Errors                : [green]0x%02X %s"
            % (b.error, get_error_str(b.error))
        )

    table.add_row("Name                  : [bold yellow]%s" % (name))
    console.print(table)
    b.get_current_state()
    b.get_fs_state()
    b.get_bt_state()
    b.get_config()

    if argsd["verbose"]:
        print(b.get_current_state())
        print(b.get_fs_state())
        print(b.get_bt_state())
        b.print_config()

    with console.status("Testing...") as status:
        test_banner("Testing PFx Brick...")
        test_result(
            "Operating mode 0x%02X and error status 0x%02X" % (b.status, b.error),
            (b.status == 0 and b.error == 0),
        )

        if argsd["button"]:
            test_button_events(b)

        if argsd["config"]:
            res = test_config(b)
            test_result("Configuration flash test", res)
        res = test_dac(b)
        test_result("DAC register test", res)

        res = test_millisec(b)
        test_result("Millisec timer test", res)
        res = test_sec(b)
        test_result("Second timer test", res)
        if b.has_bluetooth:
            res = test_bt_status(b)
            test_result("Bluetooth configuration", res)

        if argsd["motors"]:
            test_banner("Testing Motor Channels...")
            backup_config = snapshot_config(b)
            b.config.motors[0].accel = 0
            b.config.motors[0].decel = 0
            b.config.motors[1].accel = 0
            b.config.motors[1].decel = 0
            b.set_config()
            time.sleep(2)
            res = test_motor_channel(b, 1, 50)
            test_result("Motor channel A +50", res)
            res = test_motor_channel(b, 1, -50)
            test_result("Motor channel A -50", res)

            res = test_motor_channel(b, 2, 75)
            test_result("Motor channel B +75", res)
            res = test_motor_channel(b, 2, -75)
            test_result("Motor channel B -75", res)
            restore_config(b, backup_config)

        if argsd["lights"]:
            test_banner("Testing Individual Light Channels...")
            for ch in range(1, 9):
                res = test_light_ch(b, ch)
                test_result("Light channel %d test" % (ch), res)

        if argsd["combo"]:
            test_banner("Testing Combo Light Effects...")
            for fx in combo_fx:
                b.combo_light_fx(fx[1], fx[2])
                time.sleep(argsd["time"])
                st = b.get_current_state()
                test_result(fx[0], st.lightmask == fx[3])
                if not st.lightmask == fx[3]:
                    console.log(
                        "[red]Combo light fx %s output channels=0x%02X, expected 0x%02X"
                        % (fx[0], st.lightmask, fx[3])
                    )
                b.light_off(list(range(1, 9)))

    if argsd["files"]:
        test_banner("Testing File System...")
        files = [
            (0, SINFILE, 0x0000, 0x000204CE, 0x0000002C, "sin150Hz.wav"),
            (1, PINKFILE, 0x0000, 0x000204CE, 0x0000002C, "pink6dB.wav"),
            (2, YAMANOTE_FILE, 0x0000, 0x00054A80, 0x0000002C, "yamanote.wav"),
        ]

        for file in files:
            test_file_transfer(file[1], file[0], file[5])

        b.refresh_file_dir()
        for file in files:
            f = b.filedir.get_file_dir_entry(file[0])
            test_result(
                "File %s attributes=%X" % (file[5], f.attributes),
                f.attributes == file[2],
            )
            test_result(
                "File %s UserData1=%X" % (file[5], f.userData1), f.userData1 == file[3]
            )
            test_result(
                "File %s UserData2=%X" % (file[5], f.userData2), f.userData2 == file[4]
            )
            oldfn = f.name
            newfn = "file%d%d%d" % (
                random.randint(0, 9),
                random.randint(0, 9),
                random.randint(0, 9),
            )
            console.log("Renaming file %s to %s" % (oldfn, newfn))
            b.rename_file(file[0], newfn)
            time.sleep(2)
            ok = False
            b.refresh_file_dir()
            for e in b.filedir.files:
                if e.name == newfn:
                    ok = True
                    break
            test_result("File %s renamed to %s" % (oldfn, newfn), ok)

            console.log("Restoring filename %s to %s" % (newfn, oldfn))
            b.rename_file(file[0], oldfn)
            time.sleep(2)
            ok = False
            b.refresh_file_dir()
            for e in b.filedir.files:
                if e.name == oldfn:
                    ok = True
                    break
            test_result("File %s renamed to %s" % (oldfn, newfn), ok)

    if argsd["scripts"]:
        test_banner("Testing Script Execution...")
        if is_version_less_than(b.icd_rev, "3.38"):
            console.log(
                "Cannot run test scripts since the PFx Brick must support ICD v.3.38 or newer"
            )
        else:
            test_scripts(b)

    with console.status("Testing...") as status:
        if argsd["audio"]:
            test_banner("Testing Audio Playback...")
            test_audio_playback(b, 0)
            test_audio_playback(b, 1)

    b.close()


if __name__ == "__main__":
    main()


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
