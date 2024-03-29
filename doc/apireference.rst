.. _apireference:

***********************
PFx Brick API Reference
***********************

The PFx Brick API has a top level :obj:`PFxBrick` class object.  An instance of :obj:`PFxBrick` is used to open, maintain, and close an operating session with a PFx Brick.  This class internally contains several supporting child classes used as convenient containers for related data.  In particular, it contains a :obj:`PFxConfig` and :obj:`PFxDir` class which store configuration and file system data respectively.

The :obj:`PFxAction` class is used to specify actions the PFx Brick can perform including motor control, lighting effects, and sound effects.  It has many supporting methods to conveniently specify popular actions.  A host application can also directly modify the field attributes of a :obj:`PFxAction` instance to specify a detailed action description.  Details of specifying these fields can be found in the `PFx Brick Interface Control Document (ICD) <https://www.fxbricks.com//downloads/PFxBrickICD-Rev3.38.pdf>`_.

This page summarizes the main functional groups of functionality contained in this API in sections that follow.

Connection USB
--------------

Functions to establish a USB connected session with a PFx Brick.

.. currentmodule:: pfxbrick

.. autosummary::
    find_bricks
    PFxBrick.open
    PFxBrick.close

.. autofunction:: find_bricks

Connection BLE
--------------

Functions to establish a BLE connected session with a PFx Brick.

.. currentmodule:: pfxbrick

.. autosummary::
    ble_device_scanner
    find_ble_pfxbricks
    PFxBrickBLE.open
    PFxBrickBLE.close

.. autofunction:: ble_device_scanner

.. autofunction:: find_ble_pfxbricks


Information
-----------

Functions to get information and status from the PFx Brick.

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.get_icd_rev
    PFxBrick.get_status
    PFxBrick.print_status
    PFxBrick.get_name
    PFxBrick.set_name
    PFxBrick.get_current_state
    PFxBrick.get_fs_state
    PFxBrick.get_bt_state

Configuration
-------------

Functions which query and modify PFx Brick configuration and settings.

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.get_config
    PFxBrick.set_config
    PFxBrick.print_config
    PFxBrick.reset_factory_config

Event/Action LUT
----------------

Functions which query and modify the event/action look up table in the PFx Brick.

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.get_action
    PFxBrick.get_action_by_address
    PFxBrick.set_action
    PFxBrick.set_action_by_address

File System
-----------

Functions which interact with the PFx Brick file system.

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.refresh_file_dir
    PFxBrick.put_file
    PFxBrick.get_file
    PFxBrick.remove_file
    PFxBrick.format_fs
    PFxBrick.rename_file
    PFxBrick.set_file_attributes
    PFxBrick.file_id_from_str_or_int


Actions
-------

Functions which specify and perform common actions.

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.test_action

Motor Actions
=============

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.set_motor_speed
    PFxBrick.stop_motor

.. currentmodule:: pfxbrick.pfxaction

.. autosummary::
    PFxAction.set_motor_speed
    PFxAction.stop_motor

Light Actions
=============

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.light_on
    PFxBrick.light_off
    PFxBrick.light_toggle
    PFxBrick.set_brightness
    PFxBrick.light_fx
    PFxBrick.combo_light_fx

.. currentmodule:: pfxbrick.pfxaction

.. autosummary::
    PFxAction.light_on
    PFxAction.light_off
    PFxAction.light_toggle
    PFxAction.set_brightness
    PFxAction.light_fx
    PFxAction.combo_light_fx

Sound Actions
=============

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.play_audio_file
    PFxBrick.repeat_audio_file
    PFxBrick.stop_audio_file
    PFxBrick.set_volume
    PFxBrick.sound_fx

.. currentmodule:: pfxbrick.pfxaction

.. autosummary::
    PFxAction.play_audio_file
    PFxAction.repeat_audio_file
    PFxAction.stop_audio_file
    PFxAction.set_volume
    PFxAction.sound_fx

Running scripts
---------------

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.run_script
    PFxBrick.stop_script

BLE Notifications
-----------------

.. currentmodule:: pfxbrick.pfxble

.. autosummary::
    PFxBrickBLE.set_notifications
    PFxBrickBLE.disable_notifications
