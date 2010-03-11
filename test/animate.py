import matplotlib
matplotlib.use('GTKAgg')
import pygrib, time ,gobject
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

# animation example.

grbs = pygrib.open('../sampledata/safrica.grib2')
# grab all "brightness temp" grib messages.
btemps = [grb for grb in grbs if grb['name']=='Brightness temperature']
lats, lons = grb.latlons()
projd = grb.projparams
grbs.close()

# create a map projection for the domain, plot 1st image on it.
m =\
Basemap(projection=projd['proj'],lat_ts=projd['lat_ts'],lon_0=projd['lon_0'],\
        lat_0=projd['lat_0'],rsphere=(projd['a'],projd['b']),\
        llcrnrlat=lats[0,0],urcrnrlat=lats[-1,-1],\
        llcrnrlon=lons[0,0],urcrnrlon=lons[-1,-1],resolution='i')
plt.figure(figsize=(8,7))
m.drawcoastlines()
m.drawcountries()
grb = btemps[0]
im = m.imshow(grb['values'],interpolation='nearest',vmin=230,vmax=310)
plt.colorbar(orientation='horizontal')
m.drawparallels(np.arange(-80,10,10),labels=[1,0,0,0])
m.drawmeridians(np.arange(-80,81,20),labels=[0,0,0,1])
txt = plt.title(grb,fontsize=8)

manager = plt.get_current_fig_manager()
# callback function to update image.
def updatefig(*args):
    global cnt, delay
    grb = btemps[cnt]
    im.set_data(grb['values'])
    txt.set_text(repr(grb))
    manager.canvas.draw()
    if cnt==0 or cnt==1: time.sleep(delay)
    cnt = cnt+1
    if cnt==len(btemps): cnt=0
    return True

cnt = 0 # image counter
delay = 1 # delay at beginning and end of loop
gobject.idle_add(updatefig)
print 'close window to exit ...'
plt.show()
print 'done'
