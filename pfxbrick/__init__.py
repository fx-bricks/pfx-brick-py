"""Package for PFx Brick

   isort:skip_file
"""
import os

# fmt: off
__project__ = 'pfxbrick'
__version__ = '0.8.6'

# API version

VERSION = __project__ + "-" + __version__

# ICD version this API is compliant with
#   for more detail, consult:
#   https://www.fxbricks.com/downloads/PFxBrickICD-Rev3.39.pdf
#   and
#   https://github.com/fx-bricks/pfx-brick-dev

ICD_REV = '3.39'

script_dir = os.path.dirname(__file__)

from .pfx import *
from .pfxaction import PFxAction
from .pfxconfig import PFxConfig
from .pfxstate import PFxState
from .pfxfiles import (PFxDir, PFxFile, fs_copy_file_from, fs_copy_file_to,
                       fs_get_fileid_from_name, fs_remove_file)
from .pfxbrick import PFxBrick, find_bricks
from .pfxble import PFxBrickBLE, ble_device_scanner, find_ble_pfxbricks
from .pfxdict import *
from .pfxexceptions import *
from .pfxmsg import *
from .pfxhelpers import *

# fmt: on
