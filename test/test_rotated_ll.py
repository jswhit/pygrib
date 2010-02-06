import pygrib
import numpy as np
import matplotlib.pyplot as plt
import pyproj
from mpl_toolkits.basemap import Basemap
grbs = pygrib.open('../sampledata/rotated_ll.grib1')
grb = grbs.next()
lats, lons = grb.latlons()
data = grb['values']
m = Basemap(projection='stere',lon_0=5,lat_0=60,width=4000.e3,height=3000.e3,resolution='l')
x,y = m(lons,lats)
m.drawcoastlines()
m.contourf(x,y,data,15)
m.scatter(x[::10,::10].flat,y[::10,::10].flat,1,marker='o',color='k',zorder=10)
m.drawmeridians(np.arange(-60,61,5))
m.drawparallels(np.arange(20,80,5))
plt.title(grb['name'])
plt.show()
