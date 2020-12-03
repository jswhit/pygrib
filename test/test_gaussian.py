import pygrib
import pytest
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs

grbs = pygrib.open('../sampledata/flux.grb')
grb = grbs.message(2)
lats, lons = grb.latlons()
lons1 = lons[0,:]; lats1 = lats[:,0]
data = grb.values
# add cyclic (wrap-around) point to global grid
data,lons1 = add_cyclic_point(data, coord=lons1)
lons,lats = np.meshgrid(lons1,lats1)

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=True)
def test_gaussian():
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    ax.coastlines()
    ax.contourf(lons,lats,data,15)
    # plot location of every 4th grid point
    plt.scatter(lons[::4,::4].ravel(),lats[::4,::4].ravel(),1,marker='o',color='k',zorder=10)
    plt.title('Global Gaussian Grid')
    return fig

# if running with GUI backend, show plot.
if matplotlib.get_backend().lower() != 'agg':
    test_gaussian()
    plt.show()
