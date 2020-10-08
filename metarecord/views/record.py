from rest_framework import serializers, viewsets
from rest_framework.mixins import RetrieveModelMixin

from metarecord.models import Record
from metarecord.views.base import StructuralElementSerializer


class RecordSerializer(StructuralElementSerializer):
    modified_by = serializers.SerializerMethodField()

    class Meta(StructuralElementSerializer.Meta):
        model = Record

    def get_modified_by(self, obj):
        return obj._modified_by or None


class RecordViewSet(RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = RecordSerializer
    queryset = Record.objects.all()
    lookup_field = 'uuid'
