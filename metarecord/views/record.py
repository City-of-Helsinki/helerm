from rest_framework import serializers, viewsets

from metarecord.models import Record, RecordType

from .base import DetailSerializerMixin, HexPrimaryKeyRelatedField, HexRelatedField, StructuralElementSerializer


class RecordTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordType


class RecordTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecordType.objects.all()
    serializer_class = RecordTypeSerializer


class RecordListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Record

    action = HexRelatedField(read_only=True)
    type = HexPrimaryKeyRelatedField(read_only=True)


class RecordDetailSerializer(RecordListSerializer):
    pass


class RecordViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Record.objects.select_related('action', 'type')
    serializer_class = RecordListSerializer
    serializer_class_detail = RecordDetailSerializer
    lookup_field = 'uuid'
