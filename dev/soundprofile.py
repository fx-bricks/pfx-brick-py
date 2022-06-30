# from typeshed import SupportsDivMod
import os

from audiofile import AudioFile
from toolbox import *

from pfxbrick.pfx import *
from pfxbrick.pfxaction import *
from pfxbrick.pfxfiles import fs_copy_file_to
from pfxbrick.pfxhelpers import uint16_to_bytes, uint32_to_bytes

fileid_dict = {
    "startup": 0xEF,
    "shutdown": 0xF7,
    "set_off_sound": 0xFB,
    "rapid_accel_loop": 0xFC,
    "brake_stop_sound": 0xFE,
    "rapid_decel_loop": 0xFD,
    "change_dir_sound": 0xFA,
    "bell": 0xF8,
    "short_whistle": 0xF9,
    "long_whistle": 0xCF,
}
attr_dict = {
    "startup": 0x5C,
    "shutdown": 0x7C,
}


def listify(x):
    if not isinstance(x, list):
        return [x]
    return x


def map_pct_to_motor_step(amount):
    if isinstance(amount, str):
        pct = amount.replace("%", "")
        pct = int(pct)
    elif isinstance(amount, float):
        pct = int(amount * 100.0)
    else:
        pct = int(amount)
    if pct >= 33:
        return 9
    if pct >= 25:
        return 8
    if pct >= 20:
        return 7
    if pct >= 10:
        return 6
    if pct >= 6:
        return 5
    if pct >= 5:
        return 4
    if pct >= 3:
        return 3
    if pct >= 2:
        return 2
    if pct >= 1:
        return 1
    return 0


class LoopList:
    def __init__(self, path, files, fileid_base, attr_base=None, **kwargs):
        self.loops = []
        self.fileid_base = fileid_base
        self.append(path, files, fileid_base=fileid_base, attr_base=attr_base, **kwargs)

    def append(self, path, files, fileid_base=None, attr_base=None, **kwargs):
        prefix = None
        virtual = False
        if fileid_base is not None:
            self.fileid_base = fileid_base
        if "prefix" in kwargs:
            prefix = kwargs["prefix"]
        if "virtual" in kwargs:
            virtual = kwargs["virtual"]
        for idx, file in enumerate(files):
            fileid = self.fileid_base + idx
            vs = file.split()
            if len(vs) > 1:
                vf = vs[0]
                vn = float(vs[1])
            else:
                vf = file
                vn = None
            if attr_base is not None:
                attr = attr_base + idx * 4
            else:
                attr = 0
            if prefix is not None:
                f0 = full_path(path + os.sep + vf)
                p, f1 = split_path(f0)
                name, ext = split_filename(f1)
                new_name = prefix + name + ext
            else:
                new_name = None
            if virtual:
                fn = vf
            else:
                fn = path + os.sep + vf
            loop = AudioFile(
                fn,
                fileid=fileid,
                attr=attr,
                new_name=new_name,
                virtual=virtual,
                norm=vn,
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
        if "fileid_base" not in kwargs:
            kwargs["fileid_base"] = 0xD0
        super().__init__(path, files, attr_base=0x10, **kwargs)


class SoundProfile:
    def __init__(self):
        self.source_path = None
        self.motor_speed = "target"
        self.motor_ch = 0
        self.acceleration = None
        self.deceleration = None
        self.vmin = None
        self.vmid = None
        self.vmax = None
        self.motor_invert = None
        self.motor_pfmode = None
        self.motor_low_torque = None

        self.increase_speed = None
        self.decrease_speed = None
        self.change_dir = None
        self.stop = None
        self.emergency_stop = None
        self.increase_volume = None
        self.decrease_volume = None
        self.increase_brightness = None
        self.decrease_brightness = None
        self.clear_remote = None
        self.forward_lights = None
        self.reverse_lights = None

        self.default_volume = None
        self.rapid_accel_thr = 0
        self.rapid_decel_thr = 0
        self.brake_decel_thr = 0
        self.brake_speed_thr = 0

        self.change_dir_sound = None
        self.set_off_sound = None
        self.rapid_accel_loop = None
        self.brake_stop_sound = None
        self.rapid_decel_loop = None

        self.notch_count = 0
        self.notch_bounds = []
        self.idle_loops = None
        self.accel_loops = None
        self.decel_loops = None
        self.gated_loops = None
        self.startup = None
        self.shutdown = None
        self.skip_startup = True
        self.gated_gain = 50
        self.other_sounds = None
        self.bell = None
        self.short_whistle = None
        self.long_whistle = None

        self.audio_files = None

    def clear(self):
        self.source_path = None
        self.acceleration = None
        self.deceleration = None
        self.vmin = None
        self.vmid = None
        self.vmax = None
        self.motor_invert = None
        self.motor_pfmode = None
        self.motor_low_torque = None

        self.increase_speed = None
        self.decrease_speed = None
        self.change_dir = None
        self.stop = None
        self.emergency_stop = None
        self.increase_volume = None
        self.decrease_volume = None
        self.increase_brightness = None
        self.decrease_brightness = None
        self.clear_remote = None
        self.forward_lights = None
        self.reverse_lights = None

        self.default_volume = None
        self.rapid_accel_thr = 0
        self.rapid_decel_thr = 0
        self.brake_decel_thr = 0
        self.brake_speed_thr = 0

        self.change_dir_sound = None
        self.set_off_sound = None
        self.rapid_accel_loop = None
        self.brake_stop_sound = None
        self.rapid_decel_loop = None

        self.notch_count = 0
        self.notch_bounds = []
        self.idle_loops = None
        self.accel_loops = None
        self.decel_loops = None
        self.gated_loops = None
        self.startup = None
        self.shutdown = None
        self.skip_startup = True
        self.motor_speed = "target"
        self.motor_ch = 0
        self.gated_gain = 50
        self.other_sounds = None

        self.audio_files = None

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

    def set_with_dict(self, d):
        fid = 1
        self.other_sounds = None
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

            elif k in fileid_dict:
                fk = fileid_dict[k]
                if k in attr_dict:
                    attr = attr_dict[k]
                else:
                    attr = 0
                vs = v.split()
                if len(vs) > 1:
                    vf = vs[0]
                    vn = float(vs[1])
                else:
                    vf = v
                    vn = None
                fn = d["source"] + os.sep + vf
                self.__dict__[k] = AudioFile(fn, fileid=fk, attr=attr, norm=vn)
            elif k in ["random_sounds", "random", "other_sounds"]:
                dd = []
                for vv in v:
                    dk = {}
                    for kk, vk in vv.items():
                        if vk is None:
                            fn = d["source"] + os.sep + kk
                            dk["audiofile"] = AudioFile(fn, fileid=fid, attr=0)
                        else:
                            dk[kk] = vk
                    dd.append(dk)
                    fid += 1
                if self.other_sounds is None:
                    self.other_sounds = dd
                else:
                    self.other_sounds.extend(dd)
            elif k in ["notch_levels", "notch_count"]:
                self.notch_count = v
            elif k == "notch_bounds":
                new_bounds = [0] * 8
                for i, e in enumerate(v):
                    new_bounds[i] = e
                self.notch_bounds = new_bounds
            elif k == "notch_loops":
                self.idle_loops = IdleLoops(d["source"], v)
            elif k == "accel_loops":
                self.accel_loops = AccelLoops(d["source"], v)
            elif k == "decel_loops":
                self.decel_loops = DecelLoops(d["source"], v)
            elif k in [
                "gated_notch1",
                "gated_notch2",
                "gated_notch3",
                "gated_notch4",
                "gated_loops",
            ]:
                if k in ["gated_notch1", "gated_loops"]:
                    base = 0xD0
                    prefix = "L1"
                elif k == "gated_notch2":
                    base = 0xD4
                    prefix = "L2"
                elif k == "gated_notch3":
                    base = 0xD8
                    prefix = "L3"
                elif k == "gated_notch4":
                    base = 0xDC
                    prefix = "L4"
                if self.gated_loops is not None:
                    self.gated_loops.append(
                        d["source"], v, fileid_base=base, prefix=prefix
                    )
                else:
                    self.gated_loops = GatedLoops(
                        d["source"], v, fileid_base=base, prefix=prefix
                    )
            elif k == "skip_startup":
                self.skip_startup = v
            elif k == "vmin":
                self.vmin = int(v)
            elif k == "vmid":
                self.vmid = int(v)
            elif k == "vmax":
                self.vmax = int(v)
            elif k in [
                "increase_speed",
                "decrease_speed",
                "stop",
                "change_dir",
                "emergency_stop",
                "clear_remote",
                "motor_invert",
                "motor_pfmode",
                "motor_low_torque",
                "increase_volume",
                "decrease_volume",
                "increase_brightness",
                "decrease_brightness",
                "forward_lights",
                "reverse_lights",
            ]:
                self.__dict__[k] = v
            elif k == "motor_channel":
                if len(str(v)) == 1:
                    if str(v).lower() in ["a", "0"]:
                        self.motor_ch = 0
                    elif str(v).lower() in ["b", "1"]:
                        self.motor_ch = 1
                elif len(str(v)) == 2:
                    if str(v).lower() == "ab":
                        self.motor_ch = -1
            elif k == "motor_speed":
                if v.lower() not in ["target", "current"]:
                    raise ValueError(
                        "motor_speed key must either be 'target' or 'current' not %s"
                        % v.lower()
                    )
                else:
                    self.motor_speed = v.lower()

        if not "notch_bounds" in d:
            new_bounds = self.bounds_from_notchcount(self.notch_count)
            self.notch_bounds = new_bounds

    def update_audiofile_with_id(self, audiofile, fileid):
        for k, v in fileid_dict.items():
            if fileid == v:
                self.__dict__[k] = audiofile
        if (fileid & 0xF0) == 0xE0:
            idx = fileid & 0x0F
            if idx < 8:
                self.idle_loops.loops[idx] = audiofile
            elif idx < 0x0F and idx >= 8:
                self.accel_loops.loops[idx] = audiofile
        elif (fileid & 0xF0) == 0xF0:
            idx = fileid & 0x0F
            if idx < 7:
                self.decel_loops.loops[idx] = audiofile

    def export_script(self, filename=None, as_bytes=False, to_brick=None):
        """Exports a startup.pfx script file which can be copied to a PFx Brick
        automatically configure it for this sound profile.
        """
        s = []
        s.append("# Sound profile configuration script\n")
        s.append("# Set configuration\n")
        if self.default_volume is not None:
            s.append("set config vol = %d" % (self.default_volume))
        ch = "a" if self.motor_ch == 0 else "b"
        ch = []
        if self.motor_ch == 0 or self.motor_ch == -1:
            ch.append("a")
        if self.motor_ch == 1 or self.motor_ch == -1:
            ch.append("b")
        for c in ch:
            if self.acceleration is not None:
                s.append("set config motor %s accel = %d" % (c, self.acceleration))
            if self.deceleration is not None:
                s.append("set config motor %s decel = %d" % (c, self.deceleration))
            if self.vmin is not None:
                s.append("set config motor %s v0 = %d" % (c, self.vmin))
            if self.vmid is not None:
                s.append("set config motor %s v1 = %d" % (c, self.vmid))
            if self.vmax is not None:
                s.append("set config motor %s v2 = %d" % (c, self.vmax))
            if self.motor_invert is not None:
                s.append(
                    "set config motor %s invert = %d" % (c, int(self.motor_invert))
                )
            if self.motor_pfmode is not None:
                s.append("set config motor %s pf = %d" % (c, int(self.motor_pfmode)))
            if self.motor_low_torque is not None:
                s.append(
                    "set config motor %s torque = %d" % (c, int(self.motor_low_torque))
                )
        s.append("set config nc = %d" % (self.notch_count))
        for i in range(self.notch_count - 1):
            s.append("set config nb %d = %d" % (i + 1, self.notch_bounds[i]))
        if self.rapid_accel_thr is not None:
            s.append("set config thr accel = %d" % (self.rapid_accel_thr))
        if self.rapid_decel_thr is not None:
            s.append("set config thr decel = %d" % (self.rapid_decel_thr))
        if self.brake_decel_thr is not None:
            s.append("set config thr rate = %d" % (self.brake_decel_thr))
        if self.brake_speed_thr is not None:
            s.append("set config thr speed = %d" % (self.brake_speed_thr))
        s.append("\n# Set file assignments\n")
        files = [
            ("startup", self.startup),
            ("shutdown", self.shutdown),
            ("changedir", self.change_dir_sound),
            ("brake off", self.set_off_sound),
            ("brake on", self.brake_stop_sound),
            ("thr accel", self.rapid_accel_loop),
            ("thr decel", self.rapid_decel_loop),
        ]
        for file in files:
            if file[1] is not None:
                if isinstance(file[1], (str, list)):
                    break
                s.append('set file %s = "%s"' % (file[0], file[1].filename))
        if self.idle_loops is not None:
            for i, loop in enumerate(self.idle_loops.loops):
                s.append('set file speed %d = "%s"' % (i + 1, loop.filename))
        if self.accel_loops is not None:
            for i, loop in enumerate(self.accel_loops.loops):
                s.append('set file accel %d = "%s"' % (i + 1, loop.filename))
        if self.decel_loops is not None:
            for i, loop in enumerate(self.decel_loops.loops):
                s.append('set file decel %d = "%s"' % (i + 1, loop.filename))
        if self.gated_loops is not None:
            for i, loop in enumerate(self.gated_loops.loops):
                if loop.fileid >= 0xD0 and loop.fileid <= 0xD3:
                    loopid = 11 + (loop.fileid - 0xD0)
                elif loop.fileid >= 0xD4 and loop.fileid <= 0xD7:
                    loopid = 21 + (loop.fileid - 0xD4)
                elif loop.fileid >= 0xD8 and loop.fileid <= 0xDB:
                    loopid = 31 + (loop.fileid - 0xD8)
                elif loop.fileid >= 0xDC and loop.fileid <= 0xDF:
                    loopid = 41 + (loop.fileid - 0xDC)
                s.append('set file gated %d = "%s"' % (loopid, loop.filename))

        if self.notch_count > 1:
            s.append("\n# Activate motor indexed sound effects")
            idx_options = 0
            if self.startup is not None:
                idx_options |= 0x04
            if self.skip_startup:
                idx_options |= 0x08
            motor_op = 0
            if self.motor_ch == 1:
                motor_op = 1
            if self.motor_speed == "current":
                motor_op |= 0x04
            s.append("sound fx 12 0 0x%02X 0x%02X" % (motor_op, idx_options))
        if self.gated_loops is not None:
            s.append("\n# Activate motor gated sound effects")
            if len(self.gated_loops) > 0:
                motor_op = 1 if self.motor_ch == 1 else 0
                # assert using current speed
                motor_op |= 0x04
                s.append("sound fx 9 0 0x%02X 0x%02X" % (motor_op, self.gated_gain))

        if self.other_sounds is not None:
            s.append("\n# Other sound effects")
            for sound in self.other_sounds:
                name = sound["audiofile"].name + sound["audiofile"].ext
                if "probability" in sound:
                    s.append("# random sound effect")
                    a = PFxAction().sound_fx(
                        fx=13, param=[sound["probability"], 0], fileID=name
                    )
                    s.append(a.to_script_str())
                elif "trigger" in sound:
                    if "repeat" in sound and sound["repeat"]:
                        a = PFxAction().repeat_audio_file(fileID=name)
                    else:
                        a = PFxAction().play_audio_file(fileID=name)
                    s.append(
                        a.to_event_script_str(
                            *script_ir_mask_to_evtch(sound["trigger"])
                        )
                    )

        if self.forward_lights is not None:
            s.append("\n# Forward (head) lights")
            mopt = 3 if self.motor_ch == 1 else 1
            a = PFxAction().light_fx(
                self.forward_lights["channels"], 1, param=[mopt, 4, 0, 1, 0]
            )
            s.append(a.to_script_str())

        if self.reverse_lights is not None:
            s.append("\n# Reverse (tail) lights")
            mopt = 4 if self.motor_ch == 1 else 2
            a = PFxAction().light_fx(
                self.reverse_lights["channels"], 1, param=[mopt, 4, 0, 1, 0]
            )
            s.append(a.to_script_str())

        if self.motor_ch == 0:
            ch = 1
        elif self.motor_ch == 1:
            ch = 2
        elif self.motor_ch == -1:
            ch = [1, 2]
        s.append("\n# Setup remote control")
        if self.increase_speed is not None:
            step = 0
            if "amount" in self.increase_speed:
                step = map_pct_to_motor_step(self.increase_speed["amount"])
            s.append("# Increase speed")
            for t in listify(self.increase_speed["trigger"]):
                a = PFxAction().increase_speed(ch, step=step, bidir=False)
                s.append(a.to_event_script_str(*script_ir_mask_to_evtch(t)))
        if self.decrease_speed is not None:
            step = 0
            if "amount" in self.decrease_speed:
                step = map_pct_to_motor_step(self.decrease_speed["amount"])
            s.append("# Decrease speed")
            for t in listify(self.decrease_speed["trigger"]):
                a = PFxAction().decrease_speed(ch, step=step, bidir=False)
                s.append(a.to_event_script_str(*script_ir_mask_to_evtch(t)))
        if self.stop is not None:
            s.append("# Stop")
            for t in listify(self.stop["trigger"]):
                a = PFxAction().stop_motor(ch, estop=False)
                s.append(a.to_event_script_str(*script_ir_mask_to_evtch(t)))
        if self.emergency_stop is not None:
            s.append("# Emergency Stop")
            for t in listify(self.emergency_stop["trigger"]):
                a = PFxAction().stop_motor(ch, estop=True)
                s.append(a.to_event_script_str(*script_ir_mask_to_evtch(t)))
        if self.change_dir is not None:
            s.append("# Change direction")
            for t in listify(self.change_dir["trigger"]):
                a = PFxAction().change_dir(ch)
                s.append(a.to_event_script_str(*script_ir_mask_to_evtch(t)))
        if self.increase_volume is not None:
            s.append("# Increase volume")
            for t in listify(self.increase_volume["trigger"]):
                a = PFxAction().sound_fx(fx=1)
                s.append(a.to_event_script_str(*script_ir_mask_to_evtch(t)))
        if self.decrease_volume is not None:
            s.append("# Decrease volume")
            for t in listify(self.decrease_volume["trigger"]):
                a = PFxAction().sound_fx(fx=2)
                s.append(a.to_event_script_str(*script_ir_mask_to_evtch(t)))
        if self.increase_brightness is not None:
            s.append("# Increase brightness")
            for t in listify(self.increase_brightness["trigger"]):
                a = PFxAction().light_fx([x + 1 for x in range(8)], fx=2)
                s.append(a.to_event_script_str(*script_ir_mask_to_evtch(t)))
        if self.decrease_brightness is not None:
            s.append("# Decrease brightness")
            for t in listify(self.decrease_brightness["trigger"]):
                a = PFxAction().light_fx([x + 1 for x in range(8)], fx=3)
                s.append(a.to_event_script_str(*script_ir_mask_to_evtch(t)))
        if self.clear_remote is not None:
            s.append("# clear actions from remote events")
            for e in listify(self.clear_remote):
                a = PFxAction()
                s.append(a.to_event_script_str(*script_ir_mask_to_evtch(e)))
        s.append("\n")

        if to_brick is not None:
            if to_brick.filedir.has_file("startup.pfx"):
                fid = to_brick.file_id_from_str_or_int("startup.pfx")
            else:
                fid = to_brick.filedir.find_available_file_id()
            sbytes = bytes("\n".join(s), encoding="utf-8")
            fs_copy_file_to(to_brick, fid, "startup.pfx", with_bytes=sbytes)
        elif as_bytes:
            return "\n".join(s)
        else:
            if filename is None:
                return None
            if len(filename) == 0:
                return None
            with open(filename, "w") as f:
                f.write("\n".join(s))
            return None

    def export_pfx_profile(self, fn, brick, audiofiles):
        with open(fn, "wb") as f:
            f.write(bytes("PFX0002", encoding="ascii"))
            pb = []
            pb.extend([0x03, 0x37])
            pb.extend([0xA2, 0x16])
            pb.extend([0, 0, 0, 0])
            pb.append(brick.config.audio.bass)
            pb.append(brick.config.audio.treble)
            pb.append(brick.config.settings_byte())
            for i in range(4):
                pb.append(brick.config.motors[i].to_config_byte())
                pb.extend(brick.config.motors[i].to_speed_bytes())
            pb.append(brick.config.audio.defaultVolume)
            pb.append(brick.config.lights.defaultBrightness)

            pb.append(brick.config.lights.startupBrightness[0])
            pb.append(brick.config.lights.startupBrightness[1])
            pb.append(brick.config.lights.startupBrightness[2])
            pb.append(brick.config.lights.startupBrightness[3])
            pb.append(brick.config.lights.startupBrightness[4])
            pb.append(brick.config.lights.startupBrightness[5])
            pb.append(brick.config.lights.startupBrightness[6])
            pb.append(brick.config.lights.startupBrightness[7])
            pb.append(brick.config.lights.pfBrightnessA)
            pb.append(brick.config.lights.pfBrightnessB)

            pb.append(brick.config.settings.notchCount)
            pb.append(brick.config.settings.notchBounds[0])
            pb.append(brick.config.settings.notchBounds[1])
            pb.append(brick.config.settings.notchBounds[2])
            pb.append(brick.config.settings.notchBounds[3])
            pb.append(brick.config.settings.notchBounds[4])
            pb.append(brick.config.settings.notchBounds[5])
            pb.append(brick.config.settings.notchBounds[6])

            pb.append(brick.config.settings.irAutoOff)
            pb.append(brick.config.settings.bleAutoOff)
            pb.append(brick.config.settings.bleMotorWhenDisconnect)
            pb.append(brick.config.settings.bleAdvertPower)
            pb.append(brick.config.settings.bleSessionPower)
            f.write(bytes(pb))

            file_count = 0
            file_ids = []
            for af in audiofiles:
                if af.is_valid():
                    nBytes = os.path.getsize(af.audiofile.exportpath)
                    pb = []
                    file_ids.append(af.audiofile.fileid)
                    pb.append(af.audiofile.fileid)
                    pb.extend(uint32_to_bytes(nBytes))
                    pb.extend(uint16_to_bytes(af.audiofile.audio.frame_rate))
                    pb.append(16)
                    pb.append(0)
                    pb.extend(uint16_to_bytes(af.audiofile.attr))
                    mb = bytes(af.filename, "utf-8")
                    for x in mb:
                        pb.append(x)
                    for i in range(32 - len(mb)):
                        pb.append(0)
                    f.write(bytes(pb))
                    with open(af.audiofile.exportpath, "rb") as fa:
                        afb = fa.read()
                    f.write(afb)
                    file_count += 1
            script = self.export_script("", as_bytes=True)
            nBytes = len(script)
            pb = []
            for i in range(255):
                if i not in file_ids:
                    pb.append(i)
                    break
            pb.extend(uint32_to_bytes(nBytes))
            pb.extend(uint16_to_bytes(0))
            pb.append(0)
            pb.append(0)
            pb.extend(uint16_to_bytes(0x3080))
            mb = bytes("startup.pfx", "utf-8")
            for x in mb:
                pb.append(x)
            for i in range(32 - len(mb)):
                pb.append(0)
            f.write(bytes(pb))
            f.write(bytes(script, "utf-8"))
            file_count += 1
            for _ in range(PFX_AUDIO_FILES_MAX - file_count):
                f.write(bytes([0xFF]))
            for ch in range(4):
                for ev in range(EVT_ID_TEST_EVENT):
                    action = brick.get_action(ev, ch)
                    f.write(bytes(action.to_bytes()))
