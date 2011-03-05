import pygrib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
grbs = pygrib.open('../sampledata/reduced_latlon_surface.grib2')
grb = grbs.readline()
data = grb['values']
lats, lons = grb.latlons()
llcrnrlon = lons[0,0]
llcrnrlat = lats[0,0]
urcrnrlon = lons[-1,-1]
urcrnrlat = lats[-1,-1]
m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
            urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
            resolution='c',projection='cyl')
x,y = m(lons,lats)
m.drawcoastlines()
m.contourf(x,y,data,15)
plt.title(grb['name'])
plt.show()
