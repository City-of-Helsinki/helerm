from rest_framework import serializers, viewsets

from metarecord.models import Function

from .base import AttributeFilter, DetailSerializerMixin, StructuralElementSerializer
from .phase import PhaseDetailSerializer


class FunctionListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Function

    phases = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    children = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


class FunctionDetailSerializer(FunctionListSerializer):
    phases = PhaseDetailSerializer(many=True, read_only=True)


class FunctionViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Function.objects.all()
    serializer_class = FunctionListSerializer
    serializer_class_detail = FunctionDetailSerializer
    filter_backends = (AttributeFilter,)
