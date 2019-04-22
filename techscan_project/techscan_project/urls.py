from django.contrib import admin
from django.urls import path
from techscan import views
from django.views.generic import TemplateView

urlpatterns = [
	path('',views.index),
	path('main', views.main),
	path('overview', views.overview),
	path('weibo', views.weibo),
	path('scholar', views.scholar),
	path('news', views.news),
	path('tweets', views.tweets),
	path('zhihu', views.zhihu),
	path('facial_recognition', views.facial_recognition),
	path('speech_text', views.speech_text),
	path('admin/', admin.site.urls),
	path('plotneo4jgraph/', TemplateView.as_view(template_name="graph/neo4jgraph.html"), name= 'plotneo4jgraph'),
	path('plotlinetweets/', TemplateView.as_view(template_name="graph/basic_line_graph_tweets.html"),name='plotlinetweets'),
	path('heatmap/', TemplateView.as_view(template_name="graph/heatmap.html"), name= 'heatmap'),
	path('plotgraphall/',TemplateView.as_view(template_name="graph/main_graph_all.html"), name= 'plotgraphall'),
	path('zhihu_graph/', TemplateView.as_view(template_name="graph/zhihu_author_bar.html"), name='zhihu_graph'),
	path('weibo_hashtag_graph/', TemplateView.as_view(template_name="graph/weibo_hashtag_count.html"), name='weibo_hashtag_graph'),
	path('twitter_hashtag_bubble/', TemplateView.as_view(template_name="graph/twitter_hashtag_bubble.html"), name='twitter_hashtag_bubble'),
	]
