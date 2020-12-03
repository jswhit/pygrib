import pygrib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.testing.compare import compare_images

grbs = pygrib.open('../sampledata/ngm.grb')
grb = grbs.select(parameterName='Pressure',typeOfLevel='surface')[0]
data = grb.values; lats,lons = grb.latlons()

globe = ccrs.Globe(ellipse='sphere', semimajor_axis=grb.projparams['a'], semiminor_axis=grb.projparams['b'])
pj = ccrs.Stereographic(globe=globe,central_longitude=grb.projparams['lon_0'],
     central_latitude=grb.projparams['lat_0'],
     true_scale_latitude=grb.projparams['lat_ts']) 
ax = plt.axes(projection=pj)
coords = pj.transform_points(                                                                
         ccrs.PlateCarree(), np.asarray([lons[0,0],lons[-1,-1]]), np.asarray([lats[0,0],lats[-1,-1]]))
ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], crs=pj)
# this should work but doesn't?
#ax.set_extent([lons[0,0],lons[-1,-1],lats[0,0],lats[-1,-1]],crs=ccrs.PlateCarree())
ax.scatter(lons.flat,lats.flat,3,marker='o',color='k',zorder=10,transform=ccrs.PlateCarree())
ax.coastlines()
# this should work but looks wonky
#cs = ax.contourf(lons,lats,data,15,transform=ccrs.PlateCarree())
coords = pj.transform_points(ccrs.PlateCarree(), lons, lats)
cs = ax.contourf(coords[:,:,0],coords[:,:,1],data,15)
plt.title('Stereographic Model Grid (NCEP)')
# raise exception if generated image doesn't match baseline 
plt.savefig('stere.png')
assert( compare_images('stere_baseline.png','stere.png',10) is None )

plt.figure()
grbs = pygrib.open('../sampledata/CMC_reg_WIND_ISBL_300_ps60km_2010052400_P012.grib')
# this file has key "projectionCenterFlag"
grb = grbs.readline()
data = grb['values']
lats,lons = grb.latlons()

globe = ccrs.Globe(ellipse='sphere', semimajor_axis=grb.projparams['a'], semiminor_axis=grb.projparams['b'])
pj = ccrs.Stereographic(globe=globe,central_longitude=grb.projparams['lon_0'],
     central_latitude=grb.projparams['lat_0'],
     true_scale_latitude=grb.projparams['lat_ts']) 
ax = plt.axes(projection=pj)
coords = pj.transform_points(                                                                
         ccrs.PlateCarree(), np.asarray([lons[0,0],lons[-1,-1]]), np.asarray([lats[0,0],lats[-1,-1]]))
ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], crs=pj)
# this should work but doesn't?
#ax.set_extent([lons[0,0],lons[-1,-1],lats[0,0],lats[-1,-1]],crs=ccrs.PlateCarree())
#ax.scatter(lons.flat,lats.flat,3,marker='o',color='k',zorder=10,transform=ccrs.PlateCarree())
ax.coastlines()
# this should work but looks wonky
#cs = ax.contourf(lons,lats,data,15,transform=ccrs.PlateCarree())
coords = pj.transform_points(ccrs.PlateCarree(), lons, lats)
cs = ax.contourf(coords[:,:,0],coords[:,:,1],data,15)
plt.title('Stereographic Model Grid (CMC)')
if matplotlib.get_backend().lower() == 'agg':
    # raise exception if generated image doesn't match baseline 
    plt.savefig('stere.png')
    assert( compare_images('stere_baseline2.png','stere.png',10) is None )
plt.show()
