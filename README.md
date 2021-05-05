## Description
A python project that:
* validates consistency of the HDSR FEWS-WIS meetpunt configuration;   
* complements the configuration's locationsets attributes;
* outputs 1 excel_file with multiple sheets, each sheet containing the results of 1 check;
* outputs a new csvs: waterstandlocaties, sublocaties, and eventually hoofdlocaties (if sublocations holds no errors).
* outputs eventually new validation csv (added missing internal locations)

### Usage
1. define all paths in class PathConstants in mptconfig_checker/mptconfig/constants
2. run project:
```
cd <project_root>
main.py
```

### License 
[MIT][mit]

[mit]: https://github.com/hdsr-mid/mptconfig_checker/blob/main/LICENSE.txt

### Releases
None

### Contributions
All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are
welcome on https://github.com/hdsr-mid/mptconfig_checker/issues

### Test Coverage (May-5-2021)
most of the tests are integration tests (since lack of time): 
the checker is tested against two FEWS configs (see mptconfig/tests/fixtures.py)
)
```
---------- coverage: platform win32, python 3.7.10-final-0 --
Name                             Stmts   Miss  Cover
----------------------------------------------------
main.py                             32     32     0%
mptconfig\__init__.py                0      0   100%
mptconfig\checker.py               968    234    76%
mptconfig\checker_helpers.py       208     39    81%
mptconfig\constants.py             263     34    87%
mptconfig\description.py             0      0   100%
mptconfig\excel.py                 184     97    47%
mptconfig\fews_utilities.py        170     28    84%
mptconfig\idmapping_choices.py      45      8    82%
mptconfig\utils.py                  76     18    76%
setup.py                            10     10     0%
----------------------------------------------------
TOTAL                             1956    500    74%
```


### Conda general tips
#### Build conda environment (on Windows) from any directory using environment.yml:
```
> conda env create -f <path_to_repo>/environment.yml --name <conda_env_name> python=<python_version>
> conda info --envs  # verify <conda_env_name> is in this list 
```
#### Start the application from any directory:
```
> conda activate <conda_env_name>
> (<conda_env_name>) python <path_to_repo>/main.py
```
#### Build virtual environment (on Windows) using requirement.txt
```
# First build vitual environment and activate it, then:
pip install -r <path_to_repo>/requirements.txt
```
#### Test the application:
```
# Use system-wide pytest:
> cd <path_to_repo>
> pytest

# Use pytest in environment
> conda activate <conda_env_name>
> conda install pytest
> cd <path_to_repo>
> pytest
```
#### List all conda environments on your machine:
```
> conda info --envs
```
#### Build empty conda env with specific python version:
```
# With '--no-deps' conda will skip specified packages in the .condarc file.
# To get the location of this conda configuration file type 'conda info'
> cd <does_not_matter>
> conda create --name <conda_env_name> python=<python_version> --no-deps
```
#### Delete a conda env:
```
> conda env remove --name <conda_env_name>
# Then remove the env folder by hand afterwards
```
#### Write dependencies to environment.yml:
```
# By default, the YAML includes platform-specific build constraints. 
# If you transfer across platforms (e.g. win32 to 64) omit the build info with '--no-builds':
> conda env export -f <path_to_repo>/environment.yml --name  <conda_env_name> --no-builds 
```
#### Pip and Conda:
```
# If a packaga is not available on all conda channels, but available as pip package, one can do:
> conda activate <conda_env_name>
> conda install pip
> pip install <pip_package>
# Note that mixing packages from conda and pip is always a potential problem: conda calls pip, but 
# pip does not know how to satisfy missing dependencies with packages from Anaconda repositories.

# Your environment.yml might look like:
channels:
  - defaults
dependencies:
  - <a conda package>=<version>
  - pip
  - pip:
    - <a pip package>==<version>

# You can also write a requirements.txt file:
> pip list --format=freeze > <path_to_repo>/requirements.txt
```
