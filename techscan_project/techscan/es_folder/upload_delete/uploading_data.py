import json
from ...config import es
import pandas as pd

def upload_data(file_location, index_name): #Upload from local drive
	with open(file_location) as f:
		data = json.load(f)

	for i in range(len(data)):
		es.index(index = str(index_name), doc_type = str(index_name) + '_papers',
			body = data[i])

def upload_crawled_data(index_name, crawled_data):
	if index_name not in es.indices.get_alias().keys():
		es.indices.create(index = index_name)
		for i in range(len(crawled_data)):
			es.index(index = str(index_name), doc_type = str(index_name) + '_papers',
				body = crawled_data[i])
	else:
		unique_list = remove_duplicate(index_name, crawled_data)
		for i in range(len(unique_list)):
			es.index(index = str(index_name), doc_type = str(index_name) + '_papers',
				body = unique_list[i])

def remove_duplicate(index_name, crawled_data):
	if index_name not in es.indices.get_alias().keys():
		es.indices.create(index = index_name)
	res = es.search (index = index_name, size = 10000, scroll = '2m', body = {'query':{"match_all":{}}})['hits']['hits']
	es_data = []
	for each_es_data in res:
		es_data.append(each_es_data['_source'])
	# es_data = [each_es_data['_source'] for each_es_data in res]
	df_es_data = pd.DataFrame(es_data)
	df_crawled_data = pd.DataFrame(crawled_data).drop_duplicates(subset = 'summary', keep = 'first')
	json_crawled_data = df_crawled_data.to_dict('records')
	es_summary = df_es_data['summary'].tolist()
	unique_data = list()
	unique_data.extend([data for data in json_crawled_data if data['summary'] not in es_summary])
	return unique_data
	# for data in json_crawled_data:
	#     if data['summary'] not in es_summary:
	#         no_duplicate.append(data)
	# return unique_data

"""
Example on how to use function:
upload_data(location, 'news')
"""
# upload_data(location, 'tweets')