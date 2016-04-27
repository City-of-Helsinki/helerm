from rest_framework import serializers, viewsets

from metarecord.models import Attribute


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute

    values = serializers.SerializerMethodField()

    def get_values(self, obj):
        if obj.is_free_text:
            return None
        return obj.values.all().values_list('value', flat=True)


class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
