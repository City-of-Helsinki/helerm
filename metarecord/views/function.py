from rest_framework import viewsets

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
    queryset = Function.objects.filter(is_template=False).prefetch_related('phases')
    serializer_class = FunctionListSerializer
    serializer_class_detail = FunctionDetailSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        state = self.request.query_params.get('state')
        if state == 'approved':
            return self.queryset.latest_approved()
        return self.queryset.latest_version()
