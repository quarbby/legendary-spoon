import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot
import pandas as pd
import json
from . import main_functions
from pprint import pprint
from ..config import es
# import uploading_data 
# import train_heatmap_index


def heatmap(keyword):
    search_term = main_functions.chi_translation(keyword)
    res = es.search(index = 'heatmap' , size = int(10000), scroll = '2m', body = {"query" : {
        "match" : {"labels" : search_term}
        }})
    res_input = res['hits']['hits']
    # pprint(res_input[0]['_source']['labels'])

    resItems = []
    for i in range (len(res_input)):
        if res_input[i]['_source']['labels'] == search_term :
            resItems.append(res_input[i])

    # pprint(resItems[0])
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

    if resItems == []:
        return [] 
        # Items = find_NER(search_term)
        # upload_data_ner(Items, 'latitude_test')
        # for i in range (len(Items)):
        #     companies.append(Items[i]['publisher'])
        #     Latitude.append(Items[i]['Address'][0]['geometry']['location']['lat'])
        #     longtitude.append(Items[i]['Address'][0]['geometry']['location']['lng'])
        #     address.append(Items[i]['Address'][0]['formatted_address'])
        #     if 0 < int(Items[i]['weighting']) <= 5:
        #         # colouring.append("#00284d")
        #         weight.append(100)

        #     elif 5 < int(Items[i]['weighting']) <= 20:
        #         # colouring.append("#004f99")
        #         weight.append(200)

        #     elif 20 < int(Items[i]['weighting']) <= 50:
        #         # colouring.append("#0077e6")
        #         weight.append(500)

        #     elif 50 < int(Items[i]['weighting']) <= 100:
        #         # colouring.append("#339cff")
        #         weight.append(1000)

        #     elif 100 < int(Items[i]['weighting'] ):
        #         # colouring.append("#ff3333")
        #         weight.append(3000)

        #     if Items[i]['types'] == 'Institutions':
        #         colouring.append("#00cc66")
        #         institude.append(Items[i]['types'])
        #         countx1 += 1

        #     elif Items[i]['types'] == 'Private_Companies':    
        #         colouring.append("#000080")
        #         institude.append(Items[i]['types'])
        #         countx2 += 1

        #     elif Items[i]['types'] == 'Government_Sectors':
        #         colouring.append("#ff3333")
        #         institude.append(Items[i]['types'])
        #         countx3 += 1

        #     elif Items[i]['types'] == 'news':
        #         colouring.append("#cc6600")
        #         institude.append(Items[i]['types'])
        #         countx4 += 1
    else :
        for i in range (len(resItems)):
            companies.append(resItems[i]['_source']['publisher'])
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
    ds = pd.DataFrame({'companies': companies, 'Lat': Latitude, 'Lng': longtitude , 'address': address, 'weight': weight, 'colors': colouring, 'institude': institude})
    df = ds.sort_values(['colors'])


    colors = ['Private Companies','Institutions','News Publishers','Government Sectors']
    limits = [(0,countx2),(countx2,countx2+countx1),(countx2+countx1,countx2+countx1+countx4),(countx2+countx1+countx4,countx2+countx1+countx4+countx3)]

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
            text = colors[i]+": "+df_sub['companies']+"  |  Location: "+df_sub['address'],
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
                text = 'China News Reports on {}'.format(keyword.lower())
            ),
            showlegend = True,
            font = go.layout.Font(size = 20),
            autosize = True,
            # Tickformatstops = go.layout.tickformatstops(dtickrange = [50,100]),
            xaxis = dict (fixedrange = True),
            yaxis = dict (fixedrange = True),
                # fixedrange = True),
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
    plot(fig, filename='techscan/templates/graph/heatmap.html', auto_open=False)