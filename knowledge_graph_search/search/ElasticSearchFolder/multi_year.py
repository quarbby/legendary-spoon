from config import es
from scroll_query import query
from processing_dataframe import processing_df
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from textblob.inflect import singularize as _singularize
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot

"""
Function to plot graph based on similar
important terms found in the summaries
"""
def multi_year(keyword, index = "scholar"):
	#setting the stopwords
	stop_words = stopwords.words('english')
	df = query(str(keyword), str(index))
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

	df0 = query(tv.get_feature_names()[0], str(index))
	df0 = processing_df(df0)
	df0 = df0['published_year'].value_counts()
	df0 = df0.sort_index(ascending = False)

	trace0 = go.Scatter(
		x = df0.index,
		dx = 5,
		y = df0.values,
		mode = 'lines+markers',
		name = "{}".format(str(tv.get_feature_names()[0])))

	df1 = query(tv.get_feature_names()[1],str(index))
	df1 = processing_df(df1)
	df1 = df1['published_year'].value_counts()
	df1 = df1.sort_index(ascending = False)

	trace1 = go.Scatter(
		x = df1.index,
		dx = 5,
		y = df1.values,
		mode = 'lines+markers',
		name = "{}".format(str(tv.get_feature_names()[1])))

	df2 = query(tv.get_feature_names()[2], str(index))
	df2 = processing_df(df2)
	df2 = df2['published_year'].value_counts()
	df2 = df2.sort_index(ascending = False)

	trace2 = go.Scatter(
		x = df2.index,
		dx = 5,
		y = df2.values,
		mode = 'lines+markers',
		name = "{}".format(str(tv.get_feature_names()[2])))

	data = [trace, trace0, trace1, trace2]
	fig = dict(data=data)
	plot(fig, filename = "search/templates/basic_line_graph_scholar.html", auto_open=False)
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt

# cloud = WordCloud().generate(' '.join(tv.get_feature_names()))

# plt.imshow(cloud, interpolation = 'bilinear')
# plt.axis('off')
# plt.show()

"""
Example on how to use it:
multi_year("biology")
"""
# multi_year("biology")