from elasticsearch import Elasticsearch
from neo4j import GraphDatabase


location = 'data/scholar_paper_02.json'

# Connect to ES
es = Elasticsearch([{'host' : 'localhost', 'port' : 9200}])

# Connect to neo4j
uri = "bolt://localhost:7687/db/data/"
neo4jdriver = GraphDatabase.driver(uri, auth=("neo4j", "123"))