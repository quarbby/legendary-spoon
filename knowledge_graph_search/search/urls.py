from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.index),
    path('search/',views.search_word),
    path('plotpy/', TemplateView.as_view(template_name="basic_pie_chart.html"),name='plotpy'),
    path('plotlinetweets/', TemplateView.as_view(template_name="basic_line_graph_tweets.html"),name='plotlinetweets'),
    path('plotlinenews/', TemplateView.as_view(template_name="basic_line_graph_news.html"),name='plotlinenews'),
    path('plotlinescholar/', TemplateView.as_view(template_name="basic_line_graph_scholar.html"),name='plotlinescholar'),
    path('plotneo4jgraph/', TemplateView.as_view(template_name="neo4jgraph.html"), name= 'plotneo4jgraph'),
    path('plotlineweibo/', TemplateView.as_view(template_name="basic_line_graph_weibo.html"),name='plotlineweibo'),

]

 