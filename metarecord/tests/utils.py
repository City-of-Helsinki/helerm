from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


def set_permissions(api_client, permissions):
    """
    Set permissions for api_client user.

    Just setting the permissions for the user isn't enough because then
    Django will use cached permissions in views.
    """
    if type(permissions) == str:
        permissions = [permissions]

    codenames = [perm.split('.')[1] for perm in permissions]

    user = api_client.user
    user.user_permissions = Permission.objects.filter(codename__in=codenames)
    user = get_user_model().objects.get(pk=user.pk)
    api_client.force_authenticate(user)
