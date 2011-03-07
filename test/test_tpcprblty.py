import pygrib, sys
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap,cm
import numpy as np
grbs = pygrib.open('../sampledata/tpcprblty.grib2')
grb=grbs.select(parameterName='Wind speed',scaledValueOfUpperLimit=17491,stepRange='0-120')[0]
sys.stdout.write(repr(grb)+'\n')
lats, lons = grb.latlons()
data = grb.values
map =\
Basemap(projection='lcc',lon_0=-90,lat_0=30,width=4000.e3,height=2000.e3,resolution='l')
map.bluemarble()
map.drawcoastlines(color='yellow')
x,y = map(lons,lats)
levels = np.arange(10,101,10)
map.contourf(x,y,data,levels,cmap=cm.GMT_haxby_r)
upperlim = float(grb.scaledValueOfUpperLimit)/np.power(10,grb.scaleFactorOfUpperLimit)
plt.title('TC Wind Speed Prob > %5.2f m/s fcst hrs %s from %s' %\
        (upperlim,grb.stepRange,repr(grb.dataDate)+repr(grb.dataTime)[0:2]),fontsize=12)
map.drawparallels(np.arange(0,41,5),labels=[1,0,0,0],color='0.8')
map.drawmeridians(np.arange(180,360,10),labels=[0,0,0,1],color='0.8')
cb = plt.colorbar(orientation='horizontal')
cb.ax.set_xlabel('percent')
plt.show()
