import pygrib

grib1 = False
if grib1:
    infile = '../sampledata/regular_latlon_surface.grib1'
else:
    infile = '../sampledata/regular_latlon_surface.grib2'
outfile = 'out.grib'
grbs = pygrib.open(infile)
grb = grbs.readline()
data = grb['values']
grb['missingValue']=9999.
grb['bitmapPresent']=1
nx = grb['Ni']; ny = grb['Nj']
data[3*ny//8:5*ny//8,3*nx//8:5*nx//8]=grb['missingValue']
grb['values']=data
msg = grb.tostring()
grbs.close()
f = open(outfile,'wb')
f.write(msg)
f.close()
 
grbs = pygrib.open('out.grib')
grb = grbs.readline()
data = grb['values']
lats,lons = grb.latlons()
grbs.close()
# should be a hole in the middle of the plot
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
m = Basemap(llcrnrlon=lons.min(),urcrnrlon=lons.max(),llcrnrlat=lats.min(),urcrnrlat=lats.max(),projection='cyl')
m.drawcoastlines()
m.contourf(lons,lats,data,15)
plt.show()
