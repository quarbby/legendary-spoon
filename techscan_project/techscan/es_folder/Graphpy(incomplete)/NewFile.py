import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot
import math
import pandas as pd
from ast import literal_eval
import numpy as np
import json
from pprint import pprint


with open("Zhihu_AI.json") as f: 
    content = json.load(f)

df = pd.DataFrame.from_dict(content, orient='columns')
maximum = df.upvotes.max()
minimum = df.upvotes.min()


upvotes_count = df.groupby(['author']).sum().reset_index()	
post_freq = df.groupby(['author']).size().rename('size').reset_index().sort_values('size', ascending = False)
post_freq.rename(columns={'author': 'author_1'}, inplace=True)
df_new = pd.concat([upvotes_count, post_freq], axis = 1).drop(columns = ['author_1'])
df_new['average'] = df_new['upvotes']/df_new['size']
df_new['max'] = df.groupby('author', as_index=False)['upvotes'].max()['upvotes']

df_new['weighted'] = (0.6 * df_new['max']) + (0.15*df_new['upvotes']) + (0.25*df_new['average'])
df_new = df_new.sort_values('upvotes', ascending=True)
# print(math.floor(len(df_new)*9/10))

def percentile (Authorlist,countlist):
	initial = 0
	for i in range (len(countlist)):
		if initial < math.floor(len(df_new)*9.5/10):
			initial = initial + countlist[i] 
		else :
			value = i
			break
	return value
	
def Add_in_Authors (author, li, min, max):
	ctr = 0
	place_names = []
	for k in range(len(li)):
		if min < li[k] <= max:
			place_names.append(author[k])
			ctr += 1
	return place_names, ctr

def Set_List_color (val):
	colorList = []
	for i in range (val):
		colorList.append('#00cc66')	
	for j in range (val,(len(Totalcount))):
		colorList.append('#ff3333')
	return colorList


rng = []
max_range = 22000
for i in range (int(max_range/50)):
	rng.append(str(i*50) + '-' + str((i+1)*50))

AuthorList = []
Totalcount = []
for j in range (len(rng)):

	x , y = Add_in_Authors(df_new['author'],df_new['upvotes'], j*50, (j+1)*50)
	AuthorList.append(x)
	Totalcount.append(y)
print (len(rng))

x = percentile(AuthorList,Totalcount)
ColorList = Set_List_color(x)

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
    marker=dict( color= ColorList[0]),
    name = 'Lower 95th Percentile '
    )
trace2 = go.Bar(
	# histfunc ="sum",
	# autobinx = False,
	hoverinfo = "text",	
    x=rng,
    y=chunks_count_upper,
    text = chunks_Author_upper,
    marker=dict( color= ColorList[100]),
    name = 'Upper 5th percentile'
    )
layout = go.Layout(barmode='stack',
	xaxis = dict(
		dtick=10	,
		# range = [0,30]
		) ,
	yaxis =  dict( range = [0,150],
		dtick=50
		),
	bargap=0,
    bargroupgap=0.01,
    showlegend = True,
    title = go.layout.Title(
            text = 'ZhiHu: Upvote counts for Authors')
    # violinmode = "group"
	)
data = [trace1,trace2]
fig = go.Figure(data = data, layout=layout)

plot(fig, filename='zhihu upvote statistic.html')
