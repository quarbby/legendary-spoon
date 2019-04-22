from uploading_data import upload_data
from config import location, es
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def plot_stocks():
	res = es.search(index = 'stockmarket_10years', size = 10000, scroll = '2m' , body= {"query": {"match_all": {}}})
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
	plot_url = plot(fig)
	# details = res['hits']['hits'][2]['_source']['company']

	# pprint(details)
	# dates=list()
	# values=list()
	# for key, value in details:
	# 	dates.append(key)
	# 	value.append(value)
	# pprint(dates)
	# pprint(values)

	# for i in res['hits']['hits']:
	# 	print(i)

		
plot_stocks()

