import pygrib
import pytest
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs

grbs = pygrib.open('../sampledata/reduced_latlon_surface.grib2')
grb = grbs.readline()
data = grb.values
lats, lons = grb.latlons()
lons1 = lons[0,:]; lats1 = lats[:,0]
# add cyclic (wrap-around) point to global grid
data,lons1 = add_cyclic_point(data, coord=lons1)
lons,lats = np.meshgrid(lons1,lats1)

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=True)
def test_reduced_ll():
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    cs = ax.contourf(lons,lats,data,15)
    ax.coastlines()
    plt.title(grb.name)
    return fig

# if running with GUI backend, show plot.
if matplotlib.get_backend().lower() != 'agg':
    test_reduced_ll()
    plt.show()
