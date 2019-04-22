import re
import plotly
import codecs
import jieba
import nltk
import math
import numpy as np
import pandas as pd
from PIL import Image
import plotly.plotly as py
import plotly.graph_objs as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from textblob.inflect import singularize as _singularize
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from ..config import location, es
from .processing_dataframe import processing_df
from .main_functions import chi_translation
from .scroll_query import graph_query, processing_hits
from sklearn.feature_extraction.text import TfidfVectorizer
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def plot_pie_chart(keyword):

	df,_= graph_query(keyword)
	if df is not None:
		group_by = df.groupby("_index").size()
		labels = []
		values = []
		colors = ['#FEBFB3', '#96D38C']
		for key in group_by:
			values.append(key)

		for value in group_by.index:
			labels.append(value)

		trace = go.Pie(labels=labels, values=values, marker=dict(colors=colors, 
							line=dict(color='#000000', width=2)))
		data = [trace]
		fig = dict(data=data)
		graph = plot(fig, filename = 'search/templates/graph/basic_pie_chart.html', auto_open=False)
	else:
		pass

def count_year(keyword, indexes):
	df,_ = graph_query(str(keyword), indexes)
	df['published_year'] = df['published'].apply(lambda x:  ' '.join(re.sub('-\S+', '', x).split()))
	df = df['published_year'].value_counts()
	df = df.sort_index(ascending = False)

	trace = go.Scatter(
		x = df.index,
		dx = 5,
		y = df.values,
		mode = 'lines+markers',
		name = 'number of papers by day',
		)
	data = [trace]
	fig = dict(data=data)
	plot(fig, filename = 'search/templates/graph/basic_line_graph_{}.html'.format(indexes), auto_open=False)
		# chart = plot(fig, include_plotlyjs=False, output_type='div')
	# , filename = "Paper count by year.html"

def count_date(keyword, indexes):
	df,_ = graph_query(str(keyword),indexes)
	if df is not None:
		df['published_date'] = df['published'].apply(lambda x:  ' '.join(re.sub('T\S+', '', x).split()))
		df = df['published_date'].value_counts()
		df = df.sort_index(ascending = False)
		trace = go.Bar(
			x = df.index,
			dx = 5,
			y = df.values,
			name = 'number of papers by day')
		data = [trace]

		layout = go.Layout(
	    	margin=go.layout.Margin(
	        l=60,
	        r=60,
	        b=50,
	        t=50,
	        pad=4))
		fig = dict(data=data, layout=layout)
		plot(fig, filename = 'search/templates/graph/basic_line_graph_{}.html'.format(indexes), auto_open=False)
	else:
		pass

def multi_year(keyword, index = "scholar"):
	#setting the stopwords
	df,_ = graph_query(str(keyword),index)
	if df is not None:
		df = processing_df(df)
		stop_words = stopwords.words('english')
		

		"""
		This portion is about making the terms to singular form such as:
		machines --> machine to prevent the same term from appearing 
		multiple times
		"""
		blob = TextBlob(df['processed'].iloc[1])
		singular = [word.singularize() for word in blob.words]
		#remove stop words then convert to singular
		df['processed'] = df['processed'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
		df['singular'] = df['processed'].apply(lambda x: ' '.join([word.singularize()
			for word in TextBlob(x).words]))
		df['singular'] = df['singular'].apply(lambda x: x.lower())
		df['published_year'] = df['published'].apply(lambda x:  ' '.join(re.sub('-\S+', '', x).split()))


		"""
		Performing TFIDF to get important terms
		ngram of 2-3 works better than 1-3 as it
		provides terms such as neural network instead
		of neural then network
		"""
		all_summary = df['singular'].tolist()
		tv = TfidfVectorizer(analyzer = 'word', ngram_range = (2,3), stop_words = 'english',
			max_features = 10)
		tv.fit_transform(all_summary)

		#Getting the paper count for the various terms

		df = df['published_year'].value_counts()
		df = df.sort_index(ascending = False)

		trace = go.Scatter(
			x = df.index,
			dx = 5,
			y = df.values,
			mode = 'lines+markers',
			name = "{}".format(str(keyword)))

		
		df0,_ = graph_query(tv.get_feature_names()[2],index)
		df0['published_year'] = df0['published'].apply(lambda x:  ' '.join(re.sub('-\S+', '', x).split()))
		df0 = df0['published_year'].value_counts()
		df0 = df0.sort_index(ascending = False)

		trace0 = go.Scatter(
			x = df0.index,
			dx = 5,
			y = df0.values,
			mode = 'lines+markers',
			name = "{}".format(str(tv.get_feature_names()[2])))

		df1,_ = graph_query(tv.get_feature_names()[3],index)
		df1['published_year'] = df1['published'].apply(lambda x:  ' '.join(re.sub('-\S+', '', x).split()))
		df1 = df1['published_year'].value_counts()
		df1 = df1.sort_index(ascending = False)
		trace1 = go.Scatter(
			x = df1.index,
			dx = 5,
			y = df1.values,
			mode = 'lines+markers',
			name = "{}".format(str(tv.get_feature_names()[3])))

		# df2,_ = graph_query(tv.get_feature_names()[2],index)
		# df2 = processing_df(df2)
		# df2 = df2['published_year'].value_counts()
		# df2 = df2.sort_index(ascending = False)

		# trace2 = go.Scatter(
		# 	x = df2.index,
		# 	dx = 5,
		# 	y = df2.values,
		# 	mode = 'lines+markers',
		# 	name = "{}".format(str(tv.get_feature_names()[2])))

		layout = go.Layout(
	    margin=go.layout.Margin(
	        l=60,
	        r=60,
	        b=40,
	        t=20,
	        pad=4))
		data = [trace, trace0, trace1]
		fig = dict(data=data, layout = layout )
		plot(fig, filename = "search/templates/graph/basic_line_graph_scholar.html", auto_open=False)
	else:
		pass

def main_graph(keyword):
	df_english,_ = graph_query(str(keyword))
	df_chinese,_ = graph_query(str(chi_translation(keyword)))
	df = pd.concat([df_english,df_chinese], ignore_index = True)
	dates = ['2017', '2018', '2019']
	df = df[df.published.str.contains('|'.join(dates))]

	if df is not None:
		df['published_date'] = df['published'].apply(lambda x:  x[:7])
		df_2017 = df[df.published_date.str.contains('2017')]
		df_2017 = df_2017['published_date'].value_counts()
		df_2017 = df_2017.sort_index(ascending = False)
		df_2018 = df[df.published_date.str.contains('2018')]
		df_2018 = df_2018['published_date'].value_counts()
		df_2018 = df_2018.sort_index(ascending = False)
		df_2019 = df[df.published_date.str.contains('2019')]
		df_2019 = df_2019['published_date'].value_counts()
		df_2019 = df_2019.sort_index(ascending = False)
		df = df['published_date'].value_counts()
		df = df.sort_index(ascending = False)
		# trace = go.Bar(
		#  showlegend = True,
		#  x = df.index,
		#  dx = 5,
		#  y = df.values,
		#  visible = True,
		#  name = "Total count")
		trace_2017 = go.Bar(
			showlegend = True,
			x = df_2017.index,
			dx = 5,
			y = df_2017.values,
			visible = True,
			name = "Total count (2017)",
			marker=dict(
				color='rgb(158,225,219)'))
		trace_2018 = go.Bar(
			showlegend = True,
			x = df_2018.index,
			dx = 5,
			y = df_2018.values,
			visible = True,
			name = "Total count (2018)",
			marker=dict(
				color='rgb(160,225,158)'))
		trace_2019 = go.Bar(
			showlegend = True,
			x = df_2019.index,
			dx = 5,
			y = df_2019.values,
			visible = True,
			name = "Total count (2019)",
			marker=dict(
				color='rgb(225,170,158)'))
		data = [trace_2017, trace_2018, trace_2019]

		layout = go.Layout(
			margin=go.layout.Margin(
				l=60,
				r=60,
				b=50,
				t=50,
				pad=4),
			legend = dict(x = -.1, y = 1.1, orientation = "h"),
			updatemenus = list([
				dict(
					buttons = list([
						dict(
							args = [{'visible': [True,True,True]},
							{'title' : "Total Count"}],
							label = "All",
							method = "update",
							),
						dict(
							args = [{'visible':[True,False,False]},
							{'title' : "Total Count for 2017"}],
							label = "2017",
							method = "update",
							),
						dict(
							args = [{'visible':[False,True,False]},
							{'title' : "Total Count for 2018"}],
							label = "2018",
							method = "update",
							),
						dict(
							args = [{'visible':[False,False,True]},
							{'title' : "Total Count for 2019"}],
							label = "2019",
							method = "update",
							)
						])
					)
				])
			)
		fig = dict(data=data, layout=layout)
		plot(fig, filename = 'techscan/templates/graph/main_graph_all.html', auto_open=False)
	else:
		pass

def top_hashtag(keyword):
	df,_ = graph_query(chi_translation(keyword),'weibo')
	df ['hashtags']= df['hashtags'].apply(lambda x:''.join(x))
	df = df[df['hashtags']!='']
	records = df.to_dict('records')
	hashtag_count = Counter(hashtag['hashtags'] for hashtag in records)
	tophashtags = hashtag_count.most_common(15)
	hashtag=[]
	counts=[]
	for i in tophashtags:
		hashtag.append(i[0])
		counts.append(i[1])

	data = [go.Bar(
		x = hashtag,
		y = counts,
		marker=dict(
			color='rgb(246,156,99)')
		)]
	layout = go.Layout(
		yaxis=dict(
			title='Frequency of Hashtags',
			titlefont=dict(
				family = '-webkit-body',
				size=16,
				color='rgb(107, 107, 107)'
				)
			),
		legend=dict(
			x=0,
			y=1.0,
			bgcolor='rgba(255, 255, 255, 0)',
			bordercolor='rgba(255, 255, 255, 0)'
			),
		bargap=0.15,
		)

	fig = dict(data = data , layout=layout)
	plot(fig, filename='techscan/templates/graph/weibo_hashtag_count.html', auto_open=False)

def twitter_bubble(keyword):
	df,_ = graph_query(keyword, 'tweets')
	df2 = df.groupby(['hashtags']).sum().reset_index().sort_values('retweet_count', ascending = False)
	df2 = df2.drop(columns = ['_score'])
	df2 = df2[df2['retweet_count'] >= 10]
	df2 = df2[df2['hashtags'] != '[]']
	df2['hashtags'] = df2['hashtags'].apply(lambda x: re.sub("['\]\[']", '', x.lower()))
	df2['hashtags'] = df2['hashtags'].apply(lambda x: x.replace("ai", "artificial intelligence"))
	df2['hashtags'] = df2['hashtags'].apply(lambda x: x.split(', '))
	if len(df2) > 20:
		df2 = df2.head(10)

	hashtag_used = {}
	for i in range(len(df2)):
		for hashtag in df2['hashtags'].iloc[i]:
			if hashtag in hashtag_used:
				count['favorite_count'] = count['favorite_count'] + df2.favorite_count.iloc[i]
				count['retweet_count'] = count['retweet_count'] + df2.retweet_count.iloc[i]

			else:
				count = {}
				count['favorite_count'] = df2.favorite_count.iloc[i]
				count['retweet_count'] = df2.retweet_count.iloc[i]
				hashtag_used[hashtag] = count


	slope = 2.666051223553066e-05
	hover_text = []
	bubble_size = []
	favorite_count = []
	retweet_count = []

	for key in hashtag_used.keys():
		hover_text.append(('Hashtag: {hashtag}<br>' +
			'Retweet Count: {retweet}<br>' +
			'Favorite Count: {favorite}').format(hashtag=key,
				retweet=hashtag_used[key]['retweet_count'],
				favorite=hashtag_used[key]['favorite_count']))
		bubble_size.append(math.sqrt((hashtag_used[key]['favorite_count'] + hashtag_used[key]['retweet_count'])*slope))
		favorite_count.append(hashtag_used[key]['favorite_count'])
		retweet_count.append(hashtag_used[key]['retweet_count'])

	sizeref = 2.*max(bubble_size)/(100**2)

	trace0 = go.Scatter(
		x = retweet_count,
		y = favorite_count,
		mode = 'markers',
		text = hover_text,
		marker = dict(
			color = 'rgb(41,129,113)',
			symbol = 'circle',
			sizemode = 'area',
			sizeref = sizeref,
			size = bubble_size,
			line = dict(
				width = 2
				),
			)
		)
	data = [trace0]
	layout = go.Layout(
		xaxis = dict(
			title = 'Retweet Count',
			titlefont=dict(
				family = '-webkit-body',
				size=16,
				color='rgb(107, 107, 107)'
				),
			gridcolor = 'rgb(255, 255, 255)',
			zerolinewidth = 1,
			ticklen = 5,
			gridwidth = 2,
			),
		yaxis = dict(
			title = 'Favorite Count',
			titlefont=dict(
				family = '-webkit-body',
				size=16,
				color='rgb(107, 107, 107)'
				),
			gridcolor = 'rgb(255, 255, 255)',
			zerolinewidth = 1,
			ticklen = 5,
			gridwidth = 2,
			),
		)

	fig = dict(data=data, layout=layout)
	plot(fig, filename='techscan/templates/graph/twitter_hashtag_bubble.html', auto_open=False)

def plot_stocks():
	res = es.search(index = 'stock', size = 10000, scroll = '2m' , body= {"query": {"match_all": {}}})
	company = []
	date = []
	closing_price = []
	percentage = []

	for i in range(len(res)):
		com = res['hits']['hits'][i]['_source']
		company.append(com['company'])
		
		date.append( com['date'])
		closing_price.append(com['close'])
		percentage.append( com['percentage'])

	trace1 = {
		"x": date[0],
		"y": closing_price[0],
		"line": {"color": "rgba(31,119,180,1)"}, 
		"mode": "lines", 
		"name": company[0], 
		"type": "scatter", 
		"xaxis": "x", 
		"yaxis": "y"
		}
	trace2 = {
		"x": date[1],
		"y": closing_price[1],
		"line": {"color": "rgba(255,129,14,1)"}, 
		"mode": "lines", 
		"name": company[1], 
		"type": "scatter", 
		"xaxis": "x", 
		"yaxis": "y"
		}
	trace3 = {
		"x": date[2],
		"y": closing_price[2],
		"line": {"color": "rgba(3,255,160,1)"}, 
		"mode": "lines", 
		"name": company[2], 
		"type": "scatter", 
		"xaxis": "x", 
		"yaxis": "y"
		}
	trace4 = {
		"x": date[3],
		"y": closing_price[3],
		"line": {"color": "rgba(1,11,190,12)"}, 
		"mode": "lines", 
		"name": company[3], 
		"type": "scatter", 
		"xaxis": "x", 
		"yaxis": "y"
		}
	trace5 = {
		"x": date[4],
		"y": closing_price[4],
		"line": {"color": "rgba(31,119,180,1)"}, 
		"mode": "lines", 
		"name": company[4], 
		"type": "scatter", 
		"xaxis": "x", 
		"yaxis": "y"
		}



	data = go.Data([trace1, trace2, trace3, trace4, trace5])
	layout = {
		"showlegend" : True,
		"margin": {
			"r": 10, 
			"t": 25, 
			"b": 40, 
			"l": 60
			}, 
		"title": "Stock Prices", 
		"xaxis": {
		"domain": [0, 1], 
		"rangeselector": {"buttons": 
		[{
		"count": 3, 
		"label": "3 mo", 
		"step": "month", 
		"stepmode": "backward"
		}, 
		{
		"count": 6, 
		"label": "6 mo", 
		"step": "month", 
		"stepmode": "backward"
		}, 
		{
		"count": 1, 
		"label": "1 yr", 
		"step": "year", 
		"stepmode": "backward"
		}, 
		{
		"count": 1, 
		"label": "YTD", 
		"step": "year", 
		"stepmode": "todate"
		}, 
		{"step": "all"}
		]}, 
		"title": "Date"
		}, 
		"yaxis": {
		"domain": [0, 1], 
		"title": "Price"
		}}
		
	fig = dict(data=data, layout=layout)
	plot(fig, filename = 'techscan/templates/graph/stock_graph.html', auto_open=False)

def twitter_graph(keyword):
	df,_ = graph_query(keyword, 'tweets')
	df_new = df.groupby(['user_screen_name']).sum().reset_index()
	rng = []
	max_range = 15500
	for i in range (int(max_range/50)):
		rng.append(str(i*50) + '-' + str((i+1)*50))
	AuthorList = []
	Totalcount = []
	for j in range (len(rng)):
		x , y = count_range_in_list(df_new['user_screen_name'],df_new['favorite_count'], j*50, (j+1)*50)
		AuthorList.append(x)
		Totalcount.append(y)
	# print (AuthorList)
	# print(Totalcount)

	x = percentile(AuthorList,Totalcount, df_new)
	# print(x)

	chunks_count_lower = Totalcount.copy()
	chunks_Author_lower = AuthorList.copy()
	chunks_count_upper = Totalcount.copy()
	chunks_Author_upper = AuthorList.copy()

	for i in range (x, len(Totalcount)):
		chunks_count_lower[i] = 0
		chunks_Author_lower[i] = []

	for i in range (x):
		chunks_count_upper[i] = 0
		chunks_Author_upper[i] = []
	# print(len(chunks_Author_upper))
	# print(len(rng))
	trace1 = go.Bar(
		hoverinfo = "text",	
		x=rng,
		y=chunks_count_lower,	
		text = chunks_Author_lower,
		name = 'Lower 99th Percentile '
		)
	trace2 = go.Bar(
		hoverinfo = "text",	
		x=rng,
		y=chunks_count_upper,
		text = chunks_Author_upper,
		name = 'Upper 1st percentile'
		)
	layout = go.Layout(barmode='stack',
		xaxis = dict(
			dtick=10	,
			) ,
		yaxis =  dict(
			range = [0,100]
			),
		bargap=0,
		bargroupgap=0.01,
		showlegend = True,
		title = go.layout.Title(
			text = 'tweets: favorite counts for usernames')
		)
	data = [trace1,trace2]
	fig = go.Figure(data = data, layout=layout)

	plot(fig, filename='techscan/templates/graph/twitter_graph.html', auto_open=False)

def percentile (Authorlist,countlist, df):
	initial = 0
	for i in range (len(countlist)):
		if initial < math.floor(len(df)*9.9/10):
			initial = initial + countlist[i] 
		else :
			val = i
			break
	return val

def count_range_in_list (author, li, min, max):
	ctr = 0
	place_names = []
	for k in range(len(li)):
		if min <= li[k] < max:
			place_names.append(author[k])
			ctr += 1
	return place_names, ctr

def wordcloud(keyword, indexes = 'weibo'):
	df,_ = graph_query(keyword,indexes)
	if indexes == 'weibo' or indexes == 'zhihu':
		stopword = codecs.open('techscan/static/word_cloud/stopword.txt', 'r', 'utf-8').read()
		df['summary'] = df['summary'].apply(lambda x: ' '.join([word for word in jieba.cut(x,cut_all=False) if word not in stopword]))
	else:
		stopword = stopwords.words('english')
		df['summary'] = df['summary'].apply(lambda x: re.sub('[\W]', '', x))
		df['summary'] = df['summary'].apply(lambda x: ''.join([word for word in x.split(' ') if word not in stopword]))
	
	df = df[df['summary']!='']
	summary_list = df['summary'].tolist()
	summary_string = ''.join(summary_list)
	if indexes == 'weibo' or indexes == 'zhihu':
		mask = np.array(Image.open('techscan/static/word_cloud/circle.png'))
	else:
		mask = np.array(Image.open('techscan/static/word_cloud/tweet.png'))
			
	font_path = 'techscan/static/word_cloud/STFangSong.ttf'
	wordcloud = WordCloud( background_color="white",collocations = False, max_words=100,font_path=font_path,
		max_font_size=100, random_state=42, width=1000, height=860, margin=2, mask =mask).generate(summary_string)
	
	wordcloud.to_file("techscan/templates/graph/{}_wordcloud.png".format(indexes))

