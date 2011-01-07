"""
Introduction
============

Python module for reading and writing GRIB (editions 1 and 2) files.
GRIB is the World Meterological Organization
U{standard<http://www.wmo.ch/pages/prog/www/WMOCodes/GRIB.html>} 
for distributing gridded data. 
The module is a python interface to the
U{GRIB API<http://www.ecmwf.int/products/data/software/grib_api.html>} C library
from the European Centre for Medium-Range Weather Forecasts
(U{ECMWF<http://www.ecmwf.int>}).

Required
========

- U{Python<http://python.org>} 2.4 or higher.
- U{numpy<http://sourceforge.net/project/showfiles.php?group_id=1369>}
  N-dimensional array object for python. Version 1.2.1 or higher.
- U{pyproj<http://code.google.com/p/pyproj/>} Python interface to 
  U{PROJ.4<http://trac.osgeo.org/proj>} library for cartographic
  transformations B{or} U{matplotlib<http://matplotlib.sf.net>} and
  the U{basemap<http://matplotlib.sf.net/basemap/doc/html>} toolkit.
  
- U{GRIB API<http://www.ecmwf.int/products/data/software/grib_api.html>} C library
  for encoding and decoding GRIB messages (edition 1 and edition 2).
  Version 1.8.0 or higher required.
  To be fully functional, the GRIB API library requires
  U{Jasper<http://www.ece.uvic.ca/~mdadams/jasper>} or 
  U{OpenJPEG<http://www.openjpeg.org>} for JPEG200 encoding,
  and U{PNG<http://www.libpng.org/pub/png/libpng.html>} for PNG encoding.

Installation
============

 - U{Download<http://code.google.com/p/pygrib/downloads/list>} the source code. 
 - set the environment variables C{$GRIBAPI_DIR}, C{$JASPER_DIR}, C{$OPENJPEG_DIR},
 C{$PNG_DIR} and C{$ZLIB_DIR} so that the include files and libraries for
 GRIB API, Jasper, OpenJPEG, PNG and zlib will be found.  
 For example, the include files for 
 jasper should be found in C{$JASPER_DIR/include} or
 C{$JASPER_DIR/include/jasper}, and the jasper
 library should be found in C{$JASPER_DIR/lib} or C{$JASPER_DIR/lib64}. If any of
 those environment variables are not set, then the default search paths will be used.  
 If the GRIB API library was compiled without JASPER, PNG or OpenJPEG support, then the 
 corresponding environment variable need not be set. If the libraries and
 include files are installed in separate locations, the environment variables
 C{$GRIBAPI_INCDIR} and C{$GRIBAPI_LIBDIR} can be used to define the locations
 separately (same goes for C{JASPER}, C{OPENJPEG}, C{PNG} and C{ZLIB}).
 - Run 'python setup.py build' and then 'python setup.py install', as root if necessary.
 - Run 'python test.py' to test your installation.
 - Look at examples in C{test} directory (most require 
 U{matplotlib<http://matplotlib.sf.net>} and
 U{basemap<http://matplotlib.sourceforge.net/basemap/doc/html/>}).


Example usage
=============

 - from the python interpreter prompt, import the package::
    >>> import pygrib
 - open a GRIB file, create a grib message iterator::
    >>> grbs = pygrib.open('sampledata/flux.grb')  
 - pygrib open instances behave like regular python file objects, with
 C{seek}, C{tell}, C{read}, C{readline} and C{close} methods, except that offsets
 are measured in grib messages instead of bytes::
    >>> grbs.seek(2)
    >>> grbs.tell()
    2
    >>> grb = grbs.read(1)[0] # read returns a list with the next N (N=1 in this case) messages.
    >>> print grb # printing a grib message object displays summary info
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200
    >>> grbs.tell()
    3
 - print an inventory of the file::
    >>> grbs.seek(0)
    >>> for grb in grbs:
    >>>     print grb 
    1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120:from 200402291200
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120:from 200402291200
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2 m:fcst time 108-120:from 200402291200
 - find the first grib message with a matching name::
    >>> grb = grbs.select(name='Maximum temperature')[0]
 - extract the data values using the 'values' key
 (grb.keys() will return a list of the available keys)::
    # The data is returned as a numpy array, or if missing values or a bitmap
    # are present, a numpy masked array.  Reduced lat/lon or gaussian grid
    # data is automatically expanded to a regular grid. Details of the internal
    # representation of the grib data (such as the scanning mode) are handled
    # automatically.
    >>> maxt = grb.values # same as grb['values']
    >>> print maxt.shape, maxt.min(), maxt.max()
    (94, 192) 223.7 319.9
 - get the latitudes and longitudes of the grid::
    >>> lats, lons = grb.latlons()
    >>> print lats.shape, lats.min(), lats.max(), lons.shape, lons.min(), lons.max()
    (94, 192) -88.5419501373 88.5419501373  0.0 358.125
 - get the second grib message::
    >>> grb = grbs.message(2) # same as grbs.seek(1); grb=grbs.read(1)[0], or grb=grbs[2]
    >>> print grb
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120:from 200402291200
 - modify the values associated with existing keys (either via attribute or
 dictionary access)::
    >>> grb['forecastTime'] = 240
    >>> grb.dataDate = 20100101
 - get the binary string associated with the coded message::
    >>> msg = grb.tostring()
    >>> grbs.close() # close the grib file.
 - write the modified message to a new GRIB file::
    >>> grbout = open('test.grb','wb')
    >>> grbout.write(msg)
    >>> grbout.close()
    >>> print pygrib.open('test.grb').readline() 
    1:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 240:from 201001011200

Documentation
=============

 - see below for the full python API documentation.
  
Changelog
=========

 - see U{Changelog<http://pygrib.googlecode.com/svn/trunk/Changelog>} file.

@author: Jeffrey Whitaker.

@contact: U{Jeff Whitaker<mailto:jeffrey.s.whitaker@noaa.gov>}

@version: 1.8.1

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
PERFORMANCE OF THIS SOFTWARE."""
__test__ = None
del __test__ # hack so epydoc doesn't show __test__
__version__ = '1.8.1'

import numpy as np
from numpy import ma
try:
    import pyproj
except ImportError:
    try:
        from mpl_toolkits.basemap import pyproj
    except:
        raise ImportError("either pyproj or basemap required")
import_array()

cdef extern from "stdlib.h":
    ctypedef long size_t
    void *malloc(size_t size)
    void free(void *ptr)

cdef extern from "stdio.h":
    ctypedef struct FILE
    FILE *fopen(char *path, char *mode)
    int	fclose(FILE *)
    size_t fwrite(void *ptr, size_t size, size_t nitems, FILE *stream)
    void rewind (FILE *)

cdef extern from "Python.h":
    char * PyString_AsString(object)
    object PyString_FromString(char *s)
    object PyString_FromStringAndSize(char *s, size_t size)

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
    ctypedef struct grib_index
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
        GRIB_MISSING_LONG 
        GRIB_MISSING_DOUBLE
    int grib_get_size(grib_handle *h, char *name, size_t *size)
    int grib_get_native_type(grib_handle *h, char *name, int *type)
    int grib_get_long(grib_handle *h, char *name, long *ival)
    int grib_set_long(grib_handle *h, char *name, long val)
    int grib_get_long_array(grib_handle *h, char *name, long *ival, size_t *size)
    int grib_set_long_array(grib_handle *h, char *name, long *ival, size_t size)
    int grib_get_double(grib_handle *h, char *name, double *dval)
    int grib_set_double(grib_handle *h, char *name, double dval)
    int grib_get_double_array(grib_handle *h, char *name, double *dval, size_t *size)
    int grib_set_double_array(grib_handle *h, char *name, double *dval, size_t size)
    int grib_get_string(grib_handle *h, char *name, char *mesg, size_t *size)
    int grib_set_string(grib_handle *h, char *name, char *mesg, size_t *size)
    grib_keys_iterator* grib_keys_iterator_new(grib_handle* h,unsigned long filter_flags, char* name_space)
    int grib_keys_iterator_next(grib_keys_iterator *kiter)
    char* grib_keys_iterator_get_name(grib_keys_iterator *kiter)
    int grib_handle_delete(grib_handle* h)
    grib_handle* grib_handle_new_from_file(grib_context* c, FILE* f, int* error)        
    char* grib_get_error_message(int code)
    int grib_keys_iterator_delete( grib_keys_iterator* kiter)
    void grib_multi_support_on(grib_context* c)
    void grib_multi_support_off(grib_context* c)
    int grib_get_message(grib_handle* h ,  void** message,size_t *message_length)
    int grib_get_message_copy(grib_handle* h ,  void* message,size_t *message_length)
    long grib_get_api_version()
    int grib_count_in_file(grib_context* c, FILE* f,int* n)
    grib_handle* grib_handle_clone(grib_handle* h)
    grib_index* grib_index_new_from_file(grib_context* c,\
                            char* filename,char* keys,int *err)
    int grib_index_get_size(grib_index* index,char* key,size_t* size)
    int grib_index_get_long(grib_index* index,char* key,\
                        long* values,size_t *size)
    int grib_index_get_double(grib_index* index,char* key,\
                              double* values,size_t *size)
    int grib_index_get_string(grib_index* index,char* key,\
                          char** values,size_t *size)
    int grib_index_select_long(grib_index* index,char* key,long value)
    int grib_index_select_double(grib_index* index,char* key,double value)
    int grib_index_select_string(grib_index* index,char* key,char* value)
    grib_handle* grib_handle_new_from_index(grib_index* index,int *err)
    void grib_index_delete(grib_index* index)
    int grib_is_missing(grib_handle* h, char* key, int* err)
    grib_handle* grib_handle_new_from_message(grib_context * c, void * data,\
                             size_t data_len)
    # new in 1.9.0
    #grib_index* grib_index_new(grib_context* c, char* keys,int *err)
    #int grib_index_add_file(grib_index *index, const char *filename)
    #int grib_index_write(grib_index *index, char *filename)
    #grib_index* grib_index_read(grib_context* c, char* filename,int *err)


missingvalue_int = GRIB_MISSING_LONG
#this doesn't work, since defined constants are assumed to be integers
#missingvalue_float = GRIB_MISSING_DOUBLE
missingvalue_float = -1.e100 # value given in grib_api.h version 1.90
grib_api_version = grib_get_api_version()

cdef class open(object):
    """ 
    open(filename)
    
    returns GRIB file iterator object given GRIB filename. When iterated, returns
    instances of the L{gribmessage} class. Behaves much like a python file
    object, with L{seek}, L{tell}, L{read} and L{close} methods, 
    except that offsets are measured in grib messages instead of bytes.
    Additional methods include L{rewind} (like C{seek(0)}), L{message}
    (like C{seek(N-1)}; followed by C{read(1)}), and L{select} (filters
    messages based on specified conditions).  The C{__call__} method forwards
    to L{select}, and instances can be sliced with C{__getitem__} (returning
    lists of L{gribmessage} instances).  The position of the iterator is not
    altered by slicing with C{__getitem__}.
     
    @ivar messages: The total number of grib messages in the file.

    @ivar messagenumber: The grib message number that the iterator currently
    points to (the value returned by L{tell}).

    @ivar name: The GRIB file which the instance represents."""
    cdef FILE *_fd
    cdef grib_handle *_gh
    cdef public object name, messagenumber, messages, closed
    def __cinit__(self, filename):
        # initialize C level objects.
        cdef grib_handle *gh
        cdef FILE *_fd
        self._fd = fopen(filename, "rb") 
        if self._fd == NULL:
            raise IOError("could not open %s", filename)
        self._gh = NULL
    def __init__(self, filename):
        cdef int err,nmsgs
        # initalize Python level objects
        self.name = filename
        self.closed = False
        self.messagenumber = 0
        # turn on support for multi-field grib messages.
        grib_multi_support_on(NULL)
        # count number of messages in file.
        err = grib_count_in_file(NULL, self._fd, &nmsgs)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        self.messages = nmsgs 
    def __iter__(self):
        return self
    def __next__(self):
        cdef grib_handle* gh 
        cdef int err
        if self.messagenumber == self.messages:
            raise StopIteration
        if self._gh is not NULL:
            err = grib_handle_delete(self._gh)
            if err:
                raise RuntimeError(grib_get_error_message(err))
        gh = grib_handle_new_from_file(NULL, self._fd, &err)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        if gh == NULL:
            raise StopIteration
        else:
            self._gh = gh
            self.messagenumber = self.messagenumber + 1
        return _create_gribmessage(self._gh, self.messagenumber)
    def __getitem__(self, key):
        if type(key) == slice:
            # for a slice, return a list of grib messages.
            beg, end, inc = key.indices(self.messages)
            msg = self.tell()
            grbs = [self.message(n+1) for n in xrange(beg,end,inc)]
            self.seek(msg) # put iterator back in original position
            return grbs
        elif type(key) == int or type(key) == long:
            # for an integer, return a single grib message.
            msg = self.tell()
            grb = self.message(key)
            self.seek(msg) # put iterator back in original position
            return grb
        else:
            raise KeyError('key must be an integer message number or a slice')
    def __call__(self, **kwargs):
        """same as L{select}"""
        return self.select(**kwargs)
    def tell(self):
        """returns position of iterator (grib message number, 0 means iterator
        is positioned at beginning of file)."""
        return self.messagenumber
    def seek(self, msg, from_what=0):
        """
        seek(N,from_what=0)
        
        advance iterator N grib messages from beginning of file 
        (if C{from_what=0}), from current position (if C{from_what=1})
        or from the end of file (if C{from_what=2})."""
        if from_what not in [0,1,2]:
            raise ValueError('from_what keyword arg to seek must be 0,1 or 2')
        if msg == 0:
            if from_what == 0:
                self.rewind()
            elif from_what == 1:
                return
            elif from_what == 2:
                self.message(self.messages)
        else:
            if from_what == 0:
                self.message(msg)
            elif from_what == 1:
                self._advance(msg)
            elif from_what == 2:
                self.message(self.messages+msg)
    def readline(self):
        """
        readline()

        read one entire grib message from the file.
        Returns a L{gribmessage} instance, or None if an EOF is encountered."""
        try:
            grb = self.next()
        except StopIteration:
            grb = None
        return grb
    def read(self,msgs=None):
        """
        read(N=None)
        
        read N messages from current position, returning grib messages instances in a
        list.  If N=None, all the messages to the end of the file are read.
        C{pygrib.open(f).read()} is equivalent to C{list(pygrib.open(f))},
        both return a list containing L{gribmessage} instances for all the
        grib messages in the file C{f}.
        """
        if msgs is None:
            grbs = self._advance(self.messages-self.messagenumber,return_msgs=True)
        else:
            grbs = self._advance(msgs,return_msgs=True)
        return grbs
    def close(self):
        """
        close()

        close GRIB file, deallocate C structures associated with class instance"""
        # doesn't have __dealloc__, user must explicitly call close.
        # having both causes segfaults.
        cdef int err
        fclose(self._fd)
        if self._gh != NULL:
            err = grib_handle_delete(self._gh)
            if err:
                raise RuntimeError(grib_get_error_message(err))
        self.closed = True
    def rewind(self):
        """rewind iterator (same as seek(0))"""
        cdef grib_handle* gh 
        cdef int err
        rewind(self._fd)
        self._gh = NULL
        self.messagenumber = 0
    def message(self, N):
        """
        message(N)
        
        retrieve N'th message in iterator.
        same as seek(N-1) followed by read(1)."""
        cdef int err
        if N < 1:
            raise IOError('grb message numbers start at 1')
        if self.messagenumber >= N:
            self.rewind()
        # advance iterator by N messages.
        self._advance(N)
        return _create_gribmessage(self._gh, self.messagenumber)
    def select(self, **kwargs):
        """
select(**kwargs)

return a list of L{gribmessage} instances from iterator filtered by kwargs.
If keyword is a container object, each grib message
in the iterator is searched for membership in the container.
If keyword is a callable (has a _call__ method), each grib
message in the iterator is tested using the callable (which should
return a boolean).
If keyword is not a container object or a callable, each 
grib message in the iterator is tested for equality.

Example usage:

>>> import pygrib
>>> grbs = pygrib.open('sampledata/gfs.grb')
>>> selected_grbs=grbs.select(shortName='gh',typeOfLevel='isobaricInhPa',level=10)
>>> for grb in selected_grbs: print grb
26:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 10 Pa:fcst time 72:from 200412091200:lo res cntl fcst
>>> # the __call__ method does the same thing
>>> selected_grbs=grbs(shortName='gh',typeOfLevel='isobaricInhPa',level=10)
>>> for grb in selected_grbs: print grb
26:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 10 Pa:fcst time 72:from 200412091200:lo res cntl fcst
>>> # to select multiple specific key values, use containers (e.g. sequences)
>>> selected_grbs=grbs(shortName=['u','v'],typeOfLevel='isobaricInhPa',level=[10,50])
>>> for grb in selected_grbs: print grb
193:u-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 50 Pa:fcst time 72:from 200412091200:lo res cntl fcst
194:v-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 50 Pa:fcst time 72:from 200412091200:lo res cntl fcst
199:u-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 10 Pa:fcst time 72:from 200412091200:lo res cntl fcst
200:v-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 10 Pa:fcst time 72:from 200412091200:lo res cntl fcst
>>> # to select key values based on a conditional expression, use a function
>>> selected_grbs=grbs(shortName='gh',level=lambda l: l < 500 and l >= 300)
>>> for grb in selected_grbs: print grb
14:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 45000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
15:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 40000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
16:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 35000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
17:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 30000 Pa:fcst time 72:from 200412091200:lo res cntl fcst
"""
        self.rewind()
        grbs = [grb for grb in self if _find(grb, **kwargs)]
        return grbs
    def _advance(self,nmsgs,return_msgs=False):
        """advance iterator n messages from current position.
        if return_msgs==True, grib message instances are returned
        in a list"""
        if return_msgs: grbs=[]
        for n in range(self.messagenumber,self.messagenumber+nmsgs):
            err = grib_handle_delete(self._gh)
            if err:
                raise RuntimeError(grib_get_error_message(err))
            self._gh = grib_handle_new_from_file(NULL, self._fd, &err)
            if err:
                raise RuntimeError(grib_get_error_message(err))
            if self._gh == NULL:
                raise IOError('not that many messages in file')
            self.messagenumber = self.messagenumber + 1
            if return_msgs: grbs.append(_create_gribmessage(self._gh, self.messagenumber))
        if return_msgs: return grbs

# keep track of python gribmessage attributes so they can be
# distinguished from grib keys.
_private_atts =\
['_gh','expand_reduced','projparams','messagenumber','_all_keys','_ro_keys']

cdef _create_gribmessage(grib_handle *gh, object messagenumber):
    """factory function for creating gribmessage instances"""
    cdef gribmessage grb  = gribmessage.__new__(gribmessage)
    grb.messagenumber = messagenumber
    grb.expand_reduced = True
    grb._gh = grib_handle_clone(gh)
    grb._all_keys = grb.keys()
    grb._ro_keys  = grb._read_only_keys()
    return grb

def fromstring(gribstring):
    """
    fromstring(string)

    Create a gribmessage instance from a python string 
    representing a binary grib message (the reverse of L{gribmessage.tostring}).
    """
    cdef char* gribstr
    gribstr = PyString_AsString(gribstring)
    gh = grib_handle_new_from_message(NULL, <void *>gribstr, len(gribstring))
    return _create_gribmessage(gh, 1)

cdef class gribmessage(object):
    """
    Grib message object.

    @ivar messagenumber: The grib message number in the file.

    @ivar projparams: A dictionary containing proj4 key/value pairs describing 
    the grid.  Created when the L{latlons} method is invoked.

    @ivar expand_reduced:  If True (default), reduced lat/lon and gaussian grids
    will be expanded to regular grids when data is accessed via "values" key. If
    False, data is kept on unstructured reduced grid, and is returned in a 1-d
    array."""
    cdef grib_handle *_gh
    cdef public messagenumber, projparams,\
    expand_reduced, _ro_keys, _all_keys
    def __init__(self):
        # calling "__new__()" will not call "__init__()" !
        raise TypeError("This class cannot be instantiated from Python")
    def __dealloc__(self):
        # finalization (inverse of __cinit__): needed to allow garbage collector to free memory.
        cdef int err
        err = grib_handle_delete(self._gh)
    def __getattr__(self, item):
        # allow gribmessage keys to accessed like attributes.
        # this is tried after looking for item in self.__dict__.keys().
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)
    def __setattr__(self, name, value):
        # allow gribmessage keys to be set like attributes.
        if name not in _private_atts:
            # these are grib message keys
            self[name] = value
        else:
            # these are python attributes.
            self.__dict__[name]=value
    def __repr__(self):
        """prints a short inventory of the grib message"""
        inventory = []
        if self.valid_key('name'):
            inventory.append(repr(self.messagenumber)+':'+self['name'])
        if self.valid_key('units'):
            inventory.append(':'+self['units'])
        if self.valid_key('stepType'):
            inventory.append(' ('+self['stepType']+')')
        if self.valid_key('typeOfGrid') or self.valid_key('gridType'):
            if self.valid_key('typeOfGrid'):
               inventory.append(':'+self['typeOfGrid'])
            else:
               inventory.append(':'+self['gridType'])
        if self.valid_key('typeOfLevel'):
            inventory.append(':'+self['typeOfLevel'])
        if self.valid_key('topLevel') and self.valid_key('bottomLevel'):
            toplev = None; botlev = None
            levunits = 'unknown'
            if self.valid_key('unitsOfFirstFixedSurface'):
                levunits = self['unitsOfFirstFixedSurface']
            if self.valid_key('typeOfFirstFixedSurface') and self['typeOfFirstFixedSurface'] != 255:
                toplev = self['topLevel']
                if self.valid_key('scaledValueOfFirstFixedSurface') and\
                   self.valid_key('scaleFactorOfFirstFixedSurface'):
                   if self['scaleFactorOfFirstFixedSurface']:
                       toplev = self['scaledValueOfFirstFixedSurface']/\
                                np.power(10.0,self['scaleFactorOfFirstFixedSurface'])
                   else:
                       toplev = self['scaledValueOfFirstFixedSurface']
            if self.valid_key('typeOfSecondFixedSurface') and self['typeOfSecondFixedSurface'] != 255:
                botlev = self['bottomLevel']
                if self.valid_key('scaledValueOfSecondFixedSurface') and\
                   self.valid_key('scaleFactorOfSecondFixedSurface'):
                   if self['scaleFactorOfSecondFixedSurface']:
                       botlev = self['scaledValueOfSecondFixedSurface']/\
                                np.power(10.0,self['scaleFactorOfSecondFixedSurface'])
                   else:
                       botlev = self['scaledValueOfSecondFixedSurface']
            levstring = None
            if botlev is None or toplev == botlev:
                levstring = ':level %s' % toplev
            else:
                levstring = ':levels %s-%s' % (toplev,botlev)
            if levunits != 'unknown':
                levstring = levstring+' %s' % levunits
            if levstring is not None:
                inventory.append(levstring)
        elif self.valid_key('level'):
            inventory.append(':level %s' % self['level'])
        if self.valid_key('stepRange'):
            ftime = self['stepRange']
            inventory.append(':fcst time '+ftime)
        elif self.valid_key('forecastTime'):
            ftime = repr(self['forecastTime'])
            inventory.append(':fcst time '+ftime)
        if self.valid_key('dataDate') and self.valid_key('dataTime'):
            inventory.append(
            ':from '+repr(self['dataDate'])+'%04i' % self['dataTime'])
        #if self.valid_key('validityDate') and self.valid_key('validityTime'):
        #    inventory.append(
        #    ':valid '+repr(self['validityDate'])+repr(self['validityTime']))
        if self.valid_key('perturbationNumber') and\
           self.valid_key('typeOfEnsembleForecast'):
            ens_type = self['typeOfEnsembleForecast']
            pert_num = self['perturbationNumber']
            if ens_type == 0:
               inventory.append(":lo res cntl fcst")
            elif ens_type == 1:
               inventory.append(":hi res cntl fcst")
            elif ens_type == 2:
               inventory.append(":neg ens pert %d" % pert_num)
            elif ens_type == 3:
               inventory.append(":pos ens pert %d" % pert_num)
        if self.valid_key('derivedForecast'):
            if self['derivedForecast'] == 0:
                inventory.append(":ens mean")
            elif self['derivedForecast'] == 1:
                inventory.append(":weighted ens mean")
            elif self['derivedForecast'] == 2:
                inventory.append(":ens std dev")
            elif self['derivedForecast'] == 3:
                inventory.append(":normalized ens std dev")
            elif self['derivedForecast'] == 4:
                inventory.append(":ens spread")
            elif self['derivedForecast'] == 5:
                inventory.append(":ens large anomaly index")
            elif self['derivedForecast'] == 6:
                inventory.append(":ens mean of cluster")
        if self.valid_key('probabilityTypeName'):
            inventory.append(":"+self['probabilityTypeName'])
            lowerlim = None
            if self.valid_key('scaledValueOfLowerLimit') and\
               self.valid_key('scaleFactorOfLowerLimit'):
               if self['scaledValueOfLowerLimit'] and\
                  self['scaleFactorOfLowerLimit']: 
                   lowerlim = self['scaledValueOfLowerLimit']/\
                              np.power(10.0,self['scaleFactorOfLowerLimit'])
            upperlim = None
            if self.valid_key('scaledValueOfUpperLimit') and\
               self.valid_key('scaleFactorOfUpperLimit'):
               if self['scaledValueOfUpperLimit'] and\
                  self['scaleFactorOfUpperLimit']: 
                   upperlim = self['scaledValueOfUpperLimit']/\
                              np.power(10.0,self['scaleFactorOfUpperLimit'])
            if upperlim is not None and lowerlim is not None:
                inventory.append(" (%s-%s)" % (upperlim,lowerlim))
            elif upperlim is not None:
                inventory.append(" (> %s)" % upperlim)
            elif lowerlim is not None:
                inventory.append(" (< %s)" % lowerlim)
        return ''.join(inventory)
    def is_missing(self,key):
        """
        is_missing(key)

        returns True if value associated with key is equal
        to grib missing value flag (False otherwise)"""
        cdef int err,miss
        cdef char *name
        name = PyString_AsString(key)
        miss = grib_is_missing(self._gh, name, &err)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        if miss:
            return True
        else:
            return False
    def keys(self):
        """
        keys()

        return keys associated with a grib message (a dictionary-like object)
        """
        cdef grib_keys_iterator* gi
        cdef int err, typ
        cdef char *name
        # use cached keys if they exist.
        if self._all_keys is not None: return self._all_keys
        # if not, get keys from grib file.
        gi = grib_keys_iterator_new(self._gh,\
                GRIB_KEYS_ITERATOR_ALL_KEYS, NULL)
        keys = []
        while grib_keys_iterator_next(gi):
            name = grib_keys_iterator_get_name(gi)
            key = PyString_FromString(name)
            # ignore these keys.
            if key in ["zero","one","eight","eleven","false","thousand","file",
                       "localDir","7777","oneThousand"]:
                continue
            err = grib_get_native_type(self._gh, name, &typ)
            if err:
                raise RuntimeError(grib_get_error_message(err))
            # keys with these types are ignored.
            if typ not in\
            [GRIB_TYPE_UNDEFINED,GRIB_TYPE_SECTION,GRIB_TYPE_BYTES,GRIB_TYPE_LABEL,GRIB_TYPE_MISSING]:
                keys.append(key)
        err = grib_keys_iterator_delete(gi)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        return keys
    def _read_only_keys(self):
        """
        _read_only_keys()

        return read-only keys associated with a grib message (a dictionary-like object)
        """
        cdef grib_keys_iterator* gi
        cdef int err, typ
        cdef char *name
        if self._all_keys is None:
            self._all_keys = self.keys()
        gi = grib_keys_iterator_new(self._gh,\
                GRIB_KEYS_ITERATOR_SKIP_READ_ONLY, NULL)
        keys_noro = []
        while grib_keys_iterator_next(gi):
            name = grib_keys_iterator_get_name(gi)
            key = PyString_FromString(name)
            keys_noro.append(key)
        err = grib_keys_iterator_delete(gi)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        keys_ro = []
        for key in self._all_keys:
            if key not in keys_noro:
                keys_ro.append(key)
        return keys_ro
    def __setitem__(self, key, value):
        """
        change values associated with existing grib keys.
        """
        cdef int err, typ
        cdef size_t size
        cdef char *name
        cdef long longval
        cdef double doubleval
        cdef ndarray datarr
        cdef char *strdata
        if key in self._ro_keys:
            raise KeyError('key "%s" is read only' % key)
        if key not in self._all_keys:
            raise KeyError('can only modify existing grib keys (key "%s" not found)'
                    % key )
        name = PyString_AsString(key)
        err = grib_get_native_type(self._gh, name, &typ)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        elif typ == GRIB_TYPE_LONG:
            # is value an array or a scalar?
            datarr = np.asarray(value, np.int)
            is_array == False
            if datarr.shape:
                is_array = True
            if not is_array: # scalar
                longval = value
                err = grib_set_long(self._gh, name, longval)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
            else:
                if key == 'values':
                    datarr = self._unshape_mask(datarr)
                if not PyArray_ISCONTIGUOUS(datarr):
                    datarr = datarr.copy()
                size = datarr.size
                err = grib_set_long_array(self._gh, name, <long *>datarr.data, size)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
        elif typ == GRIB_TYPE_DOUBLE:
            # is value an array or a scalar?
            datarr = np.asarray(value, np.float)
            is_array == False
            if datarr.shape:
                is_array = True
            if not is_array: # scalar
                doubleval = value
                err = grib_set_double(self._gh, name, doubleval)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
            else:
                if key == 'values':
                    datarr = self._unshape_mask(datarr)
                if not PyArray_ISCONTIGUOUS(datarr):
                    datarr = datarr.copy()
                size = datarr.size
                err = grib_set_double_array(self._gh, name, <double *>datarr.data, size)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
        elif typ == GRIB_TYPE_STRING:
            size=len(value)
            strdata = PyString_AsString(value)
            err = grib_set_string(self._gh, name, strdata, &size)
            if err:
                raise RuntimeError(grib_get_error_message(err))
        else:
            raise ValueError("unrecognized grib type % d" % typ)
    def __getitem__(self, key):
        """
        access values associated with grib keys.
        
        The key "values" will return the data associated with the grib message.
        The data is returned as a numpy array, or if missing values or a bitmap
        are present, a numpy masked array.  Reduced lat/lon or gaussian grid
        data is automatically expanded to a regular grid using linear
        interpolation (nearest neighbor if an adjacent grid point is a missing
        value)."""
        cdef int err, typ
        cdef size_t size
        cdef char *name
        cdef long longval
        cdef double doubleval
        cdef ndarray datarr
        cdef char strdata[1024]
        name = PyString_AsString(key)
        err = grib_get_size(self._gh, name, &size)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        err = grib_get_native_type(self._gh, name, &typ)
        # force 'paramId' to be size 1 (it returns a size of 7,
        # which is a relic from earlier versions of grib_api in which
        # paramId was a string and not an integer)
        if key=='paramId' and typ == GRIB_TYPE_LONG: size=1
        if err:
            raise RuntimeError(grib_get_error_message(err))
        elif typ == GRIB_TYPE_LONG:
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
                datarr = np.zeros(size, np.int, order=storageorder)
                err = grib_get_long_array(self._gh, name, <long *>datarr.data, &size)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
                if key == 'values':
                    return self._reshape_mask(datarr)
                else:
                    return datarr
        elif typ == GRIB_TYPE_DOUBLE:
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
                datarr = np.zeros(size, np.double, order=storageorder)
                err = grib_get_double_array(self._gh, name, <double *>datarr.data, &size)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
                if key == 'values':
                    return self._reshape_mask(datarr)
                else:
                    return datarr
        elif typ == GRIB_TYPE_STRING:
            size=1024 # grib_get_size returns 1 ?
            err = grib_get_string(self._gh, name, strdata, &size)
            if err:
                raise RuntimeError(grib_get_error_message(err))
            msg = PyString_FromString(strdata)
            return msg.rstrip()
        else:
            raise ValueError("unrecognized grib type % d" % typ)
    def has_key(self,key):
        """
        has_key(key)

        tests whether a grib message object has a specified key.
        """
        return key in self._all_keys
    def valid_key(self,key):
        """
        valid_key(key)

        tests whether a grib message object has a specified key,
        it is not missing and it has a value that can be read.
        """
        ret =  key in self._all_keys
        # if key exists, but value is missing, return False.
        if ret and self.is_missing(key): ret = False
        if ret:
            try:
                self[key]
            except:
                ret = False
        return ret
    def tostring(self):
        """
        tostring()

        return coded grib message in a binary string.
        """
        cdef int err
        cdef size_t size
        cdef void *message
        cdef char *name
        cdef FILE *out
        name = PyString_AsString('values')
        err = grib_get_size(self._gh, name, &size)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        err = grib_get_message(self._gh, &message, &size)
        if err:
            raise RuntimeError(grib_get_error_message(err))
        msg = PyString_FromStringAndSize(<char *>message, size)
        return msg
    def _unshape_mask(self, datarr):
        """private method for reshaping and removing mask from "values" array"""
        if datarr.ndim > 2:
            raise ValueError('array must be 1d or 2d')
        # if array is masked, put in masked values and convert to plain numpy array.
        if hasattr(datarr,'mask'):
            datarr = datarr.filled()
        # raise error is expanded reduced grid array is supplied.
        if self['gridType'].startswith('reduced'):
            if datarr.ndim != 1:
                raise ValueError("reduced grid data array must be 1d")
        if datarr.ndim == 2:
            # check scan modes for rect grids.
            # rows scan in the -x direction (so flip)
            if not self['jScansPositively']:
                datsave = datarr.copy()
                datarr[::-1,:] = datsave[:,:]
            # columns scan in the -y direction (so flip)
            if self['iScansNegatively']:
                datsave = datarr.copy()
                datarr[:,::-1] = datsave[:,:]
            # adjacent rows scan in opposite direction.
            # (flip every other row)
            if self['alternativeRowScanning']:
                datsave = datarr.copy()
                datarr[1::2,::-1] = datsave[1::2,:]
        return datarr
    def _reshape_mask(self, datarr):
        """private method for reshaping and adding mask to "values" array"""
        cdef double missval
        if datarr.ndim > 2:
            raise ValueError('array must be 1d or 2d')
        # reduced grid.
        if self['gridType'].startswith('reduced'):
            try:
                ny = self['Ny']
            except:
                ny = self['Nj']
            if self.has_key('missingValue'):
                missval = self['missingValue']
            else:
                missval = 1.e30
            if self.expand_reduced:
                nx = 2*ny
                datarr = _redtoreg(2*ny, self['pl'], datarr, missval)
        elif self.has_key('Nx') and self.has_key('Ny'):
            nx = self['Nx']
            ny = self['Ny']
        # key renamed from Ni to Nx in grib_api 1.8.0.1
        elif self.has_key('Ni') and self.has_key('Nj'):
            nx = self['Ni']
            ny = self['Nj']
        else: # probably spectral data.
            return datarr
        if ny != GRIB_MISSING_LONG and nx != GRIB_MISSING_LONG:
            datarr.shape = (ny,nx)
        # check scan modes for rect grids.
        if datarr.ndim == 2:
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
           # if there is a missingValue, and some values missing,
           # create a masked array.
           if self.has_key('missingValue') and self['numberOfMissing']:
               datarr = ma.masked_values(datarr, self['missingValue'])
        return datarr
    def latlons(self):
        """
        latlons()

        compute lats and lons (in degrees) of grid.
        Currently handles reg. lat/lon, global gaussian, mercator, stereographic,
        lambert conformal, albers equal-area, space-view, azimuthal 
        equidistant, reduced gaussian, reduced lat/lon,
        lambert azimuthal equal-area, rotated lat/lon and rotated gaussian grids.

        @return: C{B{lats},B{lons}}, numpy arrays 
        containing latitudes and longitudes of grid (in degrees).

        sets the C{projparams} instance variable to a dictionary containing 
        proj4 key/value pairs describing the grid.
        """
        projparams = {}

        if self['shapeOfTheEarth'] == 6:
            projparams['a']=6371229.0
            projparams['b']=6371229.0
        elif self['shapeOfTheEarth'] in [3,7]:
            if self.has_key('scaleFactorOfMajorAxisOfOblateSpheroidEarth'):
                scalea = self['scaleFactorOfMajorAxisOfOblateSpheroidEarth']
                scaleb = self['scaleFactorOfMinorAxisOfOblateSpheroidEarth']
                if scalea and scalea is not missingvalue_int:
                    scalea = np.power(10.0,-scalea)
                    if self['shapeOfTheEarth'] == 3: # radius in km
                        scalea = 1000.*scalea
                else:
                    scalea = 1
                if scaleb and scaleb is not missingvalue_int:
                    scaleb = np.power(10.0,-scaleb)
                    if self['shapeOfTheEarth'] == 3: # radius in km
                        scaleb = 1000.*scaleb
                else:
                    scaleb = 1.
            else:
                scalea = 1.
                scaleb = 1.
            if grib_api_version < 10900:
                projparams['a']=self['scaledValueOfMajorAxisOfOblateSpheroidEarth']*scalea
                projparams['b']=self['scaledValueOfMinorAxisOfOblateSpheroidEarth']*scaleb
            else:
                projparams['a']=self['scaledValueOfEarthMajorAxis']*scalea
                projparams['b']=self['scaledValueOfEarthMinorAxis']*scaleb
            # check to make sure scale factor wasn't screwed up
            # (assume earth radius should be O(10**6) meters)
            #dec_scale = int(np.log10(projparams['a']))
            #if dec_scale != 6:
            #    dec_scale = 6-dec_scale
            #    rescale = np.power(10.0,dec_scale)
            #    projparams['a'] = rescale*projparams['a']
            #dec_scale = int(np.log10(projparams['b']))
            #if dec_scale != 6:
            #    dec_scale = 6-dec_scale
            #    rescale = np.power(10.0,dec_scale)
            #    projparams['b'] = rescale*projparams['b']
        elif self['shapeOfTheEarth'] == 2:
            projparams['a']=6378160.0
            projparams['b']=6356775.0 
        elif self['shapeOfTheEarth'] == 1:
            if self.has_key('scaleFactorOfRadiusOfSphericalEarth'):
                scalea = self['scaleFactorOfRadiusOfSphericalEarth']
                if scalea and scalea is not missingvalue_int:
                    scalea = np.power(10.0,-scalea)
                else:
                    scalea = 1
                scaleb = scalea
            else:
                scalea = 1.
                scaleb = 1.
            projparams['a']=self['scaledValueOfRadiusOfSphericalEarth']*scalea
            projparams['b']=self['scaledValueOfRadiusOfSphericalEarth']*scaleb
            # check to make sure scale factor wasn't screwed up
            # (assume earth radius should be O(10**6) meters)
            #dec_scale = int(np.log10(projparams['a']))
            #if dec_scale != 6:
            #    dec_scale = 6-dec_scale
            #    rescale = np.power(10.0,dec_scale)
            #    projparams['a'] = rescale*projparams['a']
            #    projparams['b'] = rescale*projparams['b']
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

        if self['gridType'] in ['regular_gg','regular_ll']: # regular lat/lon grid
            lons = self['distinctLongitudes']
            lats = self['distinctLatitudes']
            lons,lats = np.meshgrid(lons,lats) 
            projparams['proj']='cyl'
        elif self['gridType'] == 'reduced_gg': # reduced global gaussian grid
            lats = self['distinctLatitudes']
            ny = self['Nj']
            nx = 2*ny
            lon1 = self['longitudeOfFirstGridPointInDegrees']
            lon2 = self['longitudeOfLastGridPointInDegrees']
            lons = np.linspace(lon1,lon2,nx)
            lons,lats = np.meshgrid(lons,lats) 
            projparams['proj']='cyl'
        elif self['gridType'] == 'reduced_ll': # reduced lat/lon grid
            ny = self['Nj']
            nx = 2*ny
            lat1 = self['latitudeOfFirstGridPointInDegrees']
            lat2 = self['latitudeOfLastGridPointInDegrees']
            lon1 = self['longitudeOfFirstGridPointInDegrees']
            lon2 = self['longitudeOfLastGridPointInDegrees']
            lons = np.linspace(lon1,lon2,nx)
            lats = np.linspace(lat1,lat2,ny)
            lons,lats = np.meshgrid(lons,lats) 
            projparams['proj']='cyl'
        elif self['gridType'] == 'polar_stereographic':
            lat1 = self['latitudeOfFirstGridPointInDegrees']
            lon1 = self['longitudeOfFirstGridPointInDegrees']
            try:
               nx = self['Nx']
               ny = self['Ny']
            except:
               nx = self['Ni']
               ny = self['Nj']
            # key renamed from xDirectionGridLengthInMetres to
            # DxInMetres grib_api 1.8.0.1.
            try:
                dx = self['DxInMetres']
            except:
                dx = self['xDirectionGridLengthInMetres']
            try:
                dy = self['DyInMetres']
            except:
                dy = self['yDirectionGridLengthInMetres']
            projparams['proj']='stere'
            projparams['lat_ts']=self['latitudeWhereDxAndDyAreSpecifiedInDegrees']
            if self.has_key('projectionCentreFlag'):
                projcenterflag = self['projectionCentreFlag']
            elif self.has_key('projectionCenterFlag'):
                projcenterflag = self['projectionCenterFlag']
            else:
                raise KeyError('cannot find projection center flag')
            if projcenterflag == 0:
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
        elif self['gridType'] == 'lambert':
            lat1 = self['latitudeOfFirstGridPointInDegrees']
            lon1 = self['longitudeOfFirstGridPointInDegrees']
            try:
               nx = self['Nx']
               ny = self['Ny']
            except:
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
        elif self['gridType'] =='albers':
            lat1 = self['latitudeOfFirstGridPointInDegrees']
            lon1 = self['longitudeOfFirstGridPointInDegrees']
            try:
               nx = self['Nx']
               ny = self['Ny']
            except:
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
        elif self['gridType'] == 'space_view':
            try:
               nx = self['Nx']
               ny = self['Ny']
            except:
               nx = self['Ni']
               ny = self['Nj']
            projparams['lon_0']=self['longitudeOfSubSatellitePointInDegrees']
            projparams['lat_0']=self['latitudeOfSubSatellitePointInDegrees']
            if projparams['lat_0'] == 0.: # if lat_0 is equator, it's a
                projparams['proj'] = 'geos'
            # general case of 'near-side perspective projection' (untested)
            else:
                if projparams['a'] != projparams['b']:
                    raise ValueError('unsupported grid - earth not a perfect sphere')
                projparams['proj'] = 'nsper'
            scale = float(self['grib2divider'])
            projparams['h'] = projparams['a'] * self['Nr']/scale
            # latitude of horizon on central meridian
            lon_0=projparams['lon_0']; lat_0=projparams['lat_0']
            lonmax =\
            lon_0+90.-(180./np.pi)*np.arcsin(projparams['a']/projparams['h'])
            # longitude of horizon on equator
            latmax =\
            lat_0+90.-(180./np.pi)*np.arcsin(projparams['b']/projparams['h'])
            # h is measured from surface of earth at equator.
            projparams['h'] = projparams['h']-projparams['a']
            # truncate to nearest thousandth of a degree (to make sure
            # they aren't slightly over the horizon)
            latmax = int(1000*latmax)/1000.
            lonmax = int(1000*lonmax)/1000.
            pj = pyproj.Proj(projparams)
            x1,y1 = pj(lon_0,latmax); x2,y2 = pj(lonmax,lat_0)
            width = 2*x2; height = 2*y1
            #dx =\
            #width/self['apparentDiameterOfEarthInGridLengthsInXDirection']
            #dy =\
            #height/self['apparentDiameterOfEarthInGridLengthsInYDirection']
            dx = width/self['dx']
            dy = height/self['dy']
            xmax = dx*(nx-1); ymax = dy*(ny-1)
            x = np.linspace(-0.5*xmax,0.5*xmax,nx)
            y = np.linspace(-0.5*ymax,0.5*ymax,ny)
            x, y = np.meshgrid(x, y)
            lons, lats = pj(x,y,inverse=True)
            # set lons,lats to 1.e30 where undefined
            abslons = np.fabs(lons); abslats = np.fabs(lats)
            lons = np.where(abslons < 1.e20, lons, 1.e30)
            lats = np.where(abslats < 1.e20, lats, 1.e30)
        elif self['gridType'] == "equatorial_azimuthal_equidistant":
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
        elif self['gridType'] == "lambert_azimuthal_equal_area":
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
        elif self['gridType'] == 'mercator':
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
            #projparams['lat_ts']=self['latitudeSAtWhichTheMercatorProjectionIntersectsTheEarth']/scale
            projparams['lat_ts']=self['LaD']/scale
            projparams['lon_0']=0.5*(lon1+lon2)
            projparams['proj']='merc'
            pj = pyproj.Proj(projparams)
            llcrnrx, llcrnry = pj(lon1,lat1)
            urcrnrx, urcrnry = pj(lon2,lat2)
            try:
               nx = self['Nx']
               ny = self['Ny']
            except:
               nx = self['Ni']
               ny = self['Nj']
            dx = (urcrnrx-llcrnrx)/(nx-1)
            dy = (urcrnry-llcrnry)/(ny-1)
            x = llcrnrx+dx*np.arange(nx)
            y = llcrnry+dy*np.arange(ny)
            x, y = np.meshgrid(x, y)
            lons, lats = pj(x, y, inverse=True)
        elif self['gridType'] in ['rotated_ll','rotated_gg']:
            rot_angle = self['angleOfRotationInDegrees']
            pole_lat = self['latitudeOfSouthernPoleInDegrees']
            pole_lon = self['longitudeOfSouthernPoleInDegrees']
            rotatedlats = self['distinctLatitudes']
            rotatedlons = self['distinctLongitudes']
            d2r = np.pi/180.
            lonsr, latsr = np.meshgrid(rotatedlons*d2r, rotatedlats*d2r)
            projparams['o_proj']='longlat'
            projparams['proj']='ob_tran'
            projparams['o_lat_p']=-pole_lat
            projparams['o_lon_p']=rot_angle
            projparams['lon_0']=pole_lon
            pj = pyproj.Proj(projparams)
            lons,lats = pj(lonsr,latsr,inverse=True)
        else:
            raise ValueError('unsupported grid %s' % self['gridType'])
        self.projparams = projparams
        return lats, lons

cdef class index(object):
    """ 
index(filename, *args)
    
returns grib index object given GRIB filename indexed by keys given in
*args.  The L{select} or L{__call__} method can then be used to selected grib messages
based on specified values of indexed keys.
Unlike L{open.select}, containers or callables cannot be used to 
select multiple key values.
However, using L{index.select} is much faster than L{open.select}.

Example usage:

>>> import pygrib
>>> grbindx=pygrib.index('sampledata/gfs.grb','shortName','typeOfLevel','level')
>>> selected_grbs=grbindx.select(shortName='gh',typeOfLevel='isobaricInhPa',level=500)
>>> for grb in selected_grbs:
>>>     print grb
1:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 500 Pa:fcst time 72:from 200412091200:lo res cntl fcst
>>> # __call__ method does same thing as select
>>> selected_grbs=grbindx(shortName='u',typeOfLevel='isobaricInhPa',level=250)
>>> for grb in selected_grbs:
>>>     print grb
1:u-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 250 Pa:fcst time 72:from 200412091200:lo res cntl fcst
>>> grbindx.close()

@ivar keys: list of strings containing keys used in the index.

@ivar types: if keys are typed, this list contains the type declarations
(C{l}, C{s} or C{d}). Type declarations are specified by appending to the key
name (i.e. C{level:l} will search for values of C{level} that are longs).
"""
    cdef grib_index *_gi
    cdef public object keys, types, name
    def __cinit__(self, filename, *args):
        # initialize C level objects.
        cdef grib_index *gi
        cdef int err
        cdef char *filenamec, *keys
        filenamec = PyString_AsString(filename)
        if args == ():
            raise ValueError('no keys specified for index')
        keys = PyString_AsString(','.join(args))
        self._gi = grib_index_new_from_file (NULL, filenamec, keys, &err)
        if err:
            raise RuntimeError(grib_get_error_message(err))
    def __init__(self, filename, *args):
        # initalize Python level objects
        self.name = filename
        # is type is specified, strip it off.
        keys = [arg.split(':')[0] for arg in args]
        # if type is declared, save it (None if not declared)
        types = []
        for arg in args:
            try: 
                type = arg.split(':')[1]
            except IndexError:
                type = None
            types.append(type)
        self.keys = keys
        self.types = types
    def __call__(self, **kwargs):
        """same as L{select}"""
        return self.select(**kwargs)
    def select(self, **kwargs):
        """
select(**kwargs)

return a list of L{gribmessage} instances from grib index object 
corresponding to specific values of indexed keys (given by kwargs).
Unlike L{open.select}, containers or callables cannot be used to 
select multiple key values.
However, using L{index.select} is much faster than L{open.select}.

Example usage:

>>> import pygrib
>>> grbindx=pygrib.index('sampledata/gfs.grb','shortName','typeOfLevel','level')
>>> selected_grbs=grbindx.select(shortName='gh',typeOfLevel='isobaricInhPa',level=500)
>>> for grb in selected_grbs:
>>>     print grb
1:Geopotential height:gpm (instant):regular_ll:isobaricInhPa:level 500 Pa:fcst time 72:from 200412091200:lo res cntl fcst
>>> # __call__ method does same thing as select
>>> selected_grbs=grbindx(shortName='u',typeOfLevel='isobaricInhPa',level=250)
>>> for grb in selected_grbs:
>>>     print grb
1:u-component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 250 Pa:fcst time 72:from 200412091200:lo res cntl fcst
>>> grbindx.close()
"""
        cdef grib_handle *gh
        cdef int err
        cdef long longval
        cdef double doubval
        cdef char *strval, *key
        # set index selection.
        # used declared type if available, other infer from type of value.
        for k,v in kwargs.iteritems():
            if k not in self.keys:
                raise KeyError('key not part of grib index')
            typ = self.types[self.keys.index(k)]
            key = PyString_AsString(k)
            if typ == 'l' or (type(v) == int or type(v) == long):
                longval = long(v)
                err = grib_index_select_long(self._gi, key, longval)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
            elif typ == 'd' or type(v) == float:
                doubval = float(v)
                err = grib_index_select_double(self._gi, key, doubval)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
            elif typ == 's' or isinstance(v,basestring):
                strval = PyString_AsString(str(v))
                err = grib_index_select_string(self._gi, key, strval)
                if err:
                    raise RuntimeError(grib_get_error_message(err))
            else:
                raise TypeError('value must be float, int or string')
        # create a list of grib messages corresponding to selection.
        messagenumber = 0; grbs = []
        while 1:
            gh = grib_handle_new_from_index(self._gi, &err)
            if err or gh == NULL:
                break
            else:
                messagenumber = messagenumber + 1
            grbs.append(_create_gribmessage(gh, messagenumber))
            err = grib_handle_delete(gh)
            if err:
                raise RuntimeError(grib_get_error_message(err))
        # return the list of grib messages.
        return grbs
    def close(self):
        """
        close()

        deallocate C structures associated with class instance"""
        grib_index_delete(self._gi)

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

def _is_container(a):
    # is object container-like?  (can test for
    # membership with "is in", but not a string)
    try: 1 in a
    except: return False
    if type(a) == type(basestring): return False
    return True

def _find(grb, **kwargs):
    # search for key/value matches in grib message.
    # If value is a container-like object, search for matches to any element.
    # If value is a function, call that function with key value to determine
    # whether it is a match.
    for k,v in kwargs.iteritems():
        if not grb.has_key(k): return False
        # is v a "container-like" non-string object?
        iscontainer = _is_container(v)
        # is v callable?
        iscallable = hasattr(v, '__call__')
        # if v is callable and container-like, treat it as a container.
        # v not a container or a function.
        if not iscontainer and not iscallable and grb[k]==v:
            continue
        elif iscontainer and grb[k] in v: # v a container.
            continue
        elif iscallable and v(grb[k]): # v a function
            continue
        else:
            return False
    return True
