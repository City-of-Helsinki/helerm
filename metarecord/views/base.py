from collections import defaultdict

from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers

from metarecord.models import Attribute, Function


class BaseModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, format='hex')


class StructuralElementSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', format='hex', read_only=True)
    attributes = serializers.DictField(child=serializers.CharField(), required=False)

    class Meta:
        ordering = ('index',)
        exclude = ('uuid', 'created_by', 'modified_by')

    @property
    def fields(self):
        fields = super(StructuralElementSerializer, self).fields

        if 'request' not in self._context:
            return fields

        request = self._context["request"]

        for field_name, field in fields.items():
            if field_name == 'modified_by' and not request.user.has_perm(Function.CAN_VIEW_MODIFIED_BY):
                fields.pop(field_name)

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
        valid_attribute_dict = self.get_valid_attribute_dict()
        required_attributes = instance.get_required_attributes()

        # add conditionally required attributes to required attributes set
        for attribute, condition in instance.get_conditionally_required_attributes().items():
            condition_attribute, value = next(iter(condition.items()))
            if condition_attribute in instance.attributes and instance.attributes[condition_attribute] == value:
                required_attributes.add(attribute)

        required_attributes = required_attributes & valid_attribute_dict.keys()

        for attribute in required_attributes:
            if attribute not in instance.attributes.keys():
                attribute_errors[attribute].append(_('This attribute is required.'))

        for attribute, value in instance.attributes.items():
            if attribute not in valid_attribute_dict:
                attribute_errors[attribute].append(_('Invalid attribute.'))
                continue

            if not (attribute in valid_attribute_dict and instance.is_attribute_allowed(attribute)):
                attribute_errors[attribute].append(_("This attribute isn't allowed."))
                continue

            attribute_obj = valid_attribute_dict[attribute]
            if attribute_obj.is_free_text():
                continue

            if value not in attribute_obj.values.values_list('value', flat=True):
                attribute_errors[attribute].append(_('Invalid value.'))

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
        if self.action in ('create', 'retrieve', 'partial_update', 'update'):
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
