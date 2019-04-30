# from neo4j import GraphDatabase
import igraph as ig
import ast
from ..config import neo4jdriver
from ..es_folder import main_functions

# def related_field(keyword):
#   with neo4jdriver.session() as session:
#     relatedField = session.run("MATCH (f:Field:SubGraphCS)<-[:PART_OF_FIELD]-(f1:Field:SubGraphCS) WHERE f.fieldName =~ '(?i).*{}.*' RETURN DISTINCT f1.fieldName,f1.fieldPaperNum ORDER BY f1.fieldPaperNum DESC LIMIT 10".format(keyword))
#   return [{"fieldName" : record['f1.fieldName']} for record in relatedField]
def related_field(keyword):
  with neo4jdriver.session() as session:
    relatedField = session.run("MATCH (f:Field)<-[:PART_OF_FIELD]-(f1:Field) WHERE f.fieldName =~ '(?i){}' RETURN DISTINCT f1.fieldName,f1.fieldPaperNum ORDER BY f1.fieldPaperNum DESC LIMIT 5".format(keyword))
    related_field_list = [{"fieldName" : record['f1.fieldName']} for record in relatedField]
    if related_field_list != []:
      return related_field_list
    else:
      relatedField = session.run("MATCH (f:Field)<-[:PART_OF_FIELD]-(f1:Field) WHERE f.fieldName =~ '(?i).*{}.*' RETURN DISTINCT f1.fieldName,f1.fieldPaperNum ORDER BY f1.fieldPaperNum DESC LIMIT 10".format(keyword))
      related_field_list = [{"fieldName" : record['f1.fieldName']} for record in relatedField]
      return related_field_list
# ColorListArrays = ['rgb(0,0,0)','rgb(15,41,68)','rgb(254,144,4)','rgb(100,100,100)','rgb(300,0,214)','rgb(0,200,0)','rgb(0,0,100)','rgb(15,41,68)']

def search_field(Keyword):
  with neo4jdriver.session() as session:
    output = session.run('MATCH f=(f1:Field)<-[r1:PART_OF_FIELD]-(q:Field) WHERE f1.fieldName =~ "(?i){}" OPTIONAL MATCH e=(q)<-[r2:PART_OF_FIELD]-(w:Field) RETURN f,e ORDER BY q.fieldPaperNum DESC LIMIT 100'.format(Keyword))
    result = [record for record in output]
    if result != []:
      return result
    else:
      output = session.run('MATCH f=(f1:Field)<-[r1:PART_OF_FIELD]-(q:Field) WHERE f1.fieldName =~ "(?i).*{}.*" OPTIONAL MATCH e=(q)<-[r2:PART_OF_FIELD]-(w:Field) RETURN f,e ORDER BY q.fieldPaperNum DESC LIMIT 100'.format(Keyword))
      result = [record for record in output]
      return result
      
def plotgraph(result):
  try:
    TotalNode = []
    relations = []
    for j in range (len(result)):
      for i in range (len(result[j]['f'].nodes)):
        if list(result[j]['f'].nodes[i].labels)[0] == 'Field' or list(result[j]['f'].nodes[i].labels)[0] == 'SubGraphCS':
          node = {"id": str(result[j]['f'].nodes[i].id) , "name": result[j]['f'].nodes[i].get('fieldName') , "Ranks": 20, "labels": 'rgb(15,41,68)'}
          if node not in TotalNode:
            TotalNode.append(node)

        elif list(result[j]['f'].nodes[i].labels)[0] == 'Author':
          node = {"id": str(result[j]['f'].nodes[i].id), "name": result[j]['f'].nodes[i].get('authorName'), "Ranks": 10, "labels": 'rgb(254,144,4)'}
          if node not in TotalNode:
            TotalNode.append(node)

        elif list(result[j]['f'].nodes[i].labels)[0] == 'Paper':
          node = {"id": str(result[j]['f'].nodes[i].id), "name": result[j]['f'].nodes[i].get('paperName'), "Ranks": 100*papers[j]['f']['nodes'][i]['properties']['articleRank'], "labels": 'rgb(15,41,68)'}
          if node not in TotalNode:
            TotalNode.append(node)

        elif list(result[j]['f'].nodes[i].labels)[0] == 'Paper':
          node = {"id": str(result[j]['f'].nodes[i].id), "name": result[j]['f'].nodes[i].get('paperName'), "Ranks": 100*papers[j]['f']['nodes'][i]['properties']['articleRank'], "labels": 'rgb(15,41,68)'}
          if node not in TotalNode:
            TotalNode.append(node)

        elif list(result[j]['f'].nodes[i].labels)[0] == 'Journal':
          node = {"id": str(result[j]['f'].nodes[i].id), "name": result[j]['f'].nodes[i].get('JournalName'), "Ranks": 8, "labels": 'rgb(15,41,68)'}
          if node not in TotalNode:
            TotalNode.append(node)

        elif list(result[j]['f'].nodes[i].labels)[0] == 'Institude':
          node = {"id": str(result[j]['f'].nodes[i].id), "name": result[j]['f'].nodes[i].get('InstituteName'), "Ranks": 123, "labels": 'rgb(15,41,68)'}
          if node not in TotalNode:
            TotalNode.append(node)

        elif list(result[j]['f'].nodes[i].labels)[0] == 'Affillation':
          node = {"id": str(result[j]['f'].nodes[i].id), "name": result[j]['f'].nodes[i].get('AffillationName'), "Ranks": 123, "labels": 'rgb(15,41,68)'}
          if node not in TotalNode:
            TotalNode.append(node)

        elif list(result[j]['f'].nodes[i].labels)[0] == 'Conference':
          node = {"id": str(result[j]['f'].nodes[i].id), "name": result[j]['f'].nodes[i].get('conferenceName'), "Ranks": 123, "labels": 'rgb(15,41,68)'}
          if node not in TotalNode:
            TotalNode.append(node)

      for i in range (len(result[j]['f'].relationships)):
          if result[j]['f'].relationships[i].type == 'PART_OF_FIELD':
            relations.append({"source": str(result[j]['f'].relationships[i].start_node.id),"target": str(result[j]['f'].relationships[i].end_node.id),"relsName": result[j]['f'].relationships[i].type,"Linkcolor": 'rgb(173,176,181)'})

          elif result[j]['f'].relationships[i].type == 'CITED':
            relations.append({"source": str(result[j]['f'].relationships[i].start_node.id),"target": str(result[j]['f'].relationships[i].end_node.id),"relsName": result[j]['f'].relationships[i].type,"Linkcolor": 'rgb(173,176,181)'})

          elif result[j]['f'].relationships[i].type == 'AUTHOR_IN_FIELD':
            relations.append({"source": str(result[j]['f'].relationships[i].start_node.id),"target": str(result[j]['f'].relationships[i].end_node.id),"relsName": result[j]['f'].relationships[i].type,"Linkcolor": 'rgb(173,176,181)'})

          elif result[j]['f'].relationships[i].type == 'WRITTEN_BY':
            relations.append({"source": str(result[j]['f'].relationships[i].start_node.id),"target": str(result[j]['f'].relationships[i].end_node.id),"relsName": result[j]['f'].relationships[i].type,"Linkcolor": 'rgb(173,176,181)'})

          elif result[j]['f'].relationships[i].type == 'WORKED_IN':
            relations.append({"source": str(result[j]['f'].relationships[i].start_node.id),"target": str(result[j]['f'].relationships[i].end_node.id),"relsName": result[j]['f'].relationships[i].type,"Linkcolor": 'rgb(173,176,181)'})

          elif result[j]['f'].relationships[i].type == 'PART_OF_AFFILIATION':
            relations.append({"source": str(result[j]['f'].relationships[i].start_node.id),"target": str(result[j]['f'].relationships[i].end_node.id),"relsName": result[j]['f'].relationships[i].type,"Linkcolor": 'rgb(173,176,181)'})

          elif result[j]['f'].relationships[i].type == 'PUBLISHED_ON':
            relations.append({"source": str(result[j]['f'].relationships[i].start_node.id),"target": str(result[j]['f'].relationships[i].end_node.id),"relsName": result[j]['f'].relationships[i].type,"Linkcolor": 'rgb(173,176,181)'})

          elif result[j]['f'].relationships[i].type == 'PAPER_IN_FIELD':
            relations.append({"source": str(result[j]['f'].relationships[i].start_node.id),"target": str(result[j]['f'].relationships[i].end_node.id),"relsName": result[j]['f'].relationships[i].type,"Linkcolor": 'rgb(173,176,181)'})
      if result[j]['e'] != None:
        for i in range (len(result[j]['e'].nodes)):
            if list(result[j]['e'].nodes[i].labels)[0] == 'Field' or list(result[j]['e'].nodes[i].labels)[0] == 'SubGraphCS':
              node = {"id": str(result[j]['e'].nodes[i].id) , "name": result[j]['e'].nodes[i].get('fieldName') , "Ranks": 20, "labels": 'rgb(15,41,68)'}
              if node not in TotalNode:
                TotalNode.append(node)

        for i in range (len(result[j]['e'].relationships)):
            if result[j]['e'].relationships[i].type == 'PART_OF_FIELD':
              relations.append({"source": str(result[j]['e'].relationships[i].start_node.id),"target": str(result[j]['e'].relationships[i].end_node.id),"relsName": result[j]['e'].relationships[i].type,"Linkcolor": 'rgb(173,176,181)'})
            

    ################# Direct nodes labels#################
    IDList = [] 
    IDList2 = []
    LabelList = []
    for w in range (len(relations)):
      if relations[w]["target"] in TotalNode[0]["id"]:
        if relations[w]["source"] not in IDList:
          IDList.append(relations[w]["source"])

    for w in range (len(IDList)):
      for l in range (len(TotalNode)):
        if IDList[w] in TotalNode[l]["id"]:
          LabelList.append(TotalNode[l]["name"])

    

    HELL=[]
    count1 = -1
    for i in range (len(TotalNode)):
      count1 += 1 
      HELL.append({"group": count1, "name": TotalNode[i]['name'], "id": TotalNode[i]['id'], "labels":TotalNode[i]['labels'], "Ranks": TotalNode[i]["Ranks"]})

    YEAH = []
    for j in range (len(relations)):
      x=[]  
      y=[]
      for k in range (len(HELL)):
        if relations[j]['source'] == HELL[k]['id']:
          x.append(HELL[k]['group'])
        if relations[j]['target'] == HELL[k]['id']:
          y.append(HELL[k]['group'])
      YEAH.append({"source": x[0], "target": y[0], "relsName": relations[j]['relsName'], "Linkcolor": relations[j]['Linkcolor']})

    graph = { 'nodes': HELL, 'edges': YEAH}

    N=len(graph['nodes'])

    L=len(graph['edges'])
    Edges=[(graph['edges'][k]['source'], graph['edges'][k]['target']) for k in range(L)]

    G=ig.Graph(Edges, directed=True)


    label=[]
    group=[]
    ranking = []
    categories = []
    edgesColor = []
    relname = []

    for node in graph['nodes']:
        label.append(node['name'])
        group.append(node['group'])
        categories.append(node['labels'])
        ranking.append(node['Ranks'])
    for rel in graph['edges']:
    	edgesColor.append(rel['Linkcolor'])
    	edgesColor.append(rel['Linkcolor'])
    	edgesColor.append([])
    	relname.append(rel['relsName'])


    layt=G.layout('kk', dim=3)

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


    trace=go.Scatter3d(x=[Xn[0]],
                   y=[Yn[0]],
                   z=[Zn[0]],
                   mode='markers+text',
                   name=label[0],
                   marker=dict(symbol='circle',
                   				size=25,
                   				color='rgb(100,100,100)',
    	                        # colorscale= 'Blackbody',
    	                        line=dict(color='rgb(15,41,68)', width=0)),
    	               text=label[0],
    		           hoverinfo='text' 

                   	)
    trace1=go.Scatter3d(x=Xe,
                   y=Ye,
                   z=Ze,
                   mode='lines',
                   line=dict(color = edgesColor, width=1.5),
                   name = relname[0],
                   hoverinfo='none',
                   text = relname,
                   # showlegend= 'text',
                   )

    trace2=go.Scatter3d(x=Xn,
                   y=Yn,
                   z=Zn,
                   mode='markers+text',
                   name='none',
                   marker=dict(symbol='circle',
    	               				
    	                            size=ranking,
    	                            color=group,
    	                            # 'rgb(15,41,68)'
    	                            colorscale='Viridis',
    	                            line=dict(color='rgb(254,144,4)', width=0)
    	                             ),
    	           text=label,
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
             autosize = True,
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

    data=[trace1, trace2,trace]
    fig=go.Figure(data=data, layout=layout)

    plot(fig, filename = 'techscan/templates/graph/neo4jgraph.html', auto_open=False)

    # IDList = [] 
    # LabelList = []
    # for w in range (len(relations)):
    #   if relations[w]["target"] in TotalNode[0]["id"]:
    #     if relations[w]["source"] not in IDList:
    #       IDList.append(relations[w]["source"])
    # for w in range (len(IDList)):
    #   for l in range (len(TotalNode)):
    #     if IDList[w] in TotalNode[l]["id"]:
    #       LabelList.append(TotalNode[l]["name"])
  except:
    return 'False'


def get_related_table(keyword):
  neo4j = related_field(keyword)
  for d in neo4j:
    d['tweetsCount'] = main_functions.check(d['fieldName'], 'tweets')
    # d['tweetsPercentile'] = main_functions.percentile(d['fieldName'], 'tweets')
    d['weiboCount'] = main_functions.check(main_functions.chi_translation(d['fieldName']), 'weibo')
    # d['weiboPercentile'] = main_functions.percentile(d['fieldName'], 'weibo')
    d['zhihuCount'] = main_functions.check(main_functions.chi_translation(d['fieldName']), 'zhihu')
    # d['zhihuPercentile'] = main_functions.percentile(d['fieldName'], 'zhihu')
    d['scholarCount'] = main_functions.check(d['fieldName'], 'scholar')
    d['newsCount'] = main_functions.check(main_functions.chi_translation(d['fieldName']), 'news')
  return neo4j