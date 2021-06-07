import argparse
import time
from datetime import datetime
from rich import print
from rich.console import Console
import soundfile as sf
import zlib

from toolbox import *
from pfxbrick import *

console = Console()


def get_file_crc32(fn):
    with open(fn, "rb") as fp:
        fb = fp.read()
    return zlib.crc32(fb) & 0xFFFFFFFF


class AudioFile:
    def __init__(self, fullpath, role, idx):
        self.fullpath = fullpath
        self.role = role
        self.idx = idx
        self.path, self.filename = split_path(fullpath)
        _, self.ext = split_filename(self.filename)
        self.info = sf.info(fullpath)
        self.crc32 = get_file_crc32(fullpath)
        self.fileid = self.reserved_id()
        self.attr = self.file_attr()

    def __str__(self):
        return "%s (%s) %d kHz %s %d ch" % (
            self.filename,
            self.info.format,
            self.info.samplerate,
            self.info.subtype,
            self.info.channels,
        )

    def reserved_id(self):
        if self.role == "notch":
            return 0xE0 + self.idx
        elif self.role == "accel":
            return 0xE8 + self.idx
        elif self.role == "decel":
            return 0xF0 + self.idx
        elif self.role == "startup":
            return 0xEF
        elif self.role == "shutdown":
            return 0xF7
        return None

    def file_attr(self):
        if self.role == "notch":
            return 0x20 + self.idx * 4
        elif self.role == "accel":
            return 0x40 + self.idx * 4
        elif self.role == "decel":
            return 0x60 + self.idx * 4
        elif self.role == "startup":
            return 0x5C
        elif self.role == "shutdown":
            return 0x7C
        return None


def test_result(desc, result):
    if result:
        res = ":green_circle:"
    else:
        res = ":red_circle:"
    console.log(res, ":", desc)
    return result


def preflight_check(proj):
    """ Verifies input files """
    ok = True
    fs = FileOps(simulate=True, verbose=False, overwrite=False)

    if not test_result("Source folder is specified", "source" in proj.__dict__):
        ok = False
    if not test_result(
        "Source folder %s exists" % (proj.source), fs.verify_dir_not_file(proj.source)
    ):
        ok = False
    if "startup" in proj.__dict__:
        fn = proj.source + os.sep + proj.startup
        if not test_result(
            "Startup %s file found" % (proj.startup), fs.verify_file(fn)
        ):
            ok = False
        else:
            proj.files[proj.startup] = AudioFile(fn, "startup", 0)
    if "shutdown" in proj.__dict__:
        fn = proj.source + os.sep + proj.shutdown
        if not test_result(
            "Shutdown %s file found" % (proj.shutdown), fs.verify_file(fn)
        ):
            ok = False
        else:
            proj.files[proj.shutdown] = AudioFile(fn, "shutdown", 0)
    if not test_result("Notch_levels are specified", "notch_levels" in proj.__dict__):
        ok = False
    if not test_result("Valid number of notches", proj.notch_levels <= 8):
        ok = False
    if not test_result(
        "Expected number of notch loops specified",
        len(proj.notch_loops) == proj.notch_levels,
    ):
        ok = False
    for i, f in enumerate(proj.notch_loops):
        fn = proj.source + os.sep + f
        if not test_result("Notch loop %s file found" % (f), fs.verify_file(fn)):
            ok = False
        else:
            proj.files[f] = AudioFile(fn, "notch", i)
    if "accel_loops" in proj.__dict__:
        if not test_result(
            "Expected accel loops specified",
            len(proj.accel_loops) + 1 == proj.notch_levels,
        ):
            ok = False
        for i, f in enumerate(proj.accel_loops):
            fn = proj.source + os.sep + f
            if not test_result("Accel loop %s file found" % (f), fs.verify_file(fn)):
                ok = False
            else:
                proj.files[f] = AudioFile(fn, "accel", i)
    if "decel_loops" in proj.__dict__:
        if not test_result(
            "Expected decel loops specified",
            len(proj.decel_loops) + 1 == proj.notch_levels,
        ):
            ok = False
        for i, f in enumerate(proj.decel_loops):
            fn = proj.source + os.sep + f
            if not test_result("Decel loop %s file found" % (f), fs.verify_file(fn)):
                ok = False
            else:
                proj.files[f] = AudioFile(fn, "decel", i)

    return ok


def file_is_on_brick(fn, brick):
    for f in brick.filedir.files:
        if fn == f.name:
            return True
    return False


def same_crc_as_on_brick(af, brick):
    for f in brick.filedir.files:
        if af.filename == f.name:
            if af.crc32 == f.crc32:
                return True
    return False


def do_file_transfer(b, af):
    fn = af.fullpath
    fid = af.fileid
    crc32 = get_file_crc32(fn)
    console.log("Copying file %s with CRC32=0x%X" % (af.filename, crc32))
    b.put_file(fn, fid)
    fcrc = 0
    console.log("Setting file attributes=0x%02X" % (af.attr))
    b.set_file_attributes(fid, af.attr)
    while fcrc == 0:
        time.sleep(1)
        b.refresh_file_dir()
        f0 = b.filedir.get_file_dir_entry(fid)
        fcrc = f0.crc32
    test_result("Copied file reports CRC32=0x%X" % (f0.crc32), f0.crc32 == crc32)
    test_result(
        "Copied file reports attributes=0x%02X" % (f0.attributes),
        f0.attributes == af.attr,
    )
    time.sleep(1)


def install_files(b, proj):
    b.get_config()
    if proj.format:
        console.log("Formatting PFx Brick filesystem")
        b.format_fs(quick=True)
        time.sleep(2)
    b.refresh_file_dir()

    for k, v in proj.files.items():
        is_found = file_is_on_brick(k, b)
        same_crc = same_crc_as_on_brick(v, b)
        if is_found:
            if proj.overwrite:
                console.log(
                    "File: [cyan]%s [white]already on brick, but forcing overwrite"
                    % (k)
                )
                console.log("Removing file %s" % (k))
                b.remove_file(k)
                time.sleep(1)
                do_file_transfer(b, v)
            elif same_crc:
                console.log(
                    "File: [cyan]%s [white]already on brick with same CRC32 hash, skipping"
                    % (k)
                )
            else:
                console.log("File: [cyan]%s [white]already on brick, skipping" % (k))

        else:
            do_file_transfer(b, v)


def set_configuration(b, proj):
    if "default_volume" in proj.__dict__:
        console.log("Setting default_volume=%d" % (proj.default_volume))
        b.config.audio.defaultVolume = proj.default_volume
        b.set_config()
    ch = 0
    if "motor_channel" in proj.__dict__:
        if proj.motor_channel.upper() == "A":
            ch = 0
        else:
            ch = 1
        if "acceleration" in proj.__dict__:
            console.log(
                "Setting motor channel %s acceleration=%d"
                % (proj.motor_channel.upper(), proj.acceleration)
            )
            b.config.motors[ch].accel = proj.acceleration
            b.set_config()
        if "deceleration" in proj.__dict__:
            console.log(
                "Setting motor channel %s deceleration=%d"
                % (proj.motor_channel.upper(), proj.deceleration)
            )
            b.config.motors[ch].decel = proj.deceleration
            b.set_config()
    newaction = PFxAction()
    newaction.soundFxId = EVT_SOUND_PLAY_IDX_MOTOR
    startup = 0x04 if "startup" in proj.__dict__ else 0x00
    skipstartup = 0x08
    if "skip_startup" in proj.__dict__:
        if proj.skip_startup == True:
            skipstartup = 0x08
        else:
            skipstartup = 0x00
    use_current = 0x04
    if "use_speed" in proj.__dict__:
        if proj.use_speed.lower() == "target":
            use_current = 0x00
        else:
            use_current = 0x04
    newaction.soundParam1 = ch | use_current
    newaction.soundParam2 = startup | skipstartup
    found_existing = False
    for e in range(EVT_STARTUP_EVENT1, EVT_STARTUP_EVENT8 + 1):
        action = b.get_action_by_address(e)
        if action.soundFxId == EVT_SOUND_PLAY_IDX_MOTOR:
            console.log("Found an existing startup event=0x%02X to modify" % (e))
            b.set_action_by_address(e, newaction)
            found_existing = True
            break
    if not found_existing:
        for e in range(EVT_STARTUP_EVENT1, EVT_STARTUP_EVENT8 + 1):
            action = b.get_action_by_address(e)
            if action.is_empty():
                console.log("Found free startup event=0x%02X to configure" % (e))
                b.set_action_by_address(e, newaction)
                break


if __name__ == "__main__":
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
    args = parser.parse_args()
    argsd = vars(args)

    fs = FileOps(simulate=True, verbose=True, overwrite=False)
    if not fs.verify_file(argsd["project"]):
        exit()
    print("Reading project file %s" % (colour_path_str(argsd["project"])))
    proj = Params(yml=argsd["project"])
    proj.files = {}
    proj.format = argsd["format"]
    proj.overwrite = argsd["overwrite"]
    r = preflight_check(proj)
    if r:
        test_result("[green bold]Preflight check completed", r)
    else:
        test_result("[red bold]Preflight check failed, exiting", r)
        exit()
    b = PFxBrick()
    r = b.open()
    if not test_result("Opening PFx Brick", r):
        exit()

    r = install_files(b, proj)
    set_configuration(b, proj)
