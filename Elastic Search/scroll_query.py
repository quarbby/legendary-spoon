import pandasticsearch
from pandasticsearch import Select
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host' : 'localhost', 'port' : '9200'}])

#convert query results to pandas dataframe
def processing_hits(res):
	df = Select.from_dict(res).to_pandas()
	return df

"""
Query with a scroll id
- Allows displaying of results more than limit
- Maximum limit: size = 10000

After query place into a dataframe.
Uses machine learning as an example
"""

# def query(index, key_word):
res = es.search(index = 'scholar', size = 10000, scroll = '2m' , body={"query" : {
	"match": {"summary" : 'economics'}}})

#get the scroll id
sid = res['_scroll_id']
scroll_size = len(res['hits']['hits'])

#Put first half of data into a dataframe
df = processing_hits(res)

#Scroll and append into the dataframe
while scroll_size > 0 :
	res = es.scroll(scroll_id = sid, scroll = '2m')
	df = df.append(processing_hits(res))
	sid = res['_scroll_id']
	scroll_size = len(res['hits']['hits'])

#reset the index and print the dataframe
df = df.reset_index(drop = True)
# print(df.summary)