from neo4j import GraphDatabase
from py2neo import Graph, Relationship, Node

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123"))


def Match_name (keyword1):
	with driver.session() as session:
			result = session.run("MATCH (a:Author{name:'"+keyword1+ "'})-[r:wrote]->(a1:Title)" " RETURN a1.Title_name")
			
			print (Keyword1 + " wrote:")
			# print(a1)
			for record in result:
        			rel = record["a1.Title_name"]
        			print(rel)
def Match_Title(keyword1):
	with driver.session() as session:
			result = session.run("MATCH (a:Author)-[r:wrote]->(a1:Title{Title_name:'"+keyword1+"'})" " RETURN a.name")
			
			print (Keyword1 + " wrote by:")

			# print(a1)
			for record in result:
        			rel = record["a.name"]
        			print(rel)

def Matching_ranking(keyword1,keyword2) :
	with driver.session() as session:
			session.run("MATCH (a:node{rank_types:"+keyword1+ "})-[r:rel]->(a1:node{rank_types:'" + keyword2 +"})" "RETURN a,a.Rankings ORDER BY a.Rankings DESC Limit 15")

def Matching_community(keyword1,keyword2):
	with driver.session() as session:
			session.run("MATCH (a:node{rank_types:"+keyword1+ "})-[r:rel]->(a1:node{rank_types:'" + keyword2 +"})" "RETURN a,a.Community ORDER BY a.Community DESC Limit 15")

Keyword1 = "Yoon Kim"
Match_name(Keyword1)
Match_Title(Keyword1)


