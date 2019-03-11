from neo4j import GraphDatabase
from py2neo import Graph, Relationship, Node

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123"))

# def Create_Node (name):
# 	person_name = Node("Person", name)
def Matching_ranking(keyword1,keyword2)
	with driver.session() as session:
			session.run("Matching (a:node{rank_types:"+keyword1+ "})")
