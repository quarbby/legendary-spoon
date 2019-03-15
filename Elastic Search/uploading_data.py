"""
Function uploads data. 
IF index DOES NOT exist, it will create a new one.
IF index ALREADY exists, data will be added.
"""
import json
import config
from config import location, es

def upload_data(file_location, index_name):
	#Load data from file location
	with open(file_location) as f:
		data = json.load(f)

	#Insert data into elastic search
	for i in range(len(data)):
		es.index(index = str(index_name), doc_type = str(index_name) + '_papers',
			body = data[i])

"""
Example on how to use function:
upload_data(location, 'news')
"""