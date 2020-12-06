import pygrib
import pytest
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import sys

grbs = pygrib.open('../sampledata/cl00010000_ecoclimap_rot.grib1')
grb = grbs.message(7)
lats, lons = grb.latlons()
data = grb.values
sys.stdout.write(repr(grb.projparams)+'\n')

globe = ccrs.Globe(ellipse='sphere', semimajor_axis=grb.projparams['a'], semiminor_axis=grb.projparams['b'])
pj = ccrs.Stereographic(globe=globe,central_longitude=10,central_latitude=55)

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=True)
def test_rotated_ll():
    fig = plt.figure()
    ax = plt.axes(projection=pj)
    coords = pj.transform_points(
             ccrs.PlateCarree(), np.asarray([-14.75,72]), np.asarray([29.5,65.6]))
    ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], crs=pj)
    ax.scatter(lons[::5,::5].flat,lats[::5,::5].flat,1,marker='o',color='k',zorder=10,transform=ccrs.PlateCarree())
    coords = pj.transform_points(ccrs.PlateCarree(), lons, lats)
    cs = ax.contourf(coords[:,:,0],coords[:,:,1],data,15)
    if matplotlib.get_backend().lower() != 'agg':
        # don't plot coastlines for image comparison
        gl = ax.gridlines(draw_labels=False)
        ax.coastlines()
    plt.title(grb.name+' Rotated Lat/Lon grid')
    return fig

# if running with GUI backend, show plot.
if matplotlib.get_backend().lower() != 'agg':
    test_rotated_ll()
    plt.show()
