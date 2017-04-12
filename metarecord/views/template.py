from rest_framework import viewsets

from metarecord.models import Function

from .base import DetailSerializerMixin, HexRelatedField, StructuralElementSerializer
from .phase import PhaseDetailSerializer


class TemplateListSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Function
        exclude = ('is_template', 'index', 'parent', 'function_id')

    phases = HexRelatedField(many=True, read_only=True)


class TemplateDetailSerializer(TemplateListSerializer):
    phases = PhaseDetailSerializer(many=True, read_only=True)


class TemplateViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Function.objects.filter(is_template=True).prefetch_related('phases')
    serializer_class = TemplateListSerializer
    serializer_class_detail = TemplateDetailSerializer
    lookup_field = 'uuid'
