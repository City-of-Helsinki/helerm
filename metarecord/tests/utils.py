from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import serializers

from metarecord.models import Function
from metarecord.views.base import (
    ClassificationRelationSerializer,
    StructuralElementSerializer,
)
from metarecord.views.function import PhaseSerializer


def set_permissions(api_client, permissions):
    """
    Set permissions for api_client user.

    Just setting the permissions for the user isn't enough because then
    Django will use cached permissions in views.
    """
    if isinstance(permissions, str):
        permissions = [permissions]

    codenames = [perm.split(".")[1] for perm in permissions]

    user = api_client.user
    user.user_permissions.set(Permission.objects.filter(codename__in=codenames))
    user = get_user_model().objects.get(pk=user.pk)
    api_client.force_authenticate(user)


def check_attribute_errors(errors, attribute, expected_error):
    """
    Assert attribute error exists in given error dict

    :param errors: attribute error dict
    :param attribute: Attribute object to check
    :param expected_error: part of expected error message
    """
    error_list = errors["attributes"].get(attribute.identifier)
    assert error_list is not None, 'no attribute "%s" in errors' % attribute.identifier
    assert any(expected_error in error for error in error_list), '"%s" not in %s' % (
        expected_error,
        errors,
    )


def assert_response_functions(response, objects):
    """
    Assert Function object or objects exist in response data.
    """
    data = response.data
    if "results" in data:
        data = data["results"]

    if not (isinstance(objects, list) or isinstance(objects, tuple)):
        objects = [objects]

    expected_ids = {obj.uuid.hex for obj in objects}
    actual_ids = {str(obj["id"]) for obj in data}
    assert expected_ids == actual_ids, "%s does not match %s" % (
        expected_ids,
        actual_ids,
    )


def get_bulk_update_function_key(function):
    return "{uuid}__{version}".format(uuid=function.uuid.hex, version=function.version)


class FunctionTestDetailSerializer(StructuralElementSerializer):
    version = serializers.IntegerField(read_only=True)
    modified_by = serializers.SerializerMethodField()
    state = serializers.CharField(read_only=True)

    # TODO these three are here to maintain backwards compatibility,
    # should be removed as soon as the UI doesn't need these anymore
    function_id = serializers.ReadOnlyField(source="get_classification_code")
    # there is also Function.name field which should be hidden for other than templates when this is removed
    name = serializers.ReadOnlyField(source="get_name")
    parent = serializers.SerializerMethodField()
    classification_code = serializers.ReadOnlyField(source="get_classification_code")
    classification_title = serializers.ReadOnlyField(source="get_name")

    classification = ClassificationRelationSerializer()

    class Meta(StructuralElementSerializer.Meta):
        model = Function
        exclude = StructuralElementSerializer.Meta.exclude + ("index", "is_template")

    def get_parent(self, obj):
        if obj.classification and obj.classification.parent:
            parent_functions = Function.objects.filter(
                classification__uuid=obj.classification.parent.uuid
            )
            if parent_functions.exists():
                return parent_functions[0].uuid.hex
        return None

    def get_fields(self):
        fields = super().get_fields()

        fields["phases"] = PhaseSerializer(many=True, required=False)

        return fields
