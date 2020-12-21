import os
import glob
import setuptools
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
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


package_data = {}
if os.environ.get("PYGRIB_WHEEL") is not None:
    package_data[""] = package_files("eccodes")

cmdclass = {"build_ext": NumpyBuildExtCommand}

searchdirs = []
if os.environ.get("GRIBAPI_DIR"):
    searchdirs.append(os.environ["GRIBAPI_DIR"])
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
ext_modules = [
    setuptools.Extension(
        "pygrib._pygrib",
        ["pygrib/_pygrib.pyx"],
        include_dirs=incdirs,
        library_dirs=libdirs,
        runtime_library_dirs=libdirs,
        libraries=["eccodes"],
    )
]

# Import README.md as PyPi long_description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md")) as f:
    long_description = f.read()

# man pages installed in MAN_DIR/man1
if os.environ.get("MAN_DIR"):
    man_dir = os.environ.get("MAN_DIR")
    manpages = glob.glob(os.path.join("man", "*.1"))
    data_files = [(os.path.join(man_dir, "man1"), manpages)]
# if MAN_DIR not set, man pages not installed
else:
    data_files = None

setuptools.setup(
    name="pygrib",
    version=extract_version("pygrib/_pygrib.pyx"),
    description="Python module for reading/writing GRIB files",
    author="Jeff Whitaker",
    author_email="jeffrey.s.whitaker@noaa.gov",
    url="https://github.com/jswhit/pygrib",
    download_url="http://python.org/pypi/pygrib",
    license="License :: OSI Approved :: MIT License",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    cmdclass=cmdclass,
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=[
        "utils/grib_list",
        "utils/grib_repack",
        "utils/cnvgrib1to2",
        "utils/cnvgrib2to1",
    ],
    ext_modules=ext_modules,
    data_files=data_files,
    packages=["pygrib"],
    package_data=package_data,
    setup_requires=["setuptools", "cython"],
    install_requires=[
        "pyproj",
        "numpy",
    ],
)
