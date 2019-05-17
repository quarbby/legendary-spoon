from scroll_query import graph_query, processing_hits
import pandas as pd
import numpy as np
from main_functions import chi_translation
import jieba
import jieba.posseg as psg
from collections import Counter
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host' : 'localhost', 'port' : 9200}])

def get_percentile(indexes):
	res = es.search(index = indexes , size = 5, scroll = '2m', body = {"query" : {
		"match_all" : {}}})

	df = processing_hits(res)
	#Get the scroll id
	sid = res['_scroll_id']
	scroll_size = len(res['hits']['hits'])

	#Put first half of data into a dataframe
	df = processing_hits(res)

	#Scroll and append into the dataframe
	while scroll_size > 0 :
		res = es.scroll(scroll_id = sid, scroll = '2m')
		df = df.append(processing_hits(res), sort = True)
		sid = res['_scroll_id']
		scroll_size = len(res['hits']['hits'])
	df.reset_index(drop = True)

	if indexes == 'tweets':
		total_favorite_count = df.favorite_count.tolist()
		total_retweet_count = df.retweet_count.tolist()
		favorite_percentile_value = np.percentile(total_favorite_count, 85)
		retweet_percentile_value = np.percentile(total_retweet_count, 85)
		return retweet_percentile_value, favorite_percentile_value

	elif indexes == 'weibo':
		total_favorite_count = df.favorite_count.tolist()
		favorite_percentile_value = np.percentile(total_favorite_count, 85)
		return favorite_percentile_value

	elif indexes == 'zhihu':
		total_upvotes_count = df.upvotes.tolist()
		upvotes_percentile_value = np.percentile(total_upvotes_count, 85)
		return upvotes_percentile_value

# tweets_retweet_percentile, tweets_favorite_percentile = get_percentile('tweets')
# print(tweets_favorite_percentile + tweets_retweet_percentile)
# weibo_favorite_percentile = get_percentile('weibo')
# print(weibo_favorite_percentile)
# zhihu_upvote_percentile = get_percentile('zhihu')
# print(zhihu_upvote_percentile)

def percentile(keyword, indexes):
	if indexes == 'tweets':	
		df_keyword,_ = graph_query(str(keyword), indexes)
		if df_keyword is not None:
			df_keyword = df_keyword.groupby(['user_screen_name']).sum().reset_index().sort_values('favorite_count', ascending=False)
			df_keyword['fav_retweet'] = df_keyword['retweet_count'] + df_keyword['favorite_count']
			df_positive = df_keyword[df_keyword.fav_retweet >= 50]
			top = len(df_positive)

	elif indexes == 'weibo':	
		df_keyword,_ = graph_query(chi_translation(keyword), indexes)
		if df_keyword is not None:
			df_keyword = df_keyword.groupby(['user_name']).sum().reset_index().sort_values('favorite_count', ascending=False)
			df_positive = df_keyword[df_keyword.favorite_count >= 40]
			top = len(df_positive)

	elif indexes == 'zhihu':
		df_keyword,_ = graph_query(chi_translation(keyword), indexes)
		if df_keyword is not None:
			df_keyword = df_keyword.groupby(['author']).sum().reset_index().sort_values('upvotes', ascending=False)
			df_positive = df_keyword[df_keyword.upvotes >= 128]
			top = len(df_positive)

	if df_keyword is not None:
		if top >= (0.1* len(df_keyword)):
			return "True"

	else:
		return "False"

def NER(chinese_sentence):
	results = []
	for token in psg.cut(chinese_sentence):
		if token.flag == "nt":
			results.append(token.word)

	if results != None:
		return results

df_news,_ = graph_query(chi_translation('artificial intelligence'), 'news')
df_news['tokens'] = df_news['summary'].apply(lambda x: NER(x))
org_list = []
for i in range(len(df_news)):
	if '公司' or '机构' or '集团' in df_news['tokens'].iloc[i]:
		org_list.append(df_news['tokens'].iloc[i])
print(org_list)
# news_summary_list = df_news.summary.tolist()
# news_summary_string = "".join(news_summary_list)
# news_tokenised = psg.cut(news_summary_string)

# org_list = []
# for token in news_tokenised:
# 	if token.flag == "nt":
# 		org_list.append(token.word)

# companies = []
# for org in org_list:
# 	if '公司' in org or '集团'in org:
# 		companies.append(org)

# companies_count = Counter(companies)
# top_companies = companies_count.most_common(10)

# count = []
# company_name = []
# color = []
# for company in top_companies:
# 	count.append(company[1])
# 	company_name.append(company[0])
# 	color.append('rgb(152,89,103)')