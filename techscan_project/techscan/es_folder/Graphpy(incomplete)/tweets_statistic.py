import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot
import random
import pandas as pd
from ast import literal_eval
import numpy as np
import json
import math
from pprint import pprint


with open("Tweets_AI.json") as f: 
    content = json.load(f)
# pprint(content[0])

df = pd.DataFrame.from_dict(content, orient='columns')
df_new = df.groupby(['user_screen_name']).sum().reset_index()
print(df_new)

def percentile (Authorlist,countlist):
	initial = 0
	for i in range (len(countlist)):
		if initial < math.floor(len(df_new)*9.9/10):
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
print (AuthorList)
print(Totalcount)

x = percentile(AuthorList,Totalcount)
print(x)

chunks_count_lower = Totalcount.copy()
chunks_Author_lower = AuthorList.copy()
chunks_count_upper = Totalcount.copy()
chunks_Author_upper = AuthorList.copy()
# print (chunks_count_lower)
# print(chunks_count_upper)
for i in range (x, len(Totalcount)):
	chunks_count_lower[i] = 0
	chunks_Author_lower[i] = []

for i in range (x):
	chunks_count_upper[i] = 0
	chunks_Author_upper[i] = []
print(len(chunks_Author_upper))
print(len(rng))
trace1 = go.Bar(
	# histfunc ="sum",
	# autobinx = False,
	hoverinfo = "text",	
    x=rng,
    y=chunks_count_lower,	
    text = chunks_Author_lower,
    # marker=dict( color= ColorList[0]),
    name = 'Lower 99th Percentile '
    )
trace2 = go.Bar(
	# histfunc ="sum",
	# autobinx = False,
	hoverinfo = "text",	
    x=rng,
    y=chunks_count_upper,
    text = chunks_Author_upper,
    # marker=dict( color= ColorList[100]),
    name = 'Upper 1st percentile'
    )
layout = go.Layout(barmode='stack',
	xaxis = dict(
		dtick=10	,
		# range = [0,30]
		) ,
	yaxis =  dict(
		range = [0,200]
		# dtick=100
		),
	bargap=0,
    bargroupgap=0.01,
    showlegend = True,
    title = go.layout.Title(
            text = 'tweets: favorite counts for usernames')
    # violinmode = "group"
	)
data = [trace1,trace2]
fig = go.Figure(data = data, layout=layout)

plot(fig, filename='tweets favorite count statistic.html')