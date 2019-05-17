from django.db import models

# Create your models here.

class Twitter(models.Model):
    categories = models.CharField(max_length = 99999)
    favorite_count = models.IntegerField()
    hashtags = models.CharField(max_length = 99999)
    hashtags_count = models.IntegerField()
    links = models.CharField(max_length = 9999)
    mentions = models.CharField(max_length = 99999)
    published = models.CharField(max_length = 99999)
    retweet_count = models.IntegerField()
    summary = models.CharField(max_length = 9999999)
    url = models.CharField(max_length = 9999)
    user_id = models.CharField(max_length = 99999)
    user_name = models.CharField(max_length = 99999)
    user_screen_name = models.CharField(max_length = 99999)
    sentiment = models.CharField(max_length = 99999)
    tweet_id = models.CharField(max_length = 99999)

class Weibo(models.Model):
    categories = models.CharField(max_length = 99999)
    favorite_count = models.IntegerField()
    hashtags = models.CharField(max_length = 99999)
    hashtags_count = models.IntegerField()
    links = models.CharField(max_length = 99999)
    published = models.CharField(max_length = 99999)
    summary = models.CharField(max_length = 9999999)
    url = models.CharField(max_length = 99999)
    user_id = models.CharField(max_length = 99999)
    user_name = models.CharField(max_length = 99999)
    weibo_id = models.CharField(max_length = 99999)

class Zhihu(models.Model):
    author = models.CharField(max_length = 99999)
    authorUrl = models.CharField(max_length = 99999)
    headline = models.CharField(max_length = 99999)
    headlineUrl = models.CharField(max_length = 99999)
    published = models.CharField(max_length = 99999)
    summary = models.CharField(max_length = 9999999)
    upvotes = models.IntegerField()

class News(models.Model):
    url = models.CharField(max_length = 99999)
    title = models.CharField(max_length = 99999)
    summary = models.CharField(max_length = 9999999)
    published = models.CharField(max_length = 99999)
    authors = models.CharField(max_length = 99999)

class Scholar(models.Model):
    authors = models.CharField(max_length = 99999)
    categories = models.CharField(max_length = 99999)
    scholar_id = models.CharField(max_length = 99999)
    published = models.CharField(max_length = 99999)
    summary = models.CharField(max_length = 9999999)
    title = models.CharField(max_length = 99999)
    updated = models.CharField(max_length = 99999)
    url = models.CharField(max_length = 99999)
