from django.shortcuts import render
from django.http import HttpResponse
from .es_folder import main_functions, scroll_query, plotgraph
from .neo4j_folder import neo4jgraph
from django.views.generic import RedirectView

def index(request):
	return render(request, 'index.html')

def main(request):
	params = request.GET.get('q')
	# neo4jgraph.plotgraph(neo4jgraph.search_field(params))
	# plotgraph.main_graph(params)
	plotgraph.plot_stocks(params)
	plotgraph.heatmap(params)
	context = {
		"chi_translation": main_functions.chi_translation(params),
		"search_word": ' '.join([word.capitalize() for word in params.split()]),
		"wiki_result": main_functions.get_wiki_data(params),
		"hit_count": main_functions.get_count(params),
		"related_table": neo4jgraph.get_related_table(params),
	}
	return render(request, 'main.html', context)

def overview2(request):
	params = request.GET.get('q')
	_,es_weibo = scroll_query.text_query(main_functions.chi_translation(params),'weibo')
	_,es_news = scroll_query.text_query(main_functions.chi_translation(params),'news')
	_,es_scholar = scroll_query.text_query(params,'scholar', sizes = 100)
	_,es_tweets = scroll_query.text_query(params,'tweets')
	_,es_zhihu = scroll_query.text_query(main_functions.chi_translation(params),'zhihu')

	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"weibo":es_weibo,
		"news":es_news,
		"scholar":es_scholar,
		"tweets":es_tweets,
		"zhihu":es_zhihu,
	}
	return render(request, 'overview2.html', context)

def details(request):
	params = request.GET.get('q')
	# plotgraph.detail_hashtag_frequency(params)
	plotgraph.top_companies(params)
	# plotgraph.twitter_bubble(params)

	_,es_weibo = scroll_query.sub_query(main_functions.chi_translation(params),'weibo')
	_,es_scholar = scroll_query.sub_query(params,'scholar')
	_,es_news = scroll_query.sub_query(main_functions.chi_translation(params),'news')
	_,es_tweets = scroll_query.sub_query(params,'tweets')
	_,es_zhihu = scroll_query.sub_query(main_functions.chi_translation(params),'zhihu')
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"weibo": es_weibo,
		"news":es_news,
		"scholar":es_scholar,
		"tweets":es_tweets,
		"zhihu":es_zhihu,
		"author_table":main_functions.overview_table(params)
	}
	return render(request, 'details.html', context)

def weibo(request):
	params = request.GET.get('q')
	plotgraph.top_hashtag(params)
	plotgraph.wordcloud(main_functions.chi_translation(params))
	_,es_weibo = scroll_query.sub_query(main_functions.chi_translation(params),'weibo')
	# eng_summary = [main_functions.eng_translation(list(es_weibo)[i]['summary']) for i in range(4)]
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"weibo":es_weibo,
		# "weibo":zip(es_weibo,eng_summary),
		"weibo_table":main_functions.weibo_author(main_functions.chi_translation(params)),
	}
	return render(request, 'weibo.html', context)

def scholar(request):
	params = request.GET.get('q')
	_,es_scholar = scroll_query.sub_query(params,'scholar')
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"scholar":es_scholar,
	}
	return render(request, 'scholar.html', context)

def news(request):
	params = request.GET.get('q')
	_,es_news = scroll_query.text_query(main_functions.chi_translation(params),'news', sizes = 5)
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"news": es_news,
	}
	return render(request, 'news.html', context)

def tweets(request):
	params = request.GET.get('q')
	# plotgraph.twitter_bubble(params)
	# plotgraph.twitter_graph(params)
	# plotgraph.wordcloud((params), indexes = 'tweets')
	_,es_tweets = scroll_query.sub_query(params,'tweets')
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"tweets": es_tweets,
		"author_table": main_functions.twitter_author(params)
	}
	return render(request, 'tweets.html', context)

def zhihu(request):
	params = request.GET.get('q')
	_,es_zhihu = scroll_query.sub_query(main_functions.chi_translation(params),'zhihu')
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"zhihu":es_zhihu,
		"author_table":main_functions.get_zh_author(main_functions.chi_translation(params)),
	}
	return render(request, 'zhihu.html', context)

def facial_recognition(request):
	params = request.GET.get('q')
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
	}
	return render(request, 'facial_recognition.html', context)

def speech_text(request):
	params = request.GET.get('q')
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
	}
	return render(request, 'speech_text.html', context)