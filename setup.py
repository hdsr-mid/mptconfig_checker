from meetpuntconfig import __description__
from meetpuntconfig import __version__
from setuptools import setup


with open("README.md", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="meetpuntconfig",
    version=__version__,
    description=__description__,
    long_description=long_description,
    url="https://github.com/d2hydro/hdsr_meetpuntconfig",
    author="Daniel Tollenaar",
    author_email="daniel@d2hydro.nl",
    license="MIT",
    packages=["meetpuntconfig"],
    python_requires=">=3.6",
    install_requires=["geopandas", "lxml", "numpy", "openpyxl", "pandas>=1.1.0", "xlrd>=1.0.0", "typing"],
    keywords="HDSR meetpuntconfig FEWS",
)
