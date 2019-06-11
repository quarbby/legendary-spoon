



def plot_stocks(keyword):
	res_input = res['hits']['hits']
	resitems = []
	for i in range (len(res_input)):
	    if res_input[i]['_source']['label'] == keyword:
	        resitems.append(res_input[i])

	stock_price = []
	date = []
	company = []
	count = []
	color = ["rgba(31,119,180,1)", "rgba(51,129,180,16)","rgba(191,29,70,6)","rgba(1,29,18,160)","rgba(101,29,8,160)"]
	if resitems == []:
		items = NER_stocks(keyword)
		upload_data_ner(items, 'stock_test')
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
			  "line": {"color": "rgba(31,119,180,1)"}, 
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
	plot(fig, filename = 'basic-barchart')