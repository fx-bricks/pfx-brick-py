.. _quickstart:

Quick Start
===========

To start using the **pfxbrick** package, import the following modules into your python source:

.. code-block:: python

  from pfxbrick import PFxBrick, find_bricks
  
Enumerating PFx Bricks and Connecting
-------------------------------------

To enumerate available PFx Bricks connected to your system, you can use the :py:func:`find_bricks` function:

.. code-block:: python

  bricks = find_bricks()
  print('%d PFx Bricks found' % (len(bricks)))

A listing of discovered PFx Bricks can be printed by setting the :py:data:`show_list` parameter:

.. code-block:: python

  bricks = find_bricks(show_list=True)

.. code-block:: none

  1. PFx Brick 4 MB, Serial No: 890F3024
  2. PFx Brick 4 MB, Serial No: 897C933B
  3. PFx Brick 4 MB, Serial No: 8951E33B
  
Connecting/Disconnecting a PFx Brick
------------------------------------

To open a session with the PFx Brick, declare an instance of the :py:class:`PFxBrick` class and use the :py:meth:`open` method:

.. code-block:: python

  brick = PFxBrick()
  brick.open()

If more than one PFx Brick has been enumerated, then you must specify the serial number of the PFx Brick to connect to:

.. code-block:: python

  brick = PFxBrick()
  brick.open('890F3024')
  
A connected session to a PFx Brick should be closed with the :py:meth:`close` method:

.. code-block:: python

  brick.close()

  
Getting PFx Brick Information
-----------------------------

Useful information about the PFx Brick identity, version, etc. can be queried using these methods:

.. hlist::
    :columns: 2

    * :py:meth:`PFxBrick.get_icd_rev`
    * :py:meth:`PFxBrick.get_name`
    * :py:meth:`PFxBrick.set_name`
    * :py:meth:`PFxBrick.get_status`
    * :py:meth:`PFxBrick.print_status`

.. code-block:: python

  print('PFx Brick Status / Identity')
  print('===========================')
  print('PFx Brick ICD version : %s' %(brick.get_icd_rev()))
  brick.get_name()
  print('PFx Brick name        : %s' %(brick.name))
  brick.get_status()
  brick.print_status()

.. code-block:: none

  PFx Brick Status / Identity
  ===========================
  PFx Brick ICD version : 03.36
  PFx Brick name        : My PFx Brick
  USB vendor ID         : 04D8
  USB product ID        : EF74
  USB product desc      : PFx Brick 4 MB
  USB manufacturer      : Fx Bricks Inc
  PFx Brick product ID  : A204, PFx Brick 4 MB
  Serial number         : 890F3024
  Firmware version      : 01.37 build 0529
  Status                : 00 Normal
  Errors                : 00 None
  
PFx Brick Configuration
-----------------------

The PFx Brick configuration settings can be queried and displayed with:

.. hlist::
    :columns: 2

    * :py:meth:`PFxBrick.get_config`
    * :py:meth:`PFxBrick.set_config`
    * :py:meth:`PFxBrick.print_config`

.. code-block:: python

  print('PFx Brick Configuration')
  print('=======================')
  brick.get_config()
  brick.print_config()

.. code-block:: none

  PFx Brick Configuration
  =======================
  Status LED            : Normally ON, blink with activity
  Volume Beep           : OFF
  Auto Power Down       : OFF
  IR Lockout Mode       : Inhibit
  IR Auto Off           : Never
  BLE Auto Off          : Never
  BLE Motor Disconnect  : Continue operation
  BLE Advert Power      : 0
  BLE Session Power     : 0
  Motor sound notches   : 8
  Motor sound bounds    : 20 40 60 80 A0 C0 E0
  Default brightness    : C0
  Startup brightness    : C0 C0 C0 C0 C0 C0 C0 C0
  PF output brightness  : C0 C0 00 00
  Audio DRC: OFF  Bass: 00  Treble: 00
  Motor Channel 0
    Invert : False  Torque comp : False  PF mode : False
    Accel  : 0  Decel : 0
    vMin   : 0  vMid  : 125  vMax : 250
  Motor Channel 1
    Invert : False  Torque comp : False  PF mode : False
    Accel  : 0  Decel : 0
    vMin   : 0  vMid  : 125  vMax : 250
  Motor Channel 2
    Invert : False  Torque comp : False  PF mode : False
    Accel  : 0  Decel : 0
    vMin   : 0  vMid  : 125  vMax : 250
  Motor Channel 3
    Invert : False  Torque comp : False  PF mode : False
    Accel  : 0  Decel : 0
    vMin   : 0  vMid  : 125  vMax : 250

Using PFx Brick Actions
-----------------------

Actions involving motors, lighting, and sound can be easily initiated by passing a :py:class:`PFxAction` class instance into the :py:meth:`test_action()` method.  The :py:class:`PFxAction` class has many convenient methods to simplify building actions.


Controlling Motors
******************

The following methods can be used to configure a :py:class:`PFxAction` for controlling motor outputs:

.. hlist::
    :columns: 2

    * :py:meth:`PFxAction.set_motor_speed`
    * :py:meth:`PFxAction.stop_motor`

.. code-block:: python

  from pfxbrick import PFxAction
  
  # Motor channel A forward 50% speed
  a = PFxAction().set_motor_speed([1], 50)
  brick.test_action(a)

  # Stop motor channel B
  a = PFxAction().stop_motor([2])
  brick.test_action(a)

  # Motor channel A & B reverse 33% speed for 2 sec self-timed
  a = PFxAction().set_motor_speed([1, 2], -33, 2)
  brick.test_action(a)

Controlling Lights
******************

:py:class:`PFxAction` methods for configuring light effects include:

.. hlist::
    :columns: 2

    * :py:meth:`PFxAction.light_on`
    * :py:meth:`PFxAction.light_off`
    * :py:meth:`PFxAction.light_toggle`
    * :py:meth:`PFxAction.set_brightness`
    * :py:meth:`PFxAction.light_fx`
    * :py:meth:`PFxAction.combo_light_fx`

.. code-block:: python

  from pfxbrick import PFxAction
  from pfxbrick.pfx import *

  # Set lights 1, 2, 3, 4 ON
  brick.test_action(PFxAction().light_on([1, 2, 3, 4]))

  # Set strobe lights 1, 4 ON, 1 sec period, 10% duty cycle, 2 flashes
  a = PFxAction().light_fx([1,4], EVT_LIGHTFX_STROBE_P, \
      [EVT_PERIOD_1S, EVT_DUTYCY_10, EVT_BURST_COUNT_2, EVT_TRANSITION_ON])
  brick.test_action(a)

  # Toggle linear sweep with 8 lights
  a = PFxAction().combo_light_fx(EVT_COMBOFX_LIN_SWEEP, \
      [EVT_PERIOD_1S, EVT_FADE_FACTOR_30, EVT_SIZE_8_LIGHTS])
  brick.test_action(a)

In order to use convenient parameter constants such as :py:const:`EVT_PERIOD_1S`, the :py:mod:`pfxbrick.pfx` module needs to be imported as shown above.

Controlling Audio
*****************

:py:class:`PFxAction` methods for configuring sound effects include:

.. hlist::
    :columns: 2

    * :py:meth:`PFxAction.play_audio_file`
    * :py:meth:`PFxAction.repeat_audio_file`
    * :py:meth:`PFxAction.stop_audio_file`
    * :py:meth:`PFxAction.set_volume`
    * :py:meth:`PFxAction.sound_fx`

.. code-block:: python

  from pfxbrick import PFxAction
  from pfxbrick.pfx import *

  # Play sound file 1
  brick.test_action(PFxAction().play_audio_file(1))

  # Play audio file 2 continuously
  brick.test_action(PFxAction().repeat_audio_file(2))

  # Set audio volume to 30%
  brick.test_action(PFxAction().set_volume(30))

  #  Stop playback of audio file 2
  brick.test_action(PFxAction().stop_audio_file(2))

PFx Brick File System
---------------------

Access to the PFx Brick file system is provided by a few convenient methods as follows:

.. hlist::
    :columns: 2

    * :py:meth:`PFxBrick.refresh_file_dir`
    * :py:meth:`PFxBrick.put_file`
    * :py:meth:`PFxBrick.get_file`
    * :py:meth:`PFxBrick.remove_file`
    * :py:meth:`PFxBrick.format_fs`

Show the PFx Brick file system directory:

.. code-block:: python

  brick.refresh_file_dir()
  print(brick.filedir)

.. code-block:: none

  ID Name                       Size    Attr    User1    User2    CRC32
  01 Bark1.wav                  22.3 kB 0000 000056B0 00000046 9D26CE7C
  00 Hero                       55.5 kB 0000 0000D8BC 0000002C DC91BD91
  02 Sosumi                     27.1 kB 0000 000069C2 0000002C 997DD19B
  3 files, 110.6 kB used, 4067.3 kB remaining

Copying a file from the host to the PFx Brick:

.. code-block:: python

  # copy ./sounds/beep1.wav and assign file ID to 3
  brick.put_file(3, './sounds/beep1.wav')

Copy a file from the PFx Brick to the host:

.. code-block:: python

  # copy file ID 5
  brick.get_file(5)
  # copy file ID 1 and rename it as 'ringtone.wav' on host
  brick.get_file(1, 'ringtone.wav')

Removing a file from the PFx Brick:

.. code-block:: python

  # delete file ID 10
  brick.remove_file(10)

