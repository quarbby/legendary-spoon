from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)
from django.shortcuts import render
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    DefaultOrderingFilterBackend,
)

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from .documents import ZhihuDocument
from .serializers import ZhihuSerializer



# Create your views here.
class ZhihuDocumentView(DocumentViewSet):

    document = ZhihuDocument
    serializer_class = ZhihuSerializer

    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    search_fields = (
        'summary.raw',
        'author.raw',
    )
    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'summary': 'summary.raw',
    }

    ordering_fields = {
        # 'id': 'id',
        'author': 'author.raw',
        'summary': 'summary.raw',
        'published': 'published'
    }

    ordering = ('id', 'author',) 
