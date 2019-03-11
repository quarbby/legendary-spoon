import json
from elasticsearch import Elasticsearch
import config
from config import location

#Connect to DB
es = Elasticsearch([{'host':'localhost', 'port':9200}])

#Load scholar paper data
with open(location) as f:
	data = json.load(f)

#insert scholar paper data into elastic search
for i in range(len(data)):
	es.index(index = 'scholar', doc_type = 'scholar paper', id = i, body = data[i])

#Check if data have been uploaded
res = es.search(index = 'scholar', size=5, body={"query": {"match_all": {}}})
print('%d hits' %res['hits']['total'])