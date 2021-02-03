# HDSR meetpuntconfig
Python scripts ter ondersteuning van het HDSR CAW FEWS:
 - het controleren van de consistentie van de configuratie met meetpunten
 - het aanvullen van attributen van locatiesets binnen de configuratie

## Voorbereiden configuratie
Het bestand *config\config_example.json* staat een voorbeeld bestand met variabelen die 
worden ingelezen door de scripts. Pas dit bestand aan met de volgende stappen:
1. hernoem/kopieer *config\config_example.json* naar *config\config.json*
1. zet alle paden in de sectie *[paden]* goed



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
