from rest_framework import serializers, viewsets

from metarecord.models import Record, RecordAttachment, RecordType

from .base import AttributeFilter, DetailSerializerMixin, StructuralElementSerializer


class RecordAttachmentSerializer(StructuralElementSerializer):
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

    attachments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


class RecordDetailSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Record

    attachments = RecordAttachmentSerializer(many=True, read_only=True)


class RecordViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordListSerializer
    serializer_class_detail = RecordDetailSerializer
    filter_backends = (AttributeFilter,)
