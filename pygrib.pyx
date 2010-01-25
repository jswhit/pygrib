"""
Introduction
============

Python module for reading GRIB (editions 1 and 2) files
(U{download<http://code.google.com/p/pygrib/downloads/list>}). 
GRIB is the World Meterological Organization
U{standard<http://www.wmo.ch/pages/prog/www/WMOCodes/GRIB.html>} 
for distributing gridded data. 
The module is a python interface to the
U{GRIB_API<http://www.ecmwf.int/products/data/software/grib_api.html>} C library
from the European Centre for Medium-Range Weather Forecasts
(U{ECMWF<http://www.ecmwf.int}).

Required
========

- U{Python<http://python.org>} 2.4 or higher.  
- U{numpy<http://sourceforge.net/project/showfiles.php?group_id=1369>}
  N-dimensional array object for python. Version 1.2.1 or higher.
- U{pyproj<http://code.google.com/p/pyproj/>} Python interface to 
  U{PROJ.4<http://proj.maptools.org>} library for cartographic transformations.
- U{GRIB_API<http://www.ecmwf.int/products/data/software/grib_api.htm.>} C library
  for encoding and decoding GRIB messages (edition 1 and edition 2).
  To be fully functional, the GRIB_API library requires
  U{Jasper<http://www.ece.uvic.ca/~mdadams/jasper>} or 
  U{OpenJPEG<http://www.openjpeg.org>} for JPEG200 encoding,
  and U{PNG<http://www.libpng.org/pub/png/libpng.html>} for PNG encoding.

Installation
============

 - set the environment variables C{$GRIBAPI_DIR}, C{$JASPER_DIR}, C{$OPENJPEG_DIR},
 C{$PNG_DIR} and C{$ZLIB_DIR} so that the include files and libraries for
 GRIB_API, JASPER, OpenJPEG, PNG and zlib will be found.  
 For example, the include files for 
 jasper should be found in C{$JASPER_DIR/include}, and the jasper
 library should be found in C{$JASPER_DIR/lib}. If any of those environment 
 variables are not set, then the default search paths will be used.  If
 GRIB_API library was compiled without JASPER, PNG or OpenJPEG support, then the 
 corresponding environment variable need not be set.

 - Run 'python setup.py install', as root if necessary.


Example usage
=============

 - from the python interpreter prompt, import the package::
    >>> import pygrib
 - open a GRIB file, create an grib message iterator::
    >>> grbs = pygrib.open('sampledata/gfs.grb')  
 - print an inventory of the file::
    >>> for grb in grbs:
    >>>     print grb 
    1:HGT [gpm]:100000 Pa (Isobaric Surface):72 Hour Forecast initialized 2004120912:Latitude/longitude:Unperturbed high-resolution control forecast member 0 of 10
    2:HGT [gpm]:97500 Pa (Isobaric Surface):72 Hour Forecast initialized 2004120912:Latitude/longitude:Unperturbed high-resolution control forecast member 0 of 10
    3:HGT [gpm]:95000 Pa (Isobaric Surface):72 Hour Forecast initialized 2004120912:Latitude/longitude:Unperturbed high-resolution control forecast member 0 of 10
  
       .....

 - find the first grib message containing 500 hPa geopotential height:: 
    >>> z500 = [g for g in grbs if g.parameter=='HGT' and g.vertical_level=='50000 Pa' and g.vertical_level_descriptor=='Isobaric Surface'][0]
 - extract the 500 hPa height data::
    >>> z500data = z500.data()
    >>> print z500.shape, z500data.min(), z500data.max()
    (73, 144) 4834.89990234 5931.20019531
 - get the latitudes and longitudes of the grid::
    >>> lats, lons = z500.grid()
    >>> print lats.shape, lats.min(), lats.max(), lons.shape, lons.min(), lons.max()
    (73, 144) -90.0 90.0 (73, 144) 0.0 357.5
 - dump just this grib message to another file::
    >>> dump('gfs_z500.grb',[z500])
 - read that file back in and verify it's contents::
    >>> grbs = Grib2Decode('gfs_z500.grb')
    >>> for g in grbs:
    >>>    print g
    1:HGT [gpm]:50000 Pa (Isobaric Surface):72 Hour Forecast initialized 2004120912:Latitude/longitude:Unperturbed high-resolution control forecast member 0 of 10

Documentation
=============

 - see below for python API documentation.
  
Links
=====

 - U{ECMWF GRIP_API<http://www.ecmwf.int/products/data/software/grib2.html>}.
   This package is a python interface to the GRIB_API library.
 - U{WMO GRIB information<http://www.wmo.ch/pages/prog/www/WMOCodes/GRIB.html>}.
 - U{wgrib2<http://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/>}
 - U{NCEP GRIB2 C and FORTRAN libraries
   <http://www.nco.ncep.noaa.gov/pmb/codes/GRIB2/>}. 
 - U{MDL GRIB2 Decoder<http://weather.gov/mdl/iwt/grib2/decoder.htm>}
 - U{Cython<http://www.cython.org>}
 (used to create python interface to g2clib and proj4).
 - U{proj.4<http://trac.osgeo.org/proj>} (used to perform cartographic
 transformations).

Changelog
=========

 - B{20100201}: initial release. Read-only support nearly
   complete, but no support for writing.

@author: Jeffrey Whitaker.

@contact: U{Jeff Whitaker<mailto:jeffrey.s.whitaker@noaa.gov>}

@version: 20100201

@copyright: copyright 2010 by Jeffrey Whitaker.

@license: Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation.
THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO
EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
""" 
__version__ = '20100201'

import numpy as np
from numpy import ma
import pyproj
import warnings
import_array()

cdef extern from "stdlib.h":
    ctypedef long size_t
    void *malloc(size_t size)
    void free(void *ptr)

cdef extern from "stdio.h":
    ctypedef struct FILE
    FILE *fopen(char *path, char *mode)
    int	fclose(FILE *)

cdef extern from "Python.h":
    char * PyString_AsString(object)
    object PyString_FromString(char *s)

cdef extern from "numpy/arrayobject.h":
    ctypedef int npy_intp 
    ctypedef extern class numpy.ndarray [object PyArrayObject]:
        cdef char *data
        cdef int nd
        cdef npy_intp *dimensions
        cdef npy_intp *strides
        cdef object base
        cdef int flags
    npy_intp PyArray_SIZE(ndarray arr)
    npy_intp PyArray_ISCONTIGUOUS(ndarray arr)
    npy_intp PyArray_ISALIGNED(ndarray arr)
    void import_array()

cdef extern from "grib_api.h":
    ctypedef struct grib_handle
    ctypedef struct grib_keys_iterator
    ctypedef struct grib_context
    cdef enum:
        GRIB_TYPE_UNDEFINED
        GRIB_TYPE_LONG
        GRIB_TYPE_DOUBLE
        GRIB_TYPE_STRING
        GRIB_TYPE_BYTES 
        GRIB_TYPE_SECTION 
        GRIB_TYPE_LABEL 
        GRIB_TYPE_MISSING 
        GRIB_KEYS_ITERATOR_ALL_KEYS            
        GRIB_KEYS_ITERATOR_SKIP_READ_ONLY         
        GRIB_KEYS_ITERATOR_SKIP_OPTIONAL          
        GRIB_KEYS_ITERATOR_SKIP_EDITION_SPECIFIC  
        GRIB_KEYS_ITERATOR_SKIP_CODED             
        GRIB_KEYS_ITERATOR_SKIP_COMPUTED         
        GRIB_KEYS_ITERATOR_SKIP_FUNCTION         
        GRIB_KEYS_ITERATOR_SKIP_DUPLICATES       
    int grib_get_size(grib_handle *h, char *name, size_t *size)
    int grib_get_native_type(grib_handle *h, char *name, int *type)
    int grib_get_long(grib_handle *h, char *name, long *ival)
    int grib_get_long_array(grib_handle *h, char *name, long *ival, size_t *size)
    int grib_get_double(grib_handle *h, char *name, double *dval)
    int grib_get_double_array(grib_handle *h, char *name, double *dval, size_t *size)
    int grib_get_string(grib_handle *h, char *name, char *mesg, size_t *size)
    int grib_get_bytes(grib_handle* h, char* key, unsigned char*  bytes, size_t *length)
    grib_keys_iterator* grib_keys_iterator_new(grib_handle* h,unsigned long filter_flags, char* name_space)
    int grib_keys_iterator_next(grib_keys_iterator *kiter)
    char* grib_keys_iterator_get_name(grib_keys_iterator *kiter)
    int grib_handle_delete(grib_handle* h)
    grib_handle* grib_handle_new_from_file(grib_context* c, FILE* f, int* error)        
    char* grib_get_error_message(int code)
    int grib_keys_iterator_delete( grib_keys_iterator* kiter)


cdef class open(object):
    cdef FILE *_fd
    cdef grib_handle *_gh
    cdef public object filename, projparams, messagenumber
    def __new__(self, filename):
        cdef grib_handle *gh
        cdef FILE *_fd
        cdef int err
        self.filename = filename
        self._fd = fopen(filename, "rb") 
        if self._fd == NULL:
            raise IOError("could not open %s", filename)
        self._gh = NULL
        self.messagenumber = 0
    def __repr__(self):
        inventory =\
        repr(self.messagenumber)+':'+self['name']+':'+self['units']+' ('+self['stepType']+')'+\
        ':'+self['typeOfGrid']+':'+self['typeOfLevel']+':top level '+repr(self['topLevel'])+\
        ':bot level '+repr(self['bottomLevel'])+':fcst time '+repr(self['forecastTime'])+\
        ':valid '+repr(self['validityDate'])+repr(self['validityTime'])
        return inventory
    def __iter__(self):
        return self
    def __next__(self):
        cdef grib_handle* gh 
        cdef int err
        self._gh = grib_handle_new_from_file(NULL, self._fd, &err)
        self.messagenumber = self.messagenumber + 1
        if self._gh == NULL and not err:
            raise StopIteration
        if err:
            raise RuntimeError(grib_get_error_message(err))
        return self
    def keys(self):
        """
 return keys associated with a grib message (a dictionary-like object)
        """
        cdef grib_keys_iterator* gi
        cdef int err, type
        cdef char *name
        gi = grib_keys_iterator_new(self._gh,\
                GRIB_KEYS_ITERATOR_ALL_KEYS, NULL)
        keys = []
        while grib_keys_iterator_next(gi):
            name = grib_keys_iterator_get_name(gi)
            key = PyString_AsString(name)
            # skip these apparently bogus keys (grib_api 1.8.0)
            if key in\
            ['zero','one','eight','eleven','false','thousand','file','localDir','7777',
             'oneThousand']:
                continue
            err = grib_get_native_type(self._gh, name, &type)
            if err:
                raise RuntimeError(grib_get_error_message(err))
            # just skip unsupported types for now.
            if type not in\
            [GRIB_TYPE_SECTION,GRIB_TYPE_BYTES,GRIB_TYPE_LABEL,GRIB_TYPE_MISSING]:
                keys.append(key)
        err = grib_keys_iterator_delete(gi)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        return keys
    def __getitem__(self, key):
        """access values associated with grib keys"""
        cdef int err, type
        cdef size_t size
        cdef char *name
        cdef long longval
        cdef double doubleval
        cdef ndarray datarr
        cdef char strdata[1024]
        cdef unsigned char *chardata
        name = PyString_AsString(key)
        err = grib_get_size(self._gh, name, &size)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        #if key.startswith('grib 2 Section'):
        #    sectnum = key.split()[3]
        #    size = int(self['section'+sectnum+'Length'])
        err = grib_get_native_type(self._gh, name, &type)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        if type == GRIB_TYPE_UNDEFINED:
            return None
        elif type == GRIB_TYPE_LONG:
            if size == 1: # scalar
                err = grib_get_long(self._gh, name, &longval)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
                return longval
            else: # array
                if self.has_key('jPointsAreConsecutive') and\
                   self['jPointsAreConsecutive']:
                    storageorder='F'
                else:
                    storageorder='C'
                datarr = np.empty(size, np.int32, order=storageorder)
                err = grib_get_long_array(self._gh, name, <long *>datarr.data, &size)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
                if key == 'values':
                    return self._reshape_mask(datarr)
                else:
                    return datarr
        elif type == GRIB_TYPE_DOUBLE:
            if size == 1: # scalar
                err = grib_get_double(self._gh, name, &doubleval)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
                return doubleval
            else: # array
                if self.has_key('jPointsAreConsecutive') and\
                   self['jPointsAreConsecutive']:
                    storageorder='F'
                else:
                    storageorder='C'
                datarr = np.empty(size, np.double, order=storageorder)
                err = grib_get_double_array(self._gh, name, <double *>datarr.data, &size)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
                if key == 'values':
                    return self._reshape_mask(datarr)
                else:
                    return datarr
        elif type == GRIB_TYPE_STRING:
            size=1024 # grib_get_size returns 1 ?
            err = grib_get_string(self._gh, name, strdata, &size)
            if err:
                raise RuntimeError(grib_get_error_message(err))
            msg = PyString_FromString(strdata)
            return msg.rstrip()
        elif type == GRIB_TYPE_BYTES:
            msg="cannot read data (size %d) for keys '%s', GRIB_TYPE_BYTES decoding not supported" %\
            (size,name)
            warnings.warn(msg)
            return None
        elif type == GRIB_TYPE_SECTION:
            msg="cannot read data (size %d) for keys '%s', GRIB_TYPE_SECTION decoding not supported" %\
            (size,name)
            warnings.warn(msg)
            return None
        elif type == GRIB_TYPE_LABEL:
            msg="cannot read data (size %d) for keys '%s', GRIB_TYPE_LABEL decoding not supported" %\
            (size,name)
            warnings.warn(msg)
            return None
        elif type == GRIB_TYPE_MISSING:
            msg="cannot read data (size %d) for keys '%s', GRIB_TYPE_MISSING decoding not supported" %\
            (size,name)
            warnings.warn(msg)
            return None
        else:
            warnings.warn("unrecognized grib type % d" % type)
            return None
    def close(self):
        """deallocate C structures associated with class instance"""
        cdef int err
        fclose(self._fd)
        if self._gh != NULL:
            err = grib_handle_delete(self._gh)
            if err:
                raise RuntimeError(grib_get_error_message(err))
    def __dealloc__(self):
        """special method used by garbage collector"""
        self.close()
    def __reduce__(self):
        """special method that allows class instance to be pickled"""
        return (self.__class__,(self.filename,))
    def has_key(self,key):
        """
 tests whether a grib message object has a specified key.
        """
        return key in self.keys()
    def _reshape_mask(self, datarr):
        cdef double missval
        if self.has_key('Ni') and self.has_key('Nj'):
            nx = self['Ni']
            ny = self['Nj']
            if ny > 0 and nx > 0:
                datarr.shape = (ny,nx)
            if self.has_key('typeOfGrid') and self['typeOfGrid'].startswith('reduced'):
                if self.has_key('missingValue'):
                    missval = self['missingValue']
                else:
                    missval = 1.e30
                datarr = _redtoreg(2*ny, self['pl'], datarr, missval)
            # check scan modes for rect grids.
            if len(datarr.shape) == 2:
                # rows scan in the -x direction (so flip)
                if not self['jScansPositively']:
                    datsave = datarr.copy()
                    datarr[:,:] = datsave[::-1,:]
                # columns scan in the -y direction (so flip)
                if self['iScansNegatively']:
                    datsave = datarr.copy()
                    datarr[:,:] = datsave[:,::-1]
                # adjacent rows scan in opposite direction.
                # (flip every other row)
                if self['alternativeRowScanning']:
                    datsave = datarr.copy()
                    datarr[1::2,:] = datsave[1::2,::-1]
            if self.has_key('missingValue') and self['numberOfMissing']:
                #if (datarr == self['missingValue']).any():
                datarr = ma.masked_values(datarr, self['missingValue'])
        return datarr
    def latlons(self):
        """
 return lats,lons (in degrees) of grid.
 currently can handle reg. lat/lon, global gaussian, mercator, stereographic,
 lambert conformal, albers equal-area, space-view, azimuthal 
 equidistant, reduced gaussian, reduced lat/lon and
 lambert azimuthal equal-area grids.

 @return: C{B{lats},B{lons}}, numpy arrays 
 containing latitudes and longitudes of grid (in degrees).
        """
        projparams = {}

        if self.has_key('scaleFactorOfMajorAxisOfOblateSpheroidEarth'):
            scalea = self['scaleFactorOfMajorAxisOfOblateSpheroidEarth']
            scaleb = self['scaleFactorOfMinorAxisOfOblateSpheroidEarth']
            if scalea:
                scalea = 1000.*np.power(10,-scalea)
            else:
                scalea = 1
            if scaleb:
                scaleb = 1000.*np.power(10,-scaleb)
            else:
                scaleb = 1.
        else:
            scalea = 1.
            scaleb = 1.
        if self['shapeOfTheEarth'] == 6:
            projparams['a']=self['radius']
            projparams['b']=self['radius']
        elif self['shapeOfTheEarth'] in [3,7]:
            projparams['a']=self['scaledValueOfMajorAxisOfOblateSpheroidEarth']*scalea
            projparams['b']=self['scaledValueOfMinorAxisOfOblateSpheroidEarth']*scaleb
        elif self['shapeOfTheEarth'] == 2:
            projparams['a']=6378160.0
            projparams['b']=6356775.0 
        elif self['shapeOfTheEarth'] == 1:
            projparams['a']=self['scaledValueOfRadiusOfSphericalEarth']*scalea
            projparams['b']=self['scaledValueOfRadiusOfSphericalEarth']*scaleb
        elif self['shapeOfTheEarth'] == 0:
            projparams['a']=6367470.0
            projparams['b']=6367470.0
        elif self['shapeOfTheEarth'] == 0: # WGS84
            projparams['a']=6378137.0
            projparams['b']=6356752.3142
        elif self['shapeOfTheEarth'] == 8:
            projparams['a']=6371200.0
            projparams['b']=6371200.0
        else:
            raise ValueError('unknown shape of the earth flag')

        if self['typeOfGrid'] in ['regular_gg','regular_ll']: # regular lat/lon grid
            lons = self['distinctLongitudes']
            lats = self['distinctLatitudes']
            lons,lats = np.meshgrid(lons,lats) 
            projparams['proj']='cyl'
        elif self['typeOfGrid'].startswith('reduced'): # reduced lat/lon grid
            lats = self['distinctLatitudes']
            ny = self['Nj']
            nx = 2*ny
            delon = 360./nx
            lon1 = self['longitudeOfFirstGridPointInDegrees']
            lon2 = self['longitudeOfLastGridPointInDegrees']
            lons = np.arange(lon1,lon2+delon,delon)
            lons,lats = np.meshgrid(lons,lats) 
            projparams['proj']='cyl'
        elif self['typeOfGrid'] == 'polar_stereographic':
            lat1 = self['latitudeOfFirstGridPointInDegrees']
            lon1 = self['longitudeOfFirstGridPointInDegrees']
            nx = self['Ni']
            ny = self['Nj']
            dx = self['xDirectionGridLengthInMetres']
            dy = self['yDirectionGridLengthInMetres']
            projparams['proj']='stere'
            projparams['lat_ts']=self['latitudeWhereDxAndDyAreSpecifiedInDegrees']
            if self['projectionCentreFlag'] == 0:
                projparams['lat_0']=90.
            else:
                projparams['lat_0']=-90.
            projparams['lon_0']=self['orientationOfTheGridInDegrees']
            pj = pyproj.Proj(projparams)
            llcrnrx, llcrnry = pj(lon1,lat1)
            x = llcrnrx+dx*np.arange(nx)
            y = llcrnry+dy*np.arange(ny)
            x, y = np.meshgrid(x, y)
            lons, lats = pj(x, y, inverse=True)
        elif self['typeOfGrid'] == 'lambert':
            lat1 = self['latitudeOfFirstGridPointInDegrees']
            lon1 = self['longitudeOfFirstGridPointInDegrees']
            nx = self['Ni']
            ny = self['Nj']
            dx = self['DxInMetres']
            dy = self['DyInMetres']
            projparams['proj']='lcc'
            projparams['lon_0']=self['LoVInDegrees']
            projparams['lat_0']=self['LaDInDegrees']
            projparams['lat_1']=self['Latin1InDegrees']
            projparams['lat_2']=self['Latin2InDegrees']
            pj = pyproj.Proj(projparams)
            llcrnrx, llcrnry = pj(lon1,lat1)
            x = llcrnrx+dx*np.arange(nx)
            y = llcrnry+dy*np.arange(ny)
            x, y = np.meshgrid(x, y)
            lons, lats = pj(x, y, inverse=True)
        elif self['typeOfGrid'] =='albers':
            lat1 = self['latitudeOfFirstGridPointInDegrees']
            lon1 = self['longitudeOfFirstGridPointInDegrees']
            nx = self['Ni']
            ny = self['Nj']
            dx = self['Dx']/1000.
            dy = self['Dy']/1000.
            projparams['proj']='aea'
            scale = float(self['grib2divider'])
            projparams['lon_0']=self['LoV']/scale
            if self['truncateDegrees']:
                projparams['lon_0'] = int(projparams['lon_0'])
            projparams['lat_0']=self['LaD']/scale
            if self['truncateDegrees']:
                projparams['lat_0'] = int(projparams['lat_0'])
            projparams['lat_1']=self['Latin1']/scale
            if self['truncateDegrees']:
                projparams['lat_1'] = int(projparams['lat_1'])
            projparams['lat_2']=self['Latin2']/scale
            if self['truncateDegrees']:
                projparams['lat_2'] = int(projparams['lat_2'])
            pj = pyproj.Proj(projparams)
            llcrnrx, llcrnry = pj(lon1,lat1)
            x = llcrnrx+dx*np.arange(nx)
            y = llcrnry+dy*np.arange(ny)
            x, y = np.meshgrid(x, y)
            lons, lats = pj(x, y, inverse=True)
        elif self['typeOfGrid'] == 'space_view':
            nx = self['Ni']
            ny = self['Nj']
            projparams['lon_0']=self['longitudeOfSubSatellitePointInDegrees']
            projparams['lat_0']=self['latitudeOfSubSatellitePointInDegrees']
            if projparams['lat_0'] == 0.: # if lat_0 is equator, it's a
                projparams['proj'] = 'geos'
            # general case of 'near-side perspective projection' (untested)
            else:
                projparams['proj'] = 'nsper'
                msg = """
only geostationary perspective is fully supported.
lat/lon values returned by grid method may be incorrect."""
                warnings.warn(msg)
            scale = float(self['grib2divider'])
            projparams['h'] = projparams['a'] *\
            self['altitudeOfTheCameraFromTheEarthSCenterMeasuredInUnitsOfTheEarth']/scale
            # latitude of horizon on central meridian
            lonmax =\
            90.-(180./np.pi)*np.arcsin(projparams['a']/projparams['h'])
            # longitude of horizon on equator
            latmax =\
            90.-(180./np.pi)*np.arcsin(projparams['b']/projparams['h'])
            # h is measured from surface of earth at equator.
            projparams['h'] = projparams['h']-projparams['a']
            # truncate to nearest thousandth of a degree (to make sure
            # they aren't slightly over the horizon)
            latmax = int(1000*latmax)/1000.
            lonmax = int(1000*lonmax)/1000.
            pj = pyproj.Proj(projparams)
            x1,y1 = pj(0.,latmax); x2,y2 = pj(lonmax,0.)
            width = 2*x2; height = 2*y1
            dx =\
            width/self['apparentDiameterOfEarthInGridLengthsInXDirection']
            dy =\
            height/self['apparentDiameterOfEarthInGridLengthsInYDirection']
            x = dx*np.indices((ny,nx),'f')[1,:,:]
            x = x - 0.5*x.max()
            y = dy*np.indices((ny,nx),'f')[0,:,:]
            y = y - 0.5*y.max()
            lons, lats = pj(x,y,inverse=True)
            # set lons,lats to 1.e30 where undefined
            abslons = np.fabs(lons); abslats = np.fabs(lats)
            lons = np.where(abslons < 1.e20, lons, 1.e30)
            lats = np.where(abslats < 1.e20, lats, 1.e30)
        elif self['typeOfGrid'] == "equatorial_azimuthal_equidistant":
            projparams['lat_0'] = self['standardParallel']/1.e6
            projparams['lon_0'] = self['centralLongitude']/1.e6
            dx = self['Dx']/1.e3
            dy = self['Dy']/1.e3
            projparams['proj'] = 'aeqd'
            lat1 = self['latitudeOfFirstGridPointInDegrees']
            lon1 = self['longitudeOfFirstGridPointInDegrees']
            pj = pyproj.Proj(projparams)
            llcrnrx, llcrnry = pj(lon1,lat1)
            x = llcrnrx+dx*np.arange(nx)
            y = llcrnry+dy*np.arange(ny)
            x, y = np.meshgrid(x, y)
            lons, lats = pj(x, y, inverse=True)
        elif self['typeOfGrid'] == "lambert_azimuthal_equal_area":
            projparams['lat_0'] = self['standardParallel']/1.e6
            projparams['lon_0'] = self['centralLongitude']/1.e6
            dx = self['Dx']/1.e3
            dy = self['Dy']/1.e3
            projparams['proj'] = 'laea'
            lat1 = self['latitudeOfFirstGridPointInDegrees']
            lon1 = self['longitudeOfFirstGridPointInDegrees']
            pj = pyproj.Proj(projparams)
            llcrnrx, llcrnry = pj(lon1,lat1)
            x = llcrnrx+dx*np.arange(nx)
            y = llcrnry+dy*np.arange(ny)
            x, y = np.meshgrid(x, y)
            lons, lats = pj(x, y, inverse=True)
        elif self['typeOfGrid'] == 'mercator':
            scale = float(self['grib2divider'])
            lat1 = self['latitudeOfFirstGridPoint']/scale
            if self['truncateDegrees']:
                lat1 = int(lat1)
            lon1 = self['longitudeOfFirstGridPoint']/scale
            if self['truncateDegrees']:
                lon1 = int(lon1)
            lat2 = self['latitudeOfLastGridPoint']/scale
            if self['truncateDegrees']:
                lat2 = int(lat2)
            lon2 = self['longitudeOfLastGridPoint']/scale
            if self['truncateDegrees']:
                lon2 = int(lon2)
            projparams['lat_ts']=self['latitudeSAtWhichTheMercatorProjectionIntersectsTheEarth']/scale
            projparams['lon_0']=0.5*(lon1+lon2)
            projparams['proj']='merc'
            pj = pyproj.Proj(projparams)
            llcrnrx, llcrnry = pj(lon1,lat1)
            urcrnrx, urcrnry = pj(lon2,lat2)
            nx = self['Ni']
            ny = self['Nj']
            dx = (urcrnrx-llcrnrx)/(nx-1)
            dy = (urcrnry-llcrnry)/(ny-1)
            x = llcrnrx+dx*np.arange(nx)
            y = llcrnry+dy*np.arange(ny)
            x, y = np.meshgrid(x, y)
            lons, lats = pj(x, y, inverse=True)
        else:
            raise ValueError('unsupported grid')
        self.projparams = projparams
        return lats, lons

cdef _redtoreg(int nlons, ndarray lonsperlat, ndarray redgrid, double missval):
# convert data on global reduced gaussian to global
# full gaussian grid using linear interpolation.
    cdef long i, j, n, im, ip, indx, ilons, nlats, npts
    cdef double zxi, zdx, flons
    cdef ndarray reggrid
    cdef double *redgrdptr, *reggrdptr
    cdef long *lonsptr
    nlats = len(lonsperlat)
    npts = len(redgrid)
    reggrid = missval*np.ones((nlats,nlons),np.double)
    # get data buffers and cast to desired type.
    lonsptr = <long *>lonsperlat.data
    redgrdptr = <double *>redgrid.data
    reggrdptr = <double *>reggrid.data
    # iterate over full grid, do linear interpolation.
    n = 0
    indx = 0
    for j from 0 <= j < nlats:
        ilons = lonsptr[j]
        flons = <double>ilons
        for i from 0 <= i < nlons:
            # zxi is the grid index (relative to the reduced grid)
            # of the i'th point on the full grid. 
            zxi = i * flons / nlons # goes from 0 to ilons
            im = <long>zxi
            zdx = zxi - <double>im
            if ilons != 0:
                im = (im + ilons)%ilons
                ip = (im + 1 + ilons)%ilons
                # if one of the nearest values is missing, use nearest
                # neighbor interpolation.
                if redgrdptr[indx+im] == missval or\
                   redgrdptr[indx+ip] == missval: 
                    if zdx < 0.5:
                        reggrdptr[n] = redgrdptr[indx+im]
                    else:
                        reggrdptr[n] = redgrdptr[indx+ip]
                else: # linear interpolation.
                    reggrdptr[n] = redgrdptr[indx+im]*(1.-zdx) +\
                                   redgrdptr[indx+ip]*zdx
            n = n + 1
        indx = indx + ilons
    return reggrid
