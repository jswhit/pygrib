import pygrib, sys
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
grbs = pygrib.open('../sampledata/ds.maxt.bin')
g = grbs.message(1)
lats, lons = g.latlons()
data = g.values
#from ncepgrib2 import Grib2Decode
#grbx = Grib2Decode(g.tostring(),gribmsg=True)
#data = grbx.data()
llcrnrlon = lons[0,0]
llcrnrlat = lats[0,0]
urcrnrlon = lons[-1,-1]
urcrnrlat = lats[-1,-1]
rsphere = (g.projparams['a'],g.projparams['b'])
lat_1 = g.projparams['lat_1']
lat_2 = g.projparams['lat_2']
lon_0 = g.projparams['lon_0']
projection = g.projparams['proj']
fig=plt.figure()
sys.stdout.write(repr(g.projparams)+'\n')
ax = fig.add_axes([0.1,0.1,0.75,0.75])
m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
            urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,rsphere=rsphere,lon_0=lon_0,
            lat_1=lat_1,lat_2=lat_2,resolution='l',projection=projection,area_thresh=10000)
x,y = m(lons, lats)
cs = m.contourf(x,y,data,20,cmap=plt.cm.jet)
m.drawcoastlines()
m.drawstates()
m.drawcountries()
# new axis for colorbar.
cax = plt.axes([0.875, 0.15, 0.03, 0.65])
plt.colorbar(cs, cax, format='%g') # draw colorbar
plt.axes(ax)  # make the original axes current again
plt.title('NDFD Temp CONUS %d-h forecast'% g['forecastTime'],fontsize=12)
plt.show()
