from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, serializers, viewsets

from metarecord.models import Function
from metarecord.models.bulk_update import BulkUpdate


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('uuid', 'username', 'first_name', 'last_name', 'permissions')

    def _get_user_bulk_update_permissions(self, user):
        content_type = ContentType.objects.get_for_model(BulkUpdate)
        permissions = Permission.objects.filter(content_type=content_type)
        return [
            perm.codename
            for perm in permissions
            if user.has_perm('%s.%s' % (content_type.app_label, perm.codename))
        ]

    def _get_user_function_permissions(self, user):
        app_label = Function._meta.app_label
        return [
            perm[0]
            for perm in Function._meta.permissions
            if user.has_perm('%s.%s' % (app_label, perm[0]))
        ]

    def get_permissions(self, obj):
        function_permissions = self._get_user_function_permissions(obj)
        bulk_update_permissions = self._get_user_bulk_update_permissions(obj)
        return function_permissions + bulk_update_permissions


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.IsAuthenticated,)
    queryset = get_user_model().objects.all().order_by('id')

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(pk=self.request.user.pk)
