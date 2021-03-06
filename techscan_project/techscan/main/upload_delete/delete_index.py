from elasticsearch import Elasticsearch

es = Elasticsearch([{'host' : 'localhost', 'port' : 9200}])

def delete_indices(index_name):
	res = es.indices.get_alias().keys()
	if str(index_name) in res:
		#Delete index.
		es.indices.delete(index = str(index_name), ignore = [400, 404])
	else:
		print('Index does not exist')

delete_indices('scholar')




# res = es.search(index = 'tweets', size = 10000, scroll = '2m' , body= {"query": {"match_all": {}}})['hits']['hits']
# print(res[0]['_source'])