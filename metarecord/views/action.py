from rest_framework import viewsets

from metarecord.models import Action
from .base import StructuralElementSerializer


class ActionSerializer(StructuralElementSerializer):
    class Meta(StructuralElementSerializer.Meta):
        model = Action


class ActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
