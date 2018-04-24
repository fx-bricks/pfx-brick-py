"""Package for PFx Brick"""

import os

__project__ = 'pfxbrick'
__version__ = '0.5.0'

VERSION = __project__ + '-' + __version__

script_dir = os.path.dirname(__file__)

from .pfxbrick import PFxBrick
from .pfxaction import PFxAction
from .pfxconfig import PFxConfig
from .pfxfiles import PFxFile, PFxDir

