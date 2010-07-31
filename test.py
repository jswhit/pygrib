def test():
    """
    demonstrates basic pygrib functionality.

    open a grib file, create an iterator.
    >>> import pygrib
    >>> grbs = pygrib.open('sampledata/flux.grb')
    >>> grb1 = grbs.next()

    first grib message
    >>> print grb1
    1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120:from 200402291200

    iterate over rest of grib messages.
    >>> for grb in grbs: print grb
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120:from 200402291200
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200

    iterator now positioned at last message
    >>> print grb
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200

    grb1 is still first grib message
    >>> print grb1
    1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120:from 200402291200

    position iterator at beginning again.
    >>> grbs.rewind() 
    >>> for grb in grbs: print grb
    1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120:from 200402291200
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120:from 200402291200
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200

    get a specific grib message from the iterator.
    iterator will be positioned at this message.
    >>> grb = grbs.message(3) 
    >>> print grb # 3rd message
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200

    indexing iterator with an integer key has the same result
    >>> grb = grbs[2] # 2nd message
    >>> print grb
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120:from 200402291200

    position iterator at next grib message.
    >>> grb = grbs.next() 
    >>> print grb # 3rd message
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200

    now the iterator should be positioned at the last (4th) message.
    >>> for grb in grbs: print grb # only last message printed.
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200

    use select method to choose grib messages based upon specified key/value pairs.
    >>> selected_grbs = grbs.select(level=2,typeOfLevel='heightAboveGround') # get all 2-m level fields
    >>> for grb in selected_grbs: print grb
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200

    or create grib index instance for faster searching
    >>> grbindx = pygrib.index('sampledata/flux.grb','name','typeOfLevel','level')
    >>> selgrbs = grbindx(name='Minimum temperature',level=2,typeOfLevel='heightAboveGround')
    >>> for grb in selgrbs: print grb
    1:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200
    >>> selgrbs = grbindx(name='Maximum temperature',level=2,typeOfLevel='heightAboveGround')
    >>> for grb in selgrbs: print grb
    1:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200
    >>> grbindx.close()

    >>> grb = selgrbs[0]
    >>> print grb
    1:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200

    get the data and the lat/lon values of the Max temp grid 
    >>> data = grb['values'] # 'values' returns the data
    >>> print 'shape/min/max data %s %6.2f %6.2f'%(str(data.shape),data.min(),data.max())
    shape/min/max data (94, 192) 223.70 319.90
    >>> lats, lons = grb.latlons() # returns lat/lon values on grid.
    >>> print 'min/max of %d lats on %s grid %4.2f %4.2f' % (grb['Nj'], grb['typeOfGrid'],lats.min(),lats.max())
    min/max of 94 lats on regular_gg grid -88.54 88.54
    >>> print 'min/max of %d lons on %s grid %4.2f %4.2f' % (grb['Ni'], grb['typeOfGrid'],lons.min(),lons.max())
    min/max of 192 lons on regular_gg grid 0.00 358.12

    get 2nd grib message from the iterator
    >>> grb = grbs.message(2)
    >>> print grb
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120:from 200402291200
    >>> print 'valid date',grb['validityDate']
    valid date 20040305
    >>> print 'min/max %5.1f %5.1f' % (grb['minimum'],grb['maximum'])
    min/max 49650.0 109330.0

    change the forecast time.
    gribmessage keys can be accessed either via attributes or key/value pairs.
    >>> grb['forecastTime'] = 168  
    >>> print grb['forecastTime']
    168
    >>> grb.forecastTime = 240
    >>> print grb.forecastTime
    240
    >>> grb['parameterNumber'] = 2 # change to pressure tendency
    >>> data = grb['values']
    >>> grb['values']=data/86400. # put in units of Pa/S

    open an output file for writing
    >>> grbout = open('test.grb','w')

    get coded binary string for modified message
    >>> msg = grb.tostring()

    write to file and close.
    >>> grbout.write(msg)
    >>> grbout.close()

    reopen file, check contents.
    >>> grbs = pygrib.open('test.grb')
    >>> grb = grbs.next()
    >>> print grb
    1:Pressure tendency:Pa s**-1 (instant):regular_gg:surface:level 0:fcst time 240:from 200402291200
    >>> print 'valid date',grb['validityDate']
    valid date 20040310
    >>> print 'min/max %4.2f %4.2f' % (grb['minimum'],grb['maximum'])
    min/max 0.57 1.27
    >>> grbs.close()

    test open.select with scalars, sequences and functions.
    >>> grbs = pygrib.open('sampledata/gfs.grb')
    >>> sel_grbs = grbs.select(shortName='t',level=500)
    >>> for grb in sel_grbs: print grb
    39:Temperature:K (instant):regular_ll:isobaricInhPa:level 50000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
    >>> sel_grbs = grbs.select(shortName='t',level=(850,700,500))
    >>> for grb in sel_grbs: print grb
    32:Temperature:K (instant):regular_ll:isobaricInhPa:level 85000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
    35:Temperature:K (instant):regular_ll:isobaricInhPa:level 70000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
    39:Temperature:K (instant):regular_ll:isobaricInhPa:level 50000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
    >>> sel_grbs = grbs.select(shortName='t',level=lambda l: l < 500 and l >= 300)
    >>> for grb in sel_grbs: print grb
    40:Temperature:K (instant):regular_ll:isobaricInhPa:level 45000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
    41:Temperature:K (instant):regular_ll:isobaricInhPa:level 40000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
    42:Temperature:K (instant):regular_ll:isobaricInhPa:level 35000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
    43:Temperature:K (instant):regular_ll:isobaricInhPa:level 30000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
    >>> grbs.close()
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
