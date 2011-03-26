from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pygrib
import numpy as np
try:
    import spharm
except:
    raise ImportError("requires pyspharm (python spherical harmonic module) from http://code.google.com/p/pyspharm")

grbs = pygrib.open('../sampledata/spherical_pressure_level.grib1')
g = grbs[1]
fld = g.values

# ECMWF normalizes the spherical harmonic coeffs differently than NCEP.
# (m=0,n=0 is global mean, instead of sqrt(2)/2 times global mean)
fld = 2.*fld/np.sqrt(2.)
fldr = fld[0::2]
fldi = fld[1::2]
fld = np.zeros(fldr.shape,'F')
fld.real = fldr
fld.imag = fldi
nlons = 360;  nlats = 181
s = spharm.Spharmt(nlons,nlats)
data = s.spectogrd(fld)
lons = (360./nlons)*np.arange(nlons)
lats = 90.-(180./(nlats-1))*np.arange(nlats)
lons, lats = np.meshgrid(lons, lats)
# stack grids side-by-side (in longitiudinal direction), so
# any range of longitudes (between -360 and 360) may be plotted on a world map.
lons = np.concatenate((lons-360,lons),1)
lats = np.concatenate((lats,lats),1)
data = np.concatenate((data,data),1)
# setup miller cylindrical map projection.
m = Basemap(llcrnrlon=-180.,llcrnrlat=-90,urcrnrlon=180.,urcrnrlat=90.,\
            resolution='l',area_thresh=10000.,projection='mill')
x, y = m(lons,lats)
CS = m.contourf(x,y,data,15,cmap=plt.cm.jet)
ax = plt.gca()
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = plt.axes([l+w+0.025, b, 0.025, h]) # setup colorbar axes
plt.colorbar(drawedges=True, cax=cax) # draw colorbar
plt.axes(ax)  # make the original axes current again
m.drawcoastlines()
# draw parallels
delat = 30.
circles = np.arange(-90.,90.+delat,delat)
m.drawparallels(circles,labels=[1,0,0,0])
# draw meridians
delon = 60.
meridians = np.arange(-180,180,delon)
m.drawmeridians(meridians,labels=[0,0,0,1])
plt.title(repr(g['level'])+' '+g['typeOfLevel']+' '+g['name']+' from Spherical Harmonic Coeffs')
plt.show()
