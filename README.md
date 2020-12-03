[![Linux Build Status](https://github.com/jswhit/pygrib/workflows/Install%20and%20Test/badge.svg)](https://github.com/jswhit/pygrib/actions)
[![PyPI package](https://badge.fury.io/py/pygrib.svg)](http://python.org/pypi/pygrib)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pygrib/badges/version.svg)](https://anaconda.org/conda-forge/pygrib)
[![DOI](https://zenodo.org/badge/28599617.svg)](https://zenodo.org/badge/latestdoi/28599617)

Provides a high-level interface to the ECWMF [ECCODES](https://confluence.ecmwf.int/display/ECC) C library for reading GRIB files.
There are limited capabilities for writing GRIB files (you can modify the contents of an existing file, but you can't create one from scratch).  See the online docs for 
[example usage](https://jswhit.github.io/pygrib/api.html#example-usage).

Quickstart
==========

The easiest way to get everything installed is to use the [conda](https://conda.io):

```
conda install -c conda-forge pygrib
```

If you don't use conda, be sure you have the ECCODES library installed first.
Then you can install pygrib with pip:

```
ECCODES_DIR=path/to/eccodes pip install pygrib
```

where `$ECCODES_DIR` is the path to the directory containing `include/grib_api.h`
and `lib/libeccodes.so`. If `ECCODES_DIR` is not specified, a few common locations
such as `$CONDA_PREFIX,/usr,/usr/local,/opt/local` will be searched.

Alternately, clone the github repo and run `python setup.py install` (after setting `$ECCCODES_DIR`).
Run `python test.py` from the source directory to test your pygrib installation.

For full installation instructions and API documentation, see https://jswhit.github.io/pygrib.

Sample [iPython](http://ipython.org/) notebooks illustrating pygrib usage: 
* http://nbviewer.jupyter.org/gist/jswhit/8635665
* https://github.com/scollis/HRRR/blob/master/notebooks/HRRR%20Grib.ipynb

Questions or comments - contact Jeff Whitaker <jeffrey.s.whitaker@noaa.gov>
or use https://github.com/jswhit/pygrib/issues.
