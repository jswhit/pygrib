import os
import setuptools
from Cython.Distutils import build_ext

class NumpyBuildExtCommand(build_ext):
    """
    build_ext command for use when numpy headers are needed.
    from https://stackoverflow.com/questions/2379898/
    and https://stackoverflow.com/questions/48283503/
    """

    def run(self):
        self.distribution.fetch_build_eggs(["numpy"])
        import numpy

        self.include_dirs.append(numpy.get_include())
        build_ext.run(self)

cmdclass = {"build_ext": NumpyBuildExtCommand}

redtoregext = setuptools.Extension(
    "redtoreg", ["redtoreg.pyx"]
)
searchdirs = []
if os.environ.get("ECCODES_DIR"):
    searchdirs.append(os.environ["ECCODES_DIR"])
if os.environ.get("CONDA_PREFIX"):
    searchdirs.append(os.environ["CONDA_PREFIX"])
searchdirs += [
    os.path.expanduser("~"),
    "/usr",
    "/usr/local",
    "/opt/local",
    "/opt",
    "/sw",
]
# look for grib_api.h in searchdirs
eccdir = None
for d in searchdirs:
    try:
        incpath = os.path.join(os.path.join(d, "include"), "grib_api.h")
        f = open(incpath)
        eccdir = d
        print("eccodes found in %s" % eccdir)
        break
    except IOError:
        continue
if eccdir is not None:
    incdirs = [os.path.join(eccdir, "include")]
    libdirs = [os.path.join(eccdir, "lib"), os.path.join(eccdir, "lib64")]
else:
    print("eccodes not found, build may fail...")
    incdirs = []
    libdirs = []
pygribext = setuptools.Extension(
    "pygrib",
    ["pygrib.pyx"],
    include_dirs=incdirs,
    library_dirs=libdirs,
    runtime_library_dirs=libdirs,
    libraries=["eccodes"],
)
ext_modules = [redtoregext, pygribext]

# Import README.md as PyPi long_description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setuptools.setup(
      version = "2.1",
      description       = "Python module for reading/writing GRIB files",
      author            = "Jeff Whitaker",
      author_email      = "jeffrey.s.whitaker@noaa.gov",
      url               = "https://github.com/jswhit/pygrib",
      download_url      = "http://python.org/pypi/pygrib",
      classifiers       = ["Development Status :: 4 - Beta",
                           "Programming Language :: Python :: 2",
                           "Programming Language :: Python :: 2.4",
                           "Programming Language :: Python :: 2.5",
                           "Programming Language :: Python :: 2.6",
                           "Programming Language :: Python :: 2.7",
                           "Programming Language :: Python :: 3",
                           "Programming Language :: Python :: 3.3",
                           "Programming Language :: Python :: 3.4",
                           "Programming Language :: Python :: 3.5",
                           "Programming Language :: Python :: 3.6",
                           "Intended Audience :: Science/Research",
                           "License :: OSI Approved",
                           "Topic :: Software Development :: Libraries :: Python Modules"],
      cmdclass          = cmdclass,
      long_description  = long_description,
      long_description_content_type = 'text/markdown',
      scripts=['utils/grib_list','utils/grib_repack','utils/cnvgrib1to2','utils/cnvgrib2to1'],
      ext_modules=[redtoregext, pygribext],
      install_requires=[
          "pyproj",
          "numpy",
      ]
)
