import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
for g in pygrib.open('../sampledata/gfs.grb'):
    if g['name'] == 'Volumetric soil moisture content':
        data = g['values']
        lats,lons = g.latlons()
        break
llcrnrlon = lons[0,0]
llcrnrlat = lats[0,0]
urcrnrlon = lons[-1,-1]
urcrnrlat = lats[-1,-1]
m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
            urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
            resolution='c',projection='cyl')
#m.scatter(lons.flat,lats.flat,1,marker='o',color='k',zorder=10)
m.drawcoastlines()
x,y = m(lons,lats)
m.contourf(x,y,data,15)
#m.fillcontinents()
plt.title(g['name']+' Global Lat/Lon Grid')
plt.show()
