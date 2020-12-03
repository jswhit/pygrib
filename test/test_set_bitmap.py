import pygrib
import pytest

grib1 = False
if grib1:
    infile = '../sampledata/regular_latlon_surface.grib1'
else:
    infile = '../sampledata/regular_latlon_surface.grib2'
outfile = 'out.grib'
grbs = pygrib.open(infile)
grb = grbs.readline()
data = grb['values']
grb['missingValue']=9999.
grb['bitmapPresent']=1
nx = grb['Ni']; ny = grb['Nj']
data[3*ny//8:5*ny//8,3*nx//8:5*nx//8]=grb['missingValue']
grb['values']=data
msg = grb.tostring()
grbs.close()
f = open(outfile,'wb')
f.write(msg)
f.close()
 
grbs = pygrib.open('out.grib')
grb = grbs.readline()
data = grb['values']
lats,lons = grb.latlons()
grbs.close()
# should be a hole in the middle of the plot
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs
import matplotlib
import matplotlib.pyplot as plt

@pytest.mark.mpl_image_compare(tolerance=20,remove_text=True)
def test_set_bitmap():
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
    ax.coastlines()
    cs = ax.contourf(lons,lats,data,15)
    return fig

# if running with GUI backend, show plot.
if matplotlib.get_backend().lower() != 'agg':
    test_set_bitmap()
    plt.show()
