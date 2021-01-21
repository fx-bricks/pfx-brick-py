"""Package for PFx Brick"""

import os

# fmt: off
__project__ = 'pfxbrick'
__version__ = '0.7.1'
# fmt: on

VERSION = __project__ + "-" + __version__

script_dir = os.path.dirname(__file__)

from .pfx import *
from .pfxdict import *
from .pfxexceptions import *
from .pfxmsg import *
from .pfxaction import PFxAction
from .pfxconfig import PFxConfig
from .pfxstate import PFxState
from .pfxfiles import (
    PFxFile,
    PFxDir,
    fs_copy_file_to,
    fs_copy_file_from,
    fs_get_fileid_from_name,
)
from .pfxbrick import PFxBrick, find_bricks
from .pfxble import PFxBrickBLE, ble_device_scanner, find_ble_pfxbricks
