import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_hstore import hstore

from .attribute import Attribute
from .base import TimeStampedModel


class StructuralElement(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
                                   null=True, blank=True, related_name='%(class)s_created', editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('modified by'),
                                    null=True, blank=True, related_name='%(class)s_modified', editable=False)
    index = models.PositiveSmallIntegerField(null=True, editable=False, db_index=True)
    attributes = hstore.DictionaryField(blank=True, null=True)

    _attribute_validations = {
        'allowed': None,
        'required': None,
        'conditionally_required': None,
    }

    class Meta:
        abstract = True
        ordering = ('index',)

    @classmethod
    def get_attribute_json_schema(cls):
        return get_attribute_json_schema(**cls._attribute_validations)


def reload_attribute_schema():
    """
    Reload django-hstore schema for attributes.
    """
    whole_schema = []

    for attribute in Attribute.objects.prefetch_related('values'):
        attribute_schema = {
            'name': attribute.identifier,
            'class': 'CharField',
            'kwargs': {
                'max_length': 1024,
                'blank': True,
                'null': True,
                'verbose_name': attribute.name,
            }
        }

        values = attribute.values.all()
        if len(values):
            choices = [(value.value, value.value) for value in values]
            attribute_schema['kwargs']['choices'] = choices

        whole_schema.append(attribute_schema)

    for model in StructuralElement.__subclasses__():
        data_field = model._meta.get_field('attributes')
        data_field.reload_schema(whole_schema)


def get_attribute_json_schema(allowed=None, required=None, conditionally_required=None):
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

        if attribute.values.exists():
            enum = []
            for value in attribute.values.all():
                enum.append(value.value)
            properties.update({attribute.identifier: {'enum': enum}})
        else:
            properties.update({attribute.identifier: {'type': 'string'}})

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

            condition_attribute, value = next(iter(condition.items()))

            if len(condition) > 1:
                raise NotImplementedError('Only one condition supported at the moment. ')

            if not (required_attribute in existing_identifiers and condition_attribute in existing_identifiers):
                continue

            all_of.append({'oneOf': [
                {
                    'properties': {
                        condition_attribute: {
                            'enum': [value]
                        }
                    },
                    'required': [required_attribute]
                },
                {
                    'properties': {
                        condition_attribute: {
                            'not': {'enum': [value]}
                        }
                    },
                    'required': []
                },
            ]})

        if all_of:
            schema['allOf'] = all_of

    return schema
