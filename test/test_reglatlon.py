import pygrib
import pytest
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs

grbs = pygrib.open('../sampledata/gfs.grb')
grb = grbs.select(name='Orography')[0]
grb2 = grbs.select(name='Volumetric soil moisture content')[0]

data = grb.values; lats,lons = grb.latlons()
data2 = grb2.values
lons1d = lons[0,:]; lats1d = lats[:,0]
# add cyclic (wrap-around) point to global grid
data,lons1 = add_cyclic_point(data, coord=lons1d)
data2,lons1 = add_cyclic_point(data2, coord=lons1d)
lons,lats = np.meshgrid(lons1,lats1d)

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=True)
def test_reglatlon1():
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    ax.coastlines()
    ax.contourf(lons,lats,data,15,cmap=plt.cm.hot_r)
    plt.title('%s Global Lat/Lon Grid' % grb.name)
    return fig

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=True)
def test_reglatlon2():
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    ax.coastlines()
    ax.contourf(lons,lats,data2,15)
    plt.title('%s Global Lat/Lon Grid' % grb2.name)
    return fig

lat1=15; lat2=65; lon1=220; lon2=320
datsubset,latsubset,lonsubset=grb.data(lat1=lat1,lat2=lat2,lon1=lon1,lon2=lon2)

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=True)
def test_reglatlon3():
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    ax.set_extent([lon1,lon2,lat1,lat2],crs=ccrs.PlateCarree())
    ax.coastlines()
    ax.contourf(lonsubset,latsubset,datsubset,15,cmap=plt.cm.hot_r)
    plt.title('%s Regional Lat/Lon Grid' % grb.name)
    return fig

# if running with GUI backend, show plot.
if matplotlib.get_backend().lower() != 'agg':
    test_reglatlon1()
    test_reglatlon2()
    test_reglatlon3()
    plt.show()
