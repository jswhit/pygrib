import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

grbs = pygrib.open('../sampledata/gfs.grb')
grb = grbs.select(name='Orography')[0]
grb2 = grbs.select(name='Volumetric soil moisture content')[0]

data = grb.values; lats,lons = grb.latlons()
data2 = grb2.values

m = Basemap(llcrnrlon=lons.min(),llcrnrlat=lats.min(),urcrnrlon=lons.max(),urcrnrlat=lats.max(),projection='cyl')
m.drawcoastlines()
m.contourf(lons,lats,data,15,cmap=plt.cm.hot_r)
plt.title('%s Global Lat/Lon Grid' % grb.name)
fig = plt.figure()
m.drawcoastlines()
m.contourf(lons,lats,data2,15)
plt.title('%s Global Lat/Lon Grid' % grb2.name)

lat1=15; lat2=65; lon1=220; lon2=320
datsubset,latsubset,lonsubset=grb.data(lat1=lat1,lat2=lat2,lon1=lon1,lon2=lon2)

fig = plt.figure()
m = Basemap(llcrnrlon=lon1,llcrnrlat=lat1,urcrnrlon=lon2,urcrnrlat=lat2,projection='cyl',resolution='l')
m.drawcoastlines()
m.contourf(lonsubset,latsubset,datsubset,15,cmap=plt.cm.hot_r)
plt.title('%s Regional Lat/Lon Grid' % grb.name)

plt.show()
