from elasticsearch import Elasticsearch
from neo4j import GraphDatabase


location = 'data/AI_tweets_03.json'

# Connect to ES
es = Elasticsearch([{'host' : 'localhost', 'port' : 9200}])

# Connect to neo4j
try:
	uri = "bolt://localhost:11001/db/data/"
	neo4jdriver = GraphDatabase.driver(uri, auth=("neo4j", "123"))
except:
	print("Not Connected to Neo4j!")