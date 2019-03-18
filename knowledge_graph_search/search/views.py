from django.shortcuts import render
from django.http import HttpResponse
from .ElasticSearch import scroll_query
from neo4j import GraphDatabase
# Create your views here.

uri = "bolt://localhost:7687/db/data/"
neo4jdriver = GraphDatabase.driver(uri, auth=("neo4j", "123"))
def index(request):
	return render(request, 'index.html')

def search_word(request):
	params = request.GET.get('q')
	query_result = scroll_query.query(params)
	neo4jresult = []
	with neo4jdriver.session() as session:
		result = session.run("MATCH (f:Field{{fieldName:'{}'}})<-[:PART_OF_FIELD]-(f2:Field) RETURN f2.fieldName LIMIT 25".format(params))
		print (type(result))
		for record in result:
			a = record['f2.fieldName']
			neo4jresult.append(a)
	return HttpResponse('Neo4j Stuff{} ElasticSearch Stuff{}'.format(neo4jresult,query_result), end ='')

