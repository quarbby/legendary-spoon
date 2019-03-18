from config import es
from pprint import pprint
from indexes import indexes

for i in range(len(indexes)):
	res = es.search(index = str(indexes[i]), size=5, body={"query": {"match_all": {}}})
	print('%d hits' %res['hits']['total'])