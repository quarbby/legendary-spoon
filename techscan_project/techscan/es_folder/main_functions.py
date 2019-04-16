import requests
from pprint import pprint
from textblob import TextBlob
from ..config import location, es
from .scroll_query import graph_query, processing_hits
import pandas as pd


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
		df_new['average'] = df_new['upvotes']/df_new['size']
		df_new['max'] = df.groupby('author', as_index=False)['upvotes'].max()['upvotes']
		df_new['weighted'] = (0.6 * df_new['max']) + (0.15*df_new['upvotes']) + (0.25*df_new['average'])

		df_new = df_new.sort_values('weighted',ascending = False).reset_index()[:10]
		if graph == True:
			df_new.sort_values('weighted',ascending = True)
			data = [go.Bar(
			            x=df_new['size'],
			            y=df_new['author'],
			            orientation = 'h',
			)]
			plot(data, filename='search/templates/zhihu_author_bar.html',auto_open=False)
		else:
			# df_new = df_new.reset_index(drop = True)
			json_frame = df_new.to_dict('index').values()
			return json_frame
	else:
		pass