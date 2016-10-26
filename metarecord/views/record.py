from rest_framework import serializers, viewsets

from metarecord.models import Record, RecordType

from .base import DetailSerializerMixin, HexPrimaryKeyRelatedField, StructuralElementSerializer


class RecordTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordType


class RecordTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecordType.objects.all()
    serializer_class = RecordTypeSerializer


class RecordListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Record

    action = HexPrimaryKeyRelatedField(read_only=True, source='action_id')
    type = HexPrimaryKeyRelatedField(read_only=True, source='type_id')


class RecordDetailSerializer(RecordListSerializer):
    pass


class RecordViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Record.objects.select_related('action', 'type')
    serializer_class = RecordListSerializer
    serializer_class_detail = RecordDetailSerializer
