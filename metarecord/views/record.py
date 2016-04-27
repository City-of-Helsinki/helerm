from rest_framework import viewsets

from metarecord.models import Record, RecordAttachment
from .base import StructuralElementSerializer


class RecordSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Record


class RecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


class RecordAttachmentSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = RecordAttachment


class RecordAttachmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecordAttachment.objects.all()
    serializer_class = RecordAttachmentSerializer
