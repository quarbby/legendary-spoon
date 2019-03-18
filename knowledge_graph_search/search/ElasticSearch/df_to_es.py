import json
import pandas as pd
from config import es
from elasticsearch.helpers import bulk

"""
This function will put the dataframe
back into elastic search such that original query
can be processed using pandas and called using elastic search.

**NOTE**
Use a delete index to remove index:"results"
prior to a second query else error will occur.
"""

def pd_to_es(df):

	#Drop conflicting columns
	df['Original index'] = df['_index']
	df = df.drop(["_index", "_id",
		"_score", "_type"], axis = 1)

	#Fill null values with 0 and ensure df can be read by es
	df = df.fillna(0)
	df = df.astype(str)
	df = df.reindex()
	results = df.to_dict(orient = 'records')

	#Create an index and store "results"
	es.indices.create(index='results',body={})
	bulk(es, results, index = 'results', doc_type = 'results_papers')