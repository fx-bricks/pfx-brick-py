#! /usr/bin/env python3

# PFx Brick file system helpers

import hid
from pfxbrick.pfx import *
from pfxbrick.pfxhelpers import *

class PFxFile:
    
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
        
    def read_from_brick(self, msg):
        self.id = msg[3]
        self.size = uint32_toint(msg[4:8])
        self.firstSector = uint16_toint(msg[8:10])
        self.attributes = uint16_toint(msg[8:10])
        self.userData1 = uint32_toint(msg[12:16])
        self.userData2 = uint32_toint(msg[16:20])
        self.crc32 = uint32_toint(msg[20:24])
        sn = bytes(msg[24:56]).decode("utf-8")
        self.name = sn.rstrip('\0')
        
    def __str__(self):
        s = '%02X %-24s %6.1f kB %04X %08X %08X %08X' % (self.id, self.name, float(self.size/1000), self.attributes, self.userData1, self.userData2, self.crc32)
        return s

class PFxDir:
    
    def __init__(self):
        self.numFiles = 0
        self.files = []
        self.bytesUsed = 0
        self.bytesLeft = 0
        
    def __str__(self):
        sb = []
        sb.append('%2s %-24s %6s    %4s %8s %8s %8s' % ('ID', 'Name', 'Size', 'Attr', 'User1', 'User2', 'CRC32'))
        for file in self.files:
            sb.append(str(file))
        sb.append('%d files, %.1f kB used, %.1f kB remaining' % (len(self.files), float(self.bytesUsed/1000), float(self.bytesLeft/1000)))
        s = '\n'.join(sb)
        return s    
        