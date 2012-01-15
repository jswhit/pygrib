import pygrib
import numpy as np
from numpy import ma
from ncepgrib2 import Grib2Decode, Grib2Encode
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

grbs = pygrib.open('../sampledata/gfs.t12z.pgrbf120.2p5deg.grib2')
grbmsg = grbs[208] # soil moisture
data = grbmsg.values
print data.min(), data.max()

grb = Grib2Decode(grbmsg.tostring(), gribmsg=True)
f=open('test_masked.grb','wb')
grbo = Grib2Encode(grb.discipline_code,grb.identification_section)
grbo.addgrid(grb.grid_definition_info,grb.grid_definition_template)
# add product definition template, data representation template
# and data (data and optional bitmap).
print ma.isMA(data)
print data.min(), data.max()
print grb.bitmap_indicator_flag
# bitmap read from data mask.
grbo.addfield(grb.product_definition_template_number,grb.product_definition_template,grb.data_representation_template_number,grb.data_representation_template,data)
# finalize the grib message.
grbo.end()
# write it to the file.
f.write(grbo.msg)
# close the output file
f.close()

grbs = pygrib.open('test_masked.grb')
grb = grbs.readline()
#grbs = pygrib.open('../sampledata/gfs.t12z.pgrbf120.2p5deg.grib2')
#grb = grbs[208] # soil moisture
lats,lons = grb.latlons()
data = grb.values
#data = ma.masked_values(data,9999.0)
print data.min(), data.max()
print ma.isMA(data)
m = Basemap(lon_0=180,projection='kav7')
x, y = m(lons, lats)
CS = m.contourf(x,y,data,15,cmap=plt.cm.jet)
m.drawmapboundary(fill_color='w')
m.colorbar()
m.drawcoastlines()
# draw parallels
delat = 30.
circles = np.arange(-90.,90.+delat,delat)
m.drawparallels(circles,labels=[1,0,0,0])
# draw meridians
delon = 60.
meridians = np.arange(0,360,delon)
m.drawmeridians(meridians,labels=[0,0,0,1])
plt.title('soil moisture')
plt.show()
