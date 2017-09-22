from rest_framework import serializers, viewsets

from metarecord.models import Classification

from .base import HexRelatedField


class ClassificationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', format='hex', read_only=True)
    parent = HexRelatedField(read_only=True)

    class Meta:
        model = Classification
        fields = ('id', 'created_at', 'modified_at', 'code', 'title', 'parent', 'description', 'description_internal',
                  'related_classification', 'additional_information')


class ClassificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Classification.objects.order_by('code')
    serializer_class = ClassificationSerializer
    lookup_field = 'uuid'
