import glob
import os
import setuptools
import sys
from Cython.Distutils import build_ext


class NumpyBuildExtCommand(build_ext):
    """
    build_ext command for use when numpy headers are needed.
    from https://stackoverflow.com/questions/2379898/
    and https://stackoverflow.com/questions/48283503/
    """

    def run(self):
        import numpy

        self.distribution.fetch_build_eggs(["numpy"])
        self.include_dirs.append(numpy.get_include())
        build_ext.run(self)


def extract_version(CYTHON_FNAME):
    version = None
    with open(CYTHON_FNAME) as fi:
        for line in fi:
            if line.startswith("__version__"):
                _, version = line.split("=")
                version = version.strip()[1:-1]  # Remove quotation characters.
                break
    return version


def package_files(directory):
    owd = os.getcwd()
    os.chdir(os.path.join('src','pygrib'))
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    os.chdir(owd)
    return paths

if os.environ.get("PYGRIB_WHEEL") is not None:
    package_data={'':package_files('share')}
else:
    package_data={}

cmdclass = {"build_ext": NumpyBuildExtCommand}

searchdirs = []
if os.environ.get("GRIBAPI_DIR"):
    searchdirs.append(os.environ["GRIBAPI_DIR"])
if os.environ.get("ECCODES_DIR"):
    searchdirs.append(os.environ["ECCODES_DIR"])
if os.environ.get("CONDA_PREFIX"):
    searchdirs.append(os.environ["CONDA_PREFIX"])
    searchdirs.append(os.path.join(os.environ["CONDA_PREFIX"],'Library')) # windows
searchdirs += [
    os.path.expanduser("~"),
    "/usr",
    "/usr/local",
    "/opt/local",
    "/opt/homebrew",
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
if sys.platform == 'win32':
    runtime_lib_dirs = []
else:
    runtime_lib_dirs = libdirs
ext_modules = [
    setuptools.Extension(
        "pygrib._pygrib",
        ["src/pygrib/_pygrib.pyx"],
        include_dirs=incdirs,
        library_dirs=libdirs,
        runtime_library_dirs=runtime_lib_dirs,
        libraries=["eccodes"],
    )
]

# man pages installed in MAN_DIR/man1
if os.environ.get("MAN_DIR"):
    man_dir = os.environ.get("MAN_DIR")
    manpages = glob.glob(os.path.join("man", "*.1"))
    data_files = [(os.path.join(man_dir, "man1"), manpages)]
# if MAN_DIR not set, man pages not installed
else:
    data_files = None

# See pyproject.toml for project metadata
setuptools.setup(
    name="pygrib",  # need by GitHub dependency graph
    version=extract_version("src/pygrib/_pygrib.pyx"),
    cmdclass=cmdclass,
    scripts=[
        "utils/grib_list",
        "utils/grib_repack",
        "utils/cnvgrib1to2",
        "utils/cnvgrib2to1",
    ],
    ext_modules=ext_modules,
    data_files=data_files,
    package_data=package_data,
)
