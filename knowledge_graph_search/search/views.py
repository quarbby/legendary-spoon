from django.shortcuts import render
from django.http import HttpResponse
from .ElasticSearchFolder import scroll_query, paper_count, plotgraph
from .Neo4jFolder import neo4j_ace_query, neo4j_main_query, neo4jgraph
import json
from textblob import TextBlob

def chi_keyword(keyword):
	word = TextBlob(str(keyword))
	chinese = word.translate(to = 'zh')
	return (str(chinese))

def index(request):
	return render(request, 'index.html')

def search_word(request):

	# try:
		params = request.GET.get('q')
		# plotgraph.plot_pie_chart(params)
		# plotgraph.multi_year(params, 'scholar')
		# plotgraph.count_date(params, 'news')
		# plotgraph.count_date(params, 'tweets')

		_,es_result_news = scroll_query.text_query(params,'news')
		_,es_result_scholar = scroll_query.text_query(params,'scholar')
		_,es_result_tweets = scroll_query.text_query(params,'tweets',15)
		_,es_result_weibo = scroll_query.text_query(chi_keyword(params),'weibo',15)
		neo4jgraph.plot_neo4j_graph()
		# neo4j_field_result = neo4j_ace_query.related_field(params)
		# neo4j_author_result = neo4j_ace_query.related_author(params)
		# neo4j_paper_result = neo4j_ace_query.related_paper(params)

		context = {
			"searchTerm": params,
			"elasticSearchNews": es_result_news,
			"elasticSearchScholar": es_result_scholar,
			"elasticSearchTweets": es_result_tweets,
			"elasticSearchWeibo": es_result_weibo,
			# "neo4j_field": json.loads(neo4j_field_result),
			# "neo4j_author" : json.loads(neo4j_author_result),
			"chiKeyword": chi_keyword(params)
			# "neo4j_paper" : json.loads(neo4j_paper_result),
		}
		return render(request, 'results.html', context)
		
	# except:
		# 
