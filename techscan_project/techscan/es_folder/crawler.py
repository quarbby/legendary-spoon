from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import bs4 as bs
from datetime import datetime
import dateparser
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

def sentiment(sentence):
    analyzer = SentimentIntensityAnalyzer()
    VS = analyzer.polarity_scores(sentence)

    if VS['compound'] >= 0.05:
        return('Positive')
    elif VS['compound'] > -0.05 and VS['compound'] < 0.05:
        return('Neutral')
    else:
        return('Negative')

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
            "favorite_count": int(tweet.select('span.ProfileTweet-actionCount')[2]['data-tweet-stat-count']),
            "sentiment": sentiment(tweet.select('p.tweet-text')[0].get_text())
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
        try:
            post['upvote_count'] = int(cards[i]['data-za-extra-module'].split(',')[4].split(':')[1])
        except:
            post['upvote_count'] = 0
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

def convert_to_posts(cards):
    
    posts = list()
    post = list()
    for i, card in enumerate (cards):
        entry = card.find('div', {'node-type':'like'});
        post = dict()
        text_html = entry.find('p', {'node-type':'feed_list_content'})
        if entry.find('p', {'node-type':'feed_list_content_full'}):
            text_html = entry.find('p', {'node-type':'feed_list_content_full'})
        for br in text_html.find_all('br'):
            br.replace_with('\n')
        text = text_html.get_text().strip()
        text = text.replace('收起全文d', '').strip()
        text = text.replace('O网页链接', '').strip()
        text = re.sub(r'L.*的.*视频', '', text).strip()

        links = [a['href'] for a in text_html.find_all('a') 
                 if re.search(r'(http:\/\/t\.cn/[a-zA-Z0-9]*)', a['href'])]

        hashtags = re.findall(r'\#([^#]*)\#', text)

        name_html  = entry.find('a', {'class':'name'})
        name = name_html.get_text().strip()

        date_html = entry.find('p', {'class':'from'}).find('a')
        date = date_html.get_text().split()[0].strip()
        try:
            if '今天' in str(date):
                date = str(datetime.now())
                date = dateparser.parse(date)
                date = date.isoformat()
            elif '年' not in str(date):
                year = date.today().year
    #             date = str(year) + '年' + date
                date = dateparser.parse(date)
                date = date.replace(year=int(year)).isoformat()
            else:
                date = dateparser.parse(date)
                date = date.isoformat()
        except:
            date = datetime.now()

        url_search = re.search(r'\/\/weibo.com\/([0-9]*\/[a-zA-z0-9]*)', date_html['href'])
        if url_search:
            post_id = url_search.group(1)
            url = 'https://www.weibo.com/{}'.format(post_id)


        name_search = re.search(r'\/\/weibo.com\/([0-9]*)\?', name_html['href'])
        if name_search:
            uid = name_search.group(1)

        like_html = card.find('a', {'title':'赞'})
        like_count = like_html.get_text().strip()
        like_count = int(like_count) if like_count else 0
        
        post['summary'] = text
        post['id'] = post_id
        post['user_id'] = uid
        post['author'] = name
        post['date'] = date
        post['links'] = links
        post['hashtags'] = hashtags
        post['hashtag_count'] = len(hashtags)
        post['favorite_count'] = like_count
        post['summary_url'] = url

       

        posts.append(post)
    
    return posts

def weibo_login():
    # Open chrome and login to Weibo for access to search term data
    caps = DC().CHROME
    caps['pageLoadStrategy'] = "none"
    browser = webdriver.Chrome( executable_path="chromedriver")
    browser.get('https://s.weibo.com/weibo?q=谷歌华为&nodup=1&page=1')
    browser.implicitly_wait(10)
    WebDriverWait(browser, timeout = 120, poll_frequency = 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '登录')]")))

    try:
        credentials= browser.find_elements_by_css_selector(".form_login_register .W_input, .Bv6_layer .form_login_register .W_input")
        username = credentials[0]
        password = credentials[1]
        username.send_keys('weichao1995@gmail.com')
        password.send_keys('31O55h95')
        login_button = browser.find_element_by_css_selector(".Bv6_layer .W_btn_a")
        login_button.click()

    except:
        login_page = browser.find_element_by_xpath("//*[contains(text(), '登录')]")
        login_page.click()
        
        time.sleep(10)
        
        credentials= browser.find_elements_by_css_selector(".form_login_register .W_input, .Bv6_layer .form_login_register .W_input")
        username = credentials[0]
        password = credentials[1]
        username.send_keys('weichao1995@gmail.com')
        password.send_keys('31O55h95')
        login_button = browser.find_element_by_css_selector(".Bv6_layer .W_btn_a")
        login_button.click()

def crawl_weibo(url):
    caps = DC().CHROME
    caps['pageLoadStrategy'] = "none"
    browser = webdriver.Chrome(desired_capabilities = caps, executable_path="chromedriver")
    browser.get(url)
    time.sleep(10)
    source = browser.page_source 
    soup = bs.BeautifulSoup(source, 'lxml')
    cards = list()
    cards_temp = soup.find_all('div', {'class':'card-wrap'})
    
    for card in cards_temp:
        if card.find('div', {'node-type':'like'}):
            cards.append(card)
    all_weibo = convert_to_posts(cards)

    return all_weibo






