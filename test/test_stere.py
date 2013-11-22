import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
grbs = pygrib.open('../sampledata/ngm.grb')
grb = grbs.select(parameterName='Pressure',typeOfLevel='surface')[0]
data = grb.values; lats,lons = grb.latlons()
llcrnrlon = lons[0,0]
llcrnrlat = lats[0,0]
urcrnrlon = lons[-1,-1]
urcrnrlat = lats[-1,-1]
rsphere = (grb.projparams['a'], grb.projparams['b'])
lat_ts = grb.projparams['lat_ts']
lon_0 = grb.projparams['lon_0']
lat_0 = grb.projparams['lat_0']
projection = grb.projparams['proj']
m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
            urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,rsphere=rsphere,lon_0=lon_0,
            lat_ts=lat_ts,lat_0=lat_0,resolution='l',projection=projection)
x,y = m(lons, lats)
m.scatter(x.flat,y.flat,3,marker='o',color='k',zorder=10)
m.drawcoastlines()
m.contourf(x,y,data,15)
plt.title('Stereographic Model Grid (NCEP)')

plt.figure()
grbs = pygrib.open('../sampledata/CMC_reg_WIND_ISBL_300_ps60km_2010052400_P012.grib')
# this file has key "projectionCenterFlag"
grb = grbs.readline()
data = grb['values']
lats,lons = grb.latlons()
llcrnrlon = lons[0,0]
llcrnrlat = lats[0,0]
urcrnrlon = lons[-1,-1]
urcrnrlat = lats[-1,-1]
rsphere = (grb.projparams['a'], grb.projparams['b'])
lat_ts = grb.projparams['lat_ts']
lon_0 = grb.projparams['lon_0']
lat_0 = grb.projparams['lat_0']
projection = grb.projparams['proj']
m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
            urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,rsphere=rsphere,lon_0=lon_0,
            lat_ts=lat_ts,lat_0=lat_0,resolution='l',projection=projection)
m.drawcoastlines()
x,y = m(lons,lats)
m.contourf(x,y,data,15)
plt.title('Stereographic Model Grid (CMC)')
plt.show()
