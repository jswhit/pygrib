import pygrib, sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.testing.compare import compare_images

grbs = pygrib.open('../sampledata/ds.maxt.bin')
grb = grbs.message(1)
lats, lons = grb.latlons()
data = grb.values

globe = ccrs.Globe(ellipse='sphere', semimajor_axis=grb.projparams['a'], semiminor_axis=grb.projparams['b'])
pj = ccrs.LambertConformal(globe=globe,central_longitude=grb.projparams['lon_0'],
     central_latitude=grb.projparams['lat_0'],
     standard_parallels =(grb.projparams['lat_1'],grb.projparams['lat_2']))
plt.figure()
ax = plt.axes([0.1,0.1,0.75,0.75],projection=pj)
coords = pj.transform_points(                                                                
         ccrs.PlateCarree(), np.asarray([lons[0,0],lons[-1,-1]]), np.asarray([lats[0,0],lats[-1,-1]]))
ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], crs=pj)
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle='-');
ax.add_feature(cfeature.STATES, linestyle='-');
coords = pj.transform_points(ccrs.PlateCarree(), lons, lats)
cs = ax.contourf(coords[:,:,0],coords[:,:,1],data,20,cmap=plt.cm.jet)
# new axis for colorbar.
cax = plt.axes([0.875, 0.15, 0.03, 0.65])
plt.colorbar(cs, cax, format='%g') # draw colorbar
plt.axes(ax)  # make the original axes current again
plt.title('NDFD Temp CONUS %d-h forecast'% grb.forecastTime,fontsize=12)
if matplotlib.get_backend().lower() == 'agg':
    # raise exception if generated image doesn't match baseline 
    plt.savefig('ndfd_conus.png')
    assert( compare_images('ndfd_conus_baseline.png','ndfd_conus.png',10) is None )
plt.show()
