PFx Brick Python API
====================

This repository contains the API for developing python scripts and applications which communicate with the PFx Brick.

Getting Started
===============

Requirements
------------

* Python 3.6+
* hidapi
* PFx Brick Interface Control Document (ICD) v.3.36

Installation
------------

pfx-brick-py can be installed with pip:

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

    from pfxbrick import PFxBrick

    # Open a PFx Brick session instance
    brick = PFxBrick()
    brick.open()
    
    # Get the status and identity of the PFx Brick
    print('PFx Brick ICD version : %s' %(brick.get_icd_rev()))
    brick.get_status()
    brick.print_status()
    
    # Get the PFx Brick configuration settings
    brick.get_config()
    brick.print_config()
    
    # Get the user defined name of the PFx Brick
    brick.get_name()
    print(brick.name)
    
    # Change the user defined name
    brick.set_name('My Cool Brick')
    
    # End the session
    brick.close()


---------------

If you want to learn more about PFx Brick, check out `our website <https://fxbricks.com/pfxbrick>`_.