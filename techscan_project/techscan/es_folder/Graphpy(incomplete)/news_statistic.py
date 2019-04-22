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


with open("News.json") as f: 
    content = json.load(f)

emptyones = []
for i in range (len(content)):
	if content[i]['authors'].split('[')[1].split(']')[0] == 'None' or content[i]['authors'].split("[")[1].split("]")[0] =="''":
		emptyones.append(i)
		# pprint (content[i]['authors'])
	# pprint(content[i]['authors'].split('[')[1].split(']')[0])

emptyones.reverse()
for i in range(len(emptyones)):
	del content[emptyones[i]]

# print(len(content))

empty = []
for j in range (len(content)):
	a = content[j]['authors'].split("[")[1].split("]")[0].split("'")[1].split(",")[0]
	# print(a)
	if "www." in a or "@" in a or "#" in a or ".com" in a or "Ð¡Ð¾Ð»Ð¾Ð¼Ð¾Ð½Ð¾Ð²Ð°" in a or "Ð°ÐºÐ¾Ð²Ð°" in a or "MIT" in a: 
		empty.append(j)
	# content[j]['authors'] = content[j]['authors'].split("[")[1].split("]")[0].split("'")[1]	
empty.reverse()
for i in range(len(empty)):
	del content[empty[i]]

for i in range (len(content)):	
	
	content[i]['authors'] = content[i]['authors'].split("[")[1].split("]")[0].split("'")[1].split(",")[0].split('&')
	pprint(content[i])


# for i in range(len(content)):
# 	for j in range (len(content[i]['authors'])):
# 		print(content[i]['authors'][j])