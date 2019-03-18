import pandas as pd
from df_to_es import pd_to_es
from scroll_query import processing_hits, query
from delete_index import delete_indices
from config import es
from uploading_data import upload_data
from processing_dataframe import processing_df
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot

"""
Function to plot Linear graph by year
"""

def count_year(keyword):
	df = query(str(keyword))
	df = processing_df(df)
	df = df['published_year'].value_counts()
	df = df.sort_index(ascending = False)

	trace = go.Scatter(
		x = df.index,
		dx = 5,
		y = df.values,
		mode = 'lines+markers',
		name = 'number of papers by day')
	data = [trace]
	fig = dict(data=data)
	chart = plot(fig, filename = "Paper count by year.html")

	return(chart)


"""
Function to plot Linear graph by day
"""

def count_date(keyword):
	df = query(str(keyword))
	df = processing_df(df)
	df = df['published_date'].value_counts()
	df = df.sort_index(ascending = False)
	trace = go.Scatter(
		x = df.index,
		dx = 5,
		y = df.values,
		mode = 'lines+markers',
		name = 'number of papers by day')
	data = [trace]

	layout = dict(
		title='Paper count by date',
		xaxis=dict(rangeselector=dict(
			buttons=list([
				dict(count=1,
					label='1m',
					step='month',
					stepmode='backward'),
				dict(count=6,
				label='6m',
				step='month',
				stepmode='backward'),
				dict(count = 1,
					label = '1yr',
					step = 'year',
					stepmode = 'backward'),
				dict(step = 'all')
				])
			),
		rangeslider=dict(
			visible = True
			),
		type='date'
		))
	fig = dict(data=data, layout=layout)
	chart = plot(fig, filename = "Paper count by date.html")
	return(chart)
