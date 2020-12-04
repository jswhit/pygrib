import pygrib
import pytest
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

grbs = pygrib.open('../sampledata/dspr.temp.bin')
grb = grbs.select(forecastTime=26)[0]
data = grb['values']
lats, lons = grb.latlons()

globe = ccrs.Globe(ellipse='sphere', semimajor_axis=grb.projparams['a'], semiminor_axis=grb.projparams['b'])
pj = ccrs.Mercator(globe=globe,central_longitude=grb.projparams['lon_0'],
     latitude_true_scale=grb.projparams['lat_ts'])

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=True)
def test_ndfd_pr():
    fig = plt.figure()
    ax = plt.axes([0.1,0.1,0.75,0.75],projection=pj)
    coords = pj.transform_points(
             ccrs.PlateCarree(), np.asarray([lons[0,0],lons[-1,-1]]), np.asarray([lats[0,0],lats[-1,-1]]))
    ax.set_extent([coords[0, 0], coords[1, 0], coords[0, 1], coords[1, 1]], crs=pj)
    coords = pj.transform_points(ccrs.PlateCarree(), lons, lats)
    cs = ax.contourf(coords[:,:,0],coords[:,:,1],data,20,cmap=plt.cm.jet)
    # new axis for colorbar.
    cax = plt.axes([0.875, 0.15, 0.03, 0.65])
    plt.colorbar(cs, cax, format='%g') # draw colorbar
    plt.axes(ax)  # make the original axes current again
    if matplotlib.get_backend().lower() != 'agg':
        # don't plot coastlines or gridlines for image comparison
        ax.coastlines(resolution='50m')
        gl = ax.gridlines(draw_labels=True)
        gl.ylabels_top = False; gl.xlabels_top = False
        gl.ylabels_right = False; gl.xlabels_right = False
    plt.title('NDFD Temp Puerto Rico %d-h fcst from %d' %\
            (grb.forecastTime,grb.dataDate),fontsize=12)
    return fig

# if running with GUI backend, show plot.
if matplotlib.get_backend().lower() != 'agg':
    test_ndfd_pr()
    plt.show()
