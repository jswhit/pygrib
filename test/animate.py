import matplotlib
matplotlib.use('GTKAgg')
import pygrib
import matplotlib.pyplot as plt
import numpy as np
import time
from mpl_toolkits.basemap import Basemap

# animation example.

grbs = pygrib.open('../sampledata/safrica.grib2')
# grab all "brightness temp" grib messages.
btemps = [grb for grb in grbs if grb['name']=='Brightness temperature']
lats, lons = grb.latlons()
projd = grb.projparams
grbs.close()
print projd

# create a map projection for the domain, plot 1st image on it.
m =\
Basemap(projection=projd['proj'],lat_ts=projd['lat_ts'],lon_0=projd['lon_0'],\
        lat_0=projd['lat_0'],rsphere=(projd['a'],projd['b']),\
        llcrnrlat=lats[0,0],urcrnrlat=lats[-1,-1],\
        llcrnrlon=lons[0,0],urcrnrlon=lons[-1,-1],resolution='i')
plt.ion() # set interactive mode on
plt.figure(figsize=(8,7))
m.drawcoastlines()
m.drawcountries()
grb = btemps[0]
im = m.imshow(grb['values'],interpolation='nearest',vmin=230,vmax=310)
plt.colorbar(orientation='horizontal')
m.drawparallels(np.arange(-80,10,10),labels=[1,0,0,0])
m.drawmeridians(np.arange(-80,81,20),labels=[0,0,0,1])
plt.title(grb,fontsize=8)
plt.draw()

# loop 4 times, plot all images sequentially.
for loop in range(4):
   time.sleep(5)
   for grb in btemps:
       print grb
       im.set_data(grb['values'])
       plt.title(grb,fontsize=8)
       plt.draw()
time.sleep(5)
