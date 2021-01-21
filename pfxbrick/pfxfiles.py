#! /usr/bin/env python3
#
# Copyright (C) 2018  Fx Bricks Inc.
# This file is part of the pfxbrick python module.
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# PFx Brick file system helpers

import hid
import os
from pfxbrick import *
from pfxbrick.pfxhelpers import *


def fs_get_fileid_from_name(hdev, name):
    """
    Resolves a text string filename into a numeric file ID.

    :param hdev: device I/O handle
    :returns: integer file ID or 0xFF if not found
    """
    fileid = 0xFF
    fb = bytes(name, "utf-8")
    p = [len(fb)]
    p.extend(fb)
    res = cmd_file_dir(hdev, PFX_DIR_REQ_GET_NAMED_FILE_ID, p)
    if len(res) >= 3:
        fileid = int(res[2])
    return fileid


def fs_error_check(res):
    """
    Convenience error status lookup function used by other file system functions.

    :param res: result status code byte returned by almost all file system ICD messages
    :returns: True if there is an error, False on success
    """
    if res > 62:
        print("File system error: [%02X] %s" % (res, get_error_str(res)))
        return True
    else:
        return False


def fs_format(hdev, quick=False):
    """
    Sends an ICD message to format the PFx Brick file system.

    :param hdev: USB HID session handle
    :param boolean quick: If True, only occupied sectors are erased. If False, every sector is erased, i.e. a complete format.
    """
    msg = [PFX_CMD_FILE_FORMAT_FS, PFX_FORMAT_BYTE0, PFX_FORMAT_BYTE1, PFX_FORMAT_BYTE2]
    if quick:
        msg.append(0)
    else:
        msg.append(1)
    res = usb_transaction(hdev, msg)
    fs_error_check(res[1])


def fs_remove_file(hdev, fid):
    """
    Sends an ICD message to remove a file from the PFx Brick file system.

    :param hdev: USB HID session handle
    :param fid: the file ID of the file to remove
    """
    msg = [PFX_CMD_FILE_REMOVE]
    msg.append(fid)
    res = usb_transaction(hdev, msg)
    fs_error_check(res[1])


def fs_copy_file_to(hdev, fid, fn, show_progress=True):
    """
    File copy handler to put a file on the PFx Brick.

    This function handles the process of opening and transferring
    file data from the host to the PFx Brick file system. A copy session
    may involve many message transactions with the PFx Brick and could
    be time consuming. Therefore, a progress bar can be optionally shown
    on the console to monitor the transfer.

    :param hdev: USB HID session handle
    :param fid: a unique file ID to assign the copied file.
    :param fn: the host filename (optionally including path) to copy
    :param boolean show_progress: a flag to show the progress bar indicator during transfer.
    """
    nBytes = os.path.getsize(fn)
    if nBytes > 0:
        msg = [PFX_CMD_FILE_OPEN]
        msg.append(fid)
        msg.append(0x06)  # CREATE | WRITE mode
        msg.extend(uint32_to_bytes(nBytes))
        name = os.path.basename(fn)
        nd = bytes(name, "utf-8")
        for b in nd:
            msg.append(b)
        for i in range(32 - len(nd)):
            msg.append(0)
        res = usb_transaction(hdev, msg)

        if res:
            if not fs_error_check(res[1]):
                f = open(fn, "rb")
                nCount = 0
                err = False
                while (nCount < nBytes) and not err:
                    buf = f.read(61)
                    nRead = len(buf)
                    nCount += nRead
                    if nRead > 0:
                        msg = [PFX_CMD_FILE_WRITE]
                        msg.append(fid)
                        msg.append(nRead)
                        for b in buf:
                            msg.append(b)
                        res = usb_transaction(hdev, msg)
                        err = fs_error_check(res[1])
                        if show_progress:
                            printProgressBar(
                                nCount,
                                nBytes,
                                prefix="Copying:",
                                suffix="Complete",
                                length=50,
                            )
                f.close()
                msg = [PFX_CMD_FILE_CLOSE]
                msg.append(fid)
                res = usb_transaction(hdev, msg)
                fs_error_check(res[1])


def fs_copy_file_from(hdev, pfile, fn=None, show_progress=True):
    """
    File copy handler to get a file from the PFx Brick.

    This function handles the process of opening and transferring
    file data from the PFx Brick file system to the host. A copy session
    may involve many message transactions with the PFx Brick and could
    be time consuming. Therefore, a progress bar can be optionally shown
    on the console to monitor the transfer.

    :param hdev: USB HID session handle
    :param PFxFile pfile: a PFxFile object specifying the file to copy.
    :param fn: optional name to override the filename of the host's copy.
    :param boolean show_progress: a flag to show the progress bar indicator during transfer.
    """
    msg = [PFX_CMD_FILE_OPEN]
    msg.append(pfile.id)
    msg.append(0x01)  # READ mode
    res = usb_transaction(hdev, msg)
    if res:
        if not fs_error_check(res[1]):
            nf = pfile.name
            if fn is not None:
                nf = fn
            f = open(nf, "wb")
            nCount = 0
            err = False
            while (nCount < pfile.size) and not err:
                msg = [PFX_CMD_FILE_READ]
                msg.append(pfile.id)
                nToRead = pfile.size - nCount
                if nToRead > 62:
                    nToRead = 62
                msg.append(nToRead)
                res = usb_transaction(hdev, msg)
                err = fs_error_check(res[1])
                if not err:
                    nCount += res[1]
                    b = bytes(res[2 : 2 + res[1]])
                    f.write(b)
                if show_progress:
                    printProgressBar(
                        nCount,
                        pfile.size,
                        prefix="Copying:",
                        suffix="Complete",
                        length=50,
                    )
            f.close()
            msg = [PFX_CMD_FILE_CLOSE]
            msg.append(pfile.id)
            res = usb_transaction(hdev, msg)
            fs_error_check(res[1])


class PFxFile:
    """
    File directory entry container class.

    This class contains directory entry data for a file on the PFx file system.

    Attributes:
        id (:obj:`int`): unique file ID

        size (:obj:`int`): size in bytes

        firstSector (:obj:`int`): the first 4k sector index in flash memory

        attributes (:obj:`int`): 16-bit attributes field

        userData1 (:obj:`int`): 32-bit user defined data field

        userData2 (:obj:`int`): 32-bit user defined data field

        crc32 (:obj:`int`): CRC32 hash of the file (auto computed after write)

        name (:obj:`str`): UTF-8 filename up to 32 bytes
    """

    def __init__(self):
        self.id = 0
        self.size = 0
        self.firstSector = 0
        self.attributes = 0
        self.userData1 = 0
        self.userData2 = 0
        self.crc32 = 0
        self.name = ""

    def is_audio_file(self):
        """
        Checks the file attributes to see if this file is a valid audio WAV file.

        :returns: True if it is valid audio WAV file
        """
        if (self.attributes & PFX_FILE_FMT_MASK) == PFX_FILE_FMT_WAV:
            if self.userData1 != 0 and self.userData2 != 0:
                return True
        return False

    def is_script_file(self):
        """
        Checks the file attributes to see if this file is a valid script file.

        :returns: True if it is valid script file
        """
        if (self.attributes & PFX_FILE_ATTR_MASK) == PFX_FILE_ATTR_SCRIPT:
            return True
        if (self.attributes & PFX_FILE_FMT_MASK) == PFX_FILE_FMT_PFX:
            return True
        return False

    def from_bytes(self, msg):
        """
        Converts the message string bytes read from the PFx Brick into
        the corresponding data members of this class.
        """
        self.id = msg[3]
        self.size = uint32_toint(msg[4:8])
        self.firstSector = uint16_toint(msg[8:10])
        self.attributes = uint16_toint(msg[10:12])
        self.userData1 = uint32_toint(msg[12:16])
        self.userData2 = uint32_toint(msg[16:20])
        self.crc32 = uint32_toint(msg[20:24])
        sn = bytes(msg[24:56]).decode("utf-8")
        self.name = sn.rstrip("\0")

    def __str__(self):
        """
        Convenient human readable string of a file directory entry. This allows
        a :py:class:`PFxFile` object to be used with :obj:`str` and :obj:`print` methods.
        """
        s = "%3d %-24s %6.1f kB %04X %08X %08X %08X" % (
            self.id,
            self.name,
            float(self.size / 1000),
            self.attributes,
            self.userData1,
            self.userData2,
            self.crc32,
        )
        return s


class PFxDir:
    """
    File directory container class.

    This class contains PFx file system directory.

    Attributes:
        numFiles (:obj:`int`): number of files in the file system

        files ([:obj:`PFxFile`]): a list of PFxFile objects corresponding to directory entries

        bytesUsed (:obj:`int`): bytes occupied by files

        bytesLeft (:obj:`int`): remaining space in bytes
    """

    def __init__(self):
        self.numFiles = 0
        self.files = []
        self.bytesUsed = 0
        self.bytesLeft = 0

    def get_file_dir_entry(self, fid):
        """
        Returns a file directory entry containined in a :py:class:`PFxFile` class.

        :param int fid: the unique file ID of desired directory entry
        :returns: :py:class:`PFxFile` directory entry
        """
        for f in self.files:
            if f.id == fid:
                return f

    def find_available_file_id(self):
        """
        Returns the next available unique file ID from the file system.

        The directory is scanned for all currently used file ID values and
        returns an un-used/available file ID value.

        :returns: :obj:`int` next available file ID value, or None
        """
        used_ids = [x.id for x in self.files]
        for x in range(255):
            if x not in used_ids:
                return x
        return None

    def __str__(self):
        """
        Convenient human readable string of the file directory. This allows
        a :py:class:`PFxDir` object to be used with :obj:`str` and :obj:`print` methods.
        """
        sb = []
        sb.append(
            "%3s %-24s %6s    %4s %8s %8s %8s"
            % ("ID", "Name", "Size", "Attr", "User1", "User2", "CRC32")
        )
        for f in self.files:
            sb.append(str(f))
        sb.append(
            "%d files, %.1f kB used, %.1f kB remaining"
            % (
                len(self.files),
                float(self.bytesUsed / 1000),
                float(self.bytesLeft / 1000),
            )
        )
        s = "\n".join(sb)
        return s
