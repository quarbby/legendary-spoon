import pandasticsearch
import pandas as pd
import numpy as np
from pandasticsearch import Select
import re
from ..config import es

#convert query results to pandas dataframe
def processing_hits(res):
	df = Select.from_dict(res).to_pandas()
	return df

def text_query(keyword, indexes = '_all', sizes = 100):

	#Query from all indexes available

	# res = es.search(index = str(indexes) , size = 10, scroll = '2m', body = {"query" : {
	# 	"match" : {"summary" : keyword}
		# }})
	
	res = es.search(index = str(indexes) , size = int(sizes), scroll = '2m', body = {"query" : {
		"match" : {"summary" : keyword}
		}})
	df = processing_hits(res)
	if df is None:
		return ([],[])
	if indexes == 'weibo' or indexes == 'tweets':
		df = df.sort_values(['favorite_count'], ascending = False)
		df = df.reset_index(drop = True)
		json_frame = df.to_dict('index').values()
	elif indexes == 'zhihu':
		df = df.sort_values(['upvotes'], ascending = False)
		df = df.reset_index(drop = True)
		json_frame = df.to_dict('index').values()
	else:
		df = df.reset_index(drop = True)
		json_frame = df.to_dict('index').values()
	return df, json_frame
	

def graph_query(keyword, indexes = '_all'):

	res = es.search(index = str(indexes) , size = 10, scroll = '2m', body = {"query" : {
		"match" : {"summary" : keyword}
		}})
	df = processing_hits(res)

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
	if df is not None:
		df = df.reset_index(drop = True)
		json_frame = df.to_dict('index').values()
		
		return df, json_frame
	else:
		# json_frame = df.to_dict('index').values()
		return (df,[])

def sub_query(keyword, indexes = '_all', sizes = 100):

	#Query from all indexes available

	# res = es.search(index = str(indexes) , size = 10, scroll = '2m', body = {"query" : {
	# 	"match" : {"summary" : keyword}
		# }})
	
	res = es.search(index = str(indexes) , size = int(sizes), scroll = '2m', body = {"query" : {
		"match" : {"summary" : keyword}
		}})
	df = processing_hits(res)
	sid = res['_scroll_id']
	scroll_size = len(res['hits']['hits'])

	while scroll_size > 0 :
		res = es.scroll(scroll_id = sid, scroll = '2m')
		df = df.append(processing_hits(res), sort = True)
		sid = res['_scroll_id']
		scroll_size = len(res['hits']['hits'])

	if df is None:
		return ([],[])
	if indexes == 'weibo' or indexes == 'tweets':
		df = df.sort_values(['favorite_count'], ascending = False)
		df = df.reset_index(drop = True)
		df = df[:20]
		df['published'] = df['published'].apply(lambda x:  ' '.join(re.sub('T\S+', '', x).split()))
		json_frame = df.to_dict('index').values()
	elif indexes == 'zhihu':
		df = df.sort_values(['upvotes'], ascending = False)
		df = df.reset_index(drop = True)
		df = df[:20]
		df['published'] = df['published'].apply(lambda x:  ' '.join(re.sub('T\S+', '', x).split()))
		json_frame = df.to_dict('index').values()
	else:
		df = df.reset_index(drop = True)
		df = df[:20]
		df['published'] = df['published'].apply(lambda x:  ' '.join(re.sub('T\S+', '', x).split()))
		json_frame = df.to_dict('index').values()
	return df, json_frame

"""
Example on using this function:
df = query('machine')
print(df)
"""