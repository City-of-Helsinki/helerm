from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from metarecord.models import Attribute


class BaseModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, format='hex')


class StructuralElementSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', format='hex', read_only=True)

    class Meta:
        ordering = ('index',)
        exclude = ('uuid', 'created_by', 'modified_by')

    def validate_attributes(self, attrs):
        input_attrs = set(attrs.keys())
        valid_attrs = set(Attribute.objects.values_list('identifier', flat=True))
        invalid_attrs = input_attrs - valid_attrs
        if invalid_attrs:
            errors = {attr: [_('Invalid attribute.')] for attr in invalid_attrs}
            raise exceptions.ValidationError(errors)
        return attrs


class DetailSerializerMixin:
    def get_serializer_class(self):
        if self.action in ('create', 'retrieve', 'update'):
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
