from django.contrib.auth import get_user_model
from rest_framework import permissions, serializers, viewsets

from metarecord.models import Function


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('uuid', 'username', 'first_name', 'last_name', 'permissions')

    def get_permissions(self, obj):
        app_label = Function._meta.app_label
        return [perm[0] for perm in Function._meta.permissions if obj.has_perm('%s.%s' % (app_label, perm[0]))]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.IsAuthenticated,)
    queryset = get_user_model().objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(pk=self.request.user.pk)
