"""
Function uploads data. 
IF index DOES NOT exist, it will create a new one.
IF index ALREADY exists, data will be added.
"""
import json
from ..config import es
import pandas as pd


"""
Example on how to use function:
upload_data(location, 'news')
"""
# upload_data(location, 'weibo')

def upload_data_ner(index_name, data):
	if index_name not in es.indices.get_alias().keys():
		es.indices.create(index = index_name)
		for i in range(len(data)):
			es.index(index = str(index_name), doc_type = str(index_name) + '_papers',
				body = data[i])
	else:
		unique_list = remove_duplicate_heatmap(index_name, data)
		for i in range(len(unique_list)):
			es.index(index = str(index_name), doc_type = str(index_name) + '_papers',
				body = unique_list[i])

def remove_duplicate_heatmap (index_name, FinalIP):
	if index_name not in es.indices.get_alias().keys():
		es.indices.create(index = index_name)
	res = es.search (index = index_name, size = 10000, scroll = '2m', body = {'query':{"match_all":{}}})['hits']['hits']
	es_data = []
	for each_es_data in res:
		es_data.append(each_es_data['_source'])
	# es_data = [each_es_data['_source'] for each_es_data in res]
	df_es_data = pd.DataFrame(es_data)
	df_crawled_data = pd.DataFrame(FinalIP).drop_duplicates(subset = 'publisher', keep = 'first')
	json_crawled_data = df_crawled_data.to_dict('records')
	es_publisher = df_es_data['publisher'].tolist()
	unique_data = list()
	unique_data.extend([data for data in json_crawled_data if data['publisher'] not in es_publisher])
	return unique_data