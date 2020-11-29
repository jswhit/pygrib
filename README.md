[![Linux Build Status](https://travis-ci.org/jswhit/pygrib.svg?branch=master)](https://travis-ci.org/jswhit/pygrib)
[![PyPI package](https://badge.fury.io/py/pygrib.svg)](http://python.org/pypi/pygrib)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pygrib/badges/version.svg)](https://anaconda.org/conda-forge/pygrib)
[![DOI](https://zenodo.org/badge/28599617.svg)](https://zenodo.org/badge/latestdoi/28599617)

Python module for reading and writing GRIB files (edition 1 and edition 2).

GRIB is the World Meteorological Organization (WMO) standard
file format for the exchange of weather data.

Provides a high-level interfaces for the ECWMF ECCODES C library and
command line utilities for listing (grib_list) and repacking (grib_repack)
GRIB files.

Quickstart:

* Clone the github repository, or download a source release from https://pypi.python.org/pypi/pygrib.

* install dependencies (eccodes library, numpy, pyproj). On linux, this can
be done via `sudo apt-get install libeccodes-dev libproj-dev proj-bin; pip install numpy pyproj`.

* set ECCODES_DIR environment variable to point to where eccodes is installed (`grib_api.h` in `$ECCODE_DIR/include`, `libeccodes` in `$ECCODES_DIR/lib`). If `ECCODES_DIR` not set, some standard locations will be searched.

* Run `python setup.py build`

* Run `python setup.py install` (with sudo if necessary)

* Run `python test.py` to test your pygrib installation.

For full installation instructions and API documentation, see https://jswhit.github.io/pygrib.

Sample [iPython](http://ipython.org/) notebooks illustrating pygrib usage: 
* http://nbviewer.jupyter.org/gist/jswhit/8635665
* https://github.com/scollis/HRRR/blob/master/notebooks/HRRR%20Grib.ipynb

Questions or comments - contact Jeff Whitaker <jeffrey.s.whitaker@noaa.gov>
or use https://github.com/jswhit/pygrib/issues.
