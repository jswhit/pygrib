Installation
============

Required dependencies
---------------------

- Python >= 2.7
- `ECCODES <https://confluence.ecmwf.int/display/ECC>`__ C library version 2.19.1 or higher.
- `numpy <http://www.numpy.org/>`__ 
- `pyproj <https://pyproj4.github.io/pyproj/stable>`__ 


Instructions
------------

The easiest way to get everything installed is to use conda_ command line tool::

    $ conda install -c conda-forge pygrib

.. _conda: http://conda.io/

If you don't use conda, be sure you have the required dependencies
installed first. Then, install cftime with pip::

    $ ECCODES_DIR=path/to/eccodes pip install pygrib

where ``$ECCODES_DIR`` is the path to the directory containing ``include/grib_api.h``
and ``lib/libeccodes.so``. If ``ECCODES_DIR`` is not specified, a few common locations
such as ``$CONDA_PREFIX,/usr,/usr/local,/opt/local`` will be searched..


Developing
----------

When developing we recommend cloning the GitHub repository,
building the extension in-place with `cython <http://cython.org/>`__ 0.19 or later
``python setup.py build_ext --inplace``

and running the test script to check if the changes are passing the tests
``python test.py``
