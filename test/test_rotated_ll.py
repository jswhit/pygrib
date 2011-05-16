import pygrib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import sys
grbs = pygrib.open('../sampledata/cl00010000_ecoclimap_rot.grib1')
grb = grbs.message(7)
lats, lons = grb.latlons()
sys.stdout.write(repr(grb.projparams)+'\n')
data = grb['values']
m = Basemap(projection='stere',lon_0=10,lat_0=55,width=5000.e3,height=5000.e3,resolution='l')
x,y = m(lons,lats)
m.drawcoastlines()
m.contourf(x,y,data,15)
m.scatter(x[::5,::5].flat,y[::5,::5].flat,1,marker='o',color='k',zorder=10)
m.drawmeridians(np.arange(-60,61,5))
m.drawparallels(np.arange(20,80,5))
plt.title(grb['name'])
plt.show()
