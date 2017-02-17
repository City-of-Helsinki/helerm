from rest_framework import viewsets

from metarecord.models import Record

from .base import DetailSerializerMixin, HexRelatedField, StructuralElementSerializer


class RecordListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Record

    action = HexRelatedField(read_only=True)
    parent = HexRelatedField(read_only=True)


class RecordDetailSerializer(RecordListSerializer):
    pass


class RecordViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Record.objects.select_related('action')
    serializer_class = RecordListSerializer
    serializer_class_detail = RecordDetailSerializer
    lookup_field = 'uuid'
