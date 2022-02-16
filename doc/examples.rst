.. _examples:

***************
Examples
***************

This page shows some examples of using the PFx Brick API.

Brick Enumeration, Connection, Info Query USB
---------------------------------------------

.. code-block:: python

  #! /usr/bin/env python3

  # PFx Brick example script to retrieve basic information about the
  # brick including its identity and configuration settings.

  import hid
  from pfxbrick import PFxBrick, find_bricks

  bricks = find_bricks(True)
  print('%d PFx Bricks found' % (len(bricks)))

  if bricks:
      for b in bricks:
          brick = PFxBrick()
          res = brick.open(b)
          if not res:
              print("Unable to open session to PFx Brick")
          else:
              print('PFx Brick Status / Identity')
              print('===========================')
              print('PFx Brick ICD version : %s' %(brick.get_icd_rev()))
              brick.get_name()
              print('PFx Brick name        : %s' %(brick.name))
              brick.get_status()
              brick.print_status()
              print('PFx Brick Configuration')
              print('=======================')
              brick.get_config()
              brick.print_config()
              brick.close()

Brick Enumeration, Connection, Info Query BLE
---------------------------------------------

.. code-block:: python

    #! /usr/bin/env python3

    # PFx Brick example script to retrieve basic information about the
    # brick including its identity and configuration settings.

    import asyncio

    from pfxbrick import *


    async def brick_session(brickdev):
        brick = PFxBrickBLE(dev_dict=brickdev)
        await brick.open()
        print("PFx Brick Status / Identity")
        print("===========================")
        print("PFx Brick ICD version : %s" % (await brick.get_icd_rev()))
        await brick.get_name()
        print("PFx Brick name        : %s" % (brick.name))
        await brick.get_status()
        brick.print_status()
        print("PFx Brick Configuration")
        print("=======================")
        await brick.get_config()
        brick.print_config()
        await brick.close()


    loop = asyncio.get_event_loop()
    pfxdevs = loop.run_until_complete(ble_device_scanner())
    print("Found %d PFx Bricks" % (len(pfxdevs)))
    if len(pfxdevs) > 0:
        bricks = loop.run_until_complete(find_ble_pfxbricks(pfxdevs))
        loop.run_until_complete(brick_session(bricks[0]))

Unless the Bluetooth hardware address of the PFx Brick is known in advance,
then it must be obtained by performing a Bluetooth peripheral device scan to
see which Bluetooth devices are currently advertising availability.  The
Bluetooth hardware address is operating system dependent and must be provided
in a UUID form that is compatible with your OS.

For Windows and Linux this is typically in the form of "24:71:89:cc:09:05"
and on macOS it is in the form of "B9EA5233-37EF-4DD6-87A8-2A875E821C46"

If you already know the Bluetooth device UUID of the PFx Brick you wish to communicate with, then you can connect to it directly:

.. code-block:: python

    import asyncio

    from pfxbrick import *


    async def brick_session(uuid):
        brick = PFxBrickBLE(uuid=uuid)
        await brick.open()
        print("PFx Brick Status / Identity")
        print("===========================")
        print("PFx Brick ICD version : %s" % (await brick.get_icd_rev()))
        await brick.get_name()
        print("PFx Brick name        : %s" % (brick.name))
        await brick.get_status()
        brick.print_status()
        r = await brick.get_rssi()
        print("RSSI = %s" % (r))
        await brick.close()

    # connect directly using the Bluetooth UUID
    loop = asyncio.get_event_loop()
    loop.run_until_complete(brick_session("059930E2-BE75-48A4-B193-3AD3F67246E4"))



Changing Configuration
----------------------

.. code-block:: python

  #! /usr/bin/env python3

  # PFx Brick example script to showing modification to the
  # brick configuration settings.

  import hid
  from pfxbrick import PFxBrick, find_bricks
  from pfxbrick.pfx import *

  bricks = find_bricks()
  print('%d PFx Bricks found' % (len(bricks)))

  if bricks:
      brick = PFxBrick()
      res = brick.open()
      if not res:
          print("Unable to open session to PFx Brick")
      else:
          print('PFx Brick Configuration')
          print('=======================')
          brick.get_config()
          brick.print_config()

          print("Change the volume beep setting...")
          if brick.config.settings.volumeBeep == PFX_CFG_VOLBEEP_ON:
              brick.config.settings.volumeBeep = PFX_CFG_VOLBEEP_OFF
          else:
              brick.config.settings.volumeBeep = PFX_CFG_VOLBEEP_ON
          brick.set_config()

          print('PFx Brick Updated Configuration')
          print('===============================')
          brick.get_config()
          brick.print_config()

          brick.close()

Modifying the Event/Action LUT
------------------------------

.. code-block:: python

  #! /usr/bin/env python3

  # PFx Brick example script to show access to the event/action LUT

  import hid
  import time
  import copy
  from pfxbrick import PFxBrick, PFxAction, find_bricks
  from pfxbrick.pfx import *

  brick = PFxBrick()
  brick.open()

  left_button_ch1 = brick.get_action(EVT_ID_8879_LEFT_BUTTON, 0)
  print("Get action for Left Button Ch 1 on Speed Remote...")
  print(left_button_ch1)

  print("Add a light effect to this action...")
  new_left_action = copy.copy(left_button_ch1)
  new_left_action.light_on([1,2,3,4])
  print(new_left_action)

  print("Save new action back to brick...")
  brick.set_action(EVT_ID_8879_LEFT_BUTTON, 0, new_left_action)
  print(brick.get_action(EVT_ID_8879_LEFT_BUTTON, 0))
  time.sleep(1)

  print("Restore the original action without the change...")
  brick.set_action(EVT_ID_8879_LEFT_BUTTON, 0, left_button_ch1)
  print(brick.get_action(EVT_ID_8879_LEFT_BUTTON, 0))

  brick.close()

Copying Audio Files
-------------------

Copy file to PFx Brick specified by command line arguments:

.. code-block:: python

  #! /usr/bin/env python3

  # PFx Brick example script to show copying files to the PFx Brick

  import hid
  from pfxbrick import PFxBrick
  from sys import argv

  if len(argv) < 3:
      print("Usage: ./filecopy.py <filename> <id>")
      print("  where <filename> is the local file to copy")
      print("        <id> is the unique file ID to assign the file on the PFx Brick")
  else:
      brick = PFxBrick()
      brick.open()

      fn = argv[1]
      fid = int(argv[2])
      print("Copying %s to brick with id %d..." % (fn, fid))
      brick.put_file(fid, fn)
      brick.refresh_file_dir()
      print(brick.filedir)

      brick.close()

Copy a list of files to the PFx Brick:

.. code-block:: python

  #! /usr/bin/env python3

  # PFx Brick example script to show copying files to the PFx Brick

  import hid
  from pfxbrick import PFxBrick
  from sys import argv

  files = ['beep1.wav', 'beep2.wav', 'siren1.wav', 'anthem.wav']

  brick = PFxBrick()
  brick.open()

  for i,file in enumerate(files):
      print("Copying %s to brick with id %d..." % (file, i))
      brick.put_file(i, file, show_progres=True)

  brick.refresh_file_dir()
  print(brick.filedir)

  brick.close()

Scripting Actions
-----------------

A demonstration of scripting multiple actions involving motors, lighting, and sound:

.. code-block:: python

    #! /usr/bin/env python3

    # PFx Brick example script to demonstrate multiple scripted actions

    import time
    import random
    from pfxbrick import *

    brick = PFxBrick()
    brick.open()

    max_speed = 100
    audiofile = "yamanote16pcm22k"

    # start looped audio playback and set volume
    brick.repeat_audio_file(audiofile)
    brick.set_volume(75)

    # ramp up the motor speed gradually to max_speed
    for x in range(max_speed):
        brick.set_motor_speed([1], x)
        # show a random light pattern
        y = random.randint(1, 8)
        brick.light_toggle([y])
        time.sleep(0.1)

    # ramp down the motor speed gradually to 0%

    for x in range(max_speed):
        brick.set_motor_speed([1], max_speed - x - 1)
        # show a random light pattern
        y = random.randint(1, 8)
        brick.light_toggle([y])
        time.sleep(0.1)

    # stop motor and turn off audio and lights
    brick.stop_motor([1])
    brick.stop_audio_file(audiofile)
    brick.light_off([ch for ch in range(1, 9)])

    brick.close()

The same script but implemented for a BLE connected PFx Brick:

.. code-block:: python

    #! /usr/bin/env python3

    # PFx Brick example script to demonstrate multiple scripted actions

    import asyncio
    import random
    from pfxbrick import *


    async def brick_session(brickdev):
        brick = PFxBrickBLE(dev_dict=brickdev, debug=False)
        await brick.open()
        max_speed = 50
        audiofile = "yamanote16pcm22k"

        # start looped audio playback and set volume
        await brick.repeat_audio_file(audiofile)
        await brick.set_volume(75)

        # ramp up the motor speed gradually to max_speed
        for x in range(max_speed):
            await brick.set_motor_speed([1], x)
            # show a random light pattern
            y = random.randint(1, 8)
            await brick.light_toggle([y])
            await asyncio.sleep(0.1)

        # ramp down the motor speed gradually to 0%

        for x in range(max_speed):
            await brick.set_motor_speed([1], max_speed - x - 1)
            # show a random light pattern
            y = random.randint(1, 8)
            await brick.light_toggle([y])
            await asyncio.sleep(0.1)

        # stop motor and turn off audio and lights
        await brick.stop_motor([1])
        await brick.stop_audio_file(audiofile)
        await brick.light_off([ch for ch in range(1, 9)])

        await brick.close()

    loop = asyncio.get_event_loop()
    pfxdevs = loop.run_until_complete(ble_device_scanner())
    print("Found %d PFx Bricks" % (len(pfxdevs)))
    if len(pfxdevs) > 0:
        bricks = loop.run_until_complete(find_ble_pfxbricks(pfxdevs))
        loop.run_until_complete(brick_session(bricks[0]))

BLE Notifications
-----------------

This example shows how to activate PFx Brick notifications to be sent asynchronously to a client application.  Notification events can trigger your own callback functions for handling within your application.

.. code-block:: python

    #! /usr/bin/env python3

    # PFx Brick example script to demonstrate using notifications from PFx Brick

    import asyncio

    from pfxbrick import *


    # our callback functions for notification events
    def motor_a_stopped():
        print("Motor ch A has stopped")

    def motor_a_speed_change(speed):
        print("Motor ch A has changed speed to %d" % (speed))

    def audio_file_started(fileid, filename):
        print("Audio playback has started for file %d: %s" % (fileid, filename))

    async def brick_session(brickdev):
        brick = PFxBrickBLE(dev_dict=brickdev, debug=False)
        await brick.open()

        # register our notification callback functions
        brick.callback_motora_stop = motor_a_stopped
        brick.callback_motora_speed = motor_a_speed_change
        brick.callback_audio_play = audio_file_started

        # activate our desired PFx Brick notifications
        await brick.set_notifications(
            PFX_NOTIFICATION_AUDIO_PLAY |
            PFX_NOTIFICATION_MOTORA_STOP |
            PFX_NOTIFICATION_MOTORA_CURR_SPD
        )

        # Motor channel A forward 50% speed
        await brick.set_motor_speed([1], -50)
        await asyncio.sleep(3)

        # Stop motor A
        await brick.stop_motor([1])
        await asyncio.sleep(1)

        # Motor channel A reverse 33% speed for 2 sec self-timed
        await brick.set_motor_speed([1], 33, 2)

        await asyncio.sleep(1)
        await brick.play_audio_file(2)
        await asyncio.sleep(2)

        # turn off notifications
        await brick.disable_notifications()

        await brick.close()


    loop = asyncio.get_event_loop()
    pfxdevs = loop.run_until_complete(ble_device_scanner())
    print("Found %d PFx Bricks" % (len(pfxdevs)))
    if len(pfxdevs) > 0:
        bricks = loop.run_until_complete(find_ble_pfxbricks(pfxdevs))
        loop.run_until_complete(brick_session(bricks[0]))
