from rest_framework import serializers, viewsets

from metarecord.models import Function

from .base import DetailSerializerMixin, HexRelatedField, StructuralElementSerializer
from .phase import PhaseDetailSerializer


class FunctionListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Function
        exclude = StructuralElementSerializer.Meta.exclude + ('index', 'is_template')

    parent = HexRelatedField(read_only=True)
    phases = HexRelatedField(many=True, read_only=True)


class FunctionDetailSerializer(FunctionListSerializer):
    phases = PhaseDetailSerializer(many=True, read_only=True)


class FunctionViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Function.objects.filter(is_template=False).prefetch_related('phases').order_by('function_id')
    serializer_class = FunctionListSerializer
    serializer_class_detail = FunctionDetailSerializer
    lookup_field = 'uuid'
