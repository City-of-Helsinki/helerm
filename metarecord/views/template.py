from rest_framework import viewsets

from metarecord.models import Function

from .base import DetailSerializerMixin, HexRelatedField, StructuralElementSerializer
from .function import PhaseSerializer


class TemplateListSerializer(StructuralElementSerializer):
    class Meta:
        model = Function
        fields = ("id", "attributes", "phases", "created_at", "modified_at", "name")

    phases = HexRelatedField(many=True, read_only=True)


class TemplateDetailSerializer(TemplateListSerializer):
    phases = PhaseSerializer(many=True, read_only=True)


class TemplateViewSet(DetailSerializerMixin, viewsets.ReadOnlyModelViewSet):
    queryset = (
        Function.objects.filter(is_template=True)
        .prefetch_related("phases")
        .order_by("created_at")
    )
    serializer_class = TemplateListSerializer
    serializer_class_detail = TemplateDetailSerializer
    lookup_field = "uuid"
