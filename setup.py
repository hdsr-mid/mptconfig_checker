from meetpuntconfig import __author__
from meetpuntconfig import __author_email__
from meetpuntconfig import __description__
from meetpuntconfig import __license__
from meetpuntconfig import __version__
from setuptools import setup


with open("README.md", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="mptconfig_checker",
    version=__version__,
    description=__description__,
    long_description=long_description,
    url="https://github.com/hdsr-mid/mptconfig_checker",
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    packages=["meetpuntconfig"],
    python_requires=">=3.6",
    install_requires=["geopandas", "pandas", "lxml", "numpy", "openpyxl", "xlrd", "typing", "pathlib"],
    keywords="HDSR, meetpuntconfig, FEWS, mptconfig_checker",
)
