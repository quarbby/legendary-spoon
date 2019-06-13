import re
import plotly
import jieba
import jieba.posseg as psg
import nltk
import math
import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
from PIL import Image
from ..config import es
from .main_functions import chi_translation
from .scroll_query import text_query, processing_hits
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.figure_factory as ff
from .uploading_data import upload_data_ner
from .update_heatmap import  findNER_esNews, googlemaps_input
import spacy


def main_graph(keyword):
	try:
		df_english = text_query(str(keyword), dataframe = True)
		df_chinese = text_query(str(chi_translation(keyword)), dataframe = True)
		df = pd.concat([df_english,df_chinese], ignore_index = True)
		dates = ['2017', '2018', '2019']
		df = df.dropna(subset = ['date'])
		df = df[df.date.str.contains('|'.join(dates))]

	
		df['published_date'] = df['date'].apply(lambda x:  x[:7])
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
			width = 780,
			height = 300,
			
			legend = dict(x = 0.1, y = 1.15, orientation = "h"),
			updatemenus = list([
				dict(
					buttons = list([
						dict(
							args = [{'visible': [True,True,True]},],
							label = "All",
							method = "update",
							),
						dict(
							args = [{'visible':[True,False,False]},],
							label = "2017",
							method = "update",
							),
						dict(
							args = [{'visible':[False,True,False]},],
							label = "2018",
							method = "update",
							),
						dict(
							args = [{'visible':[False,False,True]},],
							label = "2019",
							method = "update",
							)
						])
					)
				])
			)
		fig = dict(data=data, layout=layout)
		plot(fig, filename = 'techscan/templates/graph/main_graph_all.html', auto_open=False)
	except:
		return "False"

def top_hashtag(keyword):
	try:
		df = text_query(chi_translation(keyword),'weibo', dataframe = True)
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
	except:
		return "False"

def twitter_bubble(keyword):
	try:
		df = text_query(keyword, 'tweets', dataframe = True)
		df['hashtags'] = df['hashtags'].apply(lambda x: str(x))
		df2 = df.groupby('hashtags').sum().reset_index().sort_values('retweet_count', ascending = False)
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
	except:
		return "False"

def twitter_graph(keyword):
	df = text_query(keyword, 'tweets',dataframe = True)
	try:
		df_new = df.groupby(['author']).sum().reset_index()
		final = [df_new['favorite_count'].tolist()]
		name_List = [df_new['author'].tolist()]
		group_label = ['Favorite Count']
		fig = ff.create_distplot(final, group_label,bin_size = .1, curve_type='normal',rug_text = name_List,show_hist=False)
		fig['layout'].update(title='Distplot with Normal Distribution')
		plot(fig, filename='techscan/templates/graph/twitter_graph.html', auto_open=False)
	except:
		pass

def wordcloud(keyword):
	df_weibo = text_query(chi_translation(keyword),'weibo', dataframe = True)
	try:
		with open('techscan/static/word_cloud/stopword.txt', encoding = 'utf-8') as f:
			stopword_chinese = f.read()
		df_weibo['summary'] = df_weibo['summary'].apply(lambda x: ' '.join([word for word in jieba.cut(x,cut_all=False) if word not in stopword_chinese]))
		
		
		df_weibo = df_weibo[df_weibo['summary']!='']
		summary_list = df_weibo['summary'].tolist()
		summary_string = ''.join(summary_list)

		font_path = 'techscan/static/word_cloud/STFangSong.ttf'
		wordcloud = WordCloud( background_color = "white", collocations = False, max_words = 100, font_path=font_path,
			max_font_size = 100, random_state = 42, width = 600, height = 400, margin = 2).generate(summary_string)
		
		wordcloud.to_file("techscan/static/word_cloud/weibo_wordcloud.png")
	except:
		return "False"


def twitter_wordcloud(keyword):
	df_twitter = text_query(keyword,'tweets', dataframe = True)
	try:
		stopword_english = stopwords.words('english')
		df_twitter['summary'] = df_twitter['summary'].apply(lambda x:' '.join(re.sub('http\S+\s*', '', x).split()))
		df_twitter['summary'] = df_twitter['summary'].apply(lambda x: re.sub('[\W]', ' ', x))
		df_twitter['summary'] = df_twitter['summary'].apply(lambda x:' '.join(re.sub('http\S+\s*', '', x).split()))
		df_twitter['summary'] = df_twitter['summary'].apply(lambda x: ' '.join([word for word in x.split(' ') if word not in stopword_english]))
		df_twitter['summary'] = df_twitter['summary'][df_twitter['summary']!='']
		summary_list = df_twitter['summary'].tolist()
		summary_string = ''.join(summary_list)
		mask = np.array(Image.open('techscan/static/word_cloud/tweet.png'))
		font_path = 'techscan/static/word_cloud/STFangSong.ttf'
		wordcloud = WordCloud( background_color = "white", collocations = False, max_words = 100, font_path = font_path,
			max_font_size = 100, random_state = 42, width = 600, height = 400, margin = 2, mask = mask).generate(summary_string)
		wordcloud.to_file("techscan/static/word_cloud/tweets_wordcloud.png")
	except:
		return "False"


def detail_hashtag_frequency(keyword):
	Total_hashtag = []
	Total_count = []
	color_list = []
	text_list = []
	try:
		df_twitter = text_query(keyword, 'tweets',dataframe = True)
		df_twitter['hashtags'] = df_twitter['hashtags'].apply(lambda x:''.join(re.sub('[^\w]', '',  str(x)).split()))
		
		df_twitter['hashtags'] = df_twitter['hashtags'].apply(lambda x: x.replace("ai", "AI"))
		df_twitter = df_twitter[df_twitter['hashtags'] != '']
		twitter_record = df_twitter.to_dict('records')
		twitter_hashtag_count = Counter(hashtag['hashtags'] for hashtag in twitter_record)
		twitter_tophashtags = twitter_hashtag_count.most_common(15)

		for i in twitter_tophashtags:
			Total_hashtag.append(i[0])
			Total_count.append(i[1])
			color_list.append('rgb(106,167,156)')
			text_list.append('Twitter')
	except:
		pass

	try:
		df_weibo = text_query(chi_translation(keyword),'weibo', dataframe = True)
		df_weibo ['hashtags']= df_weibo['hashtags'].apply(lambda x:''.join(re.sub('[^\w]', '',  str(x)).split()))
		df_weibo = df_weibo[df_weibo['hashtags']!='']
		weibo_record = df_weibo.to_dict('records')
		weibo_hashtag_count = Counter(hashtag['hashtags'] for hashtag in weibo_record)
		weibo_tophashtags = weibo_hashtag_count.most_common(15)
		
		for i in weibo_tophashtags:
			Total_hashtag.append(i[0])
			Total_count.append(i[1])
			color_list.append('rgb(246,156,99)')
			text_list.append('Weibo')
	except:
		pass
	try:
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
	except:
		return "False"

def heatmap(keyword):

	search_term = chi_translation(keyword)
	if 'heatmap' not in es.indices.get_alias().keys():
		es.indices.create(index = 'heatmap')
	res = es.search(index = 'heatmap' , size = int(10000), scroll = '2m', body = {"query" : {
		"match" : {"labels" : search_term}}})
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
		try:
			Items = googlemaps_input(keyword,findNER_esNews(keyword))
			upload_data_ner(Items, 'heatmap')
		except:
			city = [go.Scattergeo(
				locationmode = 'ISO-3',)]

			layout = go.Layout(
				legend = dict(x = 1.02, y = 0.5, orientation = "v"),
				showlegend = True,
				font = go.layout.Font(size = 15,
					family = 'roboto'),
				autosize = True,
				width = 780,
				height = 300,
				margin=go.layout.Margin(
						l=0,
						r=0,
						b=0,
						t=0,
						pad=1),
					
					xaxis = dict (fixedrange = True),
					yaxis = dict (fixedrange = True),
						
						geo = go.layout.Geo(
							scope = 'world',
							projection = go.layout.geo.Projection(
								type='equirectangular'  
								),

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

			fig = go.Figure(data = city, layout=layout)
			plot(fig, filename='techscan/templates/graph/heatmap.html', auto_open=False)
			return None

		for i in range (len(Items)):
			companies.append(Items[i]['publisher'])
			Latitude.append(Items[i]['Address'][0]['geometry']['location']['lat'])
			longtitude.append(Items[i]['Address'][0]['geometry']['location']['lng'])
			address.append(Items[i]['Address'][0]['formatted_address'])
			if 0 < int(Items[i]['weighting']) <= 5:
				weight.append(100)

			elif 5 < int(Items[i]['weighting']) <= 20:
				weight.append(200)

			elif 20 < int(Items[i]['weighting']) <= 50:
				weight.append(500)

			elif 50 < int(Items[i]['weighting']) <= 100:
				weight.append(1000)

			elif 100 < int(Items[i]['weighting'] ):
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
				weight.append(100)

			elif 5 < int(resItems[i]['_source']['weighting']) <= 20:
				weight.append(200)

			elif 20 < int(resItems[i]['_source']['weighting']) <= 50:
				weight.append(500)

			elif 50 < int(resItems[i]['_source']['weighting']) <= 100:
				weight.append(1000)

			elif 100 < int(resItems[i]['_source']['weighting']  ):
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

			name = '{}'.format(df_colors) 
			)
		cities.append(city)

	layout = go.Layout(
		legend = dict(x = 1.02, y = 0.5, orientation = "v"),
		showlegend = True,
		font = go.layout.Font(size = 15,
			family = 'roboto'),
		autosize = True,
		width = 780,
		height = 300,
		margin=go.layout.Margin(
				l=0,
				r=0,
				b=0,
				t=0,
				pad=1),
			
			xaxis = dict (fixedrange = True),
			yaxis = dict (fixedrange = True),
				
				geo = go.layout.Geo(
					scope = 'world',
					projection = go.layout.geo.Projection(
						type='equirectangular'  
						),

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
	search_term = chi_translation(keyword)
	res = es.search(index = 'heatmap' , size = int(10000), scroll = '2m', body = {"query" : {"match" : {"labels" : search_term}}})
	

	res_input = res['hits']['hits']
	resItems = []

	for i in range (len(res_input)):
		if res_input[i]['_source']['labels'] == search_term :
			resItems.append(res_input[i])

	company_name = []
	count = []
	for i in range (len(resItems)):
		company_name.append(resItems[i]['_source']['publisher'])
		count.append(int(resItems[i]['_source']['weighting']))

	data = {'company' : company_name, 'count' : count}
	df_new = pd.DataFrame(data)
	df_new = df_new.sort_values('count',ascending = False)[:10]
	json_frame = df_new.to_dict('index').values()
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



def people_companies(keyword):
	nlp = spacy.load('en_core_web_md')
	df_news = text_query(chi_translation(keyword), 'news', dataframe= True)
	df_twitter = text_query(keyword, 'tweets', dataframe =True)
	with open('techscan/static/word_cloud/stopword.txt', encoding = 'utf-8') as f:
		stopword_chinese = f.read()
	try:
		df_news['summary'] = df_news['summary'].apply(lambda x: ' '.join([word for word in jieba.cut(x,cut_all=False) if word not in stopword_chinese]))
	except:
		pass
	total_tech = []
	total_company = []
	total_people = []
	try:
		stopword_english = stopwords.words('english')
		extra = ['rt', 'ai']
		stopword_english = stopword_english.extend(extra)
		df_twitter['summary'] = df_twitter['summary'].apply(lambda x: x.lower())
		df_twitter['summary'] = df_twitter['summary'].apply(lambda x: re.sub('[\W]', ' ', x))
		df_twitter['summary'] = df_twitter['summary'].apply(lambda x:' '.join(re.sub('http\S+\s*', '', x).split()))
		df_twitter['company'] = df_twitter['summary'].apply(lambda x: nlp(x))
		df_twitter['company'] = df_twitter['company'].apply(lambda x:' '.join( [word.text for word in x.ents if word.label_ == 'ORG']))
		
		tweets_companies = df_twitter['company'].tolist()
		total_company.extend(tweets_companies)
		
		tweets_summary_list = df_twitter.summary.tolist()
		total_tech.extend(tweets_summary_list)
	 
		tweets_people = df_twitter.mentions.tolist() + df_twitter.user_screen_name.tolist()
		total_people.extend(tweets_people)
	except:
		pass
	    
	try:
		news_summary_list = df_news.summary.tolist()
		news_summary_string = "".join(news_summary_list)
		total_tech.extend(news_summary_list)
		news_tokenised = psg.cut(news_summary_string)
		news_org_list = []
		news_people = []
		for token in news_tokenised:
			if token.flag == "nt":
				news_org_list.append(token.word)
			if token.flag == "nr":
				news_people.append(token.word)
		total_people.extend(news_people)
		news_companies = []
		for org in news_org_list:
			if '公司' in org or '集团'in org:
				news_companies.append(org)
		total_company.extend(news_companies)
	except:
		pass

	try:
		total_tech = ' '.join(total_tech)
		total_company = ' '.join(total_company)
		total_people = ' '.join(total_people)

		wordcloud_info = dict()
		wordcloud_info['label'] = keyword
		wordcloud_info['company'] = total_company
		wordcloud_info['people'] = total_people
		wordcloud_info['tech'] = total_tech
		wordcloud_list = []
		wordcloud_list.append(wordcloud_info)
		return(wordcloud_list)
	
	except:
		pass
		
def people_companies_wordcloud(keyword):
	if 'wordcloud' not in es.indices.get_alias().keys():
		es.indices.create(index = 'wordcloud')
	res = es.search(index = 'wordcloud' , size = int(10000), scroll = '2m', body = {"query" : {
        "match" : {"label" : keyword}
        }})
	res_input = res['hits']['hits']
	if res_input == [] :
	
		details = people_companies(keyword)
		upload_data_ner('wordcloud',details)
		total_tech = details[0]['tech']
		total_company = details[0]['company']
		total_people = details[0]['people']

	else:
		total_tech = res_input[0]['_source']['tech']
		total_company = res_input[0]['_source']['company']
		total_people = res_input[0]['_source']['people']
	
	font_path = 'techscan/static/word_cloud/STFangSong.ttf'
	
	try:
		wordcloud = WordCloud( background_color = "white", collocations = False, max_words = 100, font_path = font_path,
	    	max_font_size = 100, random_state = 42, width = 600, height = 400, margin = 2, colormap="copper").generate(total_tech)
		wordcloud.to_file("techscan/static/word_cloud/tech_wordcloud.png")
	except:
		return "False"
	try:
		wordcloud = WordCloud( background_color = "white", collocations = False, max_words = 100, font_path = font_path,
	        max_font_size = 100, random_state = 42, width = 600, height = 400, margin = 2, colormap="winter").generate(total_company)
		wordcloud.to_file("techscan/static/word_cloud/company_wordcloud.png")
	except:
		return "False"
	try:
		wordcloud = WordCloud( background_color = "white", collocations = False, max_words = 100, font_path = font_path,
	        max_font_size = 100, random_state = 42, width = 600, height = 400, margin = 2, colormap="twilight_shifted").generate(total_people)
		wordcloud.to_file("techscan/static/word_cloud/people_wordcloud.png")
	except:
		return "False"


def sort_by_dates(keyword):
	df_weibo = text_query(chi_translation(keyword),'weibo',dataframe = True)
	df_news = text_query(chi_translation(keyword),'news',dataframe = True)
	df_scholar = text_query(keyword,'scholar',dataframe = True)
	df_tweets = text_query(keyword,'tweets',dataframe = True)
	df_zhihu = text_query(chi_translation(keyword),'zhihu',dataframe = True)
	
	if df_weibo is None:
		json_weibo = []
	else:
		df_weibo = df_weibo.drop_duplicates(subset = 'summary', keep = 'first')
		df_weibo = df_weibo.sort_values(['published','favorite_count'], ascending = [False,False]).head(100)
		json_weibo = df_weibo.head(20).to_dict('records')
	
	if df_zhihu is None:
		json_zhihu = []
	else:
		df_zhihu = df_zhihu.drop_duplicates(subset = 'summary', keep = 'first')
		df_zhihu = df_zhihu.sort_values(['published','upvotes'], ascending = [False,False]).head(100)
		json_zhihu = df_zhihu.head(20).to_dict('records')

	if df_tweets is None:
		json_tweets = []
	else:
		df_tweets = df_tweets.drop_duplicates(subset = 'summary', keep = 'first')
		df_tweets = df_tweets.sort_values(['published','favorite_count'], ascending = [False,False]).head(100)
		json_tweets = df_tweets.head(20).to_dict('records')

	if df_news is None:
		json_news = []
	else:
		df_news = df_news.drop_duplicates(subset = 'summary', keep = 'first')
		df_news = df_news.sort_values('published', ascending = False)
		json_news = df_news.head(20).to_dict('records')

	if df_scholar is None:
		json_scholar = []
	else:
		df_scholar = df_scholar.drop_duplicates(subset = 'summary', keep = 'first')
		df_scholar = df_scholar.sort_values('published', ascending = False)
		json_scholar = df_scholar.head(20).to_dict('records')

	return json_zhihu, json_tweets, json_scholar, json_news, json_weibo
