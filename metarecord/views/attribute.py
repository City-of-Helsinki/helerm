import django_filters
from rest_framework import serializers, viewsets

from metarecord.models import Attribute, AttributeValue


class AttributeValueSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, format='hex')

    class Meta:
        model = AttributeValue
        exclude = ('attribute',)


class AttributeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, format='hex')
    values = AttributeValueSerializer(read_only=True, many=True)

    class Meta:
        model = Attribute


class AttributeFilterSet(django_filters.rest_framework.FilterSet):
    identifier = django_filters.Filter(lookup_type='in', widget=django_filters.widgets.CSVWidget())

    class Meta:
        model = Attribute
        fields = ('identifier',)


class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attribute.objects.prefetch_related('values')
    serializer_class = AttributeSerializer
    filter_class = AttributeFilterSet
