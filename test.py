import pygrib
# demonstrates basic functionality of module
# open a grib file, create an iterator.
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
# get a specific grib message from the iterator.
# iterator will be positioned at this message.
grb = grbs.message(2) 
print '-- 2nd message --'
print grb # 2nd message
# position iterator at next grib message.
grb = grbs.next() 
print '-- 3rd message --'
print grb # 3rd message
# now the iterator should be positioned at the last (4th) message.
print '-- iterate from 4th message to the end--'
for grb in grbs:
    print grb # only last message printed.
# rewind again
grbs.rewind()
print '-- Maximium temperature --'
# iterate over all messages until
# 'Maximum temperature' is found.
for grb in grbs:
    if grb['name'] == 'Maximum temperature': break
print grb
# get the data and the lat/lon values of the Max temp grid 
data = grb['values'] # 'values' returns the data
print '-- data values, grid info for msg number %d --' % \
grb.messagenumber # current message number
print 'shape/min/max data',data.shape,data.min(), data.max()
lats, lons = grb.latlons() # returns lat/lon values on grid.
print 'min/max of %d lats on %s grid' % (grb['Nj'], grb['typeOfGrid']),\
lats.min(),lats.max()
print 'min/max of %d lons on %s grid' % (grb['Ni'], grb['typeOfGrid']),\
lons.min(),lons.max()
