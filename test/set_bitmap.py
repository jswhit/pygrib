import pygrib

print pygrib.api_version()
infile = '../sampledata/regular_latlon_surface.grib1'
outfile = 'out.grib1'
grbs = pygrib.open(infile)
print grbs.messages
grb = grbs.next()
grb['missingValue']=9999.0
grb['bitmapPresent']=1
data = grb['values']
data[-1,0:10] = 9999.0
grb['values']=data
msg = grb.tostring()
f = open(outfile,'wb')
f.write(msg)
f.close()

grbs = pygrib.open('out.grib1')
grb = grbs.next()
data = grb['values']
lats,lons = grb.latlons()
grbs.close()
# should be some missing values in top left corner of map
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
m = Basemap(llcrnrlon=lons.min(),urcrnrlon=lons.max(),llcrnrlat=lats.min(),urcrnrlat=lats.max(),projection='cyl')
m.drawcoastlines()
m.contourf(lons,lats,data,15)
plt.show()
