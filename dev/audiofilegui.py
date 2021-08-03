import os
import PySimpleGUI as sg

from pfxbrick import *
from pfxbrick.pfxfiles import fs_error_check

from toolbox import FileOps

from audiofile import AudioFile


class AudioFileGui:
    def __init__(self, **kwargs):
        self.size = (125, 20)
        self.graph_el = None
        self.parent = None
        self.title = ""
        self.fileid = 0xFF
        self.attr = None
        self.filename = ""
        self.disabled = False
        self.highlighted = False
        self.show_progress = False
        self.looped = False
        self.show_attr = False
        self.fileid_color = "#800000"
        self.attr_color = "#000080"
        self.filename_color = "#000000"
        self.progress_color = "#00A0E0"
        self.disabled_color = "#404040"
        self.highlight_color = "#C0FFC0"
        self.fileid_size = (5, 1)
        self.attr_size = (5, 1)
        self.filename_size = (15, 1)
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v
        self.gkey = "0x%02Xbar" % (self.fileid)
        self.pkey = "0x%02Xplay" % (self.fileid)
        self.ekey = "0x%02Xerase" % (self.fileid)
        self.fkey = "0x%02Xfile" % (self.fileid)
        self.bkey = "0x%02Xbrowse" % (self.fileid)
        self.audiofile = None
        if self.attr is None:
            if self.fileid >= 0xE0 and self.fileid <= 0xE7:
                self.attr = 0x20 + (self.fileid & 0x07) * 4
            elif self.fileid >= 0xF0 and self.fileid <= 0xF6:
                self.attr = 0x60 + (self.fileid & 0x07) * 4
            elif self.fileid >= 0xE8 and self.fileid <= 0xEE:
                self.attr = 0x40 + (self.fileid & 0x07) * 4
            else:
                self.attr = 0

    def set_graph_el(self, window):
        self.graph_el = window[self.gkey]

    def set_audiofile(self, audiofile):
        self.audiofile = audiofile
        self.audiofile.looped = self.looped
        self.fileid = audiofile.fileid
        self.attr = audiofile.attr
        self.filename = audiofile.filename

    def is_valid(self):
        if self.fileid == 0xFF:
            return False
        if self.filename == "":
            return False
        if self.disabled:
            return False
        return True

    def clear(self):
        self.attr = 0
        self.filename = ""
        self.audiofile = None

    def bg_color(self, base_color=False):
        if self.fileid in [0xEF, 0xF7, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE]:
            bg = "#80E0C0"
        elif self.fileid in range(0xD0, 0xE0):
            bg = "#E0B0C0"
        else:
            bg = "#FFFFFF"
        if base_color:
            return bg
        if self.audiofile is not None:
            if self.audiofile.playback_active():
                bg = "#60C0FF"
        if self.highlighted:
            bg = "#005030"
        if self.filename == "" or self.fileid == 0xFF or self.disabled:
            bg = self.disabled_color
        return bg

    def get_layout(self):
        layout = [
            [
                sg.Text(
                    "0x%02X" % (self.fileid),
                    size=self.fileid_size,
                    background_color=self.bg_color(base_color=True),
                    text_color=self.fileid_color,
                    border_width=0,
                    font="Any 10",
                    visible=True,
                ),
                sg.Text(
                    "0x%02X" % (self.attr),
                    size=self.attr_size,
                    background_color="#FFFFFF",
                    text_color=self.attr_color,
                    border_width=0,
                    font="Any 10",
                    visible=True if self.attr > 0 and self.show_attr else False,
                ),
                sg.Button("✕", font="Any 10", key=self.ekey, enable_events=True),
                sg.Button("▶︎", font="Any 10", key=self.pkey, enable_events=True),
                sg.Input(visible=False, enable_events=True, key=self.fkey),
                sg.FileBrowse("...", font="Any 10"),
            ],
            [sg.Graph(self.size, (0, 0), self.size, key=self.gkey)],
        ]
        return [sg.Frame(self.title, layout)]

    def set_notch_count(self, count):
        if self.fileid >= 0xE0 and self.fileid <= 0xE7:
            idx = self.fileid - 0xE0
        elif self.fileid >= 0xF0 and self.fileid <= 0xF6:
            idx = self.fileid - 0xF0 + 1
        elif self.fileid >= 0xE8 and self.fileid <= 0xEE:
            idx = self.fileid - 0xE8 + 1
        else:
            return
        if idx >= count:
            self.disabled = True
        else:
            self.disabled = False

    def process_event(self, event, values, profile=None):
        if event == self.ekey:
            self.disabled = False if self.disabled else True
            if self.disabled and self.audiofile is not None:
                self.audiofile.stop()
            self.update()
        elif event == self.pkey:
            if self.audiofile is not None and not self.disabled:
                self.audiofile.playpause()
        elif event == self.fkey:
            fs = FileOps()
            if fs.verify_dir_not_file(values[self.fkey]):
                return
            self.audiofile = AudioFile(values[self.fkey], self.fileid, self.attr)
            self.filename = self.audiofile.name
            self.disabled = False
            if profile is not None:
                profile.update_audiofile_with_id(self.audiofile, self.fileid)
            self.update()

    def copy_to_brick(self, brick):
        if not self.is_valid():
            return
        self.show_progress = True
        if self.audiofile.is_on_brick(brick):
            self.update(progress=1.0)
            return
        nBytes = os.path.getsize(self.audiofile.fullpath)
        if nBytes > 0:
            msg = [PFX_CMD_FILE_OPEN]
            msg.append(self.fileid)
            msg.append(0x06)  # CREATE | WRITE mode
            msg.extend(uint32_to_bytes(nBytes))
            name = os.path.basename(self.audiofile.fullpath)
            nd = bytes(name, "utf-8")
            for b in nd:
                msg.append(b)
            for i in range(32 - len(nd)):
                msg.append(0)
            res = usb_transaction(brick.dev, msg)
            if not res:
                return
            if fs_error_check(res[1]):
                return
            f = open(self.audiofile.fullpath, "rb")
            nCount = 0
            err = False
            while (nCount < nBytes) and not err:
                buf = f.read(61)
                nRead = len(buf)
                nCount += nRead
                if nRead > 0:
                    msg = [PFX_CMD_FILE_WRITE]
                    msg.append(self.fileid)
                    msg.append(nRead)
                    for b in buf:
                        msg.append(b)
                    res = usb_transaction(brick.dev, msg)
                    err = fs_error_check(res[1])
                    self.update(progress=nRead / nCount)
            f.close()
            msg = [PFX_CMD_FILE_CLOSE]
            msg.append(self.fileid)
            res = usb_transaction(brick.dev, msg)
            fs_error_check(res[1])

    def update(self, progress=None):
        if self.disabled:
            self.show_progress = False
        sp = (
            progress is not None
            and not self.filename == ""
            and not self.disabled
            and not self.highlighted
        )
        if sp or self.show_progress:
            if progress is None:
                width = 0
            else:
                width = progress * self.size[0]
            self.graph_el.draw_rectangle(
                (1, self.size[1] - 1),
                (width, 1),
                line_color=self.progress_color,
                fill_color=self.progress_color,
            )
        else:
            self.graph_el.draw_rectangle(
                (0, self.size[1]),
                (self.size[0], 0),
                line_color="black",
                fill_color=self.bg_color(),
            )
        tc = self.highlight_color if self.highlighted else self.filename_color
        tc = tc if not self.disabled else self.disabled_color
        self.graph_el.draw_text(
            self.filename, (self.size[0] / 2, self.size[1] / 2), color=tc, font="Any 12"
        )


def main():
    af1 = AudioFile("~/Desktop/GMDLoop1.wav", 0xE0)
    afg1 = AudioFileGui(
        title="Gate Loop 1", fileid=0xE0, filename="abc123.wav", highlighted=True
    )
    afg1.set_audiofile(af1)

    afg2 = AudioFileGui(title="Gate Loop 2", fileid=0xD1, filename="")
    layout = [[afg1.get_layout(), afg2.get_layout()]]

    window = sg.Window("Widget Test", layout, finalize=True)
    afiles = [afg1, afg2]
    for f in afiles:
        f.set_graph_el(window)
    x = 0
    while True:  # Event Loop
        event, values = window.read()
        afg1.update(progress=x)
        afg2.update(progress=x)
        x += 0.1
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        for f in afiles:
            f.process_event(event)

    window.close()


if __name__ == "__main__":
    main()
