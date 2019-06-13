## Keywords traverse graph (Related Fields)

important functions: config , neo4jgraph.plotgraph, plotly

config - set up localhost. Ensure the host is equivalent to neo4j database host. else, error return: 

```
ImportError: cannot import name 'neo4jdriver'
```

plotly - nodes and relations must re-index to have id. Start node id must be zero. the re-indexing line is on 133 - 148:



## Heatmap

Important functions: chi_translation, googlemaps

chi_translation - First function to plot heatmap is through NER on news data, which is dependent on language used. translation is subjected to type of news used.

googlemaps - requires Google API key to generate latitudes and longitudes



## Crawler 

Important notes: Login, web-driver

Login: some crawl functions like weibo requires login-id and password to run.

Uses chromedriver to run


## Wordcloud

Important functions: Wordcloud, text_query, numpy, Image , spacy and jieba 

Text file: Import Chinese stop word text file to remove Chinese stop words from text

font:  Import STFangSong.ttf for Chinese words to be displayed in wordcloud

text_query: From json format to data frame

numpy and Image: Required for masking

