import pandasticsearch
import pandas as pd
import numpy as np
from pandasticsearch import Select
import re
from ..config import es


def processing_hits(res):
#convert query results to pandas dataframe

	df = Select.from_dict(res).to_pandas()
	return df

def text_query(keyword, indexes = '_all', sizes = 100, dataframe = False):
#Query from all indexes available, output either in dataframe or json by default will return json

	res = es.search(index = str(indexes) , size = int(sizes), scroll = '2m', body = {"query" : {
		"match_phrase" : {"summary" : keyword} # match_phrase for and match
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
		return []
	else:
		if dataframe == True:
			return df
		else:
			json_frame = df.to_dict('records')
			return json_frame