import numpy as np
from mpl_toolkits.basemap import Basemap
from numpy import ma
import pygrib, sys
import matplotlib.pyplot as plt

for grb in pygrib.open('../sampledata/tigge.grb'):
    fld = 0.01*grb['values'] # convert to hPa
    lats,lons = grb.latlons()
    sys.stdout.write('%s %s %s %s' % \
            (grb['centre'], fld.shape, fld.min(), fld.max()))
    fig=plt.figure(figsize=(10,5))
    fig.add_axes([0.1,0.1,0.8,0.8])
    m = Basemap(projection='cyl',lon_0=180)
    x, y = m(lons,lats)
    levels = np.arange(475,1101,25)
    CS = m.contourf(x,y,fld,levels,cmap=plt.cm.jet)
    plt.colorbar(drawedges=True, shrink=0.8) # draw colorbar
    m.drawcoastlines()
    m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0])
    m.drawmeridians(np.arange(0,360,60),labels=[0,0,0,1])
    m.drawmapboundary()
    plt.title(grb['name']+': '+grb['centre'].upper(),fontsize=12)
plt.show()
