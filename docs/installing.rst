Installation
============

Dependencies
------------

- ECCODES_ C library.
- `numpy <http://www.numpy.org/>`__ 
- `pyproj <https://pyproj4.github.io/pyproj/stable>`__ 
- `cython <https://cython.org>`__ (only needed at build-time)


Instructions
------------

The easiest way to get everything installed is to use pip_:

    >>> pip install pygrib

This will install all the dependencies for you (including the ECCODES_ C lib).

If you're using Anaconda python, use conda_:

    >>> conda install -c conda-forge pygrib

.. _pip: http://pip.pypa.io/
.. _conda: http://conda.io/
.. _ECCODES: https://confluence.ecmwf.int/display/ECC/

Developing
----------

To build from source, clone the github repository and run setup.py:

    >>> git clone https://github.com/jswhit/pygrib
    >>> cd pygrib
    >>> ECCODES_DIR=path/to/eccodes python setup.py install

where ``$ECCODES_DIR`` is the path to the directory containing ``include/grib_api.h``
and ``lib/libeccodes.so``. If ``ECCODES_DIR`` is not specified, a few common locations
such as ``$CONDA_PREFIX,/usr,/usr/local,/opt/local`` will be searched..
Then run the simple test script to check if things are working
``cd test; python test.py``.  

To be able to run all the tests, install pytest_ and run

    >>> export MPLBACKEND=agg
    >>> cd test
    >>> pytest test*py --mpl --mpl-baseline-path=baseline_images

Many tests require matplotlib_, pytest-mpl_ and cartopy_.  If you don't want to install
those, just run ``test.py`` and ``test_latlons.py``.

.. _pytest: http://pytest.org
.. _pytest-mpl: https://pypi.org/project/pytest-mpl/
.. _matplotlib: https://matplotlib.org
.. _cartopy: https://scitools.org.uk/cartopy/docs/latest/
