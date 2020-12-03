import numpy as np
import pytest
import pygrib, sys
import matplotlib
import matplotlib.pyplot as plt
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs

nplots = 10

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=False)
def test_tigge():
    fig=plt.figure(figsize=(10,50),dpi=20)
    nplot = 1
    for grb in pygrib.open('../sampledata/tigge.grb'):
        fld = 0.01*grb.values # convert to hPa
        lats,lons = grb.latlons()
        lons1 = lons[0,:]; lats1 = lats[:,0]
        # add cyclic (wrap-around) point to global grid
        fld,lons1 = add_cyclic_point(fld, coord=lons1)
        lons,lats = np.meshgrid(lons1,lats1)
        #print('%s %s %s %s' % \
        #     (grb.centre, fld.shape, fld.min(), fld.max()))
        ax = fig.add_subplot(nplots,1,nplot,projection=ccrs.PlateCarree(central_longitude=0))
        levels = np.arange(475,1101,25)
        cs = ax.contourf(lons,lats,fld,levels,cmap=plt.cm.jet)
        #plt.colorbar(cs,shrink=0.8)
        ax.coastlines()
        plt.title(grb.name+': '+grb.centre.upper(),fontsize=36)
        nplot += 1
    plt.tight_layout()
    return fig

# if running with GUI backend, show plot.
if matplotlib.get_backend().lower() != 'agg':
    test_tigge()
    plt.show()
