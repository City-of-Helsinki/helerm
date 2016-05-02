from rest_framework import filters, serializers

from metarecord.models import Attribute, AttributeValue


class AttributeValueFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue

    def to_representation(self, instance):
        return {instance.attribute.identifier: instance.value}


class AttributeFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        valid_attributes = {}

        for param, value in request.query_params.items():
            if not param.startswith('attributes__'):
                continue
            param = param[12:]
            try:
                attribute = Attribute.objects.get(identifier=param)
                valid_attributes[attribute] = value
            except Attribute.DoesNotExist:
                pass

        if not valid_attributes:
            return queryset

        for attribute, value in valid_attributes.items():
            attribute_values = AttributeValue.objects.filter(attribute=attribute, value=value)
            queryset = queryset.filter(attribute_values__in=attribute_values)

        return queryset


class StructuralElementSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('attribute_values', 'order')

    attributes = AttributeValueFieldSerializer(source='attribute_values', many=True)


class DetailSerializerMixin:
    def get_serializer_class(self):
        if self.action == 'retrieve':
            try:
                return self.serializer_class_detail
            except AttributeError:
                pass

        return super().get_serializer_class()
