# init for pygrib package
from ._datadir import eccodes_datadir
from ._pygrib import *
# Need explicit imports for names beginning with underscores
from ._pygrib import __doc__, __version__
