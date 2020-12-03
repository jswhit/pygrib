import pygrib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import sys
from matplotlib.testing.compare import compare_images

grbs = pygrib.open('../sampledata/cl00010000_ecoclimap_rot.grib1')
grb = grbs.message(7)
lats, lons = grb.latlons()
data = grb.values
sys.stdout.write(repr(grb.projparams)+'\n')

globe = ccrs.Globe(ellipse='sphere', semimajor_axis=grb.projparams['a'], semiminor_axis=grb.projparams['b'])
pj = ccrs.Stereographic(globe=globe,central_longitude=10,central_latitude=55)
coords = pj.transform_points(                                                                
         ccrs.PlateCarree(), np.asarray([-14.75,72]), np.asarray([29.5,65.6]))
ax = plt.axes(projection=pj)
ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], crs=pj)
ax.scatter(lons[::5,::5].flat,lats[::5,::5].flat,1,marker='o',color='k',zorder=10,transform=ccrs.PlateCarree())
coords = pj.transform_points(ccrs.PlateCarree(), lons, lats)
cs = ax.contourf(coords[:,:,0],coords[:,:,1],data,15)
gl = ax.gridlines(draw_labels=False)
ax.coastlines()
plt.title(grb.name+' Rotated Lat/Lon grid')
if matplotlib.get_backend().lower() == 'agg':
    # raise exception if generated image doesn't match baseline 
    plt.savefig('rotated_ll.png')
    assert( compare_images('rotated_ll_baseline.png','rotated_ll.png',10) is None )
plt.show()
