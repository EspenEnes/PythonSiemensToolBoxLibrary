import sys
import platform

MAJOR = 0
MINOR = 0
MICRO = 1
VERSION = f"{MAJOR}.{MINOR}.{MICRO}"

min_version = (3, 10, 0)

def is_right_py_version(min_py_version):
    if sys.version_info < (3,):
        sys.stderr.write("Python 2 is not supported")
        return False

    if sys.version_info < min_py_version:
        python_min_version_str = ".".join((str(num) for num in min_py_version))
        no_go = f"You are using Python {platform.python_version()}. Python >={python_min_version_str} is  required."
        sys.stderr.write(no_go)
        return False

    return True

if not is_right_py_version(min_version):
    sys.exit(-1)


from setuptools import setup, find_packages
setup(
    name = "PythonSiemensToolboxLibrary",
    author = "Espen Enes",
    author_email = "espenenes@hotmail.com",
    license = "MIT License",
    platforms = ["Any"],
    packages = [i for i in find_packages() if "tests" not in i],
    description = "Python package to read Step7 project files and blocks",
    long_description = "Python package to read Simatic Step7 projects, to extract content from DBs",
    keywords = ["toolbox", "siemens", "step7", "plc"],
    requires = ["dbfread"],
    classifiers = [ "Development Status :: 3 - Alpha",
                    "Programming Language :: Python :: 3",
                    "Intended Audience :: Education",
                    ]
)
