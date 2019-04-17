from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from metarecord.models.bulk_update import BulkUpdate
from metarecord.views.base import DetailSerializerMixin


class BulkUpdateListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    changes = serializers.DictField(required=False)
    is_approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = BulkUpdate
        ordering = ('created_at',)
        exclude = ('created_by', 'modified_by')

    def create(self, validated_data):
        user = self.context['request'].user

        if not user.has_perm(BulkUpdate.CAN_ADD):
            raise PermissionDenied(_('No permission to create bulk update'))

        user_data = {'created_by': user, 'modified_by': user}
        validated_data.update(user_data)

        return super().create(validated_data)


class BulkUpdateDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    changes = serializers.DictField(required=False)
    is_approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = BulkUpdate
        ordering = ('created_at',)
        exclude = ('created_by',)

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if not user.has_perm(BulkUpdate.CAN_CHANGE):
            raise PermissionDenied(_('No permission to update bulk update'))

        user_data = {'modified_by': user}
        validated_data.update(user_data)

        return super().update(instance, validated_data)


class BulkUpdateViewSet(DetailSerializerMixin, viewsets.ModelViewSet):
    queryset = BulkUpdate.objects.all().prefetch_related('functions').order_by('created_at')
    serializer_class = BulkUpdateListSerializer
    serializer_class_detail = BulkUpdateDetailSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = self.queryset

        if 'include_approved' not in self.request.query_params:
            queryset = queryset.exclude(is_approved=True)

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if not user.has_perm('metarecord.delete_bulkupdate'):
            raise PermissionDenied(_('No permission to delete bulk update'))

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        user = request.user
        instance = self.get_object()

        try:
            instance.approve(user)
        except (ObjectDoesNotExist, ValidationError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': e})

        return Response(status=status.HTTP_200_OK)
