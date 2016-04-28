from rest_framework import serializers

from metarecord.models import AttributeValue


class AttributeValueFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue

    def to_representation(self, instance):
        return {instance.attribute.identifier: instance.value}


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
