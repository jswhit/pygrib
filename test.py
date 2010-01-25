import pygrib
# demonstrates basic functionality of module
grbs = pygrib.open('sampledata/flux.grb')
# iterate over all grib messages.
print '-- all messages --'
for grb in grbs:
    print grb
# position iterator at beginning again.
grbs.rewind()
print '-- all messages (again)  --'
for grb in grbs:
    print grb
# get grib a specific grib message from the iterator.
# iterator will be positioned at this message.
grb = grbs.message(2)
print '-- 2nd message --'
print grb # 2nd message
# get just the next grib message.
grb.next()
print '-- 3rd message --'
print grb # 3rd message
# now the iterator should be positioned at the last (4th) message.
print '-- iterate from 4th message to the end--'
for grb in grbs:
    print grb # only last message printed.
grb.rewind()
print '-- Maximium temperature --'
for grb in grbs:
    if grb['name'] == 'Maximum temperature':
        print grb
        data = grb['values']
        print '-- data values, grid info for msg number %d --' % \
        grb.messagenumber
        print 'shape/min/max data',data.shape,data.min(), data.max()
        lats, lons = grb.latlons()
        print 'min/max lats on %s grid' % grb['typeOfGrid'], lats.min(),\
        lats.max()
        print 'min/max lons on %s grid' % grb['typeOfGrid'], lons.min(),\
        lons.max()
