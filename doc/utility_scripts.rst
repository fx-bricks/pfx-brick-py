.. _utilities:

***************
Utility Scripts
***************

Installing the pfxbrick python package also installs a collection of useful utility scripts into your python environment path.  These command line scripts can be launched directly from your system's terminal shell / command prompt.

---------------------
File System Utilities
---------------------

pfxdir
======

Show file system directory on PFx Brick.

.. code-block:: shell

    $ pfxdir -h
    usage: pfxdir [-h] [-s SERIALNO] [-c]

    PFx Brick file directory listing

    optional arguments:
    -h, --help            show this help message and exit
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)
    -c, --colour          Print directory listing in colour

.. code-block:: shell

    $ pfxdir
    ID Name                       Size    Attr    User1    User2    CRC32 Start Ext Attr
      1 ShortRelease1.wav          89.4 kB 0000 00015D2E 0000002C 9C182DB0  00AB 01
      0 chirp11k16.wav             66.2 kB 0001 00010266 0000002C E62906FE  09FC 00
    240 Decel21.wav                66.1 kB 0060 00010238 0000002C AF9852B0  0270 F0 Decel 2-1
    241 Decel32.wav                66.1 kB 0064 00010238 0000002C AF9852B0  01DC F1 Decel 3-2
    242 Decel43.wav                66.1 kB 0068 00010238 0000002C AF9852B0  0180 F2 Decel 4-3
    224 Notch1Loop.wav            209.0 kB 0020 00033030 0000002C AAAC5DE9  012F E0 Loop 1
    225 Notch2Loop.wav            205.7 kB 0024 00032370 0000002C 7121B4E2  0FB0 E1 Loop 2
    226 Notch3Loop.wav             66.1 kB 0028 00010238 0000002C AF9852B0  0ECA E2 Loop 3
    227 Notch4Loop.wav             66.1 kB 002C 00010238 0000002C E80E4426  0EDB E3 Loop 4
    232 Accel12.wav               341.2 kB 0040 000534D0 0000002C 0B2165F0  0E65 E8 Accel 1-2
    233 Accel23.wav                66.1 kB 0044 00010238 0000002C AF9852B0  0C06 E9 Accel 2-3
    234 Accel34.wav                66.1 kB 0048 00010238 0000002C AF9852B0  0C17 EA Accel 3-4
    250 DirChange.wav              44.8 kB 0000 0000AF04 0000002C 2655F9DF  0C28 FA Dir Change
    251 SetOff.wav                180.3 kB 0000 0002C00C 0000002C 78B0598B  0BD9 FB Set Off
    254 Brake.wav                 165.9 kB 0000 000287B6 0000002C 8D664E41  0AA2 FE Brake
    208 L1Chuff11.wav              66.1 kB 0000 00010238 0000002C 6533518C  09DC D0 Gated Loop 11
    212 L2Chuff21.wav              66.1 kB 0000 00010238 0000002C 6533518C  09C5 D4 Gated Loop 21
    216 L3Chuff31.wav              37.1 kB 0000 000090DE 0000002C F87F4D22  0966 D8 Gated Loop 31
    220 L4Chuff41.wav              24.9 kB 0000 00006126 0000002C 1C0194A5  0941 DC Gated Loop 41
    209 L1Chuff12.wav              66.1 kB 0000 00010238 0000002C 0C1867FE  0914 D1 Gated Loop 12
    213 L2Chuff22.wav              66.1 kB 0000 00010238 0000002C 0C1867FE  08A0 D5 Gated Loop 22
    217 L3Chuff32.wav              37.1 kB 0000 000090DE 0000002C 48A7A5E5  083C D9 Gated Loop 32
    221 L4Chuff42.wav              25.0 kB 0000 00006154 0000002C 84356417  081D DD Gated Loop 42
    210 L1Chuff13.wav              66.1 kB 0000 0001020C 0000002C 6761445C  07EF D2 Gated Loop 13
    214 L2Chuff23.wav              66.1 kB 0000 0001020C 0000002C 6761445C  0763 D6 Gated Loop 23
    218 L3Chuff33.wav              37.1 kB 0000 000090DE 0000002C E5FDE1F2  0709 DA Gated Loop 33
    222 L4Chuff43.wav              25.0 kB 0000 00006154 0000002C F89C7790  06E6 DE Gated Loop 43
    211 L1Chuff14.wav              66.1 kB 0000 0001020C 0000002C 73E1E871  06B4 D3 Gated Loop 14
    215 L2Chuff24.wav              66.1 kB 0000 0001020C 0000002C 73E1E871  0636 D7 Gated Loop 24
    219 L3Chuff34.wav              37.1 kB 0000 000090DE 0000002C C17B64C0  05D8 DB Gated Loop 34
    223 L4Chuff44.wav              24.9 kB 0000 00006126 0000002C 68782357  05B6 DF Gated Loop 44
      2 ShortRelease2.wav         110.7 kB 0000 0001B036 0000002C 6B93834B  02E5 02
      3 ShortRelease3.wav         138.1 kB 0000 00021B5C 0000002C 5B6ECDAA  0163 03
      4 Whistle1.wav              153.0 kB 0000 00025596 0000002C 5DAC6F9B  0F46 04
      5 Whistle2.wav               67.4 kB 0000 0001070C 0000002C 77DA7986  0CA5 05
      6 SlowBell.wav               54.9 kB 0000 0000D61E 0000002C D0C95492  0AFA 06
      7 FastBell.wav               68.7 kB 0000 00010C0A 0000002C 6C331841  092D 07
      8 Coupler1.wav               35.7 kB 0002 00008B46 0000002C 7DC4A0F9  077A 08
      9 Coupler2.wav              175.6 kB 0000 0002ADC8 0000002C 4CE8022A  0595 09
     16 startup.pfx                 2.7 kB 3080 00000000 00000000 4B121299  043C 10
    40 files, 3473.4 kB used, 13287.4 kB remaining

pfxcat
======

Dump the contents of a file to the console.  Similar to the unix `cat` or Windows `type` command.

.. code-block:: shell

    $ pfxcat -h
    usage: pfxcat [-h] [-s SERIALNO] file

    PFx Brick print file contents

    positional arguments:
    file                  file name or file ID to show contents

    optional arguments:
    -h, --help            show this help message and exit
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)

.. code-block:: shell

    $ pfxcat my_script.txt
    #
    # Looping test
    #
    set $A = 0.1
    set $B = 0.1
    set $C = 0.5

    light all off
    repeat 8 {
        light [1] on fade $A
        wait $B
        light [1] off fade $A
        wait $C
    }
    light all off
    $

pfxrm
=====

Removes a file from the PFx Brick file system.

.. code-block:: shell

    $ pfxrm -h
    usage: pfxrm [-h] [-s SERIALNO] file

    remove a file from the PFx Brick

    positional arguments:
    file                  file name or file ID to remove

    optional arguments:
    -h, --help            show this help message and exit
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)

pfxget
======

Gets a file from the PFx Brick and copies it to your local file system.

.. code-block:: shell

    $ pfxget -h
    usage: pfxget [-h] [-s SERIALNO] file [dest]

    copy a file from the PFx Brick to host computer

    positional arguments:
    file                  is file ID or filename to copy
    dest                  is optional local file path override for copied file

    optional arguments:
    -h, --help            show this help message and exit
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)

.. code-block:: shell

    $ pfxget GMDLoop1.wav
    Copying file GMDLoop1.wav as GMDLoop1.wav from brick...
    GMDLoop1.wav ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 33.3/33.3 KB • 28.4 kB/s • 0:00:00

.. code-block:: shell

    $ pfxget GMDLoop1.wav ~/tmp/loop1.wav
    Copying file GMDLoop1.wav as /Users/fxbricks/tmp/loop1.wav from brick...
    /Users/fxbricks/tmp/loop1.wav ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 33.3/33.3 KB • 28.3 kB/s • 0:00:00


pfxput
======

Copies a file from your local file system to the PFx Brick.

.. code-block:: shell

    $ pfxput -h
    usage: pfxput [-h] [-s SERIALNO] file [dest]

    copy a file to the PFx Brick from host computer

    positional arguments:
    file                  is the local filename to copy
    dest                  is optional file ID instead of next available ID

    optional arguments:
    -h, --help            show this help message and exit
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)

.. code-block:: shell

    $ pfxput ~/tmp/loop1.wav
    Copying file loop1.wav to PFx Brick...
    loop1.wav ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 33.3/33.3 KB • 15.6 kB/s • 0:00:00

.. code-block:: shell

    $ pfxput ~/tmp/loop1.wav 10
    Copying file loop1.wav as 10 to PFx Brick...
    loop1.wav ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 33.3/33.3 KB • 15.6 kB/s • 0:00:00

Copying a file with the same filename as a file that is on the PFx Brick will replace it.

.. code-block:: shell

    $ pfxput ~/tmp/loop1.wav
    Replacing file loop1.wav on PFx Brick...
    loop1.wav ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 33.3/33.3 KB • 23.1 kB/s • 0:00:00

pfxrename
=========

    Renames a file on the PFx Brick file system.

.. code-block:: shell

    $ pfxrename -h
    usage: pfxrename [-h] [-s SERIALNO] file newname

    Rename a file on the PFx Brick

    positional arguments:
    file                  file name or file ID to rename
    newname               new name to assign to file

    optional arguments:
    -h, --help            show this help message and exit
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)

.. code-block:: shell

    $ pfxrename GMDLoop1.wav NotchLoop1.wav
    Renamed file GMDLoop1.wav to NotchLoop1.wav


-------------------------
General Purpose Utilities
-------------------------

pfxinfo
=======

Retrieves basic information from any connected PFx Bricks.

.. code-block:: shell

    $ pfxinfo -h
    usage: pfxinfo [-h] [-c]

    Show information for all attached PFx Bricks

    optional arguments:
    -h, --help    show this help message and exit
    -c, --config  Show configuration details

.. image:: _static/pfxinfo.png

.. image:: _static/pfxinfoconfig.png

|

pfxevents
=========

Shows the event/action look up table on the PFx Brick.  The utility can also be used to clear the contents of the table.

.. code-block:: shell


    $ pfxevents -h
    usage: pfxevents [-h] [-cs] [-cj] [-cu] [-ca] [-r] [-i] [-s SERIALNO]

    PFx Brick print event/action table

    optional arguments:
    -h, --help            show this help message and exit
    -cs, --clear-speed    Clear actions for speed remote
    -cj, --clear-joystick
                            Clear actions for joystick remote
    -cu, --clear-startup  Clear startup actions
    -ca, --clear-all      Clear all actions
    -r, --raw             Show event/action table in raw numeric format
    -i, --ir              Show event/action table grouped by IR channel
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)

.. code-block:: shell

    $ pfxevents
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ IR Speed Remote                                                          ┃
    └──────────────────────────────────────────────────────────────────────────┘
    Add   Evt               Ch    Action
    0x00: L + R Button     Ch 1 : Motor Ch A B Emcy Stop
    0x01: L + R Button     Ch 2 : Motor Ch A B Emcy Stop
    0x02: L + R Button     Ch 3 : Motor Ch A B Emcy Stop
    0x03: L + R Button     Ch 4 : ---
    0x04: L Button         Ch 1 : Motor Ch A Stop
    0x05: L Button         Ch 2 : Motor Ch A Stop
    0x06: L Button         Ch 3 : Motor Ch A Stop
    0x07: L Button         Ch 4 : ---
    0x08: R Button         Ch 1 : Motor Ch A Change Dir
    0x09: R Button         Ch 2 : Motor Ch B Stop
    0x0A: R Button         Ch 3 : Motor Ch B Stop
    0x0B: R Button         Ch 4 : ---
    0x0C: L Wheel Inc      Ch 1 : Motor Ch A Inc Speed
    0x0D: L Wheel Inc      Ch 2 : Motor Ch A Inc Speed (bi-dir)
    0x0E: L Wheel Inc      Ch 3 : Motor Ch A Inc Speed (bi-dir)
    0x0F: L Wheel Inc      Ch 4 : Light Ch 1 2 3 4 5 6 7 8 Inc Bright
    0x10: L Wheel Dec      Ch 1 : Motor Ch A Dec Speed
    0x11: L Wheel Dec      Ch 2 : Motor Ch A Dec Speed (bi-dir)
    0x12: L Wheel Dec      Ch 3 : Motor Ch A Dec Speed (bi-dir)
    0x13: L Wheel Dec      Ch 4 : Light Ch 1 2 3 4 5 6 7 8 Dec Bright
    0x14: R Wheel Inc      Ch 1 : Motor Ch B Inc Speed (bi-dir)
    0x15: R Wheel Inc      Ch 2 : Motor Ch B Inc Speed (bi-dir)
    0x16: R Wheel Inc      Ch 3 : Motor Ch B Inc Speed (bi-dir)
    0x17: R Wheel Inc      Ch 4 : Sound Inc Volume
    0x18: R Wheel Dec      Ch 1 : Motor Ch B Dec Speed (bi-dir)
    0x19: R Wheel Dec      Ch 2 : Motor Ch B Dec Speed (bi-dir)
    0x1A: R Wheel Dec      Ch 3 : Motor Ch B Dec Speed (bi-dir)
    0x1B: R Wheel Dec      Ch 4 : Sound Dec Volume
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Dual Joystick Remote                                                     ┃
    └──────────────────────────────────────────────────────────────────────────┘
    Add   Evt               Ch    Action
    0x1C: L Joy Fwd        Ch 1 : Sound Play Once "Whistle1.wav" (4)
    0x1D: L Joy Fwd        Ch 2 : Sound Play Once "Coupler1.wav" (8)
    0x1E: L Joy Fwd        Ch 3 : ---
    0x1F: L Joy Fwd        Ch 4 : Light Ch 1 2 3 4 5 6 7 8 Inc Bright
    0x20: L Joy Rev        Ch 1 : Sound Play Once "Whistle2.wav" (5)
    0x21: L Joy Rev        Ch 2 : Sound Play Once "Coupler2.wav" (9)
    0x22: L Joy Rev        Ch 3 : Motor Ch A Set Speed
    0x23: L Joy Rev        Ch 4 : Light Ch 1 2 3 4 5 6 7 8 Dec Bright
    0x24: R Joy Fwd        Ch 1 : Sound Play Repeat "SlowBell.wav" (6)
    0x25: R Joy Fwd        Ch 2 : ---
    0x26: R Joy Fwd        Ch 3 : ---
    0x27: R Joy Fwd        Ch 4 : Sound Inc Volume
    0x28: R Joy Rev        Ch 1 : Sound Play Repeat "FastBell.wav" (7)
    0x29: R Joy Rev        Ch 2 : ---
    0x2A: R Joy Rev        Ch 3 : Motor Ch B Set Speed
    0x2B: R Joy Rev        Ch 4 : Sound Dec Volume
    0x2C: L Joy Ctr        Ch 1 : Motor Ch A Stop
    0x2D: L Joy Ctr        Ch 2 : Motor Ch A Stop
    0x2E: L Joy Ctr        Ch 3 : Motor Ch A Stop
    0x2F: L Joy Ctr        Ch 4 : ---
    0x30: R Joy Ctr        Ch 1 : Motor Ch B Stop
    0x31: R Joy Ctr        Ch 2 : Motor Ch B Stop
    0x32: R Joy Ctr        Ch 3 : Motor Ch B Stop
    0x33: R Joy Ctr        Ch 4 : ---
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ EV3 Remote                                                               ┃
    └──────────────────────────────────────────────────────────────────────────┘
    Add   Evt               Ch    Action
    0x34: EV3 Beacon       Ch 1 : ---
    0x35: EV3 Beacon       Ch 2 : ---
    0x36: EV3 Beacon       Ch 3 : ---
    0x37: EV3 Beacon       Ch 4 : ---
    0x38: Test Evt         Ch 1 : Motor Ch A Change Dir
    0x39: Test Evt         Ch 2 : ---
    0x3A: Test Evt         Ch 3 : ---
    0x3B: Test Evt         Ch 4 : ---
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Startup Events                                                           ┃
    └──────────────────────────────────────────────────────────────────────────┘
    Add   Evt               Ch    Action
    0x3C: Startup Evt 1    Ch 1 : ---
    0x3D: Startup Evt 2    Ch 2 : ---
    0x3E: Startup Evt 3    Ch 3 : ---
    0x3F: Startup Evt 4    Ch 4 : ---
    0x40: Startup Evt 5    Ch 1 : ---
    0x41: Startup Evt 6    Ch 2 : ---
    0x42: Startup Evt 7    Ch 3 : ---
    0x43: Startup Evt 8    Ch 4 : ---
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Other Events                                                             ┃
    └──────────────────────────────────────────────────────────────────────────┘
    Add   Evt               Ch    Action
    0x44: Button           Ch 1 : ---
    0x45: Long Button      Ch 2 : ---
    0x46: Button Down      Ch 3 : ---
    0x47: Button Up        Ch 4 : ---
    0x48: BLE Connect      Ch 1 : ---
    0x49: BLE Disconnect   Ch 2 : ---
    0x4A: USB Connect      Ch 3 : ---
    0x4B: USB Disconnect   Ch 4 : ---

pfxrun
======

Runs or stops a script file on the PFx Brick.

.. code-block:: shell

    $ pfxrun -h
    usage: pfxrun [-h] [-e] [-s SERIALNO] file

    Run a script file on the PFx Brick

    positional arguments:
    file                  file name or file ID of script

    optional arguments:
    -h, --help            show this help message and exit
    -e, --end             end script execution
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)

.. code-block:: shell

    $ pfxrun 0
    Running script file 0

.. code-block:: shell

    $ pfxrun -e
    Script execution stopped

pfxplay
=======

Plays an audio file on the PFx Brick.

.. code-block:: shell

    $ pfxplay -h
    usage: pfxplay [-h] [-l] [-e] [-s SERIALNO] file

    Play an audio file on the PFx Brick

    positional arguments:
    file                  file name or file ID to play

    optional arguments:
    -h, --help            show this help message and exit
    -l, --loop            loop playback repeatedly
    -e, --end             end playback
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)

pfxrestart
==========

Restarts the PFx Brick or halts all activity without restarting.

.. code-block:: shell

    $ pfxrestart -h
    usage: pfxrestart [-h] [-s SERIALNO] [-x]

    Restarts the PFx Brick

    optional arguments:
    -h, --help            show this help message and exit
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)
    -x, --halt            Halt all activity on PFx Brick without restarting


pfxmonitor
==========

Shows real time internal state information of a PFx Brick.

.. code-block:: shell

    $ pfxmonitor -h
    usage: pfxmonitor [-h] [-s SERIALNO]

    PFx Brick real time monitoring utility. Press <Ctrl>-C to exit monitor.

    optional arguments:
    -h, --help            show this help message and exit
    -s SERIALNO, --serialno SERIALNO
                            Perform monitoring on PFx Brick with specified serial
                            number

.. code-block:: shell

    $ pfxmonitor

.. image:: _static/pfxmonitor.png

|

pfxtest
=======

Performs self-test diagnostics of various functions of the PFx Brick.

.. code-block:: shell

    $ pfxtest -h
    usage: pfxtest [-h] [-c] [+b] [-l] [-lc] [-m] [-f] [+fl] [-a] [+sc] [-t]
                [-s SERIALNO] [-k] [-v]

    PFx Brick self test. Most tests are run by default but individual tests can be
    omitted using command line arguments.

    optional arguments:
    -h, --help            show this help message and exit
    -c, --config          Omit config flash test
    +b, --button          Include button press test
    -l, --lights          Omit light channel test
    -lc, --combo          Omit combo light effects test
    -m, --motors          Omit motor channel test
    -f, --files           Omit file transfer test
    +fl, --long           Perform long file transfer test
    -a, --audio           Omit audio playback test
    +sc, --scripts        Include script execution test
    -t, --time            Dwell time for each combo light effect test
    -s SERIALNO, --serialno SERIALNO
                            Perform test on PFx Brick with specified serial number
    -k, --keep            Keep test files on PFx Brick after tests are completed
    -v, --verbose         Show verbose details of PFx Brick

.. code-block:: shell

    $ pfxtest.py

.. image:: _static/pfxtest.png

|

-------------------
Low-Level Utilities
-------------------

pfxdump
=======

Dumps the contents of the PFx Brick flash memory.

.. code-block:: shell

    $ pfxdump -h
    usage: pfxdump [-h] [-s SERIALNO] address bytes

    PFx Brick dump flash memory contents

    positional arguments:
    address               base address to start showing contents
    bytes                 number of bytes to show

    optional arguments:
    -h, --help            show this help message and exit
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)

.. code-block:: shell

    $ pfxdump ffe000 256
    FFE000  88 FF 00 80 FF FF 00 00  00 00 00 00 00 00 00 00   ÿ.ÿÿ..........
    FFE010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ................
    FFE020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ................
    FFE030  00 00 00 00 00 00 00 00  01 00 00 00 AB 00 5A 5D   ............«.Z]
    FFE040  01 00 53 68 6F 72 74 52  65 6C 65 61 73 65 31 2E   ..ShortRelease1.
    FFE050  77 61 76 00 00 00 00 00  00 00 00 00 00 00 00 00   wav.............
    FFE060  00 00 00 00 2E 5D 01 00  2C 00 00 00 B0 2D 18 9C   .....]..,...°-.
    FFE070  FF FF 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ÿÿ..............
    FFE080  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ................
    FFE090  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ................
    FFE0A0  00 00 00 00 00 00 00 00  FF FF 00 00 00 00 00 00   ........ÿÿ......
    FFE0B0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ................
    FFE0C0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ................
    FFE0D0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ................
    FFE0E0  FF FF 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ÿÿ..............
    FFE0F0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ................

pfxfat
======

Shows the raw contents of the PFx Brick File Allocation Table (FAT).

.. code-block:: shell


    $ pfxfat -h
    usage: pfxfat [-h] [-s SERIALNO]

    Dumps the contents of the PFx Brick file allocation table (FAT)

    optional arguments:
    -h, --help            show this help message and exit
    -s SERIALNO, --serialno SERIALNO
                            Specify PFx Brick with serial number (if more than one
                            connected)

.. code-block:: shell

    $ pfxfat
    000000  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000010  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000020  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000030  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000040  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000050  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000060  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000070  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000080  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    ...
    000F80  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000F90  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000FA0  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000FB0  0FB1 0FB2 0FB3 0FB4 0FB5 0FB6 0FB7 0FB8  0FB9 0FBA 0FBB 0FBC 0FBD 0FBE 0FBF 0FC0
    000FC0  0FC1 0FC2 0FC3 0FC4 0FC5 0FC6 0FC7 0FC8  0FC9 0FCA 0FCB 0FCC 0FCD 0FCE 0FCF 0FD0
    000FD0  0FD1 0FD2 0FD3 0FD4 0FD5 0FD6 0FD7 0FD8  0FD9 0FDA 0FDB 0FDC 0FDD 0FDE 0FDF 0FE0
    000FE0  0FE1 0FE2 FFFF FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3
    000FF0  FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3 FFF3  FFF3 FFF3 FFF3 FFF3 FFFF FFFF FFFF FFFF
