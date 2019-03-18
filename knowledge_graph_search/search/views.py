from django.shortcuts import render
from django.http import HttpResponse
from neo4j import GraphDatabase
from elasticsearch import Elasticsearch
# Create your views here.

try:
	uri = "bolt://localhost:7687/db/data/"
	driver = GraphDatabase.driver(uri, auth=("neo4j", "123"))
	
except:
	print("Not connected to Neo4j database! ")


def index(request):
	return render(request, 'index.html')

def search_word(request):
	b = []
	params = request.GET.get('q')
	print(type(params))
	with driver.session() as session:
		result = session.run("MATCH (f:Field{fieldName:'" + params + "'})<-[:PART_OF_FIELD]-(f2:Field) RETURN f2.fieldName LIMIT 25")
		print (type(result))
		for record in result:
			a = record['f2.fieldName']
			b.append(a)
	return HttpResponse('The related fields are: {}'.format(b))

