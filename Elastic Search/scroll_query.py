"""
Query with a scroll id
- Allows displaying of results more than limit
- Maximum limit: size = 10000

After query, place results into a DATAFRAME.
returns a DATAFRAME
"""

import pandasticsearch
import pandas as pd
import numpy as np
from pandasticsearch import Select
from elasticsearch import Elasticsearch
from indexes import indexes

es = Elasticsearch([{'host' : 'localhost', 'port' : '9200'}])

#convert query results to pandas dataframe
def processing_hits(res):
	df = Select.from_dict(res).to_pandas()
	return df

def query(key_word):


	#Query from all indexes available

	res = es.search(size = 10, scroll = '2m', body = {"query" : {
		"match" : {"summary" : key_word}
		}})

	#Get the scroll id
	sid = res['_scroll_id']
	scroll_size = len(res['hits']['hits'])

	#Put first half of data into a dataframe
	df = processing_hits(res)
	# df = df.insert(index = indexes[i])

	#Scroll and append into the dataframe
	while scroll_size > 0 :
		res = es.scroll(scroll_id = sid, scroll = '2m')
		df = df.append(processing_hits(res), sort = True)
		sid = res['_scroll_id']
		scroll_size = len(res['hits']['hits'])
		# df = df.insert(index, indexes[i])

	#reset the index and print the dataframe
	df = df.reset_index(drop = True)
	# print(df.summary)

	return (df)

"""
Example on using this function:
df = query('machine')
print(df)
"""

df = query('economics')
print(df.iloc[1])
# print(df)