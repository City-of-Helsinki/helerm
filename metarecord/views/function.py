from rest_framework import viewsets

from metarecord.models import Function
from .base import StructuralElementSerializer


class FunctionSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Function


class FunctionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer
