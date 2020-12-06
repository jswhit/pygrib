import pygrib
import pytest
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

grbs = pygrib.open('../sampledata/ngm.grb')
grb = grbs.select(parameterName='Pressure',typeOfLevel='surface')[0]
data = grb.values; lats,lons = grb.latlons()
grbs.close()

globe = ccrs.Globe(ellipse='sphere', semimajor_axis=grb.projparams['a'], semiminor_axis=grb.projparams['b'])
pj = ccrs.Stereographic(globe=globe,central_longitude=grb.projparams['lon_0'],
     central_latitude=grb.projparams['lat_0'],
     true_scale_latitude=grb.projparams['lat_ts']) 

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=True)
def test_stere1():
    fig = plt.figure()
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
    return fig

grbs = pygrib.open('../sampledata/CMC_reg_WIND_ISBL_300_ps60km_2010052400_P012.grib')
# this file has key "projectionCenterFlag"
grb2 = grbs.readline()
data2 = grb2.values
lats2,lons2 = grb2.latlons()
grbs.close()

globe = ccrs.Globe(ellipse='sphere', semimajor_axis=grb2.projparams['a'], semiminor_axis=grb2.projparams['b'])
pj2 = ccrs.Stereographic(globe=globe,central_longitude=grb2.projparams['lon_0'],
     central_latitude=grb2.projparams['lat_0'],
     true_scale_latitude=grb2.projparams['lat_ts']) 

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=True)
def test_stere2():
    fig = plt.figure()
    ax = plt.axes(projection=pj2)
    coords = pj2.transform_points(                                                                
             ccrs.PlateCarree(), np.asarray([lons2[0,0],lons2[-1,-1]]), np.asarray([lats2[0,0],lats2[-1,-1]]))
    ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], crs=pj2)
    ax.coastlines()
    coords = pj2.transform_points(ccrs.PlateCarree(), lons2, lats2)
    cs = ax.contourf(coords[:,:,0],coords[:,:,1],data2,15)
    plt.title('Stereographic Model Grid (CMC)')
    return fig

# if running with GUI backend, show plot.
if matplotlib.get_backend().lower() != 'agg':
    test_stere1()
    test_stere2()
    plt.show()
