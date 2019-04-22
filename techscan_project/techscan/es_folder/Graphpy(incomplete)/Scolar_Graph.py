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


with open("Scholar.json") as f: 
    content = json.load(f)


# pprint(content[0])
# for i in range (len(content)):
# 	pprint(content[i]['categories'])
Authors = []
categories = []
for i in range (len(content)):
	for j in content[i]['authors']:
		for k in content[i]['categories']:
			Authors.append(j)
			categories.append(k)

print(len(categories))
print(len(Authors))

df = pd.DataFrame({'Authors': Authors,'categories': categories ,'count': 1})
SearchTerm = 'Adversarial Autoencoders'
for i in range (len(df)):
	if df['categories'][i] == SearchTerm :
		print(df['Authors'][i],df['count'][i])




