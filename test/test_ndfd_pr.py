import pygrib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.testing.compare import compare_images

grbs = pygrib.open('../sampledata/dspr.temp.bin')
grb = grbs.select(forecastTime=26)[0]
data = grb['values']
lats, lons = grb.latlons()

globe = ccrs.Globe(ellipse='sphere', semimajor_axis=grb.projparams['a'], semiminor_axis=grb.projparams['b'])
pj = ccrs.Mercator(globe=globe,central_longitude=grb.projparams['lon_0'],
     latitude_true_scale=grb.projparams['lat_ts'])
plt.figure()
ax = plt.axes([0.1,0.1,0.75,0.75],projection=pj)
coords = pj.transform_points(
         ccrs.PlateCarree(), np.asarray([lons[0,0],lons[-1,-1]]), np.asarray([lats[0,0],lats[-1,-1]]))
ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], crs=pj)
#ax.coastlines(resolution='50m')
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle='-');
ax.add_feature(cfeature.STATES, linestyle='-');
coords = pj.transform_points(ccrs.PlateCarree(), lons, lats)
cs = ax.contourf(coords[:,:,0],coords[:,:,1],data,20,cmap=plt.cm.jet)
# new axis for colorbar.
cax = plt.axes([0.875, 0.15, 0.03, 0.65])
plt.colorbar(cs, cax, format='%g') # draw colorbar
plt.axes(ax)  # make the original axes current again
gl = ax.gridlines(draw_labels=True)
gl.ylabels_top = False; gl.xlabels_top = False
gl.ylabels_right = False; gl.xlabels_right = False
plt.title('NDFD Temp Puerto Rico %d-h fcst from %d' %\
        (grb.forecastTime,grb.dataDate),fontsize=12)
if matplotlib.get_backend().lower() == 'agg':
    # raise exception if generated image doesn't match baseline 
    plt.savefig('ndfd_pr.png')
    assert( compare_images('ndfd_pr_baseline.png','ndfd_pr.png',10) is None )
plt.show()
