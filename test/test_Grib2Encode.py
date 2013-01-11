from __future__ import print_function
import pygrib
import numpy as np
from numpy import ma
from ncepgrib2 import Grib2Decode, Grib2Encode
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# read soil moisture grib record with GRIB API.
grbs = pygrib.open('../sampledata/gfs.t12z.pgrbf120.2p5deg.grib2')
grbmsg = grbs[208] # soil moisture
data = grbmsg.values
print(data.min(), data.max())

# convert grib message to a ncepgrib2.Grib2Message instance.
grb = Grib2Decode(grbmsg.tostring(), gribmsg=True)

# re-write the grib message to a new file.
f=open('test_masked.grb','wb')
grbo = Grib2Encode(grb.discipline_code,grb.identification_section)
grbo.addgrid(grb.grid_definition_info,grb.grid_definition_template)
# add product definition template, data representation template
# and data (including bitmap which is read from data mask).
grbo.addfield(grb.product_definition_template_number,grb.product_definition_template,grb.data_representation_template_number,grb.data_representation_template,data)
# finalize the grib message.
grbo.end()
# write it to the file.
f.write(grbo.msg)
# close the output file
f.close()

# read and plot the data in the new file.
# ..with pygrib
#grbs = pygrib.open('test_masked.grb')
#grb = grbs.readline()
# ..with ncepgrib2
grb = Grib2Decode('test_masked.grb')
lats,lons = grb.latlons()
data = grb.values
print(data.min(), data.max())
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
