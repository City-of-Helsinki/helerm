from django_elasticsearch_dsl_drf.pagination import (
    PageNumberPagination as ESPageNumberPagination,
)
from rest_framework.pagination import PageNumberPagination


class MetaRecordPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 10000


class ESRecordPagination(ESPageNumberPagination, MetaRecordPagination):
    pass
