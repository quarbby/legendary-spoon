from rest_framework import serializers
from techscan.models import Zhihu
from techscan import documents as doc
import json
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

#Zhihu Serializer
class ZhihuSerializer(DocumentSerializer):
    class Meta(object):
        # model = Zhihu
        document = doc.ZhihuDocument
        fields = ['author',
        'headline',
        'upvotes',
        'summary',
        'published',
        'id',
        ]