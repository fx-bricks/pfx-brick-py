# from typeshed import SupportsDivMod
import os

from toolbox import *

from audiofile import AudioFile


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
        if "fileid_base" not in kwargs:
            kwargs["fileid_base"] = 0xD0
        super().__init__(path, files, attr_base=0x10, **kwargs)


class SoundProfile:
    def __init__(self):
        self.source_path = None
        self.acceleration = None
        self.deceleration = None
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
        self.random_sounds = None

        self.audio_files = None

    def clear(self):
        self.source_path = None
        self.acceleration = None
        self.deceleration = None
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
        self.random_sounds = None

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
                if k == "set_off_sound":
                    fid = 0xFB
                elif k == "rapid_accel_loop":
                    fid = 0xFC
                elif k == "brake_stop_sound":
                    fid = 0xFE
                elif k == "rapid_decel_loop":
                    fid = 0xFD
                fn = d["source"] + os.sep + v[0]
                self.__dict__[k] = AudioFile(fn, fileid=fid, attr=0)
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

            elif k == "startup":
                fn = d["source"] + os.sep + v
                self.startup = AudioFile(fn, fileid=0xEF, attr=0x5C)
            elif k == "shutdown":
                fn = d["source"] + os.sep + v
                self.shutdown = AudioFile(fn, fileid=0xF7, attr=0x7C)
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
                elif k == "gated_notch2":
                    base = 0xD4
                elif k == "gated_notch3":
                    base = 0xD8
                elif k == "gated_notch4":
                    base = 0xDC
                if self.gated_loops is not None:
                    self.gated_loops.append(d["source"], v, fileid_base=base)
                else:
                    self.gated_loops = GatedLoops(d["source"], v, fileid_base=base)
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
            new_bounds = self.bounds_from_notchcount(self.notch_count)
            self.notch_bounds = new_bounds

    def update_audiofile_with_id(self, audiofile, fileid):
        if fileid == 0xEF:
            self.startup = audiofile
        elif fileid == 0xFA:
            self.change_dir_sound = audiofile
        elif fileid == 0xF7:
            self.shutdown = audiofile
        elif fileid & 0xE0:
            idx = fileid & 0x0F
            if idx < 8:
                self.idle_loops.loops[idx] = audiofile
            elif idx < 0x0F and idx >= 8:
                self.accel_loops.loops[idx] = audiofile
        elif fileid & 0xF0:
            idx = fileid & 0x0F
            if idx < 7:
                self.decel_loops.loops[idx] = audiofile
        elif fileid == 0xFC:
            self.rapid_accel_loop = audiofile
        elif fileid == 0xFD:
            self.rapid_decel_loop = audiofile
        elif fileid == 0xFB:
            self.set_off_sound = audiofile
        elif fileid == 0xFE:
            self.brake_stop_sound = audiofile

    def export_script(self, filename):
        """Exports a startup.pfx script file which can be copied to a PFx Brick
        automatically configure it for this sound profile.
        """
        if filename is None:
            return
        if len(filename) == 0:
            return
        s = []
        with open(filename, "w") as f:
            s.append("# Sound profile configuration script\n")
            s.append("# Set configuration\n")
            s.append("set config vol = %d" % (self.default_volume))
            ch = "a" if self.motor_ch == 0 else "b"
            s.append("set config motor %s accel = %d" % (ch, self.acceleration))
            s.append("set config motor %s decel = %d" % (ch, self.deceleration))
            s.append("set config nb = %d" % (self.notch_count))
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

            s.append("\n# Activate sound effects\n")
            if self.notch_count > 1:
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
                if len(self.gated_loops) > 0:
                    motor_op = 0
                    if self.motor_ch == 1:
                        motor_op = 1
                    # assert using current speed
                    motor_op |= 0x04
                    s.append("sound fx 9 0 0x%02X 0x%02X" % (motor_op, self.gated_gain))

            s.append("\n# Activate random sound effects\n")
            if self.random_sounds is not None:
                for sound in self.random_sounds:
                    s.append(
                        'sound fx 13 "%s" %d 0'
                        % (sound["filename"], sound["probability"])
                    )
            s.append("\n")
            f.write("\n".join(s))
