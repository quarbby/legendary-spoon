from ..config import neo4jdriver
import json

def related_field(keyword):
	with neo4jdriver.session() as session:
		relatedField = session.run("MATCH (f:Field)<-[:PART_OF_FIELD]-(f1:Field:SubGraphCS) WHERE f.fieldName =~ '(?i).*{}.*' RETURN DISTINCT f1.fieldName,f1.fieldPaperNum ORDER BY f1.fieldPaperNum DESC LIMIT 5".format(keyword))
	relatedField_list = [{"fieldName" : record['f1.fieldName']} for record in relatedField]
	
	if len(relatedField_list) < 5:
		with neo4jdriver.session() as session:
			relatedField = session.run("MATCH (f:Field)-[:PART_OF_FIELD]-(f1:Field:SubGraphCS) WHERE f.fieldName =~ '(?i).*{}.*' RETURN DISTINCT f1.fieldName,f1.fieldPaperNum ORDER BY f1.fieldPaperNum DESC LIMIT 5".format(keyword))
		relatedField_list.extend([{"fieldName" : record['f1.fieldName']} for record in relatedField])

	return(json.dumps(relatedField_list))
	
def related_paper(keyword):
	with neo4jdriver.session() as session:
		relatedPaper = session.run("MATCH (f:Field:SubGraphCS)<-[:PAPER_IN_FIELD]-(p:Paper:SubGraphCS) WHERE f.fieldName =~ '(?i).*{}.*' AND p.articleRank > 70 RETURN DISTINCT p.paperName, p.articleRank ORDER BY p.articleRank DESC LIMIT 5".format(keyword))
	relatedPaper_list = [{"paperName" : paper['p.paperName']} for paper in relatedPaper]
	return (json.dumps(relatedPaper_list))

def related_author(keyword):
	with neo4jdriver.session() as session:
		relatedAuthor = session.run("MATCH (f:Field:SubGraphCS)<-[:AUTHOR_IN_FIELD]-(a:Author) WHERE f.fieldName =~ '(?i).*{}.*' AND toInteger(a.citationCount) > 20 RETURN DISTINCT a.authorName, toInteger(a.citationCount) ORDER BY toInteger(a.citationCount) DESC LIMIT 5".format(keyword))
	relatedAuthor_list = [{"authorName" : author['a.authorName']} for author in relatedAuthor]
	return (json.dumps(relatedAuthor_list))