.. _installation:

Installing pfxbrick
===================

The PFx Brick python API has very few dependencies and should be relatively straight forward to install on almost all platforms.

Dependencies
------------

* Python 3.6+

* `HIDAPI <https://github.com/signal11/hidapi>`_

* `Bleak <https://github.com/hbldh/bleak>`_

* sphinx (for documentation)
  

Pre-install System requirements for linux
-----------------------------------------

The **pfxbrick** package will require some packages to be installed suport access to USB and Bluetooth hardware drivers.  Use your preferred package manager to install these packages:

 * libhidapi-dev
 * libudev-dev
 * libusb-1.0-0-dev
 * bluez
 * bluetooth
 * libbluetooth-dev
  
Pre-install System requirements for macOS
-----------------------------------------

It is recommended to use the `brew <https://brew.sh>`_ package manager to install the packages for USB hardware access. (Hardware support for Bluetooth will automatically be installed with **pfxbrick** :code:`setup.py` install script which installs the `bleak <https://github.com/hbldh/bleak>`_ package with its dependency to :code:`pyobjc-framework-CoreBluetooth`).

.. code-block:: shell

    $ brew install hidapi

Installation with pip
---------------------

The **pfxbrick** package can be installed with pip:

.. code-block:: shell

    $ pip install pfxbrick

Install from source
-------------------

Install directly from the source code with the :code:`setup.py` script:

.. code-block:: shell

    $ git clone https://github.com/fx-bricks/pfx-brick-py.git
    $ cd pfx-brick-py
    $ python setup.py install

Conda Virtual Environment
-------------------------

You can also use the package in a standalone conda virtual environment. To create a conda environment named :code:`pfxtest`:

.. code-block:: shell

    $ git clone https://github.com/fx-bricks/pfx-brick-py.git
    $ cd pfx-brick-py
    $ conda env create -f environment.yml
    $ conda activate pfxtest
    $ pip install -r requirements.txt
    $ python setup.py install


Verify Installation
-------------------

After installation, verify the package can imported:

.. code-block:: shell

    $ python
    >>> import pfxbrick
    >>> pfxbrick.__version__
    '0.8.0'
    >>>

If you have a PFx Brick connected, you can try the following command to see if your python installation can find your connected PFx Brick(s):

.. code-block:: shell
    
    >>> pfxbrick.find_bricks()
    ['89000001', '89000002']
    >>>

This returns a list of PFx Brick serial numbers that were found.
