import pytest
from copy import deepcopy
from django.contrib.contenttypes.models import ContentType

from metarecord.models import Action, Function, Phase, Record
from metarecord.models.attribute import create_predefined_attributes
from metarecord.models.attribute_validation import AttributeValidationRule
from metarecord.models.structural_element import refactor_conditional_validation

VALIDATION_JSON = {
    'allowed': [
        'PersonalData', 'PublicityClass', 'RetentionPeriod', 'RetentionPeriodStart', 'SecurityPeriod',
        'InformationSystem', 'Subject'
    ],
    'required': [
        'PersonalData', 'PublicityClass', 'RetentionPeriod',
    ],
    'conditionally_required': [
        {
            'attribute': 'SecurityPeriod',
            'conditions': [
                {
                    'attribute': 'PublicityClass',
                    'value': 'Salassa pidettävä',
                },
                {
                    'attribute': 'PublicityClass',
                    'value': 'Osittain salassa pidettävä',
                },
            ]
        },
    ],
    'conditionally_disallowed': [
        {
            'attribute': 'RetentionPeriodStart',
            'conditions': [
                {
                    'attribute': 'RetentionPeriod',
                    'value': '-1',
                }
            ]
        },
    ],
    'multivalued': [
        'InformationSystem', 'Subject'
    ],
    'all_or_none': [
        ['InformationSystem', 'Subject'],
    ],
    'allow_values_outside_choices': [
        'InformationSystem', 'Subject'
    ],
}


@pytest.mark.parametrize('model', [Action, Function, Phase, Record])
def test_allowed_contains_required_keys(model):
    required_keys = set(model._attribute_validations.get('required', {})) | set(
        model._attribute_validations.get('conditionally_required', {}).keys())

    assert set(model._attribute_validations['allowed']).issuperset(required_keys), \
        'allowedKeys does not contain all the required keys in the model "{}" attribute validations'.format(
            model.__name__)


def test_refactor_conditional_validation():
    attr_validations = {
        "conditionally_required": [
            {
                "attribute": "SecurityPeriod",
                "conditions": [
                    {
                        "attribute": "PublicityClass",
                        "value": "Salassa pidettävä",
                    },
                    {
                        "attribute": "PublicityClass",
                        "value": "Osittain salassa pidettävä",
                    },
                ],
            },
        ]
    }
    expected_output = {
        'conditionally_required': {
            'SecurityPeriod': {
                'PublicityClass': [
                    'Salassa pidettävä', 'Osittain salassa pidettävä'
                ]
            },
        },
    }

    refactored_validations = deepcopy(attr_validations)
    refactor_conditional_validation(attr_validations, refactored_validations, "conditionally_required")

    assert refactored_validations == expected_output


@pytest.mark.django_db
def test_structural_element_json_schema_with_defined_validation(function):
    # Function is a subclass of StructuralElement
    create_predefined_attributes()

    content_type = ContentType.objects.get_for_model(function)
    AttributeValidationRule.objects.create(
        content_type=content_type,
        validation_json=VALIDATION_JSON,
    )

    allowed_attributes = VALIDATION_JSON["allowed"]
    json_schema = function.get_attribute_json_schema()

    assert all([prop in allowed_attributes for prop in json_schema["properties"]])
    assert len(json_schema["properties"]) == len(allowed_attributes)


@pytest.mark.django_db
def test_structural_element_required_attributes_with_defined_validation(function):
    # Function is a subclass of StructuralElement
    content_type = ContentType.objects.get_for_model(function)
    AttributeValidationRule.objects.create(
        content_type=content_type,
        validation_json=VALIDATION_JSON,
    )

    required_attributes = VALIDATION_JSON["required"]
    function_required_attributes = function.get_required_attributes()

    assert all([prop in required_attributes for prop in function_required_attributes])


@pytest.mark.django_db
def test_structural_element_multivalued_attributes_with_defined_validation(function):
    # Function is a subclass of StructuralElement
    content_type = ContentType.objects.get_for_model(function)
    AttributeValidationRule.objects.create(
        content_type=content_type,
        validation_json=VALIDATION_JSON,
    )

    multivalued_attributes = VALIDATION_JSON["multivalued"]
    function_multivalued_attributes = function.get_multivalued_attributes()

    assert all([prop in multivalued_attributes for prop in function_multivalued_attributes])


@pytest.mark.django_db
def test_structural_element_conditionally_required_attributes_with_defined_validation(function):
    # Function is a subclass of StructuralElement
    content_type = ContentType.objects.get_for_model(function)
    AttributeValidationRule.objects.create(
        content_type=content_type,
        validation_json=VALIDATION_JSON,
    )

    conditionally_required_attributes = VALIDATION_JSON["conditionally_required"]
    function_conditionally_required_attributes = function.get_conditionally_required_attributes()

    assert len(function_conditionally_required_attributes) == len(conditionally_required_attributes)


@pytest.mark.django_db
def test_structural_element_conditionally_disallowed_attributes_with_defined_validation(function):
    # Function is a subclass of StructuralElement
    content_type = ContentType.objects.get_for_model(function)
    AttributeValidationRule.objects.create(
        content_type=content_type,
        validation_json=VALIDATION_JSON,
    )

    conditionally_disallowed_attributes = VALIDATION_JSON["conditionally_disallowed"]
    function_conditionally_disallowed_attributes = function.get_conditionally_required_attributes()

    assert len(function_conditionally_disallowed_attributes) == len(conditionally_disallowed_attributes)


@pytest.mark.django_db
def test_structural_element_all_or_none_attributes_with_defined_validation(function):
    # Function is a subclass of StructuralElement
    content_type = ContentType.objects.get_for_model(function)
    AttributeValidationRule.objects.create(
        content_type=content_type,
        validation_json=VALIDATION_JSON,
    )

    all_or_none = VALIDATION_JSON["all_or_none"][0]
    function_all_or_none = function.get_all_or_none_attributes()[0]

    assert all([prop in all_or_none for prop in function_all_or_none])


@pytest.mark.django_db
def test_structural_element_allow_values_outside_choices_attributes_with_defined_validation(function):
    # Function is a subclass of StructuralElement
    content_type = ContentType.objects.get_for_model(function)
    AttributeValidationRule.objects.create(
        content_type=content_type,
        validation_json=VALIDATION_JSON,
    )

    allow_values_outside_choices = VALIDATION_JSON["allow_values_outside_choices"]
    function_allow_values_outside_choices = function.get_allow_values_outside_choices_attributes()

    assert all([prop in allow_values_outside_choices for prop in function_allow_values_outside_choices])


@pytest.mark.django_db
def test_structural_element_is_attribute_allowed_with_defined_validation(function):
    # Function is a subclass of StructuralElement
    content_type = ContentType.objects.get_for_model(function)
    AttributeValidationRule.objects.create(
        content_type=content_type,
        validation_json=VALIDATION_JSON,
    )

    allowed = VALIDATION_JSON["allowed"]
    assert function.is_attribute_allowed(allowed[0])
