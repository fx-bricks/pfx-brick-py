import argparse
import fcntl
import os
import sys
import termios
import time
import zlib
from collections import OrderedDict
from datetime import datetime
from json import detect_encoding

import simpleaudio as sa
import soundfile as sf
from audiofile import AudioFile
from pydub import AudioSegment
from pydub.playback import play
from rich import inspect, print
from rich.console import Console
from rich.table import Table
from toolbox import *

from pfxbrick import *

console = Console()


def key_pressed():
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
    ret = None
    try:
        c = sys.stdin.read(1)
        if c:
            ret = c
    except IOError:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    return ret


def get_file_crc32(fn):
    with open(fn, "rb") as fp:
        fb = fp.read()
    return zlib.crc32(fb) & 0xFFFFFFFF


def test_result(desc, result):
    if result:
        res = ":green_circle:"
    else:
        res = ":red_circle:"
    console.log(res, ":", desc)
    return result


def find_startup_action(brick, fxid):
    for e in range(EVT_STARTUP_EVENT1, EVT_STARTUP_EVENT8 + 1):
        action = brick.get_action_by_address(e)
        if action.soundFxId == fxid:
            return action
    return None


def configure_startup_action(brick, newaction, fxid, overwrite=True):
    found_existing = False
    for e in range(EVT_STARTUP_EVENT1, EVT_STARTUP_EVENT8 + 1):
        action = brick.get_action_by_address(e)
        if action == newaction:
            console.log(":green_circle: : Startup action already configured")
            found_existing = True
            break
        if action.soundFxId == fxid and overwrite:
            console.log(
                ":yellow_circle: :Found an existing startup event=%d to modify"
                % (e - EVT_STARTUP_EVENT1 + 1)
            )
            brick.set_action_by_address(e, newaction)
            found_existing = True
            break
    if not found_existing:
        for e in range(EVT_STARTUP_EVENT1, EVT_STARTUP_EVENT8 + 1):
            action = brick.get_action_by_address(e)
            if action.is_empty():
                console.log(
                    ":yellow_circle: :Found free startup event=%d to configure"
                    % (e - EVT_STARTUP_EVENT1 + 1)
                )
                brick.set_action_by_address(e, newaction)
                break


# class AudioFile:
#     FADE_INTERVAL = 5

#     def __init__(self, fullpath, fileid, attr, new_name=None, virtual=False):
#         self.fullpath = fullpath
#         self.fileid = fileid
#         self.attr = attr
#         if virtual:
#             self.path = ""
#             self.filename = fullpath
#             fps = fullpath.split(".")
#             if len(fps) > 1:
#                 self.name, self.ext = fps[0], fps[1]
#             else:
#                 self.name, self.ext = fullpath, "wav"
#             self.exportpath = ""
#             self.audio = AudioSegment(
#                 data=bytearray([0, 0]), frame_rate=22050, sample_width=2, channels=1
#             )
#             self.crc32 = 0
#         else:
#             self.path, self.filename = split_path(fullpath)
#             self.name, self.ext = split_filename(self.filename)
#             if new_name is not None:
#                 self.exportpath = TMP_PATH + os.sep + new_name
#                 self.filename = new_name
#             else:
#                 self.exportpath = TMP_PATH + os.sep + self.filename
#             self.audio = AudioSegment.from_wav(self.fullpath)
#             self.convert_to_mono()
#             self.audio = self.audio.set_frame_rate(22050)
#             self.apply_fade()
#             self.export()
#             self.crc32 = get_file_crc32(self.exportpath)

#     def __str__(self):
#         return "%s rate=%d kHz samp=%s ch=%d dBFS=%.1f dur=%.3f" % (
#             self.filename,
#             self.audio.frame_rate,
#             self.audio.sample_width,
#             self.audio.channels,
#             self.audio.dBFS,
#             self.audio.duration_seconds,
#         )

#     def play(self, repeat=1):
#         ntimes = 0
#         while ntimes < repeat:
#             play_obj = sa.play_buffer(
#                 self.audio.raw_data,
#                 self.audio.channels,
#                 self.audio.sample_width,
#                 self.audio.frame_rate,
#             )
#             while play_obj.is_playing():
#                 if key_pressed() is not None:
#                     break
#                 time.sleep(0.1)
#             play_obj.stop()
#             ntimes += 1

#     @staticmethod
#     def file_table(files):
#         table = Table(show_header=True, header_style="bold blue")
#         for i, col in enumerate(
#             ["ID", "Attr", "Name", "Length (s)", "Rate (kHz)", "Samp", "Ch", "dBFS"]
#         ):
#             justify = "right" if i > 2 else "left"
#             table.add_column(col, justify=justify)
#         for file in files:
#             if file is None:
#                 continue
#             table.add_row(
#                 "[bold green]0x%02X" % (file.fileid),
#                 "[bold yellow]0x%02X" % (file.attr),
#                 "[cyan]%s" % (file.filename),
#                 "%.3f" % (file.audio.duration_seconds),
#                 "%d" % (file.audio.frame_rate),
#                 "%d" % (file.audio.sample_width),
#                 "%d" % (file.audio.channels),
#                 "%.1f" % (file.audio.dBFS),
#             )
#         return table

#     def convert_to_mono(self):
#         if self.audio.channels > 1:
#             console.log("Converting file [cyan]%s [white]to mono" % (self.filename))
#             self.audio = self.audio.set_channels(1)

#     def apply_fade(self):
#         # console.log("Adding %s ms fade in/out to [cyan]%s" % (self.FADE_INTERVAL, self.filename))
#         self.audio = self.audio.fade_in(duration=self.FADE_INTERVAL)
#         self.audio = self.audio.fade_out(duration=self.FADE_INTERVAL)

#     def export(self):
#         # console.log("Exporting [cyan]%s [white]to %s" % (self.filename, self.exportpath))
#         self.audio.export(self.exportpath, format="wav")

#     def is_on_brick(self, brick, compare_fileid=False):
#         for f in brick.filedir.files:
#             if self.filename == f.name:
#                 if compare_fileid and self.fileid == f.id:
#                     return True
#                 if not compare_fileid:
#                     return True
#         return False

#     def same_crc_as_on_brick(self, brick):
#         for f in brick.filedir.files:
#             if self.filename == f.name:
#                 if self.crc32 == f.crc32:
#                     return True
#         return False

#     def copy_to_brick(self, brick, overwrite=False, use_fileid=False):
#         if self.is_on_brick(brick, compare_fileid=use_fileid):
#             if overwrite:
#                 console.log(
#                     ":yellow_circle: : File [cyan]%s [white]already on brick, but forcing overwrite"
#                     % (self.filename)
#                 )
#                 brick.remove_file(self.filename)
#             elif self.same_crc_as_on_brick(brick):
#                 console.log(
#                     ":green_circle: : File [cyan]%s [white]already on brick with same CRC32 hash, skipping"
#                     % (self.filename)
#                 )
#                 return
#             else:
#                 brick.remove_file(self.filename)
#         time.sleep(1)
#         self.do_file_transfer(brick)

#     def do_file_transfer(self, brick):
#         fn = self.exportpath
#         crc32 = get_file_crc32(fn)
#         console.log("Copying file %s with CRC32=0x%X" % (self.filename, crc32))
#         brick.put_file(fn, self.fileid)
#         fcrc = 0
#         if self.attr > 0:
#             console.log("Setting file attributes=0x%02X" % (self.attr))
#             brick.set_file_attributes(self.fileid, self.attr)
#         while fcrc == 0:
#             time.sleep(1)
#             brick.refresh_file_dir()
#             f0 = brick.filedir.get_file_dir_entry(self.fileid)
#             fcrc = f0.crc32
#         test_result("Copied file reports CRC32=0x%X" % (f0.crc32), f0.crc32 == crc32)
#         if self.attr > 0:
#             test_result(
#                 "Copied file reports attributes=0x%02X" % (f0.attributes),
#                 f0.attributes == self.attr,
#             )
#         time.sleep(1)


class LoopList:
    def __init__(self, path, files, fileid_base, attr_base=None, **kwargs):
        self.loops = []
        prefix = None
        virtual = False
        if "prefix" in kwargs:
            prefix = kwargs["prefix"]
        if "virtual" in kwargs:
            virtual = kwargs["virtual"]

        for idx, file in enumerate(files):
            fileid = fileid_base + idx
            if attr_base is not None:
                attr = attr_base + idx * 4
            else:
                attr = 0
            if prefix is not None:
                new_name = prefix + file
            else:
                new_name = None
            if virtual:
                fn = file
            else:
                fn = path + os.sep + file
            loop = AudioFile(
                fn, fileid=fileid, attr=attr, new_name=new_name, virtual=virtual
            )
            self.loops.append(loop)

    def __len__(self):
        return len(self.loops)


class IdleLoops(LoopList):
    def __init__(self, path, files, **kwargs):
        super().__init__(path, files, 0xE0, 0x20, **kwargs)


class AccelLoops(LoopList):
    def __init__(self, path, files, **kwargs):
        super().__init__(path, files, 0xE8, 0x40, **kwargs)


class DecelLoops(LoopList):
    def __init__(self, path, files, **kwargs):
        super().__init__(path, files, 0xF0, 0x60, **kwargs)


class GatedLoops(LoopList):
    def __init__(self, path, files, **kwargs):
        super().__init__(path, files, 0xDC, 0x10, **kwargs)


class GatedPlayback:
    def __init__(self):
        self.groups = 0
        self.grouped_loops = [None, None, None, None]
        self.gain = 25
        self.motor_speed = "target"
        self.motor_ch = 0

    def print(self):
        for i, group in enumerate(self.grouped_loops):
            if group is not None:
                print("[bold white]Gated Loops Group %d" % (i + 1))
                print(AudioFile.file_table(group.loops))

    def set_with_dict(self, d):
        self.grouped_loops = [None, None, None, None]
        for k, v in d.items():
            if k == "gated_gain":
                self.gain = v
            elif k == "gated_loops":
                self.grouped_loops[0] = GatedLoops(d["source"], v)
            elif k == "gated_notch1":
                self.grouped_loops[0] = LoopList(d["source"], v, 0xD0, prefix="N1")
            elif k == "gated_notch2":
                self.grouped_loops[1] = LoopList(d["source"], v, 0xD4, prefix="N2")
            elif k == "gated_notch3":
                self.grouped_loops[2] = LoopList(d["source"], v, 0xD8, prefix="N3")
            elif k == "gated_notch4":
                self.grouped_loops[3] = LoopList(d["source"], v, 0xDC, prefix="N4")
        self.groups = 0
        for e in self.grouped_loops:
            if e is not None:
                self.groups += 1

    def copy_to_brick(self, brick, overwrite=False):
        for group in self.grouped_loops:
            if group is not None:
                for f in group.loops:
                    f.copy_to_brick(brick, overwrite=overwrite)

    def configure_brick(self, brick):
        if self.groups > 0:
            newaction = PFxAction()
            newaction.soundFxId = EVT_SOUND_PLAY_GATED
            newaction.soundFileId = self.grouped_loops[0].loops[0].fileid
            use_current = 0x04 if self.motor_speed == "current" else 0x00
            newaction.soundParam1 = self.motor_ch | use_current
            newaction.soundParam2 = self.gain
            configure_startup_action(brick, newaction, EVT_SOUND_PLAY_GATED)

    def fetch_from_brick(self, brick):
        self.groups = 0
        self.grouped_loops = [None, None, None, None]
        groups = [{}, {}, {}, {}]
        for f in brick.filedir.files:
            if (f.id & 0xF0) == 0xD0:
                idx = f.id & 0x03
                group = (f.id & 0x0C) >> 2
                groups[group][idx] = f.name

        for i, g in enumerate(groups):
            if len(g) > 0:
                group = [g[x] for x in range(len(g))]
                base = 0xD0 + (i * 4)
                self.grouped_loops[i] = LoopList("", group, base, virtual=True)


class IndexedPlayback:
    def __init__(self):
        self.levels = 0
        self.level_bounds = []
        self.idle_loops = None
        self.accel_loops = None
        self.decel_loops = None
        self.startup = None
        self.shutdown = None
        self.skip_startup = True
        self.motor_speed = "target"
        self.motor_ch = 0

    def print(self):
        print("[bold white]Idle Loop Files")
        print(AudioFile.file_table(self.idle_loops.loops))
        print("[bold white]Accel Loop Files")
        print(AudioFile.file_table(self.accel_loops.loops))
        print("[bold white]Decel Loop Files")
        print(AudioFile.file_table(self.decel_loops.loops))
        if self.startup is not None or self.shutdown is not None:
            print("[bold white]Startup/Shutdown Files")
            print(AudioFile.file_table([self.startup, self.shutdown]))

    @staticmethod
    def bounds_from_notchcount(count):
        bounds = [round((x + 1) / count * 255) for x in range(count - 1)]
        return bounds

    @staticmethod
    def notch_ranges_from_bounds(bounds, count):
        ranges = []
        for i in range(count):
            if i == 0:
                mid_speed = bounds[0] / 2
                lower, upper = 0, bounds[0]
            elif i == count - 1:
                mid_speed = bounds[i - 1] + (255 - bounds[i - 1]) / 2
                lower, upper = bounds[i - 1], 255
            else:
                mid_speed = bounds[i - 1] + (bounds[i] - bounds[i - 1]) / 2
                lower, upper = bounds[i - 1], bounds[i]
            ranges.append((lower, round(mid_speed), upper))
        return ranges

    def notch_from_speed(self, speed):
        ranges = IndexedPlayback.notch_ranges_from_bounds(
            self.level_bounds, self.levels
        )
        for i, r in enumerate(ranges):
            if speed >= r[0] and speed < r[2]:
                return i

    def preview(self):
        if self.startup is not None:
            print("Playing [bold]Startup Sound...")
            self.startup.play()
        seq = []
        for i, loop in enumerate(self.idle_loops.loops):
            seq.append(loop)
            if self.accel_loops is not None and i < len(self.accel_loops):
                seq.append(self.accel_loops.loops[i])
        for i, loop in enumerate(self.idle_loops.loops):
            idx = len(self.idle_loops) - i - 1
            if self.decel_loops is not None and idx < len(self.decel_loops):
                seq.append(self.decel_loops.loops[idx])
            seq.append(self.idle_loops.loops[idx])
        for file in seq:
            print("Playing [bold]%s..." % (file.filename))
            file.play()
        if self.shutdown is not None:
            print("Playing [bold]Shutdown Sound...")
            self.shutdown.play()

    def set_with_dict(self, d):
        for k, v in d.items():
            if k == "startup":
                fn = d["source"] + os.sep + v
                self.startup = AudioFile(fn, fileid=0xEF, attr=0x5C)
            elif k == "shutdown":
                fn = d["source"] + os.sep + v
                self.shutdown = AudioFile(fn, fileid=0xF7, attr=0x7C)
            elif k == "notch_levels":
                self.levels = v
            elif k == "notch_bounds":
                new_bounds = [0] * 8
                for i, e in enumerate(v):
                    new_bounds[i] = e
                self.level_bounds = new_bounds
            elif k == "notch_loops":
                self.idle_loops = IdleLoops(d["source"], v)
            elif k == "accel_loops":
                self.accel_loops = AccelLoops(d["source"], v)
            elif k == "decel_loops":
                self.decel_loops = DecelLoops(d["source"], v)
            elif k == "skip_startup":
                self.skip_startup = v
            elif k == "motor_channel":
                if str(v).lower() in ["a", "0"]:
                    self.motor_ch = 0
                elif str(v).lower() in ["b", "1"]:
                    self.motor_ch = 1
            elif k == "motor_speed":
                if v.lower() not in ["target", "current"]:
                    raise ValueError(
                        "motor_speed key must either be 'target' or 'current' not %s"
                        % v.lower()
                    )
                else:
                    self.motor_speed = v.lower()
        if not "notch_bounds" in d:
            new_bounds = IndexedPlayback.bounds_from_notchcount(self.levels)
            self.level_bounds = new_bounds

    def copy_to_brick(self, brick, overwrite=False):
        all_files = [
            *self.idle_loops.loops,
            *self.accel_loops.loops,
            *self.decel_loops.loops,
        ]
        if self.startup is not None:
            all_files.append(self.startup)
        if self.shutdown is not None:
            all_files.append(self.shutdown)
        for f in all_files:
            f.copy_to_brick(brick, overwrite=overwrite)

    def configure_brick(self, brick):
        same_levels = True
        for i in range(self.levels):
            if self.level_bounds[i] != brick.config.settings.notchBounds[i]:
                brick.config.settings.notchBounds[i] = self.level_bounds[i]
                same_levels = False
        if not self.levels == brick.config.settings.notchCount or not same_levels:
            console.log(
                ":yellow_circle: : Specified notch levels (%d) is different from brick (%d)"
                % (self.levels, brick.config.settings.notchCount)
            )
            console.log("Setting new configuration")
            brick.config.settings.notchCount = self.levels
            brick.set_config()
        else:
            console.log(":green_circle: : Notch levels are already set correctly")

        newaction = PFxAction()
        newaction.soundFxId = EVT_SOUND_PLAY_IDX_MOTOR
        startup = 0x04 if self.startup is not None else 0x00
        skipstartup = 0x08 if self.skip_startup else 0x00
        use_current = 0x04 if self.motor_speed == "current" else 0x00
        newaction.soundParam1 = self.motor_ch | use_current
        newaction.soundParam2 = startup | skipstartup
        configure_startup_action(brick, newaction, EVT_SOUND_PLAY_IDX_MOTOR)

    def fetch_from_brick(self, brick):
        self.levels = brick.config.settings.notchCount
        self.level_bounds = [0] * (self.levels - 1)
        for level in range(self.levels - 1):
            self.level_bounds[level] = brick.config.settings.notchBounds[level]

        # find files assigned to loops
        self.startup = None
        self.shutdown = None
        self.idle_loops = None
        self.accel_loops = None
        self.decel_loops = None
        idle_loops = {}
        accel_loops = {}
        decel_loops = {}
        for f in brick.filedir.files:
            idx = (f.attributes & 0x1C) >> 2
            role = f.attributes & 0xF0
            if f.attributes == 0x5C:
                self.startup = AudioFile(f.name, fileid=0xEF, attr=0x5C, virtual=True)
            elif f.attributes == 0x7C:
                self.shutdown = AudioFile(f.name, fileid=0xF7, attr=0x7C, virtual=True)
            elif role == 0x20 or role == 0x30:
                idle_loops[idx] = f.name
            elif role == 0x40 or role == 0x50:
                accel_loops[idx] = f.name
            elif role == 0x60 or role == 0x70:
                decel_loops[idx] = f.name
        if len(idle_loops) > 0:
            group = [idle_loops[x] for x in range(len(idle_loops))]
            self.idle_loops = IdleLoops("", group, virtual=True)
        if len(accel_loops) > 0:
            group = [accel_loops[x] for x in range(len(accel_loops))]
            self.accel_loops = AccelLoops("", group, virtual=True)
        if len(decel_loops) > 0:
            group = [decel_loops[x] for x in range(len(decel_loops))]
            self.decel_loops = DecelLoops("", group, virtual=True)

        # find any configured startup actions
        action = find_startup_action(brick, EVT_SOUND_PLAY_IDX_MOTOR)
        if action is not None:
            self.motor_speed = "current" if action.soundParam1 & 0x04 else "target"
            self.skip_startup = True if action.soundParam2 & 0x08 else False
            self.motor_ch = action.soundParam1 & 0x03
            if not action.soundParam2 & 0x04:
                self.startup = None


class ProfileSettings:
    def __init__(self):
        self.source_path = None
        self.acceleration = None
        self.deceleration = None
        self.default_volume = None
        self.random_sounds = None
        self.set_off_sound = None
        self.brake_stop_sound = None
        self.rapid_accel_loop = None
        self.rapid_decel_loop = None
        self.rapid_accel_thr = None
        self.rapid_decel_thr = None
        self.brake_decel_thr = None
        self.brake_speed_thr = None

    def set_with_dict(self, d):
        for k, v in d.items():
            if k == "source":
                self.source_path = v
            elif k in ["accel", "acceleration"]:
                self.acceleration = v
            elif k in ["decel", "deceleration"]:
                self.deceleration = v
            elif k in ["default_volume", "volume"]:
                self.default_volume = v
            elif k in ["rapid_accel_thr"]:
                self.rapid_accel_thr = v
            elif k in ["rapid_decel_thr"]:
                self.rapid_decel_thr = v
            elif k in ["brake_decel_thr"]:
                self.brake_decel_thr = v
            elif k in ["brake_speed_thr"]:
                self.brake_speed_thr = v

            elif k in [
                "set_off_sound",
                "rapid_accel_loop",
                "brake_stop_sound",
                "rapid_decel_loop",
            ]:
                self.__dict__[k] = v
            elif k in ["random_sounds", "random"]:
                dd = []
                for vv in v:
                    dk = {}
                    for kk, vk in vv.items():
                        if vk is None:
                            dk["filename"] = kk
                        else:
                            dk[kk] = vk
                    dd.append(dk)
                self.random_sounds = dd

    def configure_brick(self, brick):
        if self.default_volume is not None:
            console.log("Setting default volume to %d" % (self.default_volume))
            brick.config.audio.defaultVolume = self.default_volume
        if self.acceleration is not None:
            console.log("Setting motor acceleration to %d" % (self.acceleration))
            brick.config.motors[0].accel = self.acceleration
            brick.config.motors[1].accel = self.acceleration
        if self.deceleration is not None:
            console.log("Setting motor deceleration to %d" % (self.deceleration))
            brick.config.motors[0].decel = self.deceleration
            brick.config.motors[1].decel = self.deceleration
        if self.rapid_accel_thr is not None:
            console.log(
                "Setting rapid acceleration threshold to %d" % (self.rapid_accel_thr)
            )
            brick.config.settings.rapidAccelThr = self.rapid_accel_thr
        if self.rapid_decel_thr is not None:
            console.log(
                "Setting rapid deceleration threshold to %d" % (self.rapid_decel_thr)
            )
            brick.config.settings.rapidDecelThr = self.rapid_decel_thr
        if self.brake_decel_thr is not None:
            console.log(
                "Setting brake deceleration threshold to %d" % (self.brake_decel_thr)
            )
            brick.config.settings.brakeDecelThr = self.brake_decel_thr
        if self.brake_speed_thr is not None:
            console.log("Setting brake speed threshold to %d" % (self.brake_speed_thr))
            brick.config.settings.brakeSpeedThr = self.brake_speed_thr

        brick.set_config()
        time.sleep(2.5)

    def fetch_from_brick(self, brick):
        self.default_volume = brick.config.audio.defaultVolume
        self.acceleration = brick.config.motors[0].accel
        self.rapid_accel_thr = brick.config.settings.rapidAccelThr
        self.rapid_decel_thr = brick.config.settings.rapidDecelThr
        self.brake_decel_thr = brick.config.settings.brakeDecelThr
        self.brake_speed_thr = brick.config.settings.brakeSpeedThr


class Profile:
    def __init__(self):
        self.settings = ProfileSettings()
        self.idx_playback = IndexedPlayback()
        self.gated_playback = GatedPlayback()

    def print(self):
        self.idx_playback.print()
        self.gated_playback.print()
        all_files = []
        if self.settings.random_sounds is not None:
            for file in self.settings.random_sounds:
                fileID = 0
                fp = self.settings.source_path + os.sep + file["filename"]
                af = AudioFile(fp, fileID, 0)
                all_files.append(af)
        print("[bold white]Random Sounds")
        print(AudioFile.file_table(all_files))
        all_files = []
        for k, fid in zip(
            [
                "set_off_sound",
                "rapid_accel_loop",
                "brake_stop_sound",
                "rapid_decel_loop",
            ],
            [0xFB, 0xFC, 0xFE, 0xFD],
        ):
            if self.settings.__dict__[k] is not None:
                for file in self.settings.__dict__[k]:
                    fileID = fid
                    fp = self.settings.source_path + os.sep + file
                    af = AudioFile(fp, fileID, 0)
                    all_files.append(af)
        print("[bold white]Special Files")
        print(AudioFile.file_table(all_files))

    def set_with_dict(self, d):
        self.settings.set_with_dict(d)
        self.idx_playback.set_with_dict(d)
        self.gated_playback.set_with_dict(d)

    def fetch_from_brick(self, brick):
        self.settings.fetch_from_brick(brick)
        self.idx_playback.fetch_from_brick(brick)
        self.gated_playback.fetch_from_brick(brick)

    def copy_to_brick(self, brick):
        self.idx_playback.copy_to_brick(brick)
        self.gated_playback.copy_to_brick(brick)
        if self.settings.random_sounds is not None:
            for file in self.settings.random_sounds:
                fileID = brick.filedir.find_available_file_id()
                fp = self.settings.source_path + os.sep + file["filename"]
                af = AudioFile(fp, fileID, 0)
                af.copy_to_brick(brick)
        for k, fid in zip(
            [
                "set_off_sound",
                "rapid_accel_loop",
                "brake_stop_sound",
                "rapid_decel_loop",
            ],
            [0xFB, 0xFC, 0xFE, 0xFD],
        ):
            if self.settings.__dict__[k] is not None:
                for file in self.settings.__dict__[k]:
                    fileID = fid
                    fp = self.settings.source_path + os.sep + file
                    af = AudioFile(fp, fileID, 0)
                    af.copy_to_brick(brick, use_fileid=True)

    def configure_brick(self, brick):
        self.idx_playback.configure_brick(brick)
        self.gated_playback.configure_brick(brick)
        for file in self.settings.random_sounds:
            fid = brick.file_id_from_str_or_int(file["filename"])
            if not fid == 0xFF:
                newaction = PFxAction()
                newaction.soundFxId = EVT_SOUND_PLAY_RAND
                newaction.soundFileId = fid
                newaction.soundParam1 = 0
                if "probability" in file:
                    newaction.soundParam1 = file["probability"]
                configure_startup_action(
                    brick, newaction, EVT_SOUND_PLAY_RAND, overwrite=False
                )


if __name__ == "__main__":

    def open_brick():
        b = PFxBrick()
        r = b.open()
        if not test_result("Opening PFx Brick", r):
            exit()
        b.refresh_file_dir()
        b.get_config()
        b.get_status()
        return b

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project", metavar="project", type=str, help="project file (YAML)"
    )
    parser.add_argument(
        "-f",
        "--format",
        action="store_true",
        default=False,
        help="Format PFx Brick filesystem before starting",
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        default=False,
        help="Overwrite files, even if they exist",
    )
    parser.add_argument(
        "-p",
        "--preview",
        action="store_true",
        default=False,
        help="Listen to preview of sound files",
    )
    parser.add_argument(
        "-g",
        "--get",
        action="store_true",
        default=False,
        help="Get playback settings on brick",
    )
    args = parser.parse_args()
    argsd = vars(args)

    fs = FileOps(simulate=True, verbose=True, overwrite=False)
    if not fs.verify_file(argsd["project"]):
        exit()
    print("Reading project file %s" % (argsd["project"]))
    proj = Params(yml=argsd["project"])
    proj.format = argsd["format"]
    proj.overwrite = argsd["overwrite"]
    profile = Profile()

    if argsd["get"]:
        brick = open_brick()
        # r = flash_read(brick, 0xFFF000, 256)
        # s = []
        # for rb in r:
        #     s.append("0x%02X " % (rb))
        # console.print("".join(s))
        brick.get_config()
        brick.print_config()
        profile.idx_playback.fetch_from_brick(brick)
        profile.idx_playback.print()
        profile.gated_playback.fetch_from_brick(brick)
        profile.gated_playback.print()
        inspect(profile.idx_playback)
    else:
        profile.set_with_dict(proj.__dict__)
        inspect(profile.settings)
        profile.print()

        if argsd["preview"]:
            profile.idx_playback.preview()
        else:
            brick = open_brick()
            brick.test_action(PFxAction().all_off())
            profile.copy_to_brick(brick)
            profile.configure_brick(brick)
            profile.settings.configure_brick(brick)
