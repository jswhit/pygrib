# noqa
"""High-level python interface to ECCODES library for GRIB file IO."""
from __future__ import annotations
from typing import NewType, Any
import numpy as np
import pandas as pd
import numpy.typing as npt

FloatArray = npt.NDArray[np.float_]
NData = NewType("NData[float]", FloatArray)
NLats = NewType("NLat[float]", FloatArray)
NLons = NewType("NLon[float]", FloatArray)

def fromstring(string: str) -> gribmessage:
    """Create a gribmessage instance from a python bytes object representing a binary grib message (the reverse of gribmessage.tostring())."""

def gaulats(nlats: NLats) -> np.ndarray:
    """Returns nlats gaussian latitudes, in degrees, oriented from north to south. nlats must be even."""

def get_definitions_path() -> str:
    """
    return eccodes_definitions_path currently in use.

    If empty, then definitions installed with linked eccodes lib are begin used.
    """

class gribmessage:
    """
    class pygrib.gribmessage
    Bases: object

    Grib message object.

    Each grib message has attributes corresponding to GRIB keys. Parameter names are described by the name, 
    shortName and paramID keys. pygrib also defines some special attributes which are defined below

    Variables
        messagenumber - The grib message number in the file.

        projparams - A dictionary containing proj4 key/value pairs describing the grid. Set to None for 
        unsupported grid types.

        expand_reduced - If True (default), reduced lat/lon and gaussian grids will be expanded to regular 
        grids when data is accessed via values key. If False, data is kept on unstructured reduced grid, 
        and is returned in a 1-d array.

        fcstimeunits - A string representing the forecast time units (an empty string if not defined).

        analDate - A python datetime instance describing the analysis date and time for the forecast. 
        Only set if forecastTime and julianDay keys exist.

        validDate - A python datetime instance describing the valid date and time for the forecast. 
        Only set if forecastTime and julianDay keys exist, and fcstimeunits is defined. 
        If forecast time is a range, then validDate corresponds to the end of the range.
    """

    def data(self, lat1: int = ..., lat2: int = ..., lon1: int = ..., lon2: int = ...) -> tuple[NData, NLats, NLons]:
        """
        extract data, lats and lons for a subset region defined by the keywords lat1,lat2,lon1,lon2.
        The default values of lat1,lat2,lon1,lon2 are None, which means the entire grid is returned.
        If the grid type is unprojected lat/lon and a geographic subset is requested
        (by using the lat1,lat2,lon1,lon2 keywords), then 2-d arrays are returned, otherwise 1-d arrays are returned.
        """
    def expand_grid(self, arg=True) -> None:
        """toggle expansion of 1D reduced grid data to a regular (2D) grid (on by default)."""
    def has_key(self, key: Any) -> bool:
        """tests whether a grib message object has a specified key."""
    def is_missing(self, key: Any) -> bool:
        """
        returns True if key is invalid or value associated with key is equal to
        grib missing value flag (False otherwise)
        """
    def keys(self) -> list[str]:
        """return keys associated with a grib message in a list"""
    def latlons(self) -> tuple[NLats, NLons]:
        """
        compute lats and lons (in degrees) of grid. Currently handles regular lat/lon,
        global gaussian, mercator, stereographic, lambert conformal, albers equal-area,
        space-view, azimuthal equidistant, reduced gaussian, reduced lat/lon, lambert
        azimuthal equal-area, rotated lat/lon and rotated gaussian grids.
        Returns
        lats,lons numpy arrays containing latitudes and longitudes of grid (in degrees).
        """
    def tostring(self) -> bytes:
        """
        return coded grib message in a binary string.
        """
    def valid_key(self, key: str) -> bool:
        """
        tests whether a grib message object has a specified key,
        it is not missing and it has a value that can be read
        """
    def __getitem__(self, key: str) -> int | str | np.ndarray: ...

class index:
    """
    >>> import pygrib
    >>> grbindx=pygrib.index('sampledata/gfs.grb','shortName','typeOfLevel','level')
    >>> grbindx.keys
    ['shortName', 'level']
    >>> selected_grbs=grbindx.select(shortName='gh',typeOfLevel='isobaricInhPa',level=500)
    >>> for grb in selected_grbs:
    >>>    grb
    1:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 500 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
    >>> # __call__ method does same thing as select
    >>> selected_grbs=grbindx(shortName='u',typeOfLevel='isobaricInhPa',level=250)
    >>> for grb in selected_grbs:
    >>>    grb
    1:u-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 250 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
    >>> grbindx.write('gfs.grb.idx') # save index to a file
    >>> grbindx.close()
    >>> grbindx = pygrib.index('gfs.grb.idx') # re-open index (no keys specified)
    >>> grbindx.keys # not set when opening a saved index file.
    None
    >>> for grb in selected_grbs:
    >>>     grb
    1:u-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 250 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
    """
    def __init__(self,*args):...
    keys:list[str]
    types:list[str]

class open:
    """
    Each grib message has attributes corresponding to GRIB keys. 
    
    Parameter names are described by the name, shortName and paramID keys. 
    
    pygrib also defines some special attributes which are defined below
    
    """
    has_multi_field_msgs: bool
    closed: bool
    messagenumber: int
    messages: int
    name: str
    def __init__(self, filename:str):...
    def __next__(self) -> gribmessage: ...
    def __getitem__(self, key: int | slice) -> gribmessage: ...
    def __call__(self, **kwargs) -> list[gribmessage]: ...

    def close(self) -> None:
        """close GRIB file, deallocate C structures associated with class instance"""

    def message(self, num: int) -> gribmessage:
        """retrieve N'th message in iterator. same as seek(N-1) followed by readline()."""

    def read(self, num: int = None) -> list[gribmessage]:
        """
        read N messages from current position, returning grib messages instances in a list.
        If N=None, all the messages to the end of the file are read.
        pygrib.open(f).read() is equivalent to list(pygrib.open(f)),
        both return a list containing gribmessage instances for all the grib messages in the file f.
        """
    def tell(self) -> int | None: ...
    def seek(self, num: int) -> int: ...
    def select(**kwargs) -> list[gribmessage]:
        """
        return a list of gribmessage instances from iterator filtered by kwargs. 
        If keyword is a container object, each grib message in the iterator is searched for membership in the container. 
        If keyword is a callable (has a _call__ method), each grib message in the iterator is tested using the callable (which should return a boolean). 
        If keyword is not a container object or a callable, each grib message in the iterator is tested for equality.

        Example usage:
        ```
        import pygrib
        grbs = pygrib.open('sampledata/gfs.grb')
        selected_grbs=grbs.select(shortName='gh',typeOfLevel='isobaricInhPa',level=10)
        for grb in selected_grbs: grb
        26:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 10 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
        # the __call__ method does the same thing
        selected_grbs=grbs(shortName='gh',typeOfLevel='isobaricInhPa',level=10)
        for grb in selected_grbs: grb
        26:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 10 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
        # to select multiple specific key values, use containers (e.g. sequences)
        selected_grbs=grbs(shortName=['u','v'],typeOfLevel='isobaricInhPa',level=[10,50])
        for grb in selected_grbs: grb
        193:u-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 50 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
        194:v-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 50 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
        199:u-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 10 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
        200:v-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 10 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
        # to select key values based on a conditional expression, use a function
        selected_grbs=grbs(shortName='gh',level=lambda l: l < 500 and l >= 300)
        for grb in selected_grbs: grb
        14:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 45000 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
        15:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 40000 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
        16:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 35000 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
        17:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 30000 Pa:fcst time 72 hrs:from 200412091200:lo res cntl fcst
        ```
        """
def reload(grb:gribmessage):
    """
    Recreate gribmessage object, updating all the keys to be consistent with each other. 
    For example, if the forecastTime key is changed, recreating the gribmessage object 
    with this function will cause the analDate and verifDate keys to be updated accordingly.
    Equivalent to fromstring(grb.tostring())
    """

def set_definitions_path(eccodes_definition_path:str):
    """set path to eccodes definition files (grib tables)."""

def setdates(grb:gribmessage):
    """
    set fcstimeunits, analDate and validDate attributes using the julianDay, 
    forecastTime and indicatorOfUnitOfTimeRange keys. 
    
    Called automatically when gribmessage instance created, but can be called 
    manually to update keys if one of them is modified after instance creation.
    """
def tolerate_badgrib_off():
    """raise an exception when a missing or malformed key is encountered (default behavior)."""

def tolerate_badgrib_on():
    """don't raise an exception when a missing or malformed key is encountered."""