API
===

Example usage
-------------

from the python interpreter prompt, import the package:

    >>> import pygrib

open a GRIB file, create a grib message iterator:

    >>> grbs = pygrib.open('sampledata/flux.grb')  

pygrib open instances behave like regular python file objects, with
``seek``, ``tell``, ``read``, ``readline`` and ``close`` methods, except
that offsets are measured in grib messages instead of bytes:

    >>> grbs.seek(2)
    >>> grbs.tell()
    2
    >>> grb = grbs.read(1)[0] # read returns a list with the next N (N=1 in this case) messages.
    >>> grb # printing a grib message object displays summary info
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
    >>> grbs.tell()
    3

print an inventory of the file:

    >>> grbs.seek(0)
    >>> for grb in grbs:
    >>>     grb 
    1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120 hrs (avg):from 200402291200
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200

find the first grib message with a matching name:

    >>> grb = grbs.select(name='Maximum temperature')[0]

extract the data values using the ``values`` key (``grb.keys()`` will return a list of the available keys):

    >>> maxt = grb.values # same as grb['values']
    # The data is returned as a numpy array, or if missing values or a bitmap
    # are present, a numpy masked array.  Reduced lat/lon or gaussian grid
    # data is automatically expanded to a regular grid. Details of the internal
    # representation of the grib data (such as the scanning mode) are handled
    # automatically.
    >>> maxt.shape, maxt.min(), maxt.max()
    (94, 192) 223.7 319.9

get the latitudes and longitudes of the grid:

    >>> lats, lons = grb.latlons()
    >>> lats.shape, lats.min(), lats.max(), lons.shape, lons.min(), lons.max()
    (94, 192) -88.5419501373 88.5419501373  0.0 358.125

get the second grib message:

    >>> grb = grbs.message(2) # same as grbs.seek(1); grb=grbs.readline()
    >>> grb
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200

extract data and get lat/lon values for a subset over North America:

    >>> data, lats, lons = grb.data(lat1=20,lat2=70,lon1=220,lon2=320)
    >>> data.shape, lats.min(), lats.max(), lons.min(), lons.max()
    (26, 53) 21.904439458 69.5216630593 221.25 318.75

modify the values associated with existing keys:

    >>> grb['forecastTime'] = 240
    >>> grb.dataDate = 20100101

get the binary string associated with the coded message:

    >>> msg = grb.tostring()
    >>> grbs.close() # close the grib file.

write the modified message to a new GRIB file:

    >>> grbout = open('test.grb','wb')
    >>> grbout.write(msg)
    >>> grbout.close()
    >>> pygrib.open('test.grb').readline() 
    1:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 240 hrs:from 201001011200

Module docstrings
-----------------

.. automodule:: pygrib
   :members: open, gribmessage, index, gaulats, julian_to_datetime, reload, setdates, fromstring, multi_support_off,multi_support_on, tolerate_badgrib_off, tolerate_badgrib_on
   :show-inheritance:
