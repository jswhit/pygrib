"""High-level python interface to ECCODES library for GRIB file IO."""
# init for pygrib package
from ._pygrib import *
# Need explicit imports for names beginning with underscores
from ._pygrib import __doc__, __version__
from ._ctx import read as read
