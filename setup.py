from os import path
from setuptools import find_packages
from setuptools import setup


# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

version = "1.0"

install_requires = [
    "dataclasses",
    "geopandas",
    "lxml",
    "openpyxl",
    "xlrd",
    "pathlib",
    "typing",
]

tests_require = [
    "pytest",
]

setup(
    name="mptconfig_checker",
    version=version,
    description="Check consistency HDSR mptconfig with FEWS",
    long_description=long_description,
    url="https://github.com/hdsr-mid/mptconfig_checker",
    author="Daniel Tollenaar, Renier Kramer",
    author_email="daniel@d2hydro.nl, renier.kramer@hdsr.nl",
    license="MIT",
    packages=find_packages(include=["mptconfig", "mptconfig.*"]),
    python_requires=">=3.6",
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"test": tests_require},
    classifiers=[
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="HDSR, mptconfig, FEWS, mptconfig_checker",
)
