from selenium import webdriver
import bs4 as bs
from datetime import datetime
import time
import urllib.parse
import ssl


def get_page_source(url):
    browser = webdriver.Chrome(executable_path="chromedriver")
    browser.get(url)
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    timeout = time.time() + 5  # + number of seconds to scroll
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage or time.time() > timeout:
            match=True

    return browser.page_source

def disable_ssl():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def crawl_twitter(url):
    page_source = get_page_source(url)
    soup = bs.BeautifulSoup(page_source, 'html.parser')
    all_tweets = []
    timeline = soup.select('#timeline li.stream-item')
    for tweet in timeline:
        date = tweet('a')[1]['title']
        new_date = date.split('-')[1][1:] + " " + date.split('-')[0][:-1]
        date = datetime.strptime(new_date,'%d %b %Y %I:%M %p')
        all_tweets.append({
            "tweet_id": tweet['data-item-id'],
            "author": tweet.select('b')[0].text,
            "author_url": 'https://twitter.com/' + tweet.select('b')[0].text,
            "summary": tweet.select('p.tweet-text')[0].get_text(),
            "date": date,
            "summary_url": 'https://twitter.com/' + tweet.select('b')[0].text + '/status/' + tweet['data-item-id'],
            "reply_count": int(tweet.select('span.ProfileTweet-actionCount')[0]['data-tweet-stat-count']),
            "retweet_count": int(tweet.select('span.ProfileTweet-actionCount')[1]['data-tweet-stat-count']),
            "favorite_count": int(tweet.select('span.ProfileTweet-actionCount')[2]['data-tweet-stat-count'])
        })
    return all_tweets

def crawl_zhihu(url):
    page_source = get_page_source(url)
    soup = bs.BeautifulSoup(page_source,'lxml')
    cards = (soup.find_all('div',{'ContentItem ArticleItem'}))
    all_zhihu = []
    for i in range(len(cards)):
        post = dict()
        data = (cards[i].find_all('meta'))
        post['author'] = str(data[0]['content']) if data[0] else "Data not availiable"
        post['author_url'] = str(data[2]['content']) if data[2] else "Data not availiable"
        post['title'] = str(data[4]['content']) if data[4] else "Data not availiable"
        post['summary_url'] = str(data[5]['content']) if data[5] else "Data not availiable"
        post['date'] = datetime.strptime((data[6]['content']), "%Y-%m-%dT%H:%M:%S.%fZ") if data[6] else "Data not availiable"
        post['summary'] = str(cards[i].find_all('span',{'itemprop': 'articleBody'})[0].contents[0])
        post['upvote_count'] = int(cards[i]['data-za-extra-module'].split(',')[4].split(':')[1])
        all_zhihu.append(post)
    return all_zhihu

def crawl_news(url):
    page_source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(page_source,'lxml')
    cards = (soup.find('div', {'class': 'result'})).find_all('div', {'class': 'result_con'})
    all_news = []
    for i in range(len(cards)):
        data = cards[i]
        post = dict()
        post['summary_url'] = data.find_all('a')[0]['href']
        post['title'] = data.find_all('a')[0].text.strip()
        post['summary'] = data.find_all('p')[0].text.strip()
        post['author'] = data.find_all('div')[0].text.split()[0]
        post['date'] = datetime.strptime(data.find_all('div')[0].text.split()[1] + " "+ data.find_all('div')[0].text.split()[2],'%Y-%m-%d %H:%M:%S')
        all_news.append(post)
    return all_news

def crawl_scholar(url):
    page_source = urllib.request.urlopen(url, context = disable_ssl()).read()
    soup = bs.BeautifulSoup(page_source,'lxml')
    cards_content = soup.find('dl').find_all('dd')
    cards_url = soup.find('dl').find_all('dt')
    all_scholar = []
    for i,j in zip(cards_content, cards_url):
        post = dict()
        post['title'] = cards_content[0].find_all('div')[1].text[8:]
        post['summary'] = i.select('p')[0].text
        post['author'] = [authors.text for authors in i.find_all('a')]
        post['date'] = datetime.strptime(soup.find('h3').text.split(',')[1][2:], '%d %b %y')
        post['subject'] = i.select('span')[3].text[:-8]
        post['summary_url'] = "https://arxiv.org" + j.find_all('a')[2]['href']
        all_scholar.append(post)
    return all_scholar

def crawl_weibo(url):
    page_source = urllib.request.urlopen(url, context = disable_ssl()).read()
    soup = bs.BeautifulSoup(page_source,'lxml')
    cards = soup.find_all('div','card')
    all_weibo = []
    for i in cards:
        try:
            post = dict()
            post['author'] = i.find_all('a')[3]['nick-name']
            post['author_url'] = i.find_all('a')[3]['href']
            post['date'] = i.find('div','card-act').find_all('li')[1].find('a').text
            post['summary'] = i.find('div','card-feed').find('p').text.strip()
            post['summary_url'] = i.find('p','from').find('a')['href']
            if any(char.isdigit() for char in i.find('div','card-act').find_all('li')[2].find('a').text) == True:
                post['reply_count'] = int(''.join(list(filter(str.isdigit, i.find('div','card-act').find_all('li')[2].find('a').text))))
            else:
                post['reply_count'] = 0
            if any(char.isdigit() for char in i.find('div','card-act').find_all('li')[1].find('a').text) == True:
                post['retweet_count'] = int(''.join(list(filter(str.isdigit, i.find('div','card-act').find_all('li')[1].find('a').text))))
            else:
                post['retweet_count'] = 0
            if i.find('div','card-act').find_all('li')[3].find('a').text != " ":
                post['favorite_count'] = i.find('div','card-act').find_all('li')[3].find('a').text
            else:
                post['favorite_count'] = 0
            all_weibo.append(post)
        except:
            pass
    return all_weibo