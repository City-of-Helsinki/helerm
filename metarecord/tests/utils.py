from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from metarecord.models import Function


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


def check_attribute_errors(errors, attribute, expected_error):
    """
    Assert attribute error exists in given error dict

    :param errors: attribute error dict
    :param attribute: Attribute object to check
    :param expected_error: part of expected error message
    """
    error_list = errors['attributes'].get(attribute.identifier)
    assert error_list is not None, 'no attribute "%s" in errors' % attribute.identifier
    assert any(expected_error in error for error in error_list), '"%s" not in %s' % (expected_error, errors)


def assert_response_functions(response, objects):
    """
    Assert Function object or objects exist in response data.
    """
    data = response.data
    if 'results' in data:
        data = data['results']

    if not (isinstance(objects, list) or isinstance(objects, tuple)):
        objects = [objects]

    expected_ids = {obj.uuid.hex for obj in objects}
    actual_ids = {str(obj['id']) for obj in data}
    assert expected_ids == actual_ids, '%s does not match %s' % (expected_ids, actual_ids)
