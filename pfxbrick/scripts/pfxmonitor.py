#! /usr/bin/env python3
import argparse
from functools import update_wrapper
import time
from datetime import datetime

from rich import box, print
from rich.align import Align
from rich.console import Console, RenderGroup
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.progress_bar import ProgressBar
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.bar import Bar
from rich.live import Live
from time import sleep

from pfxbrick import *

console = Console()


def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="brightvol", size=3),
        Layout(name="status", size=4),
        Layout(name="filesys", size=4),
        Layout(name="bluetooth", size=4),
        Layout(name="lights", size=11),
        Layout(name="motors", size=5),
        Layout(name="motor_rate", size=5),
        Layout(name="audio", size=7),
    )
    layout["brightvol"].split_row(
        Layout(name="bright"),
        Layout(name="vol", ratio=1),
    )
    layout["status"].split_row(
        Layout(name="status1"),
        Layout(name="status2"),
    )
    layout["audio"].split_row(
        Layout(name="audio_ch"),
        Layout(name="audio_state"),
    )
    layout["audio_state"].split_column(
        Layout(name="audio_peak"),
        Layout(name="audio_idx"),
    )
    return layout


class Header:
    """Display header with clock."""

    def __init__(self, brick):
        self.brick = brick

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=False)
        grid.add_column(justify="left", min_width=22, ratio=1)
        grid.add_column(justify="left", min_width=15, ratio=1)
        grid.add_column(justify="left", min_width=42, ratio=1)
        grid.add_column(justify="right", ratio=1)
        grid.add_row(
            "[light_slate_blue]%s [bold cyan]%s"
            % (self.brick.product_id, self.brick.product_desc),
            "S/N: [yellow]%s" % (self.brick.serial_no),
            "[white]Firmware [green]v.%s build %s [white]ICD [green]v.%s"
            % (self.brick.firmware_ver, self.brick.firmware_build, self.brick.icd_rev),
            "",
            "[bold yellow]%s" % (self.brick.name),
            # datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid)


def update_status(brick):
    st = brick.state
    panel = Table.grid(padding=0)
    for _ in range(8):
        panel.add_column(ratio=1, min_width=8, justify="center")
    panel.add_row("State", "Err", "Seconds", "Millisec", "Script", "Line", "L2")
    es = (
        "[bold red]0x%02X" % (brick.error)
        if brick.error > 0
        else "[green]0x%02X" % (brick.error)
    )
    ss = (
        "[magenta]0x%02X" % (st.script_state)
        if st.script_state == 0
        else console.status("[bold magenta]0x%02X" % (st.script_state))
    )
    panel.add_row(
        "0x%02X" % (brick.status),
        es,
        "[cyan]%5d" % (st.slow_count),
        "[cyan]%5d" % (st.millisec_count),
        ss,
        "[magenta]%3d" % (st.script_line),
        "0x%02X" % (st.status_latch2),
    )
    return Panel(panel)


def update_fs_status(st):
    panel = Table.grid(padding=0)
    for i in range(9):
        width = 7 if i < 6 else 19
        panel.add_column(ratio=1, min_width=width, justify="center")
    panel.add_row(
        "", "State", "Flags", "Files", "Open", "Erase", "Capacity", "Free", "Empty"
    )
    panel.add_row(
        "[bold white]Filesystem ",
        "[cyan]0x%02X" % (st.filesys.task_state),
        "[cyan]0x%02X" % (st.filesys.flags),
        "[magenta]%2d" % (st.filesys.file_count),
        "[magenta]%2d" % (st.filesys.open_files),
        "[cyan]0x%04X" % (st.filesys.erase_sector),
        "%d sec [b]%d kB[/b]"
        % (st.filesys.sector_capacity, st.filesys.sector_capacity * 4096 / 1000),
        "%d sec [b]%d kB[/b]"
        % (st.filesys.free_sectors, st.filesys.free_sectors * 4096 / 1000),
        "%d sec [b]%d kB[/b]"
        % (st.filesys.empty_sectors, st.filesys.empty_sectors * 4096 / 1000),
    )
    return Panel(panel)


def update_bt_status(st):
    panel = Table.grid(padding=0)
    for i in range(9):
        justify = "center" if i < 7 else "right"
        panel.add_column(ratio=1, min_width=9, justify=justify)
    panel.add_row(
        "", "State", "Flags", "Error", "Services", "Features", "Auth", "Tx", "Rx"
    )
    es = (
        "[bold red]0x%04X" % (st.bt.error)
        if st.bt.error > 0
        else "[green]0x%04X" % (st.bt.error)
    )
    stx = "[orange1]%d" % (st.bt.tx_count)
    srx = "[green]%d" % (st.bt.rx_count)
    if st.status_latch1 & 0x40:
        stx = console.status(stx)
        srx = console.status(srx)

    panel.add_row(
        "[bold white]Bluetooth ",
        "[cyan]0x%02X" % (st.bt.state),
        "[cyan]0x%04X" % (st.bt.flags),
        es,
        "0x%04X" % (st.bt.services),
        "0x%04X" % (st.bt.features),
        "0x%04X" % (st.bt.auth),
        stx,
        srx,
    )
    return Panel(panel)


def update_audio(st, brick):
    panel = Table.grid(expand=True)
    panel.title = "Audio Channels"
    panel.title_style = "bold white"
    panel.add_column(ratio=1, justify="left", min_width=4)
    panel.add_column(ratio=2, justify="left", min_width=10)
    panel.add_column(ratio=5, min_width=24)
    for i in range(4):
        fid = st.audio_ch[i].file_id
        fn = ""
        if not fid == 0xFF:
            fn = brick.filedir.get_file_dir_entry(fid)
            if fn is not None:
                fn = fn.name
        fs = "File: --- " if fid == 0xFF else "File: [aquamarine3]0x%02X %s" % (fid, fn)
        panel.add_row(
            "Ch %d " % (i),
            "Mode: [cyan]0x%02X " % (st.audio_ch[i].mode),
            fs,
        )
    return Panel(panel)


def update_audio_state(st):
    panel = Table.grid()
    level_bar = ProgressBar(
        total=255,
        complete_style="aquamarine3",
        finished_style="aquamarine3",
        completed=st.audio_peak,
    )
    for i in range(3):
        panel.add_column(ratio=1)
    panel.add_row(
        "Audio peak: ",
        level_bar,
        "[aquamarine3]0x%02X" % (st.audio_peak),
    )
    return Panel(panel)


def update_audio_idx(brick):
    panel = Table.grid()
    panel.add_column(ratio=2)
    for _ in range(brick.config.settings.notchCount):
        panel.add_column(ratio=1)
    notches = ["0x%02X " % x for x in brick.config.settings.notchBounds]
    n = brick.state.audio_notch
    if n < len(brick.config.settings.notchBounds):
        notches[n] = "[black on white]0x%02X " % (brick.config.settings.notchBounds[n])
    panel.add_row("Curr Notch ", "%d" % (brick.state.audio_notch + 1))
    panel.add_row("Notch", *notches)
    return Panel(panel)


def update_brightness(value) -> Panel:
    """Some example content."""
    panel = Table.grid(padding=1)
    bright_bar = ProgressBar(
        total=255,
        complete_style="light_slate_blue",
        finished_style="light_slate_blue",
        completed=value,
    )
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_row("Brightness: ", bright_bar, "[light_slate_blue]%3d" % (value))
    return Panel(panel)


def update_volume(value) -> Panel:
    """Some example content."""
    panel = Table.grid()
    bright_bar = ProgressBar(
        total=255,
        complete_style="aquamarine3",
        finished_style="aquamarine3",
        completed=value,
    )
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_row("Volume: ", bright_bar, "[aquamarine3]%3d" % (value))
    return Panel(panel)


def update_motors(st):
    panel = Table.grid()
    panel.title = "Motor Channels"
    panel.title_style = "bold white"
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    for ch in range(0, 2):
        motor = st.motors[ch]
        tgtspd = motor.target_speed
        curspd = motor.current_speed
        pwmspd = motor.pwm_speed
        chactive = (ch == 0 and st.status_latch2 & 0x03) or (
            ch == 1 and st.status_latch2 & 0x0C
        )
        style = "green"
        if not chactive:
            s = ":black_medium_square:"
        if chactive and motor.dir == "Forward":
            s = ":arrow_forward:"
            style = "green"
        elif chactive:
            s = ":arrow_backward:"
            tgtspd = (~tgtspd + 1) & 0xFF
            curspd = (~curspd + 1) & 0xFF
            style = "red"
        tgt = ProgressBar(
            total=255, completed=tgtspd, complete_style=style, finished_style=style
        )
        curr = ProgressBar(
            total=255, completed=curspd, complete_style=style, finished_style=style
        )
        pwm = ProgressBar(
            total=255, completed=pwmspd, complete_style=style, finished_style=style
        )
        panel.add_row(
            "Ch %d %s Tgt: " % (ch + 1, s),
            tgt,
            " [cyan]%3d " % (tgtspd),
            "Curr: ",
            curr,
            " [cyan]%3d " % (curspd),
            "PWM: ",
            pwm,
            " [cyan]0x%02X" % (pwmspd),
        )
    return Panel(panel)


def update_lights(st):
    panel = Table.grid()
    panel.title = "Light Channels"
    panel.title_style = "bold white"
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    panel.add_column(ratio=1)
    style = "light_goldenrod3"
    for ch in range(0, 8):
        light = st.lights[ch]
        tgt = ProgressBar(
            total=255,
            completed=light.target_level,
            complete_style=style,
            finished_style=style,
        )
        curr = ProgressBar(
            total=255,
            completed=light.current_level,
            complete_style=style,
            finished_style=style,
        )
        if light.active:
            s = ":black_square_button: "
        else:
            s = ":black_large_square: "
        panel.add_row(
            "Ch %d %s Tgt: " % (ch + 1, s),
            tgt,
            " [cyan]%3d " % (light.target_level),
            "Curr: ",
            curr,
            " [cyan]%3d " % (light.current_level),
        )
    return Panel(panel)


def update_bitfield(byte, size, labels):
    panel = Table.grid(expand=True)
    for _ in range(size):
        panel.add_column(width=8, justify="center", ratio=1)
    bits = []
    for x in range(size):
        mask = 1 << x
        if byte & mask:
            s = " :black_square_button: "
        else:
            s = " :black_large_square: "
        bits.append(s)
    panel.add_row(*bits)
    panel.add_row(*labels)
    return Panel(panel)


def update_motor_rates(st, b):
    panel = Table.grid(expand=True)
    panel.title = "Triggered Sound State"
    panel.title_style = "bold white"
    for _ in range(8):
        panel.add_column(width=8, justify="center", ratio=1)
    panel.add_row(
        "Motor Spd",
        "Motor PWM",
        "Motor Rate",
        "[Change Dir]",
        "[Set Off]",
        "[Rapid Acc]",
        "[Rapid Dec]",
        "[Brake]",
    )
    if st.motor_rate_ptr & 0x80:
        rate = -((~st.motor_rate_ptr + 1) & 0xFF)
    else:
        rate = st.motor_rate_ptr
    if st.trig_change_dir_state > 0:
        s1 = "[bold magenta]%2d" % (st.trig_change_dir_state)
    else:
        s1 = "[bold black]%2d" % (st.trig_change_dir_state)
    if st.trig_set_off_state > 0:
        s2 = "[bold magenta]%2d" % (st.trig_set_off_state)
    else:
        s2 = "[bold black]%2d" % (st.trig_set_off_state)
    if st.trig_rapid_accel_state > 0:
        s3 = "[bold magenta]%2d" % (st.trig_rapid_accel_state)
    else:
        s3 = "[bold black]%2d" % (st.trig_rapid_accel_state)
    if st.trig_rapid_decel_state > 0:
        s4 = "[bold magenta]%2d" % (st.trig_rapid_decel_state)
    else:
        s4 = "[bold black]%2d" % (st.trig_rapid_decel_state)
    if st.trig_brake_state > 0:
        s5 = "[bold magenta]%2d" % (st.trig_brake_state)
    else:
        s5 = "[bold black]%2d" % (st.trig_brake_state)
    panel.add_row(
        "[cyan]%3d" % (st.motor_ptr),
        "[cyan]0x%02X" % (st.motor_pwm_ptr),
        "[green]%2d" % (rate),
        s1,
        s2,
        "[green]%2d %s" % (b.config.settings.rapidAccelThr, s3),
        "[green]%2d %s" % (b.config.settings.rapidDecelThr, s4),
        "[green]%2d [cyan]%2d %s"
        % (
            b.config.settings.brakeDecelThr,
            b.config.settings.brakeSpeedThr,
            s5,
        ),
    )
    return Panel(panel)


def main():
    parser = argparse.ArgumentParser(
        description="PFx Brick real time monitoring utility. Press <Ctrl>-C to exit monitor."
    )
    parser.add_argument(
        "-s",
        "--serialno",
        default=None,
        help="Perform monitoring on PFx Brick with specified serial number",
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
            if not r:
                continue
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

    r = b.open()
    if not r:
        exit()
    b.get_status()
    b.get_config()
    icd = b.get_icd_rev()
    name = b.get_name()
    b.refresh_file_dir()

    layout = make_layout()
    layout["header"].update(Header(b))
    with Live(layout, refresh_per_second=8, screen=True):
        flip = True
        while True:
            st = b.get_current_state()
            b.get_status()
            if flip:
                b.get_fs_state()
                flip = False
            else:
                if b.has_bluetooth:
                    b.get_bt_state()
                flip = True
            layout["bright"].update(update_brightness(st.brightness))
            layout["vol"].update(update_volume(st.volume))
            layout["status1"].update(
                update_bitfield(
                    st.status_latch1,
                    8,
                    [
                        "USB:link:",
                        "USB",
                        "IR",
                        "IR:lock:",
                        ":speaker:",
                        "BLE:link:",
                        "BLE",
                        "FS",
                    ],
                )
            )
            layout["filesys"].update(update_fs_status(st))
            layout["status2"].update(update_status(b))
            if b.has_bluetooth:
                layout["bluetooth"].update(update_bt_status(st))
            layout["lights"].update(update_lights(st))
            layout["motors"].update(update_motors(st))
            layout["motor_rate"].update(update_motor_rates(st, b))
            layout["audio_ch"].update(update_audio(st, b))
            layout["audio_peak"].update(update_audio_state(st))
            layout["audio_idx"].update(update_audio_idx(b))

            time.sleep(0.15)


if __name__ == "__main__":
    main()
