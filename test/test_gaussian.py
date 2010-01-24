import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
grb = pygrib.open('../sampledata/flux.grb')
grb.next()
grb.next()
lats, lons = grb.latlons()
data = grb['values']
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
x,y = m(lons,lats)
m.drawcoastlines()
m.contourf(x,y,data,15)
#m.fillcontinents()
plt.title('Global Gaussian Grid')
plt.show()
