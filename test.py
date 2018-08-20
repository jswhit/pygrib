def test():
    """
    demonstrates basic pygrib functionality.

    open a grib file, create an iterator.
    >>> import pygrib
    >>> list(pygrib.open('sampledata/flux.grb'))
    [1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120 hrs (avg):from 200402291200, 2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200, 3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200, 4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200]
    >>> pygrib.open('sampledata/flux.grb').read()
    [1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120 hrs (avg):from 200402291200, 2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200, 3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200, 4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200]
    >>> grbs = pygrib.open('sampledata/flux.grb')

    acts like a file object
    >>> grbs.tell()
    0
    >>> grbs.read(1)
    [1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120 hrs (avg):from 200402291200]
    >>> grbs.tell()
    1
    >>> grbs.read(2)
    [2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200, 3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200]
    >>> grbs.read()
    [4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200]
    >>> grbs.seek(1)
    >>> grbs.readline()
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200
    >>> grbs.seek(-3,2)
    >>> grbs.readline()
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200
    >>> grbs.seek(1,1)
    >>> grbs.readline()
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
    >>> grbs.seek(0)

    first grib message
    >>> grb1 = grbs.readline()
    >>> grb1
    1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120 hrs (avg):from 200402291200

    iterate over rest of grib messages.
    >>> for grb in grbs: grb
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200

    iterator now positioned at last message
    >>> grb
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200

    grb1 is still first grib message
    >>> grb1
    1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120 hrs (avg):from 200402291200

    position iterator at beginning again.
    >>> grbs.rewind()
    >>> for grb in grbs: grb
    1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120 hrs (avg):from 200402291200
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200

    get a specific grib message from the iterator.
    iterator will be positioned at this message.
    >>> grb = grbs.message(3)
    >>> grb # 3rd message
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200

    indexing iterator with an integer key has the same result,
    except that the position of iterator does not change.
    >>> grbs.seek(0) # position iterator at beginning (same as grbs.rewind())
    >>> grb = grbs[2] # 2nd message
    >>> grb
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200

    position iterator at next grib message.
    >>> grb = grbs.readline()
    >>> grb # back to the 1st message
    1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120 hrs (avg):from 200402291200

    use select method to choose grib messages based upon specified key/value pairs.
    >>> selected_grbs = grbs.select(level=2,typeOfLevel='heightAboveGround') # get all 2-m level fields
    >>> for grb in selected_grbs: grb
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200

    as above, but using step key (issue #9)
    >>> selected_grbs = grbs.select(level=2,typeOfLevel='heightAboveGround',step=120)
    >>> for grb in selected_grbs: grb
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200

    or create grib index instance for faster searching
    >>> grbindx = pygrib.index('sampledata/flux.grb','name','typeOfLevel','level')
    >>> selgrbs = grbindx(name='Minimum temperature',level=2,typeOfLevel='heightAboveGround')
    >>> for grb in selgrbs: grb
    1:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
    >>> selgrbs = grbindx(name='Maximum temperature',level=2,typeOfLevel='heightAboveGround')
    >>> for grb in selgrbs: grb
    1:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
    >>> grbindx.write('flux.grb.idx') # save the index
    >>> grbindx.close()

    reload the saved index
    >>> grbindx = pygrib.index('flux.grb.idx')
    >>> selgrbs = grbindx(name='Minimum temperature',level=2,typeOfLevel='heightAboveGround')
    >>> for grb in selgrbs: grb
    1:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
    >>> selgrbs = grbindx(name='Maximum temperature',level=2,typeOfLevel='heightAboveGround')
    >>> for grb in selgrbs: grb
    1:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200
    >>> grbindx.close()

    >>> grb = selgrbs[0]
    >>> grb
    1:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120 hrs:from 200402291200

    get the data and the lat/lon values of the Max temp grid
    >>> data = grb['values'] # 'values' returns the data
    >>> 'shape/min/max data %s %6.2f %6.2f'%(str(data.shape),data.min(),data.max())
    'shape/min/max data (94, 192) 223.70 319.90'
    >>> lats, lons = grb.latlons() # returns lat/lon values on grid.
    >>> str('min/max of %d lats on %s grid %4.2f %4.2f' % (grb['Nj'], grb['typeOfGrid'],lats.min(),lats.max()))
    'min/max of 94 lats on regular_gg grid -88.54 88.54'
    >>> str('min/max of %d lons on %s grid %4.2f %4.2f' % (grb['Ni'], grb['typeOfGrid'],lons.min(),lons.max()))
    'min/max of 192 lons on regular_gg grid 0.00 358.12'

    get 2nd grib message from the iterator
    >>> grb = grbs.message(2)
    >>> grb
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120 hrs:from 200402291200
    >>> 'valid date %s' % grb['validityDate']
    'valid date 20040305'
    >>> 'min/max %5.1f %5.1f' % (grb['minimum'],grb['maximum'])
    'min/max 49650.0 109330.0'

    change the forecast time.
    gribmessage keys can be accessed either via attributes or key/value pairs.
    >>> grb['forecastTime'] = 168
    >>> grb['forecastTime']
    168
    >>> grb.forecastTime = 240
    >>> grb.forecastTime
    240
    >>> grb['parameterNumber'] = 2 # change to pressure tendency
    >>> data = grb['values']
    >>> grb['values']=data/1000. # rescale

    open an output file for writing
    >>> grbout = open('test.grb','wb')

    get coded binary string for modified message
    >>> msg = grb.tostring()

    write to file and close.
    >>> ret = grbout.write(msg)
    >>> grbout.close()

    reopen file, check contents.
    >>> grbs = pygrib.open('test.grb')
    >>> grb = grbs.readline()
    >>> grb
    1:Pressure tendency:Pa s**-1 (instant):regular_gg:surface:level 0:fcst time 240 hrs:from 200402291200
    >>> 'valid date %s' % grb['validityDate']
    'valid date 20040310'
    >>> grb.analDate
    datetime.datetime(2004, 2, 29, 12, 0)
    >>> grb.validDate
    datetime.datetime(2004, 3, 10, 12, 0)

    disable this test for now, since the result depends on the version
    of grib_api installed.
    #>>> str('min/max %4.2f %4.2f' % (grb['minimum'],grb['maximum']))
    #'min/max 49.65 109.65'

    >>> grbs.close()

    test open.select with scalars, sequences and functions.
    >>> grbs = pygrib.open('sampledata/gfs.grb')
    >>> sel_grbs = grbs.select(shortName='t',level=500)
    >>> for grb in sel_grbs: grb
    101:Temperature:K (instant):regular_ll:isobaricInhPa:level 50000 Pa:fcst time 72 hrs:from 201110080000
    >>> sel_grbs = grbs.select(shortName='t',level=(850,700,500))
    >>> for grb in sel_grbs: grb
    101:Temperature:K (instant):regular_ll:isobaricInhPa:level 50000 Pa:fcst time 72 hrs:from 201110080000
    133:Temperature:K (instant):regular_ll:isobaricInhPa:level 70000 Pa:fcst time 72 hrs:from 201110080000
    157:Temperature:K (instant):regular_ll:isobaricInhPa:level 85000 Pa:fcst time 72 hrs:from 201110080000
    >>> sel_grbs = grbs.select(shortName='t',level=lambda l: l < 500 and l >= 300)
    >>> for grb in sel_grbs: grb
    69:Temperature:K (instant):regular_ll:isobaricInhPa:level 30000 Pa:fcst time 72 hrs:from 201110080000
    77:Temperature:K (instant):regular_ll:isobaricInhPa:level 35000 Pa:fcst time 72 hrs:from 201110080000
    85:Temperature:K (instant):regular_ll:isobaricInhPa:level 40000 Pa:fcst time 72 hrs:from 201110080000
    93:Temperature:K (instant):regular_ll:isobaricInhPa:level 45000 Pa:fcst time 72 hrs:from 201110080000
    >>> from datetime import datetime
    >>> sel_grbs = grbs.select(shortName='t',level=300,validDate=datetime(2011,10,11,0))
    >>> for grb in sel_grbs: grb
    69:Temperature:K (instant):regular_ll:isobaricInhPa:level 30000 Pa:fcst time 72 hrs:from 201110080000
    >>> lats, lons = grb.latlons() # returns lat/lon values on grid.
    >>> str('min/max of %d lats on %s grid %4.2f %4.2f' % (grb['Nj'], grb['typeOfGrid'],lats.min(),lats.max()))
    'min/max of 73 lats on regular_ll grid -90.00 90.00'

    test data subsetting via data method.
    >>> datsubset,latsubset,lonsubset=grb.data(lat1=15,lat2=65,lon1=220,lon2=320)
    >>> latsubset.min(),latsubset.max(),lonsubset.min(),lonsubset.max()
    (15.0, 65.0, 220.0, 320.0)
    >>> 'shape/min/max data subset %s %6.2f %6.2f' % (str(datsubset.shape),datsubset.min(),datsubset.max())
    'shape/min/max data subset (21, 41) 219.70 247.60'

    >>> grbstr = grb.tostring()
    >>> grb2 = pygrib.fromstring(grbstr)
    >>> grb2
    1:Temperature:K (instant):regular_ll:isobaricInhPa:level 30000 Pa:fcst time 72 hrs:from 201110080000
    >>> grb2.analDate
    datetime.datetime(2011, 10, 8, 0, 0)
    >>> grb2.validDate
    datetime.datetime(2011, 10, 11, 0, 0)
    >>> grbs.close()
    >>> grbs = pygrib.open('sampledata/gfs.t12z.pgrbf120.2p5deg.grib2')
    >>> # see if multi-part grib messages are counted properly
    >>> grbs.messages
    343
    >>> grbs.close()

    test ndfd file with 'grid_complex_spatial_differencing' encoding
    >>> grbs = pygrib.open('sampledata/dspr.temp.bin')
    >>> for grb in grbs: grb
    1:Maximum temperature:K (max):mercator:surface:level 0:fcst time 2-14 hrs (max):from 201109292200
    2:Maximum temperature:K (max):mercator:surface:level 0:fcst time 26-38 hrs (max):from 201109292200
    3:Maximum temperature:K (max):mercator:surface:level 0:fcst time 50-62 hrs (max):from 201109292200
    4:Maximum temperature:K (max):mercator:surface:level 0:fcst time 74-86 hrs (max):from 201109292200
    >>> str(grb.packingType)
    'grid_complex_spatial_differencing'
    >>> data = grb.values
    >>> grbs.close()
    >>> str('min/max %5.2f %5.2f' % (data.min(), data.max()))
    'min/max 295.40 308.10'
    >>> grbs = pygrib.open('sampledata/no-radius-shapeOfEarth-7.grb2')
    >>> for grb in grbs: print(grb)
    1:Total precipitation:kg m-2 (accum):lambert:surface:level 0:fcst time 15-30 mins (accum):from 201804100000
    >>> str(grb.packingType)
    'grid_simple'
    >>> grbs.close()
    """

if __name__ == "__main__":
    import doctest
    failure_count, test_count = doctest.testmod(verbose=True)
    import pygrib, sys
    sys.stdout.write('using ECCODES library version %s\n' % pygrib.grib_api_version)
    if failure_count==0:
        sys.exit(0)
    else:
        sys.exit(1)
