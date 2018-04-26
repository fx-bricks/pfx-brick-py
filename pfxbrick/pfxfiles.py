#! /usr/bin/env python3

# PFx Brick file system helpers

import hid
import os
from pfxbrick.pfx import *
from pfxbrick.pfxhelpers import *
from pfxbrick.pfxmsg import usb_transaction

def file_system_error_check(res):
    if res > 62:
        print("File system error: %02X" % res)
        return True
    else:
        return False

def copy_file_to_brick(hdev, id, fn):
    nBytes = os.path.getsize(fn)
    if nBytes > 0:
        msg = [PFX_CMD_FILE_OPEN]
        msg.append(id)
        msg.append(0x06) # CREATE | WRITE mode
        msg.extend(uint32_to_bytes(nBytes))
        name = os.path.basename(fn)
        nd = bytes(name, "utf-8")
        for b in nd:
            msg.append(b)
        for i in range(32-len(nd)):
            msg.append(0)
        res = usb_transaction(hdev, msg)
        
        if res:
            if not file_system_error_check(res[1]):
                f = open(fn, 'rb')
                nCount = 0
                err = False
                while (nCount < nBytes) and not err:
                    buf = f.read(61)
                    nRead = len(buf)
                    nCount += nRead
                    if nRead > 0:
                        msg = [PFX_CMD_FILE_WRITE]
                        msg.append(id)
                        msg.append(nRead)
                        for b in buf:
                            msg.append(b)
                        res = usb_transaction(hdev, msg)
                        err = file_system_error_check(res[1])
                        printProgressBar(nCount, nBytes, prefix = 'Copying:', suffix = 'Complete', length = 50)
                f.close()
                msg = [PFX_CMD_FILE_CLOSE]
                msg.append(id)
                res = usb_transaction(hdev, msg)
                file_system_error_check(res[1])

def copy_file_from_brick(hdev, pfile, fn=None):

    msg = [PFX_CMD_FILE_OPEN]
    msg.append(pfile.id)
    msg.append(0x01) # READ mode
    res = usb_transaction(hdev, msg)
    if res:
        if not file_system_error_check(res[1]):
            nf = pfile.name
            if fn is not None:
                nf = fn
            f = open(nf, 'wb')
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
                err = file_system_error_check(res[1])
                if not err:
                    nCount += res[1]
                    b = bytes(res[2:2+res[1]])
                    f.write(b)
                printProgressBar(nCount, pfile.size, prefix = 'Copying:', suffix = 'Complete', length = 50)
            f.close()
            msg = [PFX_CMD_FILE_CLOSE]
            msg.append(pfile.id)
            res = usb_transaction(hdev, msg)
            file_system_error_check(res[1])

class PFxFile:
    """
    File directory entry container class.
    
    This class contains directory information for a file on the PFx file system.
    """
    def __init__(self):
        self.id = 0
        self.size = 0
        self.firstSector = 0
        self.attributes = 0
        self.userData1 = 0
        self.userData2 = 0
        self.crc32 = 0
        self.name = ''
    
    def is_audio_file(self):
        if (self.attributes & PFX_FILE_FMT_MASK) == PFX_FILE_FMT_WAV:
            if self.userData1 != 0 and self.userData2 != 0:
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
        self.name = sn.rstrip('\0')
        
    def __str__(self):
        s = '%02X %-24s %6.1f kB %04X %08X %08X %08X' % (self.id, self.name, float(self.size/1000), self.attributes, self.userData1, self.userData2, self.crc32)
        return s

class PFxDir:
    """
    File directory container class.
    
    This class contains PFx file system directory.
    """
    def __init__(self):
        self.numFiles = 0
        self.files = []
        self.bytesUsed = 0
        self.bytesLeft = 0

    def get_file_dir_entry(self, id):
        for f in self.files:
            if f.id == id:
                return f
        
    def __str__(self):
        sb = []
        sb.append('%2s %-24s %6s    %4s %8s %8s %8s' % ('ID', 'Name', 'Size', 'Attr', 'User1', 'User2', 'CRC32'))
        for f in self.files:
            sb.append(str(f))
        sb.append('%d files, %.1f kB used, %.1f kB remaining' % (len(self.files), float(self.bytesUsed/1000), float(self.bytesLeft/1000)))
        s = '\n'.join(sb)
        return s    
        