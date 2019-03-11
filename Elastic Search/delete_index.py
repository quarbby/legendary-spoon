from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port' : '9200'}])

#Delete indices. Rename index to whichever index you want to delete
es.indices.delete(index = 'papers', ignore = [400, 404])