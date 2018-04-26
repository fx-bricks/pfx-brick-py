.. _apireference:

***********************
PFx Brick API Reference
***********************

The PFx Brick API uses a top level **PFxBrick** object to create and use a communication session.

Initialization
--------------

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick
    PFxConfig
    PFxDir
    PFxFile
    PFxAction

Connection
----------

.. currentmodule:: pfxbrick

.. autosummary::
    find_bricks
    PFxBrick.open
    PFxBrick.close
    
Information
-----------

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.get_icd_rev
    PFxBrick.get_status
    PFxBrick.print_status
    PFxBrick.get_name
    PFxBrick.set_name

Configuration
-------------

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.get_config
    PFxBrick.set_config
    PFxBrick.print_config
    PFxBrick.reset_factory_config
    
Event/Action LUT
----------------

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.get_action
    PFxBrick.get_action_by_address
    PFxBrick.set_action
    PFxBrick.set_action_by_address

File System
-----------

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.refresh_file_dir
    PFxBrick.put_file
    PFxBrick.get_file
    
Actions
-------

.. currentmodule:: pfxbrick

.. autosummary::
    PFxBrick.test_action

Motor Actions
=============

.. currentmodule:: pfxbrick.pfxaction

.. autosummary::
    PFxAction.set_motor_speed
    PFxAction.stop_motor

Light Actions
=============


.. autosummary::
    PFxAction.light_on
    PFxAction.light_off
    PFxAction.light_toggle
    PFxAction.light_fx
    PFxAction.combo_light_fx
    
Sound Actions
=============

.. autosummary::
    PFxAction.play_audio_file
    PFxAction.repeat_audio_file
    PFxAction.stop_audio_file
    PFxAction.set_volume
    PFxAction.sound_fx


    
