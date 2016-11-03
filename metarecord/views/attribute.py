import django_filters
from rest_framework import serializers, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from metarecord.models import Attribute, AttributeValue, StructuralElement


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

    @list_route()
    def schemas(self, request):
        response = {}
        for cls in StructuralElement.__subclasses__():
            response[cls.__name__.lower()] = cls.get_attribute_json_schema()
        return Response(response)
