## Techscan

Techscan is  a project combining multiple technologies to give comprehensive survey of technology trends.

## URLs

List of URLs available after running server. 

```python
urlpatterns = [
	path('', views.index),
	path('update', views.update),
	path('main', views.main),
	path('details', views.details),
	path('weibo', views.weibo),
	path('scholar', views.scholar),
	path('news', views.news),
	path('tweets', views.tweets),
	path('zhihu', views.zhihu),
	...
]
```

### update

The intended use of `/update` is to update data to Elasticsearch periodically and render static html files that can be hosted on Heroku. 

On loading `localhost:8000/update` , selenium will run chrome driver and begin crawling data according to the list stored at `\techscan_project\techscan\crawl_list.py`.  Data will be stored into Elasticsearch and static html templates will be saved at`\techscan_project\techscan\pages` 

### main

To start using the app, go to `localhost:8000/main` , search for keywords and information regarding it will appear. 

The current functionalities for `/main` are:

- Text translation (translating English to Chinese)
- Text summary (obtained from wiki API)
- Word Cloud 
- Related Fields (obtained from neo4j database, source from [Acemap](<https://www.acemap.info/acekg/index#data-description>))
- Time-Series Graph (obtained using plotly)
  - To show the popularity of keyword over time from all platforms
- Heatmap (obtained using NER and Google API)
  - To show areas that are mentioned in news and the frequency of it

Clicking on any link on the side navigation bar will direct to their respective URLs 

### details

This page provides a more detailed view of the keyword, displaying post from all platforms we crawled from. 

In addition, it provides a list of top companies mentioned, the most influential authors from twitter, weibo and zhihu.  

### weibo, scholar, news, tweets, zhihu

These pages provides more information on each platform respectively.


## Additional Information

Currently there are two ways to use this application. The first way will be running it locally to have the full functionalities. Secondly will be browsing static HTML files via Heroku of **fixed keywords** that are determined on `crawl_list.py` on mobile device. However, these static files do not have any graph or tables in it. Moving on, it should be possible to add them in.