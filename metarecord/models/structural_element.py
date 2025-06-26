import uuid
from collections.abc import Iterable
from copy import deepcopy

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .attribute import Attribute
from .attribute_validation import AttributeValidationRule
from .base import TimeStampedModel


class StructuralElement(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("created by"),
        null=True,
        blank=True,
        related_name="%(class)s_created",
        editable=False,
        on_delete=models.SET_NULL,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("modified by"),
        null=True,
        blank=True,
        related_name="%(class)s_modified",
        editable=False,
        on_delete=models.SET_NULL,
    )
    _created_by = models.CharField(
        verbose_name=_("created by (text)"), max_length=200, blank=True, editable=False
    )
    _modified_by = models.CharField(
        verbose_name=_("modified by (text)"), max_length=200, blank=True, editable=False
    )
    index = models.PositiveSmallIntegerField(null=True, editable=False, db_index=True)
    attributes = models.JSONField(
        verbose_name=_("attributes"), blank=True, default=dict
    )

    _attribute_validations = {
        "allowed": None,
        "required": None,
        "conditionally_required": None,
        "conditionally_disallowed": None,
        "multivalued": None,
        "all_or_none": None,
        "allow_values_outside_choices": None,
    }

    class Meta:
        abstract = True
        ordering = ("index",)

    @classmethod
    def get_attribute_validations(cls):
        """
        Returns the attribute validation rules with the priority:
        1. Type specific attribute validation rules, combined with the general attribute validation rules.
        2. General attribute validation rules if the type specific do not exist.
        3. Hard coded `_attribute_validations` if neither type specific or general attribute validation rules exist.
        """
        content_type = ContentType.objects.get_for_model(cls)
        general_content_type = ContentType.objects.get_for_model(
            AttributeValidationRule
        )

        attr_validation_rule = AttributeValidationRule.objects.filter(
            content_type=content_type
        ).first()
        general_attr_validation_rule = AttributeValidationRule.objects.filter(
            content_type=general_content_type
        ).first()

        if attr_validation_rule and general_attr_validation_rule:
            attr_validations = attr_validation_rule.validation_json
            general_attr_validations = general_attr_validation_rule.validation_json

            # Combine type specific attribute validation rules with the general validation rules.
            for attr_key in StructuralElement._attribute_validations.keys():
                attr_validations[attr_key] += general_attr_validations[attr_key]

        elif attr_validation_rule:
            attr_validations = attr_validation_rule.validation_json
        elif general_attr_validation_rule:
            attr_validations = general_attr_validation_rule.validation_json
        else:
            return cls._attribute_validations

        refactored_validations = deepcopy(attr_validations)

        cond_type = "conditionally_required"
        refactor_conditional_validation(
            attr_validations, refactored_validations, cond_type
        )

        cond_type = "conditionally_disallowed"
        refactor_conditional_validation(
            attr_validations, refactored_validations, cond_type
        )

        return refactored_validations

    @classmethod
    def get_attribute_json_schema(cls):
        return get_attribute_json_schema(**cls.get_attribute_validations())

    @classmethod
    def get_required_attributes(cls):
        return set(cls.get_attribute_validations().get("required") or [])

    @classmethod
    def get_multivalued_attributes(cls):
        return set(cls.get_attribute_validations().get("multivalued") or [])

    @classmethod
    def get_conditionally_required_attributes(cls):
        return (
            deepcopy(cls.get_attribute_validations().get("conditionally_required"))
            or {}
        )

    @classmethod
    def get_conditionally_disallowed_attributes(cls):
        return (
            deepcopy(cls.get_attribute_validations().get("conditionally_disallowed"))
            or {}
        )

    @classmethod
    def get_all_or_none_attributes(cls):
        return [
            set(validation)
            for validation in cls.get_attribute_validations().get("all_or_none") or []
            if validation
        ]

    @classmethod
    def get_allow_values_outside_choices_attributes(cls):
        return set(
            cls.get_attribute_validations().get("allow_values_outside_choices") or []
        )

    @classmethod
    def is_attribute_allowed(cls, attribute_identifier):
        allowed = cls.get_attribute_validations().get("allowed")
        if allowed is None:
            # None means the validation isn't enabled
            return True
        return attribute_identifier in allowed

    @classmethod
    def get_child_relation_name(cls):
        child_field_names = {
            "Function": "phases",
            "Phase": "actions",
            "Action": "records",
            "Record": None,
        }
        try:
            return child_field_names[cls.__name__]
        except KeyError:
            raise NotImplementedError()

    @classmethod
    def can_view_modified_by(cls, user):
        if not user:
            return False
        return user.has_perm("metarecord.can_view_modified_by")

    def get_modified_by_display(self):
        return self._modified_by or None

    def save(self, *args, **kwargs):
        # Only update `_created_by` and `_modified_by` value if the relations
        # are set set. Text values should persist even if related user is deleted.
        if self.created_by:
            self._created_by = self.created_by.get_full_name()

        if self.modified_by:
            self._modified_by = self.modified_by.get_full_name()

        for key, value in self.attributes.copy().items():
            if value in ("", None):
                del self.attributes[key]

        super().save(*args, **kwargs)


def _get_conditionally_required_schema(
    required_attributes, condition_attribute, condition_values
):
    return {
        "oneOf": [
            {
                "properties": {condition_attribute: {"enum": condition_values}},
                "required": required_attributes,
            },
            {
                "properties": {
                    condition_attribute: {"not": {"enum": condition_values}}
                },
                "required": [],
            },
        ]
    }


def get_attribute_json_schema(**kwargs):  # noqa: C901
    if (
        "allowed" not in kwargs or kwargs["allowed"] is None
    ):  # None means the validation isn't enabled
        allowed_attributes = Attribute.objects.all()
    else:
        allowed_attributes = Attribute.objects.filter(identifier__in=kwargs["allowed"])

    allowed = {attr.identifier for attr in allowed_attributes}
    required = kwargs.get("required") or set()
    conditionally_required = kwargs.get("conditionally_required") or {}
    conditionally_disallowed = kwargs.get("conditionally_disallowed") or {}
    multivalued = kwargs.get("multivalued") or set()
    allow_values_outside_choices = kwargs.get("allow_values_outside_choices") or set()

    assert set(allowed).issuperset(set(required)), (
        '"required" contains value(s) not found in "allowed"'
    )

    properties = {}

    for attribute in allowed_attributes:
        values = attribute.values.values_list("value", flat=True)  # lots of values here
        attribute_type = {"enum": values} if values else {"type": "string"}

        if not multivalued or attribute.identifier not in multivalued:
            properties.update({attribute.identifier: attribute_type})
        else:
            properties.update(
                {
                    attribute.identifier: {
                        "anyOf": [
                            attribute_type,
                            {"type": "array", "items": attribute_type},
                        ]
                    }
                }
            )

    schema = {
        "$schema": "https://json-schema.org/draft-04/schema",
        "type": "object",
        "properties": properties,
        "additionalProperties": False,
    }

    all_of = []

    for required_attribute, condition in conditionally_required.items():
        condition_attribute, values = next(iter(condition.items()))
        if isinstance(values, str) or not isinstance(values, Iterable):
            values = (values,)

        if len(condition) > 1:
            raise NotImplementedError("Only one condition supported at the moment. ")

        if not (required_attribute in allowed and condition_attribute in allowed):
            continue

        all_of.append(
            _get_conditionally_required_schema(
                [required_attribute], condition_attribute, values
            )
        )

    actually_required = set(required)

    for required_attribute, condition in conditionally_disallowed.items():
        condition_attribute, values = next(iter(condition.items()))
        if isinstance(values, str) or not isinstance(values, Iterable):
            values = (values,)

        if len(condition) > 1:
            raise NotImplementedError("Only one condition supported at the moment. ")

        if not (required_attribute in allowed and condition_attribute in allowed):
            continue

        try:
            attribute = next(
                attr
                for attr in allowed_attributes
                if attr.identifier == condition_attribute
            )
        except StopIteration:
            continue

        not_values = set(attribute.values.values_list("value", flat=True)) - set(values)
        all_of.append(
            _get_conditionally_required_schema(
                [required_attribute], condition_attribute, not_values
            )
        )
        actually_required.discard(required_attribute)

    schema["required"] = actually_required

    if all_of:
        schema["allOf"] = all_of

    extra_validations = {}

    if allow_values_outside_choices:
        extra_validations["allow_values_outside_choices"] = allow_values_outside_choices

    schema["extra_validations"] = extra_validations

    return schema


def refactor_conditional_validation(
    attr_validations, refactored_validations, cond_type
):
    """
    Refactor the conditional (conditionally_required, conditionally_disallowed) validation rules from the JSON schema
    of the Django admin to the schema supported by the rest of the application. This needs to be done because the
    django-admin-json-editor schema does not support the existing validation schema.

    Example:

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
    ]

    ->

    'conditionally_required': {
        'SecurityPeriod': {'PublicityClass': ['Salassa pidettävä', 'Osittain salassa pidettävä']},
    },
    """
    refactored_validations[cond_type] = {}
    for conditional_validation_obj in attr_validations.get(cond_type, []):
        attribute = conditional_validation_obj["attribute"]

        if attribute not in refactored_validations[cond_type]:
            refactored_validations[cond_type][attribute] = {}

        conditions = conditional_validation_obj["conditions"]
        for condition_obj in conditions:
            cond_attribute = condition_obj["attribute"]
            cond_value = condition_obj["value"]

            if cond_attribute not in refactored_validations[cond_type][attribute]:
                refactored_validations[cond_type][attribute][cond_attribute] = []

            refactored_validations[cond_type][attribute][cond_attribute].append(
                cond_value
            )
