import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot
import pandas as pd
import json
from pprint import pprint

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host' : 'localhost', 'port' : 9200}])
res = es.search(index = 'latitude', size = 10000, scroll = '2m' , body= {"query": {"match_all": {}}})

# pprint(len(res['hits']['hits']))
resItems = res['hits']['hits']
# for i in range (len(resItems)):
#     pprint(resItems[i]['_source']['types'])

# location = 'LatitudeLast.json' 
# with open(location, 'r+') as f:
#   data = json.load(f)

address = []
weight = []
companies = []
Latitude = []
longtitude = []
colouring = []
institude = []

countx1 = 0
countx2 = 0
countx3 = 0
countx4 = 0

for i in range (len(resItems)):
    companies.append(resItems[i]['_source']['companies'])
    Latitude.append(resItems[i]['_source']['Address'][0]['geometry']['location']['lat'])
    longtitude.append(resItems[i]['_source']['Address'][0]['geometry']['location']['lng'])
    address.append(resItems[i]['_source']['Address'][0]['formatted_address'])
    if 0 < int(resItems[i]['_source']['weighting']) <= 5:
        # colouring.append("#00284d")
        weight.append(100)

    elif 5 < int(resItems[i]['_source']['weighting']) <= 20:
        # colouring.append("#004f99")
        weight.append(200)

    elif 20 < int(resItems[i]['_source']['weighting']) <= 50:
        # colouring.append("#0077e6")
        weight.append(500)

    elif 50 < int(resItems[i]['_source']['weighting']) <= 100:
        # colouring.append("#339cff")
        weight.append(1000)

    elif 100 < int(resItems[i]['_source']['weighting']  ):
        # colouring.append("#ff3333")
        weight.append(3000)

    if resItems[i]['_source']['types'] == 'Institutions':
        colouring.append("#00cc66")
        institude.append(resItems[i]['_source']['types'])
        countx1 += 1

    elif resItems[i]['_source']['types'] == 'Private_Companies':    
        colouring.append("#000080")
        institude.append(resItems[i]['_source']['types'])
        countx2 += 1

    elif resItems[i]['_source']['types'] == 'Government_Sectors':
        colouring.append("#ff3333")
        institude.append(resItems[i]['_source']['types'])
        countx3 += 1

    elif resItems[i]['_source']['types'] == 'news':
        colouring.append("#cc6600")
        institude.append(resItems[i]['_source']['types'])
        countx4 += 1
print(countx1)
print(countx2)
print(countx3)
print(countx4)

ds = pd.DataFrame({'companies': companies, 'Lat': Latitude, 'Lng': longtitude , 'address': address, 'weight': weight, 'colors': colouring, 'institude': institude})
df = ds.sort_values(['colors'])

# legendset = []
# color = list(dict.fromkeys(colouring))
# print(color)
# print(len(df))

colors = ['Private_Companies','Institutions','news publisher','Government_Sectors']
# colouring = pd.DataFrame({'colors':colors})
# colors = [{'institude':'Private_Companies'},{'institude':'Institutions'},{'institude':'news publisher'},{'institude':'Government_Sectors'}]
###########################################################################################################################################formatted_address,geometry
# df['text'] = df['name'] + '<br>Population ' + (df['pop']/1e6).astype(str)+' million'
# limits = [(0,5),(5,20),(20,50),(50,100),(100,3000)]
limits = [(0,countx2),(countx2,countx2+countx1),(countx2+countx1,countx2+countx1+countx4),(countx2+countx1+countx4,countx2+countx1+countx4+countx3)]
# limits = ["#00cc66","#000080","#ff3333","#cc6600"]
# colors = ["rgb(133,20,75)","rgb(0,116,217)","rgb(255,65,54)","rgb(255,133,27)","lightgrey"]
cities = []
scale = 5000

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[lim[0]:lim[1]]
    df_colors = colors[i]
    pprint(df_sub)
    city = go.Scattergeo(
        locationmode = 'ISO-3',
        # locations = ['asia'],
        lon = df_sub['Lng'],
        lat = df_sub['Lat'],
        text = df_sub['companies']+df_sub['address'],
        marker = go.scattergeo.Marker(
            size = df_sub['weight'],
            color = df_sub['colors'],
            line = go.scattergeo.marker.Line(
                width=0, color='rgb(40,40,40)'
            ),
            sizemode = 'area'
        ),
        # name = '{0} - {1}'.format(lim[0],lim[1]) 
        name = '{}'.format(df_colors) 
        )
    cities.append(city)

layout = go.Layout(
        title = go.layout.Title(
            text = 'China News Reports on AI'
        ),
        showlegend = True,
        font = go.layout.Font(size = 25),
        autosize = True,
        geo = go.layout.Geo(
            scope = 'world',
            projection = go.layout.geo.Projection(
                type='equirectangular'  
            ),
            #center = go.layout.geo.Center( lat = 50, lon = 50),
            ##Map Features##
            showcoastlines = True,
            showland = True,
            showocean = True,
            showcountries = True,
            showsubunits = False,
            # size and width
            subunitwidth=1,
            countrywidth=1,
            # colorings ^^
            landcolor = '#e1eaea',
            oceancolor = "#ffffff",
            subunitcolor="#9ae59a", 
            countrycolor="#b3b3b3",
            coastlinecolor  = "#b3b3b3", 
            
        )
    )

fig = go.Figure(data=cities, layout=layout)
plot(fig, filename='d3-bubble-map-populations.html')