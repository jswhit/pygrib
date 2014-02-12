from distutils.core import setup, Extension
import os, glob, numpy, sys
if sys.version_info[0] < 3:
    import ConfigParser as configparser
else:
    import configparser

grib_api_dir = os.environ.get('GRIBAPI_DIR')
grib_api_libdir = os.environ.get('GRIBAPI_LIBDIR')
grib_api_incdir = os.environ.get('GRIBAPI_INCDIR')
jasper_dir = os.environ.get('JASPER_DIR')
jasper_libdir = os.environ.get('JASPER_LIBDIR')
jasper_incdir = os.environ.get('JASPER_INCDIR')
png_dir = os.environ.get('PNG_DIR')
png_libdir = os.environ.get('PNG_LIBDIR')
png_incdir = os.environ.get('PNG_INCDIR')
zlib_dir = os.environ.get('ZLIB_DIR')
zlib_libdir = os.environ.get('ZLIB_LIBDIR')
zlib_incdir = os.environ.get('ZLIB_INCDIR')
openjpeg_dir = os.environ.get('OPENJPEG_DIR')
openjpeg_libdir = os.environ.get('OPENJPEG_LIBDIR')
openjpeg_incdir = os.environ.get('OPENJPEG_INCDIR')
# where to install man pages?
man_dir = os.environ.get('MAN_DIR')

setup_cfg = os.environ.get('PYGRIBSETUPCFG', 'setup.cfg')
# contents of setup.cfg will override env vars.
if os.path.exists(setup_cfg):
    sys.stdout.write('reading from setup.cfg...')
    config = configparser.SafeConfigParser()
    config.read(setup_cfg)
    try: grib_api_dir = config.get("directories", "grib_api_dir")
    except: pass
    try: grib_api_libdir = config.get("directories", "grib_api_libdir")
    except: pass
    try: grib_api_incdir = config.get("directories", "grib_api_incdir")
    except: pass
    try: jasper_dir = config.get("directories", "jasper_dir")
    except: pass
    try: jasper_libdir = config.get("directories", "jasper_libdir")
    except: pass
    try: jasper_incdir = config.get("directories", "jasper_incdir")
    except: pass
    try: png_dir = config.get("directories", "png_dir")
    except: pass
    try: png_libdir = config.get("directories", "png_libdir")
    except: pass
    try: png_incdir = config.get("directories", "png_incdir")
    except: pass
    try: openjpeg_dir = config.get("directories", "openjpeg_dir")
    except: pass
    try: openjpeg_libdir = config.get("directories", "openjpeg_libdir")
    except: pass
    try: openjpeg_incdir = config.get("directories", "openjpeg_incdir")
    except: pass
    try: zlib_dir = config.get("directories", "zlib_dir")
    except: pass
    try: zlib_libdir = config.get("directories", "zlib_libdir")
    except: pass
    try: zlib_incdir = config.get("directories", "zlib_incdir")
    except: pass
    try: man_dir = config.get("directories", "man_dir")
    except: pass

libdirs=[]
incdirs=[numpy.get_include()]
libraries=['grib_api']

if grib_api_libdir is None and grib_api_dir is not None:
    libdirs.append(os.path.join(grib_api_dir,'lib'))
    libdirs.append(os.path.join(grib_api_dir,'lib64'))
if grib_api_incdir is None and grib_api_dir is not None:
    incdirs.append(os.path.join(grib_api_dir,'include'))

if jasper_dir is not None or jasper_libdir is not None:
    libraries.append("jasper")
if jasper_libdir is None and jasper_dir is not None:
    libdirs.append(os.path.join(jasper_dir,'lib'))
    libdirs.append(os.path.join(jasper_dir,'lib64'))
if jasper_incdir is None and jasper_dir is not None:
    incdirs.append(os.path.join(jasper_dir,'include'))
    incdirs.append(os.path.join(jasper_dir,'include/jasper'))

if openjpeg_dir is not None or openjpeg_libdir is not None:
    libraries.append("openjpeg")
if openjpeg_libdir is None and openjpeg_dir is not None:
    libdirs.append(os.path.join(openjpeg_dir,'lib'))
    libdirs.append(os.path.join(openjpeg_dir,'lib64'))
if openjpeg_incdir is None and openjpeg_dir is not None:
    incdirs.append(os.path.join(openjpeg_dir,'include'))

if png_dir is not None or png_libdir is not None:
    libraries.append("png")
if png_libdir is None and png_dir is not None:
    libdirs.append(os.path.join(png_dir,'lib'))
    libdirs.append(os.path.join(png_dir,'lib64'))
if png_incdir is None and png_dir is not None:
    incdirs.append(os.path.join(png_dir,'include'))

if zlib_dir is not None or zlib_libdir is not None:
    libraries.append("z")
if zlib_libdir is None and zlib_dir is not None:
    libdirs.append(os.path.join(zlib_dir,'lib'))
    libdirs.append(os.path.join(zlib_dir,'lib64'))
if zlib_incdir is None and zlib_dir is not None:
    incdirs.append(os.path.join(zlib_dir,'include'))

g2clib_deps = glob.glob('g2clib_src/*.c')
g2clib_deps.append('g2clib.c')
incdirs.append("g2clib_src")
macros=[]

# if jasper or openjpeg lib not available...
if 'jasper' not in libraries and 'openjpeg' not in libraries:
    g2clib_deps.remove('g2clib_src/jpcpack.c')
    g2clib_deps.remove('g2clib_src/jpcunpack.c')
else:
    macros.append(('USE_JPEG2000',1))
# if png lib not available...
if 'png' not in libraries:
    g2clib_deps.remove('g2clib_src/pngpack.c')
    g2clib_deps.remove('g2clib_src/pngunpack.c')
else:
    macros.append(('USE_PNG',1))

if hasattr(sys,'maxsize'):
    if sys.maxsize > 2**31-1: macros.append(('__64BIT__',1))
else:
    if sys.maxint > 2**31-1: macros.append(('__64BIT__',1))

g2clibext = Extension("g2clib",g2clib_deps,include_dirs=incdirs,\
            library_dirs=libdirs,libraries=libraries,runtime_library_dirs=libdirs,define_macros=macros)
redtoregext =\
Extension("redtoreg",["redtoreg.c"],include_dirs=[numpy.get_include()])
pygribext =\
Extension("pygrib",["pygrib.c"],include_dirs=incdirs,library_dirs=libdirs,\
          runtime_library_dirs=libdirs,libraries=libraries)

# man pages installed in man_dir/man1
if man_dir is not None:
    manpages = glob.glob(os.path.join('man','*.1'))
    data_files = [(os.path.join(man_dir,'man1'), manpages)]
# if man_dir not set, man pages not installed
else:
    data_files = None



setup(name = "pygrib",
      version = "1.9.9",
      description       = "Python module for reading/writing GRIB files",
      author            = "Jeff Whitaker",
      author_email      = "jeffrey.s.whitaker@noaa.gov",
      url               = "http://code.google.com/p/pygrib",
      download_url      = "http://python.org/pypi/pygrib",
      scripts =
      ['utils/grib_list','utils/grib_repack','utils/cnvgrib1to2','utils/cnvgrib2to1'],
      ext_modules       = [pygribext,g2clibext,redtoregext],
      py_modules        = ["ncepgrib2"],
      data_files        = data_files)
