import pygrib, time
import matplotlib.pyplot as plt
import numpy as np
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.animation as animation

# animation example.

grbs = pygrib.open('../sampledata/safrica.grib2')
# grab all "brightness temp" grib messages.
btemps = [grb for grb in grbs if grb.name=='Brightness temperature']
grb = btemps[0]
lats, lons = grb.latlons()
projd = grb.projparams
print(projd)
grbs.close()

# create a map projection for the domain, plot 1st image on it.
fig = plt.figure(figsize=(8,7))
globe = ccrs.Globe(ellipse='sphere', semimajor_axis=projd['a'], semiminor_axis=projd['b'])
pj = ccrs.Stereographic(globe=globe,central_longitude=projd['lon_0'],
     central_latitude=projd['lat_0'],
     true_scale_latitude=projd['lat_ts']) 
ax = fig.add_subplot(1,1,1,projection=pj)
coords = pj.transform_points(                                                                
    ccrs.PlateCarree(), np.asarray([lons[0,0],lons[-1,-1]]), np.asarray([lats[0,0],lats[-1,-1]]))
ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], crs=pj)
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle='-');
grb = btemps[0]
im = plt.imshow(np.empty(lons.shape),vmin=230,vmax=310,transform=ccrs.PlateCarree(),origin='lower')
im.set_data(grb.values)
plt.colorbar(im,orientation='horizontal')
txt = plt.title(grb,fontsize=8)

def updatefig(nt):
    global im,txt,btemps,cnt,delay
    grb = btemps[nt]
    im.set_data(grb.values)
    txt.set_text(repr(grb))

ani = animation.FuncAnimation(fig, updatefig, frames=len(btemps))

plt.show()
