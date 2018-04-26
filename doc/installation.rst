.. _installation:

Installing pfxbrick
===================

The PFx Brick python API has very few dependencies and should be relatively straight forward to install on almost all platforms.

Dependencies
------------

* Python 3.6

* `HIDAPI <https://github.com/signal11/hidapi>`_

* sphinx (for documentation)

Installation (most platforms)
-----------------------------

The **pfxbrick** package can be installed with pip:

.. code-block:: shell

    $ pip install pfxbrick
    
or directly from the source code:

.. code-block:: shell

    $ git clone https://github.com/fx-bricks/pfx-brick-py.git
    $ cd pfx-brick-py
    $ python setup.py install

Linux
-----

pfx-brick-py uses the hidapi module which depends on libusb.  Since libusb might not be installed by default in your Linux distribution, you can install it using your favorite package manager:

.. code-block:: shell

    $ sudo apt-get install python-dev libusb-1.0-0-dev libudev-dev
    $ sudo pip install --upgrade setuptools
    $ sudo pip install hidapi
    

Verify Installation
-------------------

After installation, verify the package can imported:

.. code-block:: shell

    $ python
    >>> import pfxbrick
    >>> pfxbrick.__version__


