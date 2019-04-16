import json
from pprint import pprint
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

with open("Zhihu_AI.json") as f: 
    content = json.load(f)

df = pd.DataFrame.from_dict(content, orient='columns')
maximum = df.upvotes.max()
minimum = df.upvotes.min()

upvotes_count = df.groupby(['author']).sum().reset_index().sort_values('upvotes', ascending=False)
print(upvotes_count)

post_freq = df.groupby(['author']).size().rename('size').reset_index().sort_values('size', ascending = False)
post_freq.rename(columns={'author': 'author_1'}, inplace=True)

df_new = pd.concat([upvotes_count, post_freq], axis = 1).drop(columns = ['author_1'])
df_new['average'] = df_new['upvotes']/df_new['size']
df_new['max'] = df.groupby('author', as_index=False)['upvotes'].max()['upvotes']
df_new['weighted'] = (0.6 * df_new['max']) + (0.15*df_new['upvotes']) + (0.25*df_new['average'])

df_new = df_new.sort_values('weighted',ascending = False).reset_index()[:20].sort_values('weighted',ascending = False)
# print(df_new)
data = [go.Bar(
            x=df_new['size'],
            y=df_new['author'],
            orientation = 'h',
)]

# plot(data, filename='horizontal-bar.html')