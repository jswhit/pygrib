import numpy as np
import pygrib, sys
import matplotlib
import matplotlib.pyplot as plt
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs
from matplotlib.testing.compare import compare_images

for grb in pygrib.open('../sampledata/tigge.grb'):
    fld = 0.01*grb.values # convert to hPa
    lats,lons = grb.latlons()
    lons1 = lons[0,:]; lats1 = lats[:,0]
    # add cyclic (wrap-around) point to global grid
    fld,lons1 = add_cyclic_point(fld, coord=lons1)
    lons,lats = np.meshgrid(lons1,lats1)
    #print('%s %s %s %s' % \
    #     (grb.centre, fld.shape, fld.min(), fld.max()))
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
    if matplotlib.get_backend().lower() == 'agg':
        # raise exception if generated image doesn't match baseline
        plt.savefig('tigge_%s.png' % grb.centre.upper())
        assert( compare_images('tigge_%s_baseline.png'%grb.centre.upper(),'tigge_%s.png'%grb.centre.upper(),10) is None )
#plt.show()
