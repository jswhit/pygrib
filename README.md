[![Linux Build Status](https://travis-ci.org/jswhit/pygrib.svg?branch=master)](https://travis-ci.org/jswhit/pygrib)
[![PyPI package](https://badge.fury.io/py/pygrib.svg)](http://python.org/pypi/pygrib)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pygrib/badges/version.svg)](https://anaconda.org/conda-forge/pygrib)
[![DOI](https://zenodo.org/badge/28599617.svg)](https://zenodo.org/badge/latestdoi/28599617)

Provides a high-level interface to the ECWMF ECCODES C library for reading GRIB files.
There are limited capabilities for writing GRIB files.

Quickstart:

The easiest way to get everything installed is to use the [conda](https://conda.io)` command line tool:

```
conda install -c conda-forge pygrib
```

If you don't use conda, be sure you have the required dependencies
installed first. Then, install cftime with pip:

```
ECCODES_DIR=path/to/eccodes pip install pygrib
```

where `$ECCODES_DIR` is the path to the directory containing `include/grib_api.h`
and `lib/libeccodes.so`. If `ECCODES_DIR` is not specified, a few common locations
such as `$CONDA_PREFIX,/usr,/usr/local,/opt/local` will be searched..

Clone the github repository and run `python test.py` to test your pygrib installation.

For full installation instructions and API documentation, see https://jswhit.github.io/pygrib.

Sample [iPython](http://ipython.org/) notebooks illustrating pygrib usage: 
* http://nbviewer.jupyter.org/gist/jswhit/8635665
* https://github.com/scollis/HRRR/blob/master/notebooks/HRRR%20Grib.ipynb

Questions or comments - contact Jeff Whitaker <jeffrey.s.whitaker@noaa.gov>
or use https://github.com/jswhit/pygrib/issues.
