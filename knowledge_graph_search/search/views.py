from django.shortcuts import render
from django.http import HttpResponse
from .ElasticSearchFolder import scroll_query, paper_count, plotgraph
from .Neo4jFolder import neo4jgraph
import json
from textblob import TextBlob

def chi_keyword(keyword):
	word = TextBlob(str(keyword))
	chinese = word.translate(to = 'zh')
	return (str(chinese))

def eng_keyword(keyword):
	word = TextBlob(str(keyword))
	english = word.translate(to = 'en')
	return (str(english))

def index(request):
	return render(request, 'index.html')

def search_word(request):

	# try:
		params = request.GET.get('q')
		# plotgraph.plot_pie_chart(params)
		# plotgraph.multi_year(params, 'scholar')
		# plotgraph.count_date(params, 'news')
		# plotgraph.count_date(params, 'tweets')
		# plotgraph.count_date(chi_keyword(params), 'weibo')


		_,es_result_news = scroll_query.text_query(params,'news')
		_,es_result_scholar = scroll_query.text_query(params,'scholar')
		_,es_result_tweets = scroll_query.text_query(params,'tweets',15)
		_,es_result_weibo = scroll_query.text_query(chi_keyword(params),'weibo',15)
		graph,_ = neo4jgraph.plotgraph(neo4jgraph.search_field(params))
		
		eng_summary = [eng_keyword(list(es_result_weibo)[i]['summary']) for i in range(4)]

		context = {
			"searchTerm": params,
			"elasticSearchNews": es_result_news,
			"elasticSearchScholar": es_result_scholar,
			"elasticSearchTweets": es_result_tweets,
			"elasticSearchWeibo": zip(es_result_weibo,eng_summary),
			"chiKeyword": chi_keyword(params),
			# "translate": eng_summary,
		}
		return render(request, 'results.html', context)
		# return HttpResponse(eng_summary)
		
	# except:
		# 
