import uuid
from copy import deepcopy

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .attribute import Attribute
from .base import TimeStampedModel


class StructuralElement(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                   null=True, blank=True, related_name='%(class)s_created', editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('modified by'),
                                    null=True, blank=True, related_name='%(class)s_modified', editable=False)
    index = models.PositiveSmallIntegerField(null=True, editable=False, db_index=True)
    attributes = JSONField(verbose_name=_('attributes'), blank=True, default=dict)

    _attribute_validations = {
        'allowed': None,
        'required': None,
        'conditionally_required': None,
        'multivalued': None,
        'all_or_none': None,
    }

    class Meta:
        abstract = True
        ordering = ('index',)

    @classmethod
    def get_attribute_json_schema(cls):
        return get_attribute_json_schema(**cls._attribute_validations)

    @classmethod
    def get_required_attributes(cls):
        return set(cls._attribute_validations.get('required') or [])

    @classmethod
    def get_multivalued_attributes(cls):
        return set(cls._attribute_validations.get('multivalued') or [])

    @classmethod
    def get_conditionally_required_attributes(cls):
        return deepcopy(cls._attribute_validations.get('conditionally_required')) or {}

    @classmethod
    def get_all_or_none_attributes(cls):
        return [
            set(validation)
            for validation in cls._attribute_validations.get('all_or_none') or []
        ]

    @classmethod
    def is_attribute_allowed(cls, attribute_identifier):
        allowed = cls._attribute_validations.get('allowed')
        if allowed is None:
            # None means the validation isn't enabled
            return True
        return attribute_identifier in allowed

    @classmethod
    def get_child_relation_name(cls):
        child_field_names = {
            'Function': 'phases',
            'Phase': 'actions',
            'Action': 'records',
            'Record': None,
        }
        try:
            return child_field_names[cls.__name__]
        except KeyError:
            raise NotImplementedError()

    def save(self, *args, **kwargs):
        for key, value in self.attributes.copy().items():
            if value in ('', None):
                del self.attributes[key]
        return super().save(*args, **kwargs)


def get_attribute_json_schema(allowed=None, required=None, conditionally_required=None, multivalued=None, **kwargs):
    """
    Return schema for attributes in JSON schema draft 4 format.

    :param allowed: list of allowed attribute identifiers
    :param required: list of required attribute identifiers
    :param conditionally_required: conditionally required attribute, format:
        {
            <conditionally required attribute identifier>: {
                <condition attribute identifier>: <condition attribute value>
            }
        }
    :param multivalued: list of multivalued attribute identifiers
    :return: dict containing JSON schema data
    """

    assert set(allowed or []).issuperset(set(required or [])), '"required" contains value(s) not found in "allowed"'

    properties = {}

    if allowed is None:
        attributes = Attribute.objects.all()
    else:
        attributes = Attribute.objects.filter(identifier__in=allowed)

    existing_identifiers = set()

    for attribute in attributes:
        existing_identifiers.add(attribute.identifier)

        values = attribute.values.values_list('value', flat=True)  # lots of values here
        attribute_type = {'enum': values} if values else {'type': 'string'}

        if not multivalued or attribute.identifier not in multivalued:
            properties.update({attribute.identifier: attribute_type})
        else:
            properties.update({
                attribute.identifier: {
                    "anyOf": [
                        attribute_type,
                        {'type': 'array', 'items': attribute_type}
                    ]
                }
            })

    schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': properties,
        'additionalProperties': False,
    }

    if required:
        schema['required'] = [attr for attr in required if attr in existing_identifiers]

    if conditionally_required:
        all_of = []

        for required_attribute, condition in conditionally_required.items():

            condition_attribute, values = next(iter(condition.items()))
            if not (isinstance(values, list) or isinstance(values, tuple)):
                values = (values,)

            if len(condition) > 1:
                raise NotImplementedError('Only one condition supported at the moment. ')

            if not (required_attribute in existing_identifiers and condition_attribute in existing_identifiers):
                continue

            all_of.append({'oneOf': [
                {
                    'properties': {
                        condition_attribute: {
                            'enum': values
                        }
                    },
                    'required': [required_attribute]
                },
                {
                    'properties': {
                        condition_attribute: {
                            'not': {'enum': values}
                        }
                    },
                    'required': []
                },
            ]})

        if all_of:
            schema['allOf'] = all_of

    return schema
