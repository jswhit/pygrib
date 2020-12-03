import pygrib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from cartopy.util import add_cyclic_point
from matplotlib.testing.compare import compare_images
import cartopy.crs as ccrs
grbs = pygrib.open('../sampledata/flux.grb')
grb = grbs.message(2)
lats, lons = grb.latlons()
lons1 = lons[0,:]; lats1 = lats[:,0]
data = grb.values
# add cyclic (wrap-around) point to global grid
data,lons1 = add_cyclic_point(data, coord=lons1)
lons,lats = np.meshgrid(lons1,lats1)
plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
ax.coastlines()
ax.contourf(lons,lats,data,15)
# plot location of every 4th grid point
plt.scatter(lons[::4,::4].ravel(),lats[::4,::4].ravel(),1,marker='o',color='k',zorder=10)
plt.title('Global Gaussian Grid')
if matplotlib.get_backend().lower() == 'agg':
    # raise exception if generated image doesn't match baseline 
    plt.savefig('gaussian.png')
    assert( compare_images('gaussian_baseline.png','gaussian.png',10) is None )
plt.show()
