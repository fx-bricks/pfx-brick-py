import argparse
import time
import termios, fcntl, sys, os
from datetime import datetime
from typing import OrderedDict
import zlib

from rich import print, inspect
from rich.console import Console
from rich.table import Table
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa

from toolbox import *
from pfxbrick import *

from trainprofile import IndexedPlayback

console = Console()


def get_speed_notch_loop(brick):
    brick.get_current_state()
    speed = brick.state.motors[0].current_speed
    notch = brick.state.audio_notch
    fid = brick.state.audio_ch[3].file_id
    if not fid == 0xFF:
        loop = brick.filedir.get_file_dir_entry(fid).name
    else:
        loop = ""
    return speed, notch, loop


def param_state(tgt, curr, cond, fmt):
    s = []
    s.append("[bold green]")
    s.append(fmt % (tgt))
    s.append("[/] (")
    if cond:
        s.append("[bold green]")
    else:
        s.append("[bold yellow]")
    s.append(fmt % (curr))
    s.append("[/])")
    return "".join(s)


def is_at_target_speed(brick, speed):
    notch = ip.notch_from_speed(speed)
    loop_file = ip.idle_loops.loops[notch].filename
    curr_speed, curr_notch, curr_loop = get_speed_notch_loop(brick)
    at_speed = abs(curr_speed - speed) < 10
    at_notch = curr_notch == notch
    same_loop = curr_loop == loop_file
    s = "notch=%s speed=%s loop=%s" % (
        param_state(notch, curr_notch, at_notch, "%d"),
        param_state(speed, curr_speed, at_speed, "0x%02X"),
        param_state(loop_file, curr_loop, same_loop, "%s"),
    )
    if not at_speed:
        return False, s
    if not at_notch:
        return False, s
    if not same_loop:
        return False, s
    return True, s


def set_speed(brick, speed, ip, dwell_time):
    brick.set_motor_speed(1, (speed / 255) * 100)
    notch = ip.notch_from_speed(speed)
    loop_file = ip.idle_loops.loops[notch].filename

    with console.status("Waiting for motor to reach speed...") as status:
        at_speed, s = is_at_target_speed(brick, speed)
        while not at_speed:
            at_speed, curr_state = is_at_target_speed(brick, speed)
            status.update("[orange3]Waiting[/] to reach target speed " + curr_state)
            time.sleep(0.25)
        elapsed_time = 0
        while elapsed_time < dwell_time:
            _, curr_state = is_at_target_speed(brick, speed)
            status.update(
                "[cyan]Dwelling[/] at notch speed "
                + curr_state
                + " [cyan]%.1f" % (elapsed_time)
            )
            time.sleep(0.5)
            elapsed_time += 0.5


if __name__ == "__main__":

    def open_brick():
        b = PFxBrick()
        r = b.open()
        if not r:
            exit()
        b.refresh_file_dir()
        b.get_config()
        b.get_status()
        return b

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dwell",
        action="store_true",
        default=5,
        help="Dwell time for each notch level",
    )
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        default=False,
        help="Measure random event times",
    )
    args = parser.parse_args()
    argsd = vars(args)

    brick = open_brick()
    if argsd["random"]:
        fid = 1
        is_playing = False
        tstart = 0
        tlast = 0
        telapsed = 0
        with console.status("Measuring random playback times...") as status:
            while True:
                brick.get_current_state()
                if not is_playing:
                    for ch in range(4):
                        if brick.state.audio_ch[ch].file_id == fid:
                            console.log("File %d playback started" % (fid))
                            is_playing = True
                            tlast = tstart
                            tstart = telapsed
                            console.log(
                                "Tnow=%.1f Tlast=%.1f Tdiff=%.1f"
                                % (tstart, tlast, (tstart - tlast))
                            )
                else:
                    found = False
                    for ch in range(4):
                        if brick.state.audio_ch[ch].file_id == fid:
                            found = True
                    if not found:
                        console.log("File %d playback stopped" % (fid))
                        is_playing = False
                telapsed += 0.5
                time.sleep(0.5)

    ip = IndexedPlayback()
    ip.fetch_from_brick(brick)

    notches = IndexedPlayback.notch_ranges_from_bounds(ip.level_bounds, ip.levels)
    print("Accelerating...")
    for i, notch in enumerate(notches):
        console.print(
            "Notch: [bold cyan]%d[/]  Speed: 0x%02X [bold green]0x%02X[/] 0x%02X"
            % (i, notch[0], notch[1], notch[2])
        )
        set_speed(brick, notch[1], ip, 5)
    print("Decelerating...")
    for i, notch in enumerate(reversed(notches)):
        console.print(
            "Notch: [bold cyan]%d[/]  Speed: 0x%02X [bold green]0x%02X[/] 0x%02X"
            % (ip.levels - i - 1, notch[0], notch[1], notch[2])
        )
        set_speed(brick, notch[1], ip, 2)
    print("Stopping...")
    set_speed(brick, 0, ip, 0)
