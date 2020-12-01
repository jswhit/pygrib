import numpy as np
from numpy import ma
import pygrib, sys
import matplotlib.pyplot as plt
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker

for grb in pygrib.open('../sampledata/tigge.grb'):
    fld = 0.01*grb.values # convert to hPa
    lats,lons = grb.latlons()
    lons1 = lons[0,:]; lats1 = lats[:,0]
    # add cyclic (wrap-around) point to global grid
    fld,lons1 = add_cyclic_point(fld, coord=lons1)
    lons,lats = np.meshgrid(lons1,lats1)
    sys.stdout.write('%s %s %s %s' % \
            (grb.centre, fld.shape, fld.min(), fld.max()))
    fig=plt.figure(figsize=(10,5))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    levels = np.arange(475,1101,25)
    cs = ax.contourf(lons,lats,fld,levels,cmap=plt.cm.jet)
    plt.colorbar(cs,shrink=0.8)
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True)
    gl.ylabels_top = False; gl.xlabels_top = False
    gl.ylabels_right = False; gl.xlabels_right = False
    plt.title(grb.name+': '+grb.centre.upper(),fontsize=12)
plt.show()
