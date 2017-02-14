from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, format='hex')


class StructuralElementSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', format='hex')

    class Meta:
        ordering = ('index',)
        exclude = ('uuid',)


class DetailSerializerMixin:
    def get_serializer_class(self):
        if self.action == 'retrieve':
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
