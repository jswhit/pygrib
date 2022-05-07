"""High-level python interface to ECCODES library for GRIB file IO."""
# # init for pygrib package
from ._pygrib import *
# # from ._pygrib import open
# # Need explicit imports for names beginning with underscores
from ._pygrib import __doc__, __version__
from ._ctx import read as read
