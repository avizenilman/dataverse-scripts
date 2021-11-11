# dataverse-scripts

Scripts for automating things in a Dataverse repository/installation, plus some other scripts. The scripts are written using Python 3, pipenv to manage package dependencies, and a Mac OS. Compatability with Python 2 and Windows is limited, although I plan to improve compatibility with Windows over time.

### get_dataset_PIDs.py
Gets the persistent identifiers of any datasets in a given Dataverse installation or a given Dataverse Collection within that installation (and optionally all of the Dataverse Collections within that Dataverse Collection)

### These scripts do things with a given list of either dataset PIDs or of Dataverse Collection IDs/aliases:

| Script or directory                          | Purpose                                                                                                                                                        |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| change_citation_dates.py                     | Change citation year shown in Dataverse repository's suggested citation                                            |
| get_dataset_lock_info.py                     | Get information about locks on given datasets                                                                                                              |
| delete_dataset_locks.py                      | Delete all locks of given datasets                                                                                                                             |
| delete_dataverses.py                         | Delete given Dataverse Collections                                                                                                                             |
| destroy_datasets.py                          | Delete given published datasets                                                                                                                                |
| [Get and convert metadata of datasets](https://github.com/jggautier/dataverse_scripts/tree/main/get-dataverse-metadata)         | A collection of scripts for getting JSON metadata of given datasets and parsing metadata into csv files for metadata analysis, reporting and improving.        |
| move_datasets.py                             | Move given datasets from one Dataverse Collection into another                                                                                                 |
| publish_multiple_datasets.py                 | Publish given draft datasets (or draft dataset versions)                                                                                                     |
| remove_dataset_links.py                      | Remove given dataset links from a given Dataverse Collection                                                                                                   |
| replace_dataset_metadata.py                  | Replace the metadata of given datasets                                                                                                                         |

### Misc
- **curation_report.py**: This script creates an overview of datasets created in a Dataverse installation in a given time frame, which can be useful for regular dataset curation.
- **get_dataset_metadata_of_all_installations.py**: This script downloads dataset metadata of as many known Dataverse installations as possible. Used to create the dataset at https://doi.org/10.7910/DVN/DCDKZQ.
- **combine_tables.py**: Joins CSV files in a given directory.
- **split_table.py**: Splits a given CSV file into many CSV files based on the unique values in a given column.
- **oaipmh_record_count.py**: This script writes the identifiers and statuses of records in a given OAI-PMH server and set.
  
## Installation
 * Install Python 3, pip and pipenv if you don't already have them. There's a handy guide at https://docs.python-guide.org.
 
 * [Download a zip folder with the files in this GitHub repository](https://github.com/jggautier/dataverse_scripts/archive/refs/heads/main.zip) or clone this GitHub repository:

```
git clone https://github.com/jggautier/dataverse_scripts.git
```

 * cd into the dataverse_scripts directory and use `pipenv shell` so that package dependacies for these scripts are managed separately from any Python packages already on your system
 * install packages from [requirements.txt](https://github.com/jggautier/dataverse_scripts/blob/main/requirements.txt)
 ```
pip install -r requirements.txt
```
 * run any of the Python scripts, such as get_dataset_PIDs.py
