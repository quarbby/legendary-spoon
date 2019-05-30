import time
from selenium import webdriver
import bs4 as bs
from pprint import pprint
import json
from elasticsearch import Elasticsearch
from datetime import datetime

def unique_keys(items):
    seen = set()
    for item in items:
        key = item['summary']
        if key not in seen:
             seen.add(key)
             yield item
        else:
             pass

def twitter_crawl(keywords):
    es = Elasticsearch([{'host' : 'localhost', 'port' : 9200}])
    for keyword in keywords:
        browser = webdriver.Chrome(executable_path="techscan/es_folder/chromedriver")
        browser.get("https://twitter.com/hashtag/"+ keyword +"?src=hash")

        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False

        timeout = time.time() + 10  # + number of seconds
        while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage or time.time() > timeout:
                match=True

        source_data = browser.page_source

        soup = bs.BeautifulSoup(source_data, 'html.parser')
        all_tweets = []
        timeline = soup.select('#timeline li.stream-item')
        for tweet in timeline:
            date = tweet('a')[1]['title']
            new_date = date.split('-')[1][1:] + " " + date.split('-')[0][:-1]
            date = datetime.strptime(new_date,'%d %b %Y %I:%M %p')
            all_tweets.append({
                "id": tweet['data-item-id'],
                "user_name": tweet.select('strong')[0].text,
                "user_screen_name": tweet.select('b')[0].text,
                "url": 'https://twitter.com/' + tweet.select('b')[0].text,
                "summary": tweet.select('p.tweet-text')[0].get_text(),
                "published": date,
                "tweet_url": 'https://twitter.com/' + tweet.select('b')[0].text + '/status/' + tweet['data-item-id'],
                "reply_count": int(tweet.select('span.ProfileTweet-actionCount')[0]['data-tweet-stat-count']),
                "retweet_count": int(tweet.select('span.ProfileTweet-actionCount')[1]['data-tweet-stat-count']),
                "favorite_count": int(tweet.select('span.ProfileTweet-actionCount')[2]['data-tweet-stat-count'])
            })

        res = es.search (index = 'tweets', size = 10000, scroll = '2m', body = {'query':{"match_all":{}}})['hits']['hits']
        es_data = []
        for data in res:
            es_data.append(data['_source'])
        total = es_data + all_tweets
        # print(total)
        updated_data = unique_keys(total)

        for i in range(len(updated_data)):
            es.index(index = str('tweets'), doc_type = str('tweets') + '_papers',
                body = updated_data[i])


