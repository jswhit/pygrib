import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
grbs = pygrib.open('../sampledata/gfs.grb')
for g in grbs:
    if g['name'] == 'Volumetric soil moisture content':
        data = g['values']
        lats,lons = g.latlons()
        break
print data.min(), data.max()
print lats[:,0]
print lons[0,:]
llcrnrlon = lons[0,0]
llcrnrlat = lats[0,0]
urcrnrlon = lons[-1,-1]
urcrnrlat = lats[-1,-1]
print llcrnrlon,llcrnrlat,urcrnrlon,urcrnrlat
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
