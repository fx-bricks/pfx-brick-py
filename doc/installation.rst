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

Anaconda / miniconda based environments
---------------------------------------

You can use `Anaconda <https://www.anaconda.com/download/>`_ or `miniconda <https://conda.io/miniconda.html>`_ to create a virtual python environment as a "sandbox" to try the pfxbrick API modules. On most unix platforms (macOS, linux, etc.) you can use the following commands to create a new conda environment called "pfxplay" and install the pfxbrick package (assuming conda is already installed):

.. code-block:: shell

    $ conda create --name pfxplay python=3.6
    $ source activate pfxplay
    $ pip install --upgrade pip
    $ pip install hidapi
    $ pip install pfxbrick


Linux
-----

**pfxbrick** uses the hidapi module which depends on libusb.  Since libusb might not be installed by default in your Linux distribution, you can install it using your favorite package manager:

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
    '0.7.0'
    >>>

If you have a PFx Brick connected, you can try the following command to see if your python installation can find your connected PFx Brick(s):

.. code-block:: shell
    
    >>> pfxbrick.find_bricks()
    ['89000001', '89000002']
    >>>

This returns a list of PFx Brick serial numbers that were found.
