from rest_framework import serializers
from rest_framework.decorators import list_route


class BaseModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, format='hex')


class StructuralElementSerializer(BaseModelSerializer):
    class Meta:
        ordering = ('index',)


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
