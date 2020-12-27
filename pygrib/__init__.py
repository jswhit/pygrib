# When importing from the root of the unpacked tarball or git checkout,
# Python sees the "pygrib" source directory and tries to load it, which fails.
# (unless the package was build in-place using "python setup.py build_ext
# --inplace" so that _pygrib.so exists in the pygrib source dir).
try:
    # init for pygrib package
    from ._pygrib import *
except ImportError:
    import os.path as _op
    if _op.exists(_op.join(_op.dirname(__file__), '..', 'setup.py')):
        msg="You cannot import pygrib from inside the install directory.\nChange to another directory first."
        raise ImportError(msg)
    else:
        raise
# Need explicit imports for names beginning with underscores
from ._pygrib import __doc__, __version__
