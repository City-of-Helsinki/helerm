from rest_framework import viewsets

from metarecord.models import Phase
from .base import StructuralElementSerializer


class PhaseSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Phase


class PhaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer
