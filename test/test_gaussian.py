import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
grbs = pygrib.open('../sampledata/flux.grb')
grb = grbs.message(2)
lats, lons = grb.latlons()
data = grb['values']
m = Basemap(lon_0=180)
#m.scatter(lons.flat,lats.flat,1,marker='o',color='k',zorder=10)
x,y = m(lons,lats)
m.drawcoastlines()
m.contourf(x,y,data,15)
#m.fillcontinents()
plt.title('Global Gaussian Grid')
plt.show()
