import requests
from pprint import pprint
from textblob import TextBlob
from ..config import location, es
from .scroll_query import graph_query, processing_hits
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot

def chi_translation(keyword):
	try:
		word = TextBlob(str(keyword))
		chinese = word.translate(to = 'zh')
		return (str(chinese))
	except:
		return ('Translation not available')

def get_wiki_data(keyword):
	try:
		result = requests.get('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={}&exsentences=5'.format(keyword), verify=False).json()
		return result['query']['pages'][list(result['query']['pages'].keys())[0]]['extract']
	except:
		return('No summary found!')

def get_count(keyword):
	total_hits = []
	categories = ['weibo','news','tweets','scholar','zhihu']
	for category in categories:
		count = dict()
		count['category'] = category.capitalize()
		if category == 'tweets' or category == 'scholar':
			count['hit_count'] = check(keyword, category)
		else:
			count['hit_count'] = check(chi_translation(keyword), category)
		total_hits.append(count)
	return total_hits

def check(keyword, indexes):
	res = es.search(index = indexes, size=5, body={"query": {"match": {'summary' : keyword}}})
	return (res['hits']['total'])

def get_zh_author(keyword, graph = False):

	df,_ = graph_query(keyword, 'zhihu')
	if df is not None:
		upvotes_count = df.groupby(['author']).sum().reset_index().sort_values('upvotes', ascending=False)

		post_freq = df.groupby(['author']).size().rename('size').reset_index().sort_values('size', ascending = False)
		post_freq.rename(columns={'author': 'author_1'}, inplace=True)

		df_new = pd.concat([upvotes_count, post_freq], axis = 1).drop(columns = ['author_1'])
		df_new['average'] = (df_new['upvotes']/df_new['size']).astype(int)
		df_new['max'] = df.groupby('author', as_index=False)['upvotes'].max()['upvotes']
		df_new['weighted'] = (0.6 * df_new['max']) + (0.15*df_new['upvotes']) + (0.25*df_new['average'])

		df_new = df_new.sort_values('weighted',ascending = False).reset_index()[:10]
		if graph == True:
			df_new.sort_values('weighted',ascending = True)
			data = [go.Bar(
				marker=dict(color='rgb(85,118,154)'),
				x=df_new['size'],
				y=df_new['author'],
				orientation = 'h',
				)]

			layout = go.Layout(
				yaxis = go.layout.YAxis(
					title = go.layout.yaxis.Title(
						text = 'User',
						font = dict(
							family = '-webkit-body',
							size = 18,
							)
						)
					)
				)

			fig = dict(data = data, layout = layout)
			plot(fig, filename='techscan/templates/graph/zhihu_author_bar.html', auto_open=False)
		else:
			# df_new = df_new.reset_index(drop = True)
			json_frame = df_new.to_dict('index').values()
			return json_frame
	else:
		pass

def weibo_author(keyword):

	df,_ = graph_query(keyword, 'weibo')
	if df is not None:
		favorite_count = df.groupby(['user_name']).sum().reset_index().sort_values('favorite_count', ascending=False)

		post_freq = df.groupby(['user_name']).size().rename('size').reset_index().sort_values('size', ascending = False)
		post_freq.rename(columns={'user_name': 'user_name_1'}, inplace=True)

		df_new = pd.concat([favorite_count, post_freq], axis = 1).drop(columns = ['user_name_1'])
		df_new['average'] = (df_new['favorite_count']/df_new['size']).astype(int)
		df_new['max'] = df.groupby('user_name', as_index=False)['favorite_count'].max()['favorite_count']
		df_new['weighted'] = (0.6 * df_new['max']) + (0.15*df_new['favorite_count']) + (0.25*df_new['average'])

		df_new = df_new.sort_values('weighted',ascending = False).reset_index()[:10]
		json_frame = df_new.to_dict('index').values()
		return json_frame
	else:
		pass


# def get_percentile(indexes):
# 	res = es.search(index = indexes , size = 5, scroll = '2m', body = {"query" : {
# 		"match_all" : {}}})
  
# 	df = processing_hits(res)
# 	#Get the scroll id
# 	sid = res['_scroll_id']
# 	scroll_size = len(res['hits']['hits'])

# 	#Put first half of data into a dataframe
# 	df = processing_hits(res)

# 	#Scroll and append into the dataframe
# 	while scroll_size > 0 :
# 		res = es.scroll(scroll_id = sid, scroll = '2m')
# 		df = df.append(processing_hits(res), sort = True)
# 		sid = res['_scroll_id']
# 		scroll_size = len(res['hits']['hits'])
# 	df.reset_index(drop = True)
  
# 	if indexes == 'tweets':
# 		total_favorite_count = df.favorite_count.tolist()
# 		total_retweet_count = df.retweet_count.tolist()
# 		favorite_percentile_value = np.percentile(total_favorite_count, 85)
# 		retweet_percentile_value = np.percentile(total_retweet_count, 85)
# 		return retweet_percentile_value, favorite_percentile_value

# 	elif indexes == 'weibo':
# 		total_favorite_count = df.favorite_count.tolist()
# 		favorite_percentile_value = np.percentile(total_favorite_count, 85)
# 		return favorite_percentile_value

# 	elif indexes == 'zhihu':
# 		total_upvotes_count = df.upvotes.tolist()
# 		upvotes_percentile_value = np.percentile(total_upvotes_count, 85)
# 		return upvotes_percentile_value

# tweets_retweet_percentile, tweets_favorite_percentile = get_percentile('tweets')
# weibo_favorite_percentile = get_percentile('weibo')
# zhihu_upvote_percentile = get_percentile('zhihu')

# def percentile(keyword, indexes):
# 	if indexes == 'tweets':	
# 		df_keyword,_ = graph_query(str(keyword), indexes)
# 		if df_keyword is not None:
# 			df_positive = df_keyword[df_keyword.retweet_count >= tweets_retweet_percentile]
# 			top = len(df_positive)

# 	elif indexes == 'weibo':	
# 		df_keyword,_ = graph_query(chi_translation(keyword), indexes)
# 		if df_keyword is not None:
# 			df_positive = df_keyword[df_keyword.favorite_count >= weibo_favorite_percentile]
# 			top = len(df_positive)

# 	elif indexes == 'zhihu':
# 		df_keyword,_ = graph_query(chi_translation(keyword), indexes)
# 		if df_keyword is not None:
# 			df_positive = df_keyword[df_keyword.upvotes >= zhihu_upvote_percentile]
# 			top = len(df_positive)

# 	if df_keyword is not None:
# 		if top >= (0.1* len(df_keyword)):
# 			return "True"

# 	else:
# 		return "False"

def overview_table(keyword):
	df_twitter,_ = graph_query(str(keyword), 'tweets')
	df_zhihu,_ = graph_query(chi_translation(str(keyword)), 'zhihu')
	df_weibo,_ = graph_query(chi_translation(str(keyword)), 'weibo')
	df_twitter = df_twitter.rename(columns = {'user_screen_name':'author',
		'url':'authorUrl'})
	df_twitter['fav_retweet'] = df_twitter['favorite_count'] + df_twitter['retweet_count']
	df_weibo = df_weibo.rename(columns = {
		'user_name':'author',
		'url':'authorUrl'
		})

	if df_zhihu is not None:
		upvotes_count = df_zhihu.groupby(['author']).sum().reset_index().sort_values('upvotes', ascending=False)
		post_freq = df_zhihu.groupby(['author']).size().rename('size').reset_index().sort_values('size', ascending = False)
		post_freq.rename(columns = {'author': 'author_1'}, inplace = True)
		df_zhihu_new = pd.concat([upvotes_count, post_freq], axis = 1).drop(columns = ['author_1'])
		df_zhihu_new['average'] = (df_zhihu_new['upvotes']/df_zhihu_new['size']).astype(int)
		df_zhihu_new['max'] = df_zhihu.groupby('author', as_index = False)['upvotes'].max()['upvotes']
		df_zhihu_new['weighted'] = (0.6 * df_zhihu_new['max']) + (0.15*df_zhihu_new['upvotes']) + (0.25*df_zhihu_new['average'])
		df_zhihu_new = df_zhihu_new.sort_values('weighted',ascending = False).reset_index()[:3]
		df_zhihu_new['source'] = 'Zhihu'
		#Get a list of the URL
		author_list = df_zhihu_new['author'].values.tolist()
		author_list2 = [[i] for i in author_list]
		zhihu_url = []
		for i in range(len(author_list2)):
			temp_zhihu_url = set(df_zhihu[df_zhihu['author'].isin(list(author_list2[i]))].authorUrl.values.tolist())
			if list(temp_zhihu_url)[0] not in zhihu_url:
				zhihu_url.append(list(temp_zhihu_url)[0])
		df_zhihu_new['url'] = zhihu_url

	if df_weibo is not None:
		weibo_favorite_count = df_weibo.groupby(['author']).sum().reset_index().sort_values('favorite_count', ascending=False)
		post_freq = df_weibo.groupby(['author']).size().rename('size').reset_index().sort_values('size', ascending = False)
		post_freq.rename(columns = {'author': 'author_1'}, inplace = True)
		df_weibo_new = pd.concat([weibo_favorite_count, post_freq], axis = 1).drop(columns = ['author_1'])
		df_weibo_new['average'] = (df_weibo_new['favorite_count']/df_weibo_new['size']).astype(int)
		df_weibo_new['max'] = df_weibo.groupby('author', as_index = False)['favorite_count'].max()['favorite_count']
		df_weibo_new['weighted'] = (0.6 * df_weibo_new['max']) + (0.15*df_weibo_new['favorite_count']) + (0.25*df_weibo_new['average'])
		df_weibo_new = df_weibo_new.sort_values('weighted',ascending = False).reset_index()[:3]
		df_weibo_new['source'] = 'Weibo'
		#Get a list of URL
		author_list = df_weibo_new['author'].values.tolist()
		author_list2 = [[i] for i in author_list]
		weibo_id = []
		for i in range(len(author_list2)):
			temp_weibo_id = set(df_weibo[df_weibo['author'].isin(list(author_list2[i]))].user_id.values.tolist())
			if list(temp_weibo_id)[0] not in weibo_id:
				weibo_id.append(list(temp_weibo_id)[0])
		df_weibo_new['id'] = weibo_id
		df_weibo_new['url'] = 'https://www.weibo.com/' + df_weibo_new['id']

	if df_twitter is not None:
		twitter_fav_retweet = df_twitter.groupby(['author']).sum().reset_index().sort_values('fav_retweet', ascending=False)
		post_freq = df_twitter.groupby(['author']).size().rename('size').reset_index().sort_values('size', ascending = False)
		post_freq.rename(columns = {'author': 'author_1'}, inplace = True)
		df_twitter_new = pd.concat([twitter_fav_retweet, post_freq], axis = 1).drop(columns = ['author_1'])
		df_twitter_new['average'] = (df_twitter_new['fav_retweet']/df_twitter_new['size']).astype(int)
		df_twitter_new['max'] = df_twitter.groupby('author', as_index = False)['fav_retweet'].max()['fav_retweet']
		df_twitter_new['weighted'] = (0.6 * df_twitter_new['max']) + (0.15*df_twitter_new['fav_retweet']) + (0.25*df_twitter_new['average'])
		df_twitter_new = df_twitter_new.sort_values('weighted',ascending = False).reset_index()[:3]
		df_twitter_new['source'] = 'Twitter'
		df_twitter_new['url'] = 'https://twitter.com/' + df_twitter_new['author']

	df_all = pd.concat([df_twitter_new, df_weibo_new, df_zhihu_new], axis = 0, ignore_index = True)
	df_all = df_all.fillna('N.A')
	json_frame = df_all.to_dict('index').values()

	return json_frame