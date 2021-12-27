# For each dataset listed in dataset_pids.txt, get terms of use and access metadata

import csv
import json
import glob
import os
from tkinter import filedialog
from tkinter import ttk
from tkinter import *

# Create GUI for getting user input

# Create, title and size the window
window = Tk()
window.title('Get terms of use and access metadata')
window.geometry('550x350')  # width x height


# Function called when user presses button to browse for JSON files directory
def retrieve_jsondirectory():
    global jsonDirectory

    # Call the OS's file directory window and store selected object path as a global variable
    jsonDirectory = filedialog.askdirectory()

    # Show user which directory she chose
    label_showChosenDirectory = Label(window, text='You chose: ' + jsonDirectory, anchor='w', foreground='green', wraplength=500, justify='left')
    label_showChosenDirectory.grid(sticky='w', column=0, row=2)


# Function called when user presses button to browse for CSV file directory
def retrieve_csvdirectory():
    global csvDirectory

    # Call the OS's file directory window and store selected object path as a global variable
    csvDirectory = filedialog.askdirectory()

    # Show user which directory she chose
    label_showChosenDirectory = Label(window, text='You chose: ' + csvDirectory, anchor='w', foreground='green', wraplength=500, justify='left')
    label_showChosenDirectory.grid(sticky='w', column=0, row=6)


# Function called when Start button is pressed
def start():
    window.destroy()


# Create label for button to browse for directory containing JSON files
label_getJSONFiles = Label(window, text='Choose folder containing the JSON files:', anchor='w')
label_getJSONFiles.grid(sticky='w', column=0, row=0, pady=2)

# Create button to browse for directory containing JSON files
button_getJSONFiles = ttk.Button(window, text='Browse', command=lambda: retrieve_jsondirectory())
button_getJSONFiles.grid(sticky='w', column=0, row=1)

# Create empty row in grid to improve spacing between the two fields
window.grid_rowconfigure(3, minsize=25)

# Create label for button to browse for directory to add csv files in
label_tablesDirectory = Label(window, text='Choose folder to store the CSV file:', anchor='w')
label_tablesDirectory.grid(sticky='w', column=0, row=4, pady=2)

# Create button to browse for directory containing JSON files
button_tablesDirectory = ttk.Button(window, text='Browse', command=lambda: retrieve_csvdirectory())
button_tablesDirectory.grid(sticky='w', column=0, row=5)

# Create start button
button_Start = ttk.Button(window, text='Start', command=lambda: start())
button_Start.grid(sticky='w', column=0, row=7, pady=40)

# Keep window open until it's closed
mainloop()


# Store path of csv file to filename variable
filename = os.path.join(csvDirectory, 'terms.csv')

print('Creating CSV file')

# Create CSV file
with open(filename, mode='w', newline='') as metadatafile:
    metadatafile = csv.writer(metadatafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Create header row
    metadatafile.writerow([
        'datasetVersionId', 'persistentUrl', 'persistent_id', 'license', 'termsOfUse', 'confidentialityDeclaration',
        'specialPermissions', 'restrictions', 'citationRequirements', 'depositorRequirements',
        'conditions', 'disclaimer', 'termsOfAccess', 'dataAccessPlace', 'originalArchive',
        'availabilityStatus', 'contactForAccess', 'sizeOfCollection', 'studyCompletion'])

print('Getting metadata:')


# Function for getting value of nested key, truncating the value to 10,000 characters
# (character limit for many spreadsheet applications), or returning nothing if key doesn't exist
def improved_get(_dict, path, default=None):
    for key in path.split('.'):
        try:
            _dict = _dict[key]
        except KeyError:
            return default
    if isinstance(_dict, int):
        return _dict
    else:
        return _dict[:10000].replace('\r', ' - ')


# Save count of files in the given directory and initialize count variable to track progress of script and for debugging
path, dirs, files = next(os.walk(jsonDirectory))
file_count = len(files)
count = 0

# For each JSON file in the given directory...
for file in glob.glob(os.path.join(jsonDirectory, '*.json')):  # For each JSON file in a folder
    count += 1

    # Save the name of the file to print to the terminal with the current and total counts
    file_pid = file.rsplit('/')[-1]

    # Open each file in read mode
    with open(file, 'r') as f1:

        # Copy content to dataset_metadata variable
        dataset_metadata = f1.read()

        # Load content in variable as a json object
        dataset_metadata = json.loads(dataset_metadata)

    # Print count of files opened, total file count, and name of file
    print('%s of %s: %s' % (count, file_count, file_pid))

    # Check if status is OK and there's a latestversion key (i.e. that the dataset isn't deaccessioned)
    if (dataset_metadata['status'] == 'OK') and ('datasetVersion' in dataset_metadata['data']):

        # Save the metadata values in variables
        datasetVersionId = improved_get(dataset_metadata, 'data.datasetVersion.id')
        persistentUrl = dataset_metadata['data']['persistentUrl']
        datasetPersistentId = improved_get(dataset_metadata, 'data.datasetVersion.datasetPersistentId')
        license = improved_get(dataset_metadata, 'data.datasetVersion.license')
        termsOfUse = improved_get(dataset_metadata, 'data.datasetVersion.termsOfUse')
        confidentialityDeclaration = improved_get(dataset_metadata, 'data.datasetVersion.confidentialityDeclaration')
        specialPermissions = improved_get(dataset_metadata, 'data.datasetVersion.specialPermissions')
        restrictions = improved_get(dataset_metadata, 'data.datasetVersion.restrictions')
        citationRequirements = improved_get(dataset_metadata, 'data.datasetVersion.citationRequirements')
        depositorRequirements = improved_get(dataset_metadata, 'data.datasetVersion.depositorRequirements')
        conditions = improved_get(dataset_metadata, 'data.datasetVersion.conditions')
        disclaimer = improved_get(dataset_metadata, 'data.datasetVersion.disclaimer')
        termsOfAccess = improved_get(dataset_metadata, 'data.datasetVersion.termsOfAccess')
        dataAccessPlace = improved_get(dataset_metadata, 'data.datasetVersion.dataAccessPlace')
        originalArchive = improved_get(dataset_metadata, 'data.datasetVersion.originalArchive')
        availabilityStatus = improved_get(dataset_metadata, 'data.datasetVersion.availabilityStatus')
        contactForAccess = improved_get(dataset_metadata, 'data.datasetVersion.contactForAccess')
        sizeOfCollection = improved_get(dataset_metadata, 'data.datasetVersion.sizeOfCollection')
        studyCompletion = improved_get(dataset_metadata, 'data.datasetVersion.studyCompletion')

        # Append fields to the csv file
        with open(filename, mode='a', newline='') as metadatafile:

            # Convert all characters to utf-8
            def to_utf8(lst):
                return [unicode(elem).encode('utf-8') for elem in lst]

            # Set how values are written to a row in the CSV file
            metadatafile = csv.writer(metadatafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # Write new row
            metadatafile.writerow([
                datasetVersionId, persistentUrl, datasetPersistentId, license, termsOfUse, confidentialityDeclaration,
                specialPermissions, restrictions, citationRequirements, depositorRequirements,
                conditions, disclaimer, termsOfAccess, dataAccessPlace, originalArchive,
                availabilityStatus, contactForAccess, sizeOfCollection, studyCompletion])
