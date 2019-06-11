"""
Function uploads data. 
IF index DOES NOT exist, it will create a new one.
IF index ALREADY exists, data will be added.
"""
import json
from ..config import es


"""
Example on how to use function:
upload_data(location, 'news')
"""
# upload_data(location, 'weibo')

def upload_data_ner(data, index_name):

	for i in range(len(data)):
		es.index(index = str(index_name), doc_type = str(index_name) + '_papers',
			body = data[i])
