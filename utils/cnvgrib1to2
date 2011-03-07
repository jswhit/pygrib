#!/usr/bin/env python
import pygrib, sys

if len(sys.argv) < 3:
    sys.stdout.write("""
cnvgrib1to2 <grib1 filename> <grib2 filename> <packing scheme>
<packing_scheme> is optional - can be 'grid_simple', 'grid_complex',
'grid_complex_spatial_differencing', 'grid_jpeg', or 'grid_png'. 
Default is 'grid_jpeg'\n\n""")
    raise SystemExit
   
grbs = pygrib.open(sys.argv[1])
f = open(sys.argv[2],'wb')

if len(sys.argv) > 3:
   grb2packing = sys.argv[3]
else:
   grb2packing = 'grid_jpeg' # default is jpeg2000 

sys.stdout.write('converting %s from grib1 to grib2 (%s) with %s packing ...\n' % (sys.argv[1],sys.argv[2],grb2packing))

nmsg = 0
for grb in grbs:
    try:
        grb.editionNumber=2 
        grb.packingType = grb2packing
        nmsg = nmsg + 1
    except:
        sys.stdout.write('cannot convert message %s\n' % grb.messagenumber)
        continue
    f.write(grb.tostring())

sys.stdout.write('%s messges out of %s converted\n' % (nmsg,grbs.messages))
grbs.close()
f.close()
