.. _examples:

***************
Examples
***************

This page shows some examples of using the PFx Brick API.

Brick Enumeration, Connection, Info Query
-----------------------------------------

.. code-block:: python

  #! /usr/bin/env python3
 
  # PFx Brick example script to retrieve basic information about the
  # brick including its identity and configuration settings.

  import hid
  from pfxbrick import PFxBrick, find_bricks

  n = find_bricks(True)
  print('%d PFx Bricks found' % (n))

  if n > 0:
      brick = PFxBrick()
      res = brick.open()
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

Changing Configuration
----------------------

.. code-block:: python

  #! /usr/bin/env python3
 
  # PFx Brick example script to showing modification to the
  # brick configuration settings.

  import hid
  from pfxbrick import PFxBrick, find_bricks
  from pfxbrick.pfx import *

  n = find_bricks()
  print('%d PFx Bricks found' % (n))

  if n > 0:
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
