from ..config import neo4jdriver
import json
import ast

transit_list = []
def Match_name (Author1, location = 'C:/BigProject/knowledge_graph_search/search/Neo4jFolder/data/data.json'):
	with neo4jdriver.session() as session:
		session.run("CALL apoc.export.json.query('MATCH f=(a:Author)<-[r:WRITTEN_BY]-(b:ScholarPaper) WHERE a.authorName = {}{}{} optional match e = (l:Author)<-[r1:WRITTEN_BY]-(b) return f,e ','C:/BigProject/knowledge_graph_search/search/Neo4jFolder/data/data.json', {{params:{{age:10}}}})".format('"',Author1,'"'))
	with open(location, 'r+') as f:
		data = f.read()
		papers = ['{"f":'+ element for element in data.split('{"f":')[1:]]
		papers = [ast.literal_eval(element) for element in papers]	
	return papers
			
def Match_Title(paperTitle,location = 'C:/BigProject/knowledge_graph_search/search/Neo4jFolder/data/data.json'):
	with neo4jdriver.session() as session:
		session.run("CALL apoc.export.json.query('MATCH f=(a:Author)<-[r:WRITTEN_BY]-(b:ScholarPaper) WHERE b.paperTitle = {}{}{} optional match e = (a)-[r1:WRITTEN_BY]-(l:ScholarPaper) return f,e','C:/BigProject/knowledge_graph_search/search/Neo4jFolder/data/data.json',{{params:{{age:10}}}})".format('"',paperTitle,'"'))
		with open(location) as f:
			data = json.load(f)
	return data

def Worked_With (Author1,Author2, location = 'C:/BigProject/knowledge_graph_search/search/Neo4jFolder/data/data.json'):
	with neo4jdriver.session() as session:
		session.run("CALL apoc.export.json.query('match f = (a:Author)<-[r1:WRITTEN_BY]-(p:ScholarPaper)<-[r2:WRITTEN_BY]-(b:Author) WHERE a.authorName = {}{}{} and b.authorName = {}{}{} return f', 'C:/BigProject/knowledge_graph_search/search/Neo4jFolder/data/data.json', {{params:{{age:10}}}})".format('"',Author1,'"','"',Author2,'"'))
		with open(location) as f:
			data = json.load(f)
	return data
			
