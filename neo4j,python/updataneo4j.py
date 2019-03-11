from neo4j import GraphDatabase
from py2neo import Graph, Relationship, Node

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123"))

# def Create_Node (name):
# 	person_name = Node("Person", name)

def Define_contraint(noode, ID):
	with driver.session() as session:
		session.run("Create constraint on (a:"+noode+") Assert a." + ID + " is unique")

def Create_Node(name):
	with driver.session() as session:
		session.run("Create (a:Person{name:'"+ name +"'})")

def Create_relation(name1,name2):
	with driver.session() as session:
 		session.run("MATCH (a:Person{name:'"+ name1+ "'}), (a1:Person{name:'" + name2 + "'})" " CREATE (a)-[r:knows]->(a1)")
# Create_relation("Alice","Bob")
Define_contraint ("Person","age")

def Matching_nodes(keyword1,keyword2):
	with driver.session() as session:
 		session.run("")
	