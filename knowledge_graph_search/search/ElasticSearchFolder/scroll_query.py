import pandasticsearch
import pandas as pd
import numpy as np
from pandasticsearch import Select
from ..config import es

#convert query results to pandas dataframe
def processing_hits(res):
	df = Select.from_dict(res).to_pandas()
	return df

def text_query(keyword, indexes = '_all', sizes = 5):

	#Query from all indexes available

	# res = es.search(index = str(indexes) , size = 10, scroll = '2m', body = {"query" : {
	# 	"match" : {"summary" : keyword}
		# }})
	try:
		res = es.search(index = str(indexes) , size = int(sizes), scroll = '2m', body = {"query" : {
			"match" : {"summary" : keyword}
			}})
		if indexes == 'weibo' or indexes == 'tweets':
			df = processing_hits(res)
			df = df.sort_values(['favorite_count'], ascending = False)
			df = df.reset_index(drop = True)
			json_frame = df.to_dict('index').values()
		else:
			df = processing_hits(res)
			df = df.reset_index(drop = True)
			json_frame = df.to_dict('index').values()
		return df, json_frame
	except:
		return ('No Data','No Data')

def graph_query(keyword, indexes = '_all'):

	#Query from all indexes available

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
	df = df.reset_index(drop = True)
	json_frame = df.to_dict('index').values()
	
	return df, json_frame


# def text_query(keyword):
# 	df = query(str(keyword))
# 	json_frame = df.to_dict('index')
# 	return(json_frame)


"""
Example on using this function:
df = query('machine')
print(df)
"""