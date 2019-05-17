from django_elasticsearch_dsl import DocType, Index, fields
from techscan.models import Twitter, Weibo, Zhihu, News, Scholar
from elasticsearch_dsl import analyzer
from django.conf import settings


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

tweets = Index('tweets')
@tweets.doc_type
class TwitterDocument (DocType):
    class Meta:
        model = Twitter
        fields = [
            'categories',
            'favorite_count',
            'hashtags',
            'hashtags_count',
            'links',
            'mentions',
            'published',
            'retweet_count',
            'summary',
            'url',
            'user_id',
            'user_name',
            'user_screen_name',
            'sentiment',
            'tweet_id',
        ]

weibo = Index('weibo')
@weibo.doc_type
class WeiboDocument (DocType):
    class Meta:
        model = Weibo
        fields = [
            'categories',
            'favorite_count',
            'hashtags',
            'hashtags_count',
            'links',
            'published',
            'summary',
            'url',
            'user_id',
            'user_name',
            'weibo_id',
        ]

zhihu = Index('zhihu')
@zhihu.doc_type
class ZhihuDocument (DocType):
    id = fields.IntegerField(attr='id')
    author = fields.StringField(
        fielddata = True,
        analyzer = 'standard',
        fields = {
            'raw': fields.StringField(analyzer = 'standard')
        }
    )

    authorUrl = fields.StringField()
    headline = fields.StringField(
        fielddata = True,
        analyzer = 'standard',
        # analyzer = html_strip,
        fields = {
            'raw': fields.StringField(analyzer = 'standard')
        }
    )
    headlineUrl = fields.StringField()
    published = fields.StringField()
    summary = fields.StringField(
        fielddata = True,
        analyzer = 'standard',
        # analyzer = html_strip,
        fields = {
            'raw': fields.StringField(analyzer = 'standard')
        }
    )
    upvotes = fields.IntegerField()
    class Meta:
        model = Zhihu

        # fields = [
        #     'author',
        #     'authorUrl',
        #     'headline',
        #     'headlineUrl',
        #     'published',
        #     'summary',
        #     'upvotes',
        # ]

news = Index('news')
@news.doc_type
class NewsDocument (DocType):
    class Meta:
        model = News
        fields = [
            'url',
            'title',
            'summary',
            'published',
            'authors',
        ]

scholar = Index('scholar')
@scholar.doc_type
class ScholarDocument (DocType):
    class Meta:
        model = Scholar
        fields = [
            'authors',
            'categories',
            'scholar_id',
            'published',
            'summary',
            'title',
            'updated',
            'url',
        ]