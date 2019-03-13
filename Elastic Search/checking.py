from elasticsearch import Elasticsearch
from pprint import pprint

es = Elasticsearch([{'host':'localhost', 'port':9200}])

res = es.search(index = 'news', size=5, body={"query": {"match_all": {}}})
print('%d hits' %res['hits']['total'])
print(res)