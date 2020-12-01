import pygrib
import matplotlib.pyplot as plt
import numpy as np
from numpy import ma
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker


grbs = pygrib.open('../sampledata/ecmwf_tigge.grb')
grb = grbs.select(parameterName='Soil moisture')[0]
fld = grb.values; lats,lons = grb.latlons()
lons1 = lons[0,:]; lats1 = lats[:,0]
# add cyclic (wrap-around) point to global grid
fld,lons1 = add_cyclic_point(fld, coord=lons1)
lons,lats = np.meshgrid(lons1,lats1)

ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
cs = ax.contourf(lons,lats,fld,15,cmap=plt.cm.jet)
plt.colorbar(cs, shrink=0.6)
ax.coastlines()
gl = ax.gridlines(draw_labels=True)
gl.ylabels_top = False; gl.xlabels_top = False
gl.ylabels_right = False; gl.xlabels_right = False
plt.title(grb.parameterName+' on ECMWF Reduced Gaussian Grid')
plt.show()
