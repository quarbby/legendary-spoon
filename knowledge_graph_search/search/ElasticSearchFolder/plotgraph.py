import plotly
from .processing_dataframe import processing_df
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from .scroll_query import graph_query, processing_hits
from ..config import location, es
from .delete_index import delete_indices
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from textblob.inflect import singularize as _singularize
import re

def plot_pie_chart(keyword):

	df,_= graph_query(keyword)

	group_by = df.groupby("_index").size()
	print(group_by)
	labels = []
	values = []
	colors = ['#FEBFB3', '#96D38C']
	for key in group_by:
		values.append(key)

	for value in group_by.index:
		labels.append(value)

	trace = go.Pie(labels=labels, values=values, marker=dict(colors=colors, 
						line=dict(color='#000000', width=2)))
	# layout = go.Layout(width=500,
 #    height=500,
 #    margin=go.layout.Margin(
 #        l=50,
 #        r=50,
 #        b=5,
 #        t=5,
 #        pad=4))
	# legend=dict(orientation="h")
	data = [trace]
	fig = dict(data=data)
	# plotly.offline.plot([trace], include_plotlyjs=False, output_type='div')
	graph = plot(fig, filename = 'search/templates/basic_pie_chart.html', auto_open=False)

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
	plot(fig, filename = 'search/templates/basic_line_graph_{}.html'.format(indexes), auto_open=False)
		# chart = plot(fig, include_plotlyjs=False, output_type='div')
	# , filename = "Paper count by year.html"

def count_date(keyword, indexes):
	df,_ = graph_query(str(keyword),indexes)
	df['published_date'] = df['published'].apply(lambda x:  ' '.join(re.sub('T\S+', '', x).split()))
	df = df['published_date'].value_counts()
	df = df.sort_index(ascending = False)
	trace = go.Scatter(
		x = df.index,
		dx = 5,
		y = df.values,
		mode = 'lines+markers',
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
	plot(fig, filename = 'search/templates/basic_line_graph_{}.html'.format(indexes), auto_open=False)


def multi_year(keyword, index = "scholar"):
	#setting the stopwords
	stop_words = stopwords.words('english')
	df,_ = graph_query(str(keyword),index)
	df = processing_df(df)

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
	plot(fig, filename = "search/templates/basic_line_graph_scholar.html", auto_open=False)