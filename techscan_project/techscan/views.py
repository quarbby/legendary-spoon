from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import RedirectView
from django.template.loader import render_to_string
from .es_folder import main_functions, scroll_query, plotgraph, crawler
from .es_folder.upload_delete import uploading_data
from .neo4j_folder import neo4jgraph
from .crawler_list import keywords
import time

def index(request):
	return render(request, 'index.html')

def update(request):
	start_time = time.time()
	crawler.weibo_login()
	for keyword in keywords:
	    for site in keyword['sites']:
	        if site['source'] == 'tweets':
	            uploading_data.upload_crawled_data(site['source'], crawler.crawl_twitter(site['url']))
	        elif site['source'] == 'zhihu':
	            uploading_data.upload_crawled_data(site['source'], crawler.crawl_zhihu(site['url']))
	        elif site['source'] == 'news':
	        	uploading_data.upload_crawled_data(site['source'], crawler.crawl_news(site['url']))
	        elif site['source'] == 'scholar':
	        	uploading_data.upload_crawled_data(site['source'], crawler.crawl_scholar(site['url']))
	        if site['source'] == 'weibo':
	        	uploading_data.upload_crawled_data(site['source'], crawler.crawl_weibo(site['url']))

	list_of_keywords = [kw['keyword'] for kw in keywords]

	for params in list_of_keywords:
		# es_zhihu, es_tweets, es_scholar, es_news, es_weibo = plotgraph.sort_by_dates(params)
		es_weibo = scroll_query.text_query(main_functions.chi_translation(params),'weibo')
		es_scholar = scroll_query.text_query(params,'scholar')
		es_news = scroll_query.text_query(main_functions.chi_translation(params),'news')
		es_tweets = scroll_query.text_query(params,'tweets')
		es_zhihu = scroll_query.text_query(main_functions.chi_translation(params),'zhihu')
		context = {
			"search_word": params,
			"chi_translation": main_functions.chi_translation(params),
			"weibo": es_weibo,
			"news":es_news,
			"scholar":es_scholar,
			"tweets":es_tweets,
			"zhihu":es_zhihu,
			"keywords": list_of_keywords
			# "author_table":main_functions.overview_table(params),
			# "company_table":plotgraph.top_companies(params)
		}

		content = render_to_string('details_template.html', context)
		with open('techscan/pages/'+ params + '.html','w', encoding='utf8') as static_file:
			static_file.write(content)

	time_taken = " %s seconds " % (time.time() - start_time)
	return HttpResponse('Done. Time taken to complete: {}. Generated {} templates on {}'.format(time_taken, len(list_of_keywords), list_of_keywords))

def main(request):
	params = request.GET.get('q')
	wiki_result_short, wiki_result_long, summary_length = main_functions.get_wiki_data(params)
	# neo4jgraph.plotgraph(neo4jgraph.search_field(params))
	plotgraph.main_graph(params)
	# plotgraph.plot_stocks(params)
	# plotgraph.heatmap(params)
	# plotgraph.people_companies_wordcloud(params)
	context = {
		"chi_translation": main_functions.chi_translation(params),
		"search_word": ' '.join([word.capitalize() for word in params.split()]),
		"wiki_result_short": wiki_result_short,
		"wiki_result_long": wiki_result_long,
		"summary_length": summary_length,
		"hit_count": main_functions.get_count(params),
		"related_table": neo4jgraph.get_related_table(params),
		# "author_table":main_functions.overview_table(params),
		"network": neo4jgraph.plotgraph(neo4jgraph.search_field(params))
	}
	return render(request, 'main.html', context)

def details(request):
	params = request.GET.get('q')
	# plotgraph.detail_hashtag_frequency(params)
	# plotgraph.top_companies(params, graph = True)
	# plotgraph.twitter_bubble(params)

	es_weibo = scroll_query.text_query(main_functions.chi_translation(params),'weibo')
	es_scholar = scroll_query.text_query(params,'scholar')
	es_news = scroll_query.text_query(main_functions.chi_translation(params),'news')
	es_tweets = scroll_query.text_query(params,'tweets')
	es_zhihu = scroll_query.text_query(main_functions.chi_translation(params),'zhihu')
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"weibo": es_weibo,
		"news":es_news,
		"scholar":es_scholar,
		"tweets":es_tweets,
		"zhihu":es_zhihu,
		"author_table":main_functions.overview_table(params),
		"company_table":plotgraph.top_companies(params)
	}

	return render(request,'details.html',context)

def weibo(request):
	params = request.GET.get('q')
	# plotgraph.top_hashtag(params)
	# plotgraph.wordcloud(main_functions.chi_translation(params))
	es_weibo = scroll_query.text_query(main_functions.chi_translation(params),'weibo')
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"weibo":es_weibo,
		"weibo_table":main_functions.weibo_author(main_functions.chi_translation(params)),
	}
	return render(request, 'weibo.html', context)

def scholar(request):
	params = request.GET.get('q')
	es_scholar = scroll_query.text_query(params,'scholar')
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"scholar":es_scholar,
	}
	return render(request, 'scholar.html', context)

def news(request):
	params = request.GET.get('q')
	es_news = scroll_query.text_query(main_functions.chi_translation(params),'news', sizes = 5)
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
	es_tweets = scroll_query.text_query(params,'tweets')
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"tweets": es_tweets,
		"author_table": main_functions.twitter_author(params)
	}
	return render(request, 'tweets.html', context)

def zhihu(request):
	params = request.GET.get('q')
	es_zhihu = scroll_query.text_query(main_functions.chi_translation(params),'zhihu')
	context = {
		"search_word": params,
		"chi_translation": main_functions.chi_translation(params),
		"zhihu":es_zhihu,
		"author_table":main_functions.get_zh_author(main_functions.chi_translation(params)),
	}
	return render(request, 'zhihu.html', context)

