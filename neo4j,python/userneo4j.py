from neo4j import GraphDatabase
from py2neo import Graph, Relationship, Node
from pprint import pprint


uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123"))

transit_list = []

def Match_name (Author1):
	with driver.session() as session:
			result = session.run("MATCH (a:Author{name:'"+Author1+ "'})-[r:wrote]->(a1:Title)" " RETURN a1.Title_name")
			
			
			# print(a1)
			for record in result:
        			rel = record["a1.Title_name"]
        			transit_list.append(rel)
        			# print(rel)
			print()
			for i in range (len(transit_list)):
					output = session.run("MATCH (a:Author)-[r1:wrote]-(t:Title{Title_name:'"+transit_list[i]+"'})" "WHERE NOT a.name = '"+Author1+"'" " RETURN DISTINCT a.name LIMIT 15" )
					print(transit_list[i])
					print('__________________________________________________________')
					count = -1
					for record in output:
        					rol = record["a.name"]
        					count += 1
        					
        					print(str(count+1) + ")" + rol)
					print('.............')
					print('.............')

def Match_Title(Author1):
	with driver.session() as session:
			result = session.run("MATCH (a:Author)-[r:wrote]->(a1:Title{Title_name:'"+Author1+"'})" " RETURN  a.name")
			
			

			# print(a1)
			for record in result:
        			rel = record["a.name"]
        			transit_list.append(rel)
        			pprint(rel)
			print()
			for i in range (len(transit_list)):
					output = session.run("MATCH (a:Author{name:'"+transit_list[i]+ "'})-[r1:wrote]-(t:Title)" " RETURN DISTINCT t.Title_name LIMIT 15" )
					print(transit_list[i])
					print('__________________________________________________________')
					count = -1
					for record in output:
        					rol = record["t.Title_name"]
        					count += 1
        					
        					print(str(count+1) + ")" + rol)
					print('.............')
					print('.............')

def Recommend_Author (Author1,Paper_title):
	with driver.session() as session:
			result = session.run("MATCH (a:Author)-[r:wrote]->(t:Title{Title_name:'"+Paper_title+"'})" " WHERE NOT a.name = '" + Author1 +"'" " RETURN a.name")
			

			# print(a1)
			for record in result:
        			rel = record["a.name"]
        			transit_list.append(rel)
        			# pprint(rel)

			for i in range (len(transit_list)):
					output = session.run("MATCH (a:Author{name:'"+transit_list[i]+ "'})-[r1:wrote]-(t:Title)" " RETURN DISTINCT t.Title_name LIMIT 15" )
					print(transit_list[i])
					print('__________________________________________________________')
					count = -1
					for record in output:
        					rol = record["t.Title_name"]
        					count += 1
        					
        					print(str(count+1) + ")" + rol)
					print('.............')
					print('.............')

def Worked_With (Author1,Paper_title):
	with driver.session() as session:
			result = session.run ("MATCH (a:Author)-[r1:wrote]->(t:Title)<-[r2:wrote]-(a1:Author)" "WHERE a.name = '"+Author1+"' and a1.name = '"+Paper_title+"'" "RETURN DISTINCT t.Title_name")
			for record in result:
	        			rel = record["t.Title_name"]
	        			transit_list.append(rel)
	        			pprint(rel)
			print()
			for i in range (len(transit_list)):
						output = session.run("MATCH (a:Author)-[r1:wrote]-(t:Title{Title_name:'"+transit_list[i]+"'})"  " WHERE NOT a.name = '"+ Author1 +"' and NOT a.name = '"+ Paper_title +"'" " RETURN DISTINCT a.name LIMIT 15" )
						print(transit_list[i])
						print('__________________________________________________________')
						count = -1
						for record in output:
	        					rol = record["a.name"]
	        					count += 1
	        					
	        					print(str(count+1) + ")" + rol)
						print('.............')
						print('.............')

def Matching_ranking(Author1,Paper_title) :
	with driver.session() as session:
			session.run("MATCH (a:node{rank_types:"+Author1+ "})-[r:rel]->(a1:node{rank_types:'" + Paper_title +"})" "RETURN a,a.Rankings ORDER BY a.Rankings DESC Limit 15")

def Matching_community(Author1,Paper_title):
	with driver.session() as session:
			session.run("MATCH (a:node{rank_types:"+Author1+ "})-[r:rel]->(a1:node{rank_types:'" + Paper_title +"})" "RETURN a,a.Community ORDER BY a.Community DESC Limit 15")

Author1 = []
Author2 = []
Paper_title = "Multi-task Neural Networks for QSAR Predictions"
# Match_name(Author1)
# Match_Title(Author1)
if Author2 != []:
	print(Author1 + " and " + Author2 + " wrote: ")
	Worked_With (Author1,Author2)

if Author1 != [] and Paper_title != [] and Author2==[]:
	print (Author1 + " wrote '" + Paper_title + "' with:" )
	print('')
	Recommend_Author(Author1,Paper_title)
	# print()
	# print (Author1 + " also wrote:")
	# Match_name(Author1)
	# print()
	# print (Author1 + " also worked with the following authors")
	# Worked_With (Author1)


elif Author1 != [] and Paper_title == [] and Author2==[]:
	print (Author1 + " wrote :" )
	Match_name(Author1)
	# print (Author1 + " also worked with the following authors:")
	# Worked_With (Author1)
elif Author1 == [] and Paper_title != [] and Author2==[]:
	
	print (Paper_title + " written by :" )
	print ()
	Match_Title (Paper_title)



