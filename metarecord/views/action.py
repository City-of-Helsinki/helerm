from rest_framework import serializers, viewsets

from metarecord.models import Action

from .base import AttributeFilter, DetailSerializerMixin, StructuralElementSerializer
from .record import RecordDetailSerializer


class ActionListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Action

    records = serializers.PrimaryKeyRelatedField(many=True, read_only=True,
                                                 pk_field=serializers.UUIDField(format='hex'))


class ActionDetailSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Action

    records = RecordDetailSerializer(many=True, read_only=True)


class ActionViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionListSerializer
    serializer_class_detail = ActionDetailSerializer
    filter_backends = (AttributeFilter,)
