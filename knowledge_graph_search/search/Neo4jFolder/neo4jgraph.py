import json
import ast
import igraph as ig
from pprint import pprint

location = 'search/Neo4jFolder/data/query.json'
def plot_neo4j_graph():
	###NodeID###
	TotalNode = []
	NodeID = []
	###Relations###
	relations = []

	with open(location, 'r+') as f:
	  data = f.read()
	  papers = ['{"f":'+ element for element in data.split('{"f":')[1:]]
	  papers = [ast.literal_eval(element) for element in papers]

	# pprint(papers[0]['f']['rels'][0])

	for j in range (len(papers)):
	 for i in range (len(papers[j]['f']['nodes'])):
	  if papers[j]['f']['nodes'][i]['labels'][0] == 'Field':
	   node = {"id": papers[j]['f']['nodes'][i]['id'], "name": papers[j]['f']['nodes'][i]['properties']['fieldName']}
	   if node not in TotalNode:
	    TotalNode.append(node)

	 for l in range (len(papers[j]['f']['rels'])):
	  relations.append({"source": papers[j]['f']['rels'][l]['start']['id'],"target": papers[j]['f']['rels'][l]['end']['id']})

	HELL=[]
	count1 = -1
	for i in range (len(TotalNode)):
	 count1 += 1 
	 HELL.append({"group": count1, "name": TotalNode[i]['name'], "id": TotalNode[i]['id']})


	YEAH = []
	for j in range (len(relations)):
	 x=[]
	 y=[]
	 for k in range (len(HELL)):
	  if relations[j]['source'] == HELL[k]['id']:
	   x.append(HELL[k]['group'])
	  if relations[j]['target'] == HELL[k]['id']:
	   y.append(HELL[k]['group'])
	 YEAH.append({"source": x[0], "target": y[0]})

	graph = { 'nodes': HELL, 'edges': YEAH}
	# pprint(graph)
	N=len(graph['nodes'])
	print(N)

	L=len(graph['edges'])
	Edges=[(graph['edges'][k]['source'], graph['edges'][k]['target']) for k in range(L)]
	# pprint(len(graph['nodes']['id']))
	G=ig.Graph(Edges, directed=False)

	labels=[]
	group=[]
	for node in graph['nodes']:
	    labels.append(node['name'])
	    group.append(node['group'])


	layt=G.layout('kk', dim=3) 
	print(len(layt))

	Xn=[layt[k][0] for k in range(N-1)]# x-coordinates of nodes
	Yn=[layt[k][1] for k in range(N-1)]# y-coordinates
	Zn=[layt[k][2] for k in range(N-1)]# z-coordinates
	Xe=[]
	Ye=[]
	Ze=[]
	for e in Edges:
	    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
	    Ye+=[layt[e[0]][1],layt[e[1]][1], None]  
	    Ze+=[layt[e[0]][2],layt[e[1]][2], None]

	import plotly.plotly as py
	import plotly.graph_objs as go
	from plotly.offline import download_plotlyjs, init_notebook_mode, plot

	trace1=go.Scatter3d(x=Xe,
	               y=Ye,
	               z=Ze,
	               mode='lines',
	               line=dict(color='rgb(125,125,125)', width=1),
	               hoverinfo='none'
	               )

	trace2=go.Scatter3d(x=Xn,
	               y=Yn,
	               z=Zn,
	               mode='markers+text',
	               name='actors',
	               marker=dict(symbol='circle',
	                             size = 10,
	                             color=group,
	                             colorscale='Viridis',
	                             line=dict(color='rgb(50,50,50)', width=0.5)
	                             ),
	               text=labels,
	               hoverinfo='text'
	               )

	axis=dict(showbackground=False,
	          showline=False,
	          zeroline=False,
	          showgrid=False,
	          showticklabels=False,
	          title='',
						showspikes=False
	          )

	layout = go.Layout(
	         # title="Related Fields and Authors",
	         # width=500,
	         # height=500,
	         # autosize = True,
	         showlegend=False,
	         scene=dict(
	             xaxis=dict(axis),
	             yaxis=dict(axis),
	             zaxis=dict(axis),
	        ),
	     margin=dict(
	        t=0,
	        l=0,
	        r=0,
	        b=0

	    ),
	    hovermode='closest',

	    # annotations=[
	    #        dict(
	    #        showarrow=False,
	    #         text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
	    #         xref='paper',
	    #         yref='paper',
	    #         x=0,
	    #         y=0.1,
	    #         xanchor='left',
	    #         yanchor='bottom',
	    #         font=dict(
	    #         size=14
	    #         )
	    #         )
	    #     ],  
	          )

	data=[trace1, trace2]
	fig=go.Figure(data=data, layout=layout)

	plot(fig, filename = 'search/templates/neo4jgraph.html', auto_open=False)