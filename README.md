# Dataverse repository curation app
A small application for automating things in repositories that use the Dataverse software (https://dataverse.org). With this application you can:
- Get dataset metadata as CSV files
- Delete published datasets (to do this you'll need a "super user" account, usually used by administrators of Dataverse installations)

The application is written using the Dataverse software's APIs, Python 3, and Python's tkinter library (for creating the user interface), and made into an executable file using [pyInstaller](https://pyinstaller.readthedocs.io/).

## Status
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)  
Work in progress: Doing usability testing, fixing UI bugs, adding more documentation 

## Using the application
### Executable file
The executable file works only on MacOS and may only work on macOS Monterey (12) and later MacOS versions. To use it, [download the ZIP file](https://github.com/jggautier/dataverse-scripts/raw/main/Dataverse%20Repository%20Curation%20App.zip), and extract the Dataverse Repository Curation App file.

### Python script
If you'd like to run the application on earlier versions of MacOS or on other operating systems, or if you run into problems with the exectable file, you can run the curation_app_main.py file. You'll need Python 3 installed and may need Python 3.7 or later, as well as the Python libraries listed in the [requirements.txt file](https://github.com/jggautier/dataverse-scripts/blob/main/dataverse_repository_curation_app/requirements.txt):

* Install Python 3, pip and pipenv if you don't already have them. There's a handy guide at https://docs.python-guide.org.
 
 * [Download a zip folder with the files in this GitHub repository](https://github.com/jggautier/dataverse-scripts/archive/refs/heads/main.zip) or clone this GitHub repository:

```
git clone https://github.com/jggautier/dataverse-scripts.git
```

 * Iin your terminal, cd into the dataverse_repository_curation_app directory and use `pipenv shell` so that package dependencies for these scripts are managed separately from any Python packages already on your system
 * Install packages from the requirements.txt file
```
pip install -r requirements.txt
```
 * Run dataverse_repository_curation_app_main.py to run the application

Note: The tkinter library comes with most installations of Python 3, so pip doesn't include it in the requirements.txt it produces. But if after installing packages in a pipenv shell, you get error messages about tkinter not being defined, you may have to install tkinter "manually". For example, if you use homebrew's version of Python 3, you might have to `brew install python-tk`

## Upcoming changes

I plan to add more functionality to the application over time, including:
- Merging dataverse accounts
- Getting the guestbooks of all Dataverse Collections within a dataverse Collection
- Deleting Dataverse Collections (and optionally all collections and datasets within it)
- Changing datasets' citation dates
- Deleting dataset locks
- Getting information about locked datasets in a Dataverse repository
- Moving datasets to different Dataverse Collections
- Publishing datasets
- Removing dataset links in Dataverse Collections

## Other scripts
The [other_scripts directory](https://github.com/jggautier/dataverse-scripts/tree/main/other_scripts) contains Python scripts I've written over the past three years for automating some common curation and research-related tasks. Some of these scripts do what the Dataverse repository curation app does or will do. I'll remove these scripts from the directory as the scripts functionality gets added to the application.
