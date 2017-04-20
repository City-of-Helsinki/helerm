from rest_framework import serializers, viewsets

from metarecord.models import Action

from .base import DetailSerializerMixin, HexRelatedField, StructuralElementSerializer
from .record import RecordDetailSerializer


class ActionListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Action

    name = serializers.CharField(read_only=True, source='get_name')
    phase = HexRelatedField(read_only=True)
    records = HexRelatedField(many=True, read_only=True)


class ActionDetailSerializer(ActionListSerializer):
    records = RecordDetailSerializer(many=True)

    class Meta(ActionListSerializer.Meta):
        read_only_fields = ('index',)


class ActionViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.prefetch_related('records')
    serializer_class = ActionListSerializer
    serializer_class_detail = ActionDetailSerializer
    lookup_field = 'uuid'
