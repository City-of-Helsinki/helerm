from rest_framework import serializers, viewsets

from metarecord.models import Record, RecordAttachment, RecordType

from .base import AttributeFilter, DetailSerializerMixin, HexPrimaryKeyRelatedField, StructuralElementSerializer


class RecordAttachmentSerializer(StructuralElementSerializer):
    record = HexPrimaryKeyRelatedField(read_only=True, source='record_id')

    class Meta(StructuralElementSerializer.Meta):
        model = RecordAttachment


class RecordAttachmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecordAttachment.objects.all()
    serializer_class = RecordAttachmentSerializer
    filter_backends = (AttributeFilter,)


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
    attachments = HexPrimaryKeyRelatedField(many=True, read_only=True)


class RecordDetailSerializer(RecordListSerializer):
    attachments = RecordAttachmentSerializer(many=True, read_only=True)


class RecordViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordListSerializer
    serializer_class_detail = RecordDetailSerializer
    filter_backends = (AttributeFilter,)
