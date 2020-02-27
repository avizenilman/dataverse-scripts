'''
Provide a date range and optional API key and this script will get info for datasets and files created within that date range.
Useful when curating deposited data, especially spotting problem datasets (e.g. dataset with no data).
This script first uses the Search API to find PIDs of datasets.
For each dataset found, the script uses the "Get Versions" API endpoint to get dataset and file metadata of the latest version of each dataset,
and formats and writes that metadata to a CSV file on the users computer.
'''

import csv
import json
import os
import sys
import urllib.request
from urllib.request import urlopen

# Get required info from user
server='https://dataverse.harvard.edu/'
startdate='' # yyyy-mm-dd
enddate='' # yyyy-mm-dd
apikey='' # for getting unpublished datasets accessible to Dataverse account
directory='' # directory for the CSV file containing the dataset and file info, e.g. '/Users/username/Desktop/'

# Initialization for paginating through Search API results
start=0
condition=True

# List for storing indexed dataset PIDs and variable for counting misindexed datasets
dataset_pids=[]
misindexed_datasets_count=0

print('Searching for dataset PIDs:')
while (condition):
	try:
		per_page=10
		url='%s/api/search?q=*&fq=metadataSource:"Harvard+Dataverse"&type=dataset&per_page=%s&start=%s&sort=date&order=desc&fq=dateSort:[%sT00:00:00Z+TO+%sT23:59:59Z]&key=%s' %(server, per_page, start, startdate, enddate, apikey)
		data=json.load(urlopen(url))

		# Get total number of results
		total=data['data']['total_count']

		# For each item object...
		for i in data['data']['items']:

			# Get the dataset PID and add it to the dataset_pids list
			global_id=i['global_id']
			dataset_pids.append(global_id)

		print('Dataset PIDs found: %s of %s' %(len(dataset_pids), total), end='\r', flush=True)

		# Update variables to paginate through the search results
		start=start+per_page

	# Print error message if misindexed datasets break the Search API call, and try the next page. (See https://github.com/IQSS/dataverse/issues/4225)
	except urllib.error.URLError:
		try:
			per_page=1
			url='%s/api/search?q=*&fq=metadataSource:"Harvard+Dataverse"&type=dataset&per_page=%s&start=%s&sort=date&order=desc&fq=dateSort:[%sT00:00:00Z+TO+%sT23:59:59Z]&key=%s' %(server, per_page, start, startdate, enddate, apikey)
			data=json.load(urlopen(url))

			# Get dataset PID and save to dataset_pids list
			global_id=data['data']['items'][0]['global_id']
			dataset_pids.append(global_id)

			print('Dataset PIDs found: %s of %s' %(len(dataset_pids), total), end='\r', flush=True)

			# Update variables to paginate through the search results
			start=start+per_page

		except urllib.error.URLError:
			misindexed_datasets_count+=1			
			start=start+per_page

	# Stop paginating when there are no more results
	condition=start<total

print('Dataset PIDs found: %s of %s' %(len(dataset_pids), total))

if misindexed_datasets_count:
	print('Datasets misindexed: %s' %(misindexed_datasets_count))

# If api key is used, deduplicate PIDs in dataset_pids list. (For published datasets with a draft version, the Search API lists the PID twice, once for published and draft versions.)
if apikey:
	unique_dataset_pids=set(dataset_pids)
	print('Unique datasets: %s (The Search API lists both the draft and most recently published versions of datasets)' %(len(unique_dataset_pids)))
# Other, copy dataset_pids to unique_dataset_pids variable
else:
	unique_dataset_pids = dataset_pids

# Store name of csv file, which includes the dataset start and end date range, to the 'filename' variable
filename='datasetinfo_%s-%s.csv' %(startdate.replace('-', '.'), enddate.replace('-', '.'))

# Create variable for directory path and file name
csvfilepath=os.path.join(directory, filename)

# Create CSV file
with open(csvfilepath, mode='w') as opencsvfile:
	opencsvfile=csv.writer(opencsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	# Create header row
	opencsvfile.writerow(['datasetURL (publication state)', 'ds_title', 'fileinfo'])

# For each data file in each dataset, add to the CSV file the dataset's URL and publication state, dataset title, data file name and data file contentType

print('\nWriting dataset and file info to %s:' %(csvfilepath))

for pid in unique_dataset_pids:
	# Construct "Get Versions" API url
	if apikey:
		url='https://dataverse.harvard.edu/api/datasets/:persistentId/versions/?persistentId=%s&key=%s' %(pid, apikey)
	else:
		url='https://dataverse.harvard.edu/api/datasets/:persistentId/versions/?persistentId=%s' %(pid)
	# Store dataset and file info from API call to "data" variable
	data=json.load(urlopen(url))

	# Save dataset title, URL and publication state
	ds_title=data['data'][0]['metadataBlocks']['citation']['fields'][0]['value']
	datasetPersistentId=data['data'][0]['datasetPersistentId']
	datasetURL='https://dataverse.harvard.edu/dataset.xhtml?persistentId=%s' %(datasetPersistentId)
	versionState=data['data'][0]['versionState']
	datasetURL_pubstate='%s (%s)' %(datasetURL, versionState)

	# If the dataset contains files, write dataset and file info (file name, contenttype, and size) to the CSV
	if data['data'][0]['files']:
		for datafile in data['data'][0]['files']:
			datafilename=datafile['label']
			datafilesize=datafile['dataFile']['filesize']
			contentType=datafile['dataFile']['contentType']
			datafileinfo='%s (%s; %s bytes)' %(datafilename, contentType, datafilesize)

			# Append fields to the csv file
			with open(csvfilepath, mode='a', encoding='utf-8') as opencsvfile:

				opencsvfile=csv.writer(opencsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				
				# Create new row with dataset and file info
				opencsvfile.writerow([datasetURL_pubstate, ds_title, datafileinfo])

				# As a progress indicator, print a dot each time a row is written
				sys.stdout.write('.')
				sys.stdout.flush()

	# Otherwise print that the dataset has no files
	else:
		with open(csvfilepath, mode='a') as opencsvfile:

			opencsvfile=csv.writer(opencsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			
			# Create new row with dataset and file info
			opencsvfile.writerow([datasetURL_pubstate, ds_title, '(no files found)'])

			# As a progress indicator, print a dot each time a row is written
			sys.stdout.write('.')
			sys.stdout.flush()
print('\n')
print('Finished writing info of %s dataset(s) and their file(s) to %s' %(len(unique_dataset_pids), csvfilepath))