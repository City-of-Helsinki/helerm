import pytest

from metarecord.models.attribute import create_predefined_attributes


@pytest.mark.django_db
def test_structural_element_persistent_user_name_fields(user, function):
    # Function is a subclass of StructuralElement
    function.created_by = user
    function.modified_by = user

    function.save()
    assert function._created_by == 'John Rambo'
    assert function._modified_by == 'John Rambo'

    user.delete()
    function.refresh_from_db()
    function.save()  # Save should not affect _created_by and _modified_by contents
    assert not function.created_by
    assert function._created_by == 'John Rambo'
    assert not function.modified_by
    assert function._modified_by == 'John Rambo'


@pytest.mark.django_db
def test_structural_element_json_schema(function):
    # Function is a subclass of StructuralElement
    create_predefined_attributes()

    allowed_attributes = function._attribute_validations["allowed"]
    json_schema = function.get_attribute_json_schema()
    assert all([prop in allowed_attributes for prop in json_schema["properties"]])
