import os
import zlib
import time

from wavplay import WavePlayerLoop

from pydub import AudioSegment

from toolbox import *

TMP_PATH = full_path("~/tmp")


def get_file_crc32(fn):
    with open(fn, "rb") as fp:
        fb = fp.read()
    return zlib.crc32(fb) & 0xFFFFFFFF


class AudioFile:
    FADE_INTERVAL = 5

    def __init__(
        self, fullpath, fileid, attr=None, new_name=None, virtual=False, norm=None
    ):
        self.fullpath = full_path(fullpath)
        self.fileid = fileid
        if attr is not None:
            self.attr = attr
        else:
            if self.fileid >= 0xE0 and self.fileid <= 0xE7:
                self.attr = 0x20 + (self.fileid & 0x07) * 4
            elif self.fileid >= 0xF0 and self.fileid <= 0xF6:
                self.attr = 0x60 + (self.fileid & 0x07) * 4
            elif self.fileid >= 0xE8 and self.fileid <= 0xEE:
                self.attr = 0x40 + (self.fileid & 0x07) * 4
        if virtual:
            self.path = ""
            self.filename = fullpath
            fps = fullpath.split(".")
            if len(fps) > 1:
                self.name, self.ext = fps[0], fps[1]
            else:
                self.name, self.ext = fullpath, "wav"
            self.exportpath = ""
            self.audio = AudioSegment(
                data=bytearray([0, 0]), frame_rate=22050, sample_width=2, channels=1
            )
            self.crc32 = 0
        else:
            self.path, self.filename = split_path(fullpath)
            self.name, self.ext = split_filename(self.filename)
            if new_name is not None:
                self.exportpath = TMP_PATH + os.sep + new_name
                self.filename = new_name
            else:
                self.exportpath = TMP_PATH + os.sep + self.filename
            self.audio = AudioSegment.from_wav(self.fullpath)
            self.convert_to_mono()
            self.audio = self.audio.set_frame_rate(22050)
            if norm is not None:
                self.audio = self.audio.normalize(abs(norm))
            self.apply_fade()
            self.export()
            self.crc32 = get_file_crc32(self.exportpath)
        self.wp = None
        self.looped = False
        self.is_playing = False

    def __str__(self):
        return "%s rate=%d kHz samp=%s ch=%d dBFS=%.1f dur=%.3f" % (
            self.filename,
            self.audio.frame_rate,
            self.audio.sample_width,
            self.audio.channels,
            self.audio.dBFS,
            self.audio.duration_seconds,
        )

    def playback_active(self):
        if self.wp is not None:
            if self.wp.loop and self.is_playing:
                return True
        return False

    def playpause(self):
        if self.is_playing and not self.wp.loop:
            self.is_playing = False
        if not self.is_playing:
            self.wp = WavePlayerLoop(self.exportpath, repeat=self.looped)
            self.wp.play()
        else:
            self.wp.stop()
        self.is_playing = False if self.is_playing else True

    def stop(self):
        if self.is_playing:
            self.wp.stop()

    @staticmethod
    def file_table(files):
        table = Table(show_header=True, header_style="bold blue")
        for i, col in enumerate(
            ["ID", "Attr", "Name", "Length (s)", "Rate (kHz)", "Samp", "Ch", "dBFS"]
        ):
            justify = "right" if i > 2 else "left"
            table.add_column(col, justify=justify)
        for file in files:
            if file is None:
                continue
            table.add_row(
                "[bold green]0x%02X" % (file.fileid),
                "[bold yellow]0x%02X" % (file.attr),
                "[cyan]%s" % (file.filename),
                "%.3f" % (file.audio.duration_seconds),
                "%d" % (file.audio.frame_rate),
                "%d" % (file.audio.sample_width),
                "%d" % (file.audio.channels),
                "%.1f" % (file.audio.dBFS),
            )
        return table

    def convert_to_mono(self):
        if self.audio.channels > 1:
            self.audio = self.audio.set_channels(1)

    def apply_fade(self):
        self.audio = self.audio.fade_in(duration=self.FADE_INTERVAL)
        self.audio = self.audio.fade_out(duration=self.FADE_INTERVAL)

    def export(self):
        self.audio.export(self.exportpath, format="wav")

    def is_on_brick(self, brick, compare_fileid=False):
        for f in brick.filedir.files:
            if self.filename == f.name:
                if compare_fileid and self.fileid == f.id:
                    return True
                if not compare_fileid:
                    return True
        return False

    def same_crc_as_on_brick(self, brick):
        for f in brick.filedir.files:
            if self.filename == f.name:
                if self.crc32 == f.crc32:
                    return True
        return False

    def copy_to_brick(self, brick, overwrite=False, use_fileid=False):
        if self.is_on_brick(brick, compare_fileid=use_fileid):
            if overwrite:
                print(
                    ":yellow_circle: : File [cyan]%s [white]already on brick, but forcing overwrite"
                    % (self.filename)
                )
                brick.remove_file(self.filename)
            elif self.same_crc_as_on_brick(brick):
                print(
                    ":green_circle: : File [cyan]%s [white]already on brick with same CRC32 hash, skipping"
                    % (self.filename)
                )
                return
            else:
                brick.remove_file(self.filename)
        time.sleep(1)
        self.do_file_transfer(brick)

    def do_file_transfer(self, brick):
        fn = self.exportpath
        crc32 = get_file_crc32(fn)
        print("Copying file %s with CRC32=0x%X" % (self.filename, crc32))
        brick.put_file(fn, self.fileid)
        fcrc = 0
        if self.attr > 0:
            print("Setting file attributes=0x%02X" % (self.attr))
            brick.set_file_attributes(self.fileid, self.attr)
        while fcrc == 0:
            time.sleep(1)
            brick.refresh_file_dir()
            f0 = brick.filedir.get_file_dir_entry(self.fileid)
            fcrc = f0.crc32
        print("Copied file reports CRC32=0x%X" % (f0.crc32), f0.crc32 == crc32)
        if self.attr > 0:
            print(
                "Copied file reports attributes=0x%02X" % (f0.attributes),
                f0.attributes == self.attr,
            )
        time.sleep(1)
