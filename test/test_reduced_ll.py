import pygrib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs
from matplotlib.testing.compare import compare_images
grbs = pygrib.open('../sampledata/reduced_latlon_surface.grib2')
grb = grbs.readline()
data = grb.values
lats, lons = grb.latlons()
lons1 = lons[0,:]; lats1 = lats[:,0]
# add cyclic (wrap-around) point to global grid
data,lons1 = add_cyclic_point(data, coord=lons1)
lons,lats = np.meshgrid(lons1,lats1)
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
cs = ax.contourf(lons,lats,data,15)
ax.coastlines()
plt.title(grb.name)
if matplotlib.get_backend().lower() == 'agg':
    # raise exception if generated image doesn't match baseline 
    plt.savefig('reduced_ll.png')
    assert( compare_images('reduced_ll_baseline.png','reduced_ll.png',10) is None )
plt.show()
