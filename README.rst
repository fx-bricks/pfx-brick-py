.. image:: images/sitelogo.png


PFx Brick Python API
====================

.. image:: https://travis-ci.org/fx-bricks/pfx-brick-py.svg?branch=master
    :target: https://travis-ci.org/fx-bricks/pfx-brick-py
.. image:: https://img.shields.io/pypi/v/pfxbrick.svg
    :target: https://pypi.org/project/pfxbrick/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/fx-bricks/pfx-brick-py/blob/master/LICENSE.md
.. image:: https://img.shields.io/github/issues/fx-bricks/pfx-brick-py.svg?style=flat
    :target: https://img.shields.io/github/issues/fx-bricks/pfx-brick-py.svg?style=flat
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://img.shields.io/badge/code%20style-black-000000.svg
    
This repository contains a python package API for developing python scripts and applications which communicate with the PFx Brick.  This package supports both USB and Bluetooth LE connections to the PFx Brick and is supported for Windows, macOS and linux.

Getting Started
===============

Requirements
------------

* Python 3.6+
* `HIDAPI <https://github.com/signal11/hidapi>`_
* `Bleak <https://github.com/hbldh/bleak>`_
* sphinx (for documentation)

Installation
------------

The **pfxbrick** package can be installed with pip:

.. code-block:: shell

    $ pip install pfxbrick

or directly from the source code:

.. code-block:: shell

    $ git clone https://github.com/fx-bricks/pfx-brick-py.git
    $ cd pfx-brick-py
    $ python setup.py install

Basic Usage
===========

After installation, the package can imported:

.. code-block:: shell

    $ python
    >>> import pfxbrick
    >>> pfxbrick.__version__

An example of the package can be seen below

.. code-block:: python

    from pfxbrick import *

    # Open a PFx Brick session instance
    brick = PFxBrick()
    brick.open()

    # Get the PFx Brick configuration settings
    brick.get_config()
    brick.print_config()

    # Get the user defined name of the PFx Brick
    brick.get_name()
    print(brick.name)

    # Change the user defined name
    brick.set_name('My Cool Brick')

    # Turn on some lights for 5 sec
    brick.light_on([1, 2, 7, 8])
    time.sleep(5)
    brick.light_off([1, 2, 7, 8])

    # Set motor channel A to 50% speed gradually
    for speed in range(50):
        brick.set_motor_speed([1], speed)
        time.sleep(0.1)
    brick.stop_motor([1])

    # Play an audio file
    brick.repeat_audio_file("LongBeep1")
    time.sleep(5)
    brick.stop_audio_file("LongBeep1")

    # End the session
    brick.close()


---------------

Documentation
=============

* `PFx Brick Interface Control Document (ICD) v.3.37 <https://github.com/fx-bricks/pfx-brick-dev/raw/master/doc/ICD/PFxBrickICD-Rev3.37.pdf>`_ describes details of PFx Brick operation and communication protocol
* `Python API Reference Documentation <https://www.fxbricks.com/docs/python/index.html>`_

If you want to learn more about PFx Brick, check out `our website <https://fxbricks.com/pfxbrick>`_.
