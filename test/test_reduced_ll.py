import pygrib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
grbs = pygrib.open('../sampledata/reduced_latlon_surface.grib2')
grb = grbs.readline()
data = grb['values']
lats, lons = grb.latlons()
m = Basemap(lon_0=180)
x,y = m(lons,lats)
m.drawcoastlines()
m.contourf(x,y,data,15)
plt.title(grb['name'])
plt.show()
