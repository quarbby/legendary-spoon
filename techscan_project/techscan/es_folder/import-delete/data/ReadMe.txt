Connect to ElasticSearch the usual way. Open config.py in ElasticSearchFolder, change the location to the place the data is stored at, comment out the try except block used to connect to neo4j. Save the config.py file. Open uplaoding_data.py, uncomment the last line and change the second parameter to the index name of the data you are uplaoding. E.g 'tweets' if you are uploading tweets or 'weibo' if you are uplaoding 'weibo'. The index name must be exactly spelt correctly for it to run. 

Index Name
'tweets'
'weibo'
'zhihu'
'news'
'scholar'

 

Index keys

zhihu: author, authorUrl, headline, headlineUrl, published, summary, upvotes
news: authors, label, published, source, stance, summary, title, updated, url
tweets: categories, favorite_count, hashtags, hashtags_count, id, links, mentions, pulished, retweet_count, sentiment, summary, url, user_id, user_name, user_screen_name
scholar: authors, categories, id, published, summary, title, updated, url 
weibo: categories, favorite_count, hashtags, hashtags_count, id, links, published, summary, url, user_id, user_name

https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=javascript