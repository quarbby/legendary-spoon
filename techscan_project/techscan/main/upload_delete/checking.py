from elasticsearch import Elasticsearch

es = Elasticsearch([{'host' : 'localhost', 'port' : 9200}])

def check(keyword, indexes):
	res = es.search(index = indexes, size=5, body={"query": {"match": {'summary' : keyword}}})
	return (res['hits']['total'])


# print(check('artificial intelligence','tweets'))