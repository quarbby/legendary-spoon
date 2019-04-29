import re
import plotly
# import codecs
import jieba
import jieba.posseg as psg
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
import plotly.figure_factory as ff
from .uploading_data import upload_data_ner
from .train_heatmap_index import find_NER
from .stocks_funct import NER_stocks

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

def twitter_graph(keyword):
	df,_ = graph_query(keyword, 'tweets')
	df_new = df.groupby(['user_screen_name']).sum().reset_index()
	final = [df_new['favorite_count'].tolist()]
	name_List = [df_new['user_screen_name'].tolist()]
	group_label = ['Favorite Count']
	fig = ff.create_distplot(final, group_label,bin_size = .1, curve_type='normal',rug_text = name_List,show_hist=False)
	fig['layout'].update(title='Distplot with Normal Distribution')
	plot(fig, filename='techscan/templates/graph/twitter_graph.html', auto_open=False)

def wordcloud(keyword, indexes = 'weibo'):
	df,_ = graph_query(keyword,indexes)
	if indexes == 'weibo' or indexes == 'zhihu':
		with open('techscan/static/word_cloud/stopword.txt', encoding = 'utf-8') as f:
			stopword = f.read()
		df['summary'] = df['summary'].apply(lambda x: ' '.join([word for word in jieba.cut(x,cut_all=False) if word not in stopword]))
	else:
		stopword = stopwords.words('english')
		df['summary'] = df['summary'].apply(lambda x: re.sub('[\W]', ' ', x))
		df['summary'] = df['summary'].apply(lambda x: ' '.join([word for word in x.split(' ') if word not in stopword]))
	
	df = df[df['summary']!='']
	summary_list = df['summary'].tolist()
	summary_string = ''.join(summary_list)
	if indexes == 'weibo' or indexes == 'zhihu':
		mask = np.array(Image.open('techscan/static/word_cloud/circle.png'))
	else:
		mask = np.array(Image.open('techscan/static/word_cloud/tweet.png'))
			
	font_path = 'techscan/static/word_cloud/STFangSong.ttf'
	wordcloud = WordCloud( background_color = "white",collocations = False, max_words = 100,font_path=font_path,
		max_font_size = 100, random_state = 42, width = 1000, height = 860, margin = 2, mask = mask).generate(summary_string)
	
	wordcloud.to_file("techscan/static/word_cloud/{}_wordcloud.png".format(indexes))

def detail_hashtag_frequency(keyword):
	df_twitter,_ = graph_query(keyword, 'tweets')
	df_twitter['hashtags'] = df_twitter['hashtags'].apply(lambda x:''.join(re.sub('[^\w]', '',  x).split()))
	df_twitter['hashtags'] = df_twitter['hashtags'].apply(lambda x: x.replace("ai", "AI"))
	df_twitter = df_twitter[df_twitter['hashtags'] != '']
	twitter_record = df_twitter.to_dict('records')
	twitter_hashtag_count = Counter(hashtag['hashtags'] for hashtag in twitter_record)
	twitter_tophashtags = twitter_hashtag_count.most_common(15)

	Total_hashtag = []
	Total_count = []
	color_list = []
	text_list = []

	for i in twitter_tophashtags:
		Total_hashtag.append(i[0])
		Total_count.append(i[1])
		color_list.append('rgb(106,167,156)')
		text_list.append('Twitter')


	df_weibo,_ = graph_query(chi_translation(keyword),'weibo')
	df_weibo ['hashtags']= df_weibo['hashtags'].apply(lambda x:''.join(x))
	df_weibo = df_weibo[df_weibo['hashtags']!='']
	weibo_record = df_weibo.to_dict('records')
	weibo_hashtag_count = Counter(hashtag['hashtags'] for hashtag in weibo_record)
	weibo_tophashtags = weibo_hashtag_count.most_common(15)
	weibo_hashtag = []
	weibo_count = []
	for i in weibo_tophashtags:
		Total_hashtag.append(i[0])
		Total_count.append(i[1])
		color_list.append('rgb(246,156,99)')
		text_list.append('Weibo')

	hashtags_counting = pd.DataFrame({'hashtags': Total_hashtag, "counts": Total_count , "color": color_list, "texts": text_list})
	hashtags_count = hashtags_counting.sort_values('counts', ascending = False)



	trace1 = go.Bar(
		x = hashtags_count['hashtags'],
		y = hashtags_count['counts'],
		name='Weibo',
		marker=dict(
			color=hashtags_count['color'],
			),
		hoverinfo = 'text',
		text = "source: " + hashtags_count['texts'] + "<br>Hashtag: " + hashtags_count['hashtags'],
		)

	data = [trace1]
	layout = go.Layout(
		yaxis = dict(
			title = 'Frequency of Hashtags',
			titlefont = dict(
				family = 'roboto',
				size = 16,
				color = 'rgb(107, 107, 107)'
				)
			),
		legend = dict(
			x = 0,
			y = 1.0,
			bgcolor = 'rgba(255, 255, 255, 0)',
			bordercolor = 'rgba(255, 255, 255, 0)'
			),
		barmode ='group',
		bargap = 0.15,
		bargroupgap = 0.1,
	


		)
	fig = dict(data = data , layout = layout)
	plot(fig, filename = 'techscan/templates/graph/detail_hashtag_frequency.html', auto_open = False)

def heatmap(keyword):
    search_term = chi_translation(keyword)
    res = es.search(index = 'heatmap' , size = int(10000), scroll = '2m', body = {"query" : {
        "match" : {"labels" : search_term}
        }})
    res_input = res['hits']['hits']

    resItems = []
    for i in range (len(res_input)):
        if res_input[i]['_source']['labels'] == search_term :
            resItems.append(res_input[i])

    address = []
    weight = []
    companies = []
    Latitude = []
    longtitude = []
    colouring = []
    institude = []

    countx1 = 0
    countx2 = 0
    countx3 = 0
    countx4 = 0

    if resItems == []:
        # return [] 
        Items = find_NER(search_term)
        upload_data_ner(Items, 'heatmap')
        for i in range (len(Items)):
            companies.append(Items[i]['publisher'])
            Latitude.append(Items[i]['Address'][0]['geometry']['location']['lat'])
            longtitude.append(Items[i]['Address'][0]['geometry']['location']['lng'])
            address.append(Items[i]['Address'][0]['formatted_address'])
            if 0 < int(Items[i]['weighting']) <= 5:
                # colouring.append("#00284d")
                weight.append(100)

            elif 5 < int(Items[i]['weighting']) <= 20:
                # colouring.append("#004f99")
                weight.append(200)

            elif 20 < int(Items[i]['weighting']) <= 50:
                # colouring.append("#0077e6")
                weight.append(500)

            elif 50 < int(Items[i]['weighting']) <= 100:
                # colouring.append("#339cff")
                weight.append(1000)

            elif 100 < int(Items[i]['weighting'] ):
                # colouring.append("#ff3333")
                weight.append(3000)

            if Items[i]['types'] == 'Institutions':
                colouring.append("#00cc66")
                institude.append(Items[i]['types'])
                countx1 += 1

            elif Items[i]['types'] == 'Private_Companies':    
                colouring.append("#000080")
                institude.append(Items[i]['types'])
                countx2 += 1

            elif Items[i]['types'] == 'Government_Sectors':
                colouring.append("#ff3333")
                institude.append(Items[i]['types'])
                countx3 += 1

            elif Items[i]['types'] == 'news':
                colouring.append("#cc6600")
                institude.append(Items[i]['types'])
                countx4 += 1
    else :
        for i in range (len(resItems)):
            companies.append(resItems[i]['_source']['publisher'])
            Latitude.append(resItems[i]['_source']['Address'][0]['geometry']['location']['lat'])
            longtitude.append(resItems[i]['_source']['Address'][0]['geometry']['location']['lng'])
            address.append(resItems[i]['_source']['Address'][0]['formatted_address'])
            if 0 < int(resItems[i]['_source']['weighting']) <= 5:
                # colouring.append("#00284d")
                weight.append(100)

            elif 5 < int(resItems[i]['_source']['weighting']) <= 20:
                # colouring.append("#004f99")
                weight.append(200)

            elif 20 < int(resItems[i]['_source']['weighting']) <= 50:
                # colouring.append("#0077e6")
                weight.append(500)

            elif 50 < int(resItems[i]['_source']['weighting']) <= 100:
                # colouring.append("#339cff")
                weight.append(1000)

            elif 100 < int(resItems[i]['_source']['weighting']  ):
                # colouring.append("#ff3333")
                weight.append(3000)

            if resItems[i]['_source']['types'] == 'Institutions':
                colouring.append("#00cc66")
                institude.append(resItems[i]['_source']['types'])
                countx1 += 1

            elif resItems[i]['_source']['types'] == 'Private_Companies':    
                colouring.append("#000080")
                institude.append(resItems[i]['_source']['types'])
                countx2 += 1

            elif resItems[i]['_source']['types'] == 'Government_Sectors':
                colouring.append("#ff3333")
                institude.append(resItems[i]['_source']['types'])
                countx3 += 1

            elif resItems[i]['_source']['types'] == 'news':
                colouring.append("#cc6600")
                institude.append(resItems[i]['_source']['types'])
                countx4 += 1
    ds = pd.DataFrame({'companies': companies, 'Lat': Latitude, 'Lng': longtitude , 'address': address, 'weight': weight, 'colors': colouring, 'institude': institude})
    df = ds.sort_values(['colors'])


    colors = ['Private Companies','Institutions','News Publishers','Government Sectors']
    limits = [(0,countx2),(countx2,countx2+countx1),(countx2+countx1,countx2+countx1+countx4),(countx2+countx1+countx4,countx2+countx1+countx4+countx3)]

    cities = []
    scale = 5000

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
        df_colors = colors[i]
        city = go.Scattergeo(
            locationmode = 'ISO-3',
            # locations = ['asia'],
            lon = df_sub['Lng'],
            lat = df_sub['Lat'],
            text = colors[i]+": "+df_sub['companies']+"  |  Location: "+df_sub['address'],
            marker = go.scattergeo.Marker(
                size = df_sub['weight'],
                color = df_sub['colors'],
                line = go.scattergeo.marker.Line(
                    width=0, color='rgb(40,40,40)'
                ),
                sizemode = 'area'
            ),
            # name = '{0} - {1}'.format(lim[0],lim[1]) 
            name = '{}'.format(df_colors) 
            )
        cities.append(city)

    layout = go.Layout(
            title = go.layout.Title(
                text = 'China News Reports on {}'.format(keyword.lower())
            ),
            showlegend = True,
            font = go.layout.Font(size = 20),
            autosize = True,
            # Tickformatstops = go.layout.tickformatstops(dtickrange = [50,100]),
            xaxis = dict (fixedrange = True),
            yaxis = dict (fixedrange = True),
                # fixedrange = True),
            geo = go.layout.Geo(
                scope = 'world',
                projection = go.layout.geo.Projection(
                    type='equirectangular'  
                ),
                #center = go.layout.geo.Center( lat = 50, lon = 50),
                ##Map Features##
                showcoastlines = True,
                showland = True,
                showocean = True,
                showcountries = True,
                showsubunits = False,
                # size and width
                subunitwidth=1,
                countrywidth=1,
                # colorings ^^
                landcolor = '#e1eaea',
                oceancolor = "#ffffff",
                subunitcolor="#9ae59a", 
                countrycolor="#b3b3b3",
                coastlinecolor  = "#b3b3b3", 
                
            )
        )

    fig = go.Figure(data=cities, layout=layout)
    plot(fig, filename='techscan/templates/graph/heatmap.html', auto_open=False)

def top_companies(keyword, indexes = 'news', graph = False):
	df,_ = graph_query(chi_translation(keyword), indexes)
	summary_list = df.summary.tolist()
	summary_string = "".join(summary_list)
	tokenised = psg.cut(summary_string)
	org_list = []
	for token in tokenised:
		if token.flag == "nt":
			org_list.append(token.word)

	companies = []
	for org in org_list:
		if '公司' in org or '集团'in org:
			companies.append(org)

	companies_count = Counter(companies)
	top_companies = companies_count.most_common(20)

	count = []
	company_name = []
	for company in top_companies:
		count.append(company[1])
		company_name.append(company[0])
	data = {'company' : company_name, 'count' : count}
	df_new = pd.DataFrame(data)
	json_frame = df_new.to_dict('index').values()
	# print(json_frame)
	
	if graph == True:
		data = [go.Bar(
			x= company_name,
			y = count,
			marker = dict(
				color = 'rgb(152,89,103)',
				),
			)]

		layout = go.Layout(
			xaxis = dict(
				title = 'Company Name',
				tickfont = dict(
					size = 14,
					color = 'rgb(107, 107, 107)',
					family = 'roboto'
					)),
			yaxis = dict(
				title = 'Company Count',
				titlefont = dict(
					size = 14,
					color = 'rgb(107, 107, 107)',
					family = 'roboto'
					),
				tickfont = dict(
					size = 14,
					color = 'rgb(107, 107, 107)'
					)
				),
			legend=dict(
				x = 0,
				y = 1.0,
				bgcolor = 'rgba(255, 255, 255, 0)',
				bordercolor = 'rgba(255, 255, 255, 0)'
				),

			bargap = 0.15,
			bargroupgap = 0.1
			)

		fig = dict(data = data , layout = layout)
		plot(fig, filename ='techscan/templates/graph/top_companies.html', auto_open = False)
	
	else:
		return json_frame


def plot_stocks(keyword):
	keyword = chi_translation(keyword)
	res = es.search(index = 'stocks_store', size = 10000, scroll = '2m' , body= {"query": {"match_all": {}}})
	res_input = res['hits']['hits']
	resitems = []
	for i in range (len(res_input)):
	    if res_input[i]['_source']['label'] == keyword:
	        resitems.append(res_input[i])
	stock_price = []
	date = []
	company = []
	count = []
	color = ["rgba(234,174,163,1)", "rgba(222,193,158,1)","rgba(140,84,97,1)","rgba(132,153,116,1)","rgba(78,81,109,1)"]
	if resitems == []:
		# return []
		items = NER_stocks(keyword)
		upload_data_ner(items, 'stocks_store')
		for i in range(len(items)):
			company.append(items[i]['english company'])
			stock_price.append(items[i]['close'])
			date.append(items[i]['date'])
			count.append(items[i]['count'])
	else:
		for i in range(len(resitems)):
			company.append(resitems[i]['_source']['english company'])
			date.append(resitems[i]['_source']['date'])
			stock_price.append(resitems[i]['_source']['close'])
			count.append(resitems[i]['_source']['count'])

	company_details = pd.DataFrame({'company':company, 'date':date, 'stock price' :stock_price, 'count':count})
	company_details =  company_details.sort_values('count', ascending = False)


	company_sorted = company_details.company.tolist()
	stock_sorted = company_details['stock price'].tolist()
	date_sorted = company_details['date'].tolist()

	data = list() 	

	if len(company_sorted) >= 5:

		for i in range(5):
			trace = {
			   "x": date_sorted[i],
			   "y": stock_sorted[i],
			  "line": {"color": color[i]}, 
			  "mode": "lines", 
			  "name": company_sorted[i], 
			  "type": "scatter", 
			  "xaxis": "x", 
			  "yaxis": "y"
			}
			data.append(trace)
	else:
		for i in range(len(company_sorted)):
			trace = {
			   "x": date_sorted[i],
			   "y": stock_sorted[i],
			  "line": {"color": color[i]}, 
			  "mode": "lines", 
			  "name": company_sorted[i], 
			  "type": "scatter", 
			  "xaxis": "x", 
			  "yaxis": "y"
			}
			data.append(trace)



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
		    "rangeselector": {"buttons": [
		        {
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
		  }
		}
	fig = go.Figure(data=data, layout=layout)
	plot(fig, filename = 'techscan/templates/graph/stock_graph.html', auto_open=False)
