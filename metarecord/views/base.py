import collections
from collections import defaultdict

from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers

from metarecord.models import Attribute, Classification, StructuralElement


class BaseModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, format='hex')


class ClassificationRelationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', format='hex', read_only=True)
    version = serializers.IntegerField(min_value=1, read_only=True)

    class Meta:
        model = Classification
        fields = ('id', 'version')

    def to_internal_value(self, data):
        return Classification.objects.get(uuid=data['id'], version=data['version'])


class StructuralElementSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', format='hex', read_only=True)
    # TODO: This DictFields child should allow only strings or array of strings.
    attributes = serializers.DictField(required=False)

    class Meta:
        ordering = ('index',)
        exclude = ('uuid', 'created_by')

    def get_fields(self):
        fields = super().get_fields()

        if 'request' not in self._context:
            return fields

        request = self._context["request"]

        fields = {
            field_name: field for field_name, field in fields.items()
            if field_name != 'modified_by' or StructuralElement.can_view_modified_by(request.user)
        }

        return fields

    def validate_attributes(self, attrs):
        # on PATCH requests we don't need to validate sent attributes,
        # they are ignored anyway
        if self.context['view'].action == 'partial_update':
            return attrs

        errors = Attribute.check_identifiers(attrs.keys())
        if errors:
            raise exceptions.ValidationError(errors)

        return attrs

    def get_valid_attribute_dict(self):
        if not hasattr(self, '_valid_attribute_dict'):
            self._valid_attribute_dict = {attr.identifier: attr for attr in Attribute.objects.all()}
        return self._valid_attribute_dict

    def get_attribute_validation_errors(self, instance, recursive=True):
        """
        Check allowed and required attributes, and verify choice attributes have valid values.

        With recursive=True get validation errors from all child StructuralElement objects as well.

        :return: validation error dict
        """
        all_errors = {}
        attribute_errors = defaultdict(list)
        disallowed_attributes = set()
        valid_attribute_dict = self.get_valid_attribute_dict()
        required_attributes = instance.get_required_attributes()
        multivalued_attributes = instance.get_multivalued_attributes()
        allow_values_outside_choices_attributes = instance.get_allow_values_outside_choices_attributes()

        # add conditionally required attributes to required attributes set
        for attribute, condition in instance.get_conditionally_required_attributes().items():
            condition_attribute, value = next(iter(condition.items()))

            if isinstance(value, str) or not isinstance(value, collections.Iterable):
                value = (value, )

            if condition_attribute in instance.attributes and instance.attributes[condition_attribute] in value:
                required_attributes.add(attribute)
            else:
                disallowed_attributes.add(attribute)

        # conditionally disallowed attributes
        for attribute, condition in instance.get_conditionally_disallowed_attributes().items():
            condition_attribute, value = next(iter(condition.items()))

            if isinstance(value, str) or not isinstance(value, collections.Iterable):
                value = (value,)

            if condition_attribute in instance.attributes and instance.attributes[condition_attribute] in value:
                disallowed_attributes.add(attribute)

        required_attributes = (required_attributes & valid_attribute_dict.keys()) - disallowed_attributes

        for attribute in required_attributes:
            if attribute not in instance.attributes.keys():
                attribute_errors[attribute].append(_('This attribute is required.'))

        for attribute, value in instance.attributes.items():
            if attribute not in valid_attribute_dict:
                attribute_errors[attribute].append(_('Invalid attribute.'))
                continue

            if not instance.is_attribute_allowed(attribute) or attribute in disallowed_attributes:
                attribute_errors[attribute].append(_("This attribute isn't allowed."))
                continue

            if isinstance(value, list) and attribute not in multivalued_attributes:
                attribute_errors[attribute].append(_("This attribute does not allow multiple values."))
                continue

            if not isinstance(value, list):
                value = [value]

            attribute_obj = valid_attribute_dict[attribute]
            if attribute_obj.is_free_text():
                for one_value in value:
                    if not isinstance(one_value, str):
                        attribute_errors[attribute].append(_('Value must be a string.'))
                continue

            for one_value in value:
                allowed_values = attribute_obj.values.values_list('value', flat=True)
                if one_value not in allowed_values and attribute not in allow_values_outside_choices_attributes:
                    attribute_errors[attribute].append(_('Invalid value.'))

        for all_or_none in instance.get_all_or_none_attributes():
            for missing_attribute in all_or_none - instance.attributes.keys():
                if _('This attribute is required.') not in attribute_errors[missing_attribute]:
                    attribute_errors[missing_attribute].append(_('This attribute is required.'))

        if attribute_errors:
            all_errors['attributes'] = attribute_errors

        child_relation_name = instance.get_child_relation_name()
        if recursive and child_relation_name:
            # run the same validations recursively for child structural elements
            child_objects = getattr(instance, child_relation_name).all().order_by('index')
            child_errors = [self.get_attribute_validation_errors(child_obj) for child_obj in child_objects]
            if any(errors for errors in child_errors):
                all_errors[child_relation_name] = child_errors

        return all_errors


class DetailSerializerMixin:
    def get_serializer_class(self):
        if self.action in ('retrieve', 'partial_update', 'update', 'delete'):
            try:
                return self.serializer_class_detail
            except AttributeError:
                pass

        return super().get_serializer_class()


class HexPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('pk_field', serializers.UUIDField(format='hex'))
        super().__init__(*args, **kwargs)


class HexRelatedField(serializers.SlugRelatedField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('slug_field', 'uuid')
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):
        value = super().to_representation(obj)
        return value.hex
