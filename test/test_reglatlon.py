import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
for g in pygrib.open('../sampledata/gfs.grb'):
    if g['name'] == 'Volumetric soil moisture content':
        data = g['values']
        lats,lons = g.latlons()
        break
m = Basemap(lon_0=180)
#m.scatter(lons.flat,lats.flat,1,marker='o',color='k',zorder=10)
m.drawcoastlines()
x,y = m(lons,lats)
m.contourf(x,y,data,15)
#m.fillcontinents()
plt.title(g['name']+' Global Lat/Lon Grid')
plt.show()
