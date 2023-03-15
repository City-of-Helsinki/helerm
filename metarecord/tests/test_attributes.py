import pytest

from metarecord.models import Attribute, AttributeValue


@pytest.mark.django_db
def test_attributes_will_get_index_numbers():
    attribute_1 = Attribute.objects.create(name="attribute 1")
    assert attribute_1.index == 1

    attribute_2 = Attribute.objects.create(name="attribute 2")
    assert attribute_2.index == 2


@pytest.mark.parametrize(
    "value",
    [
        "",
        None,
    ],
)
@pytest.mark.django_db
def test_attributes_cannot_be_empty(function, free_text_attribute, value):
    identifier = free_text_attribute.identifier
    function.attributes[identifier] = value
    function.save(update_fields=("attributes",))
    function.refresh_from_db()

    assert identifier not in function.attributes


@pytest.mark.django_db
def test_attribute_values_will_get_index_numbers(free_text_attribute):
    attribute_value_1 = AttributeValue.objects.create(
        value="attribute value 1", attribute=free_text_attribute
    )
    assert attribute_value_1.index == 1

    attribute_value_2 = AttributeValue.objects.create(
        value="attribute value 2", attribute=free_text_attribute
    )
    assert attribute_value_2.index == 2
