from rest_framework import serializers, viewsets

from metarecord.models import Classification

from .base import HexRelatedField


class ClassificationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', format='hex', read_only=True)
    parent = HexRelatedField(read_only=True)
    function = serializers.SerializerMethodField()

    class Meta:
        model = Classification
        fields = ('id', 'created_at', 'modified_at', 'code', 'title', 'parent', 'description', 'description_internal',
                  'related_classification', 'additional_information', 'function')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_function(self, obj):
        functions = list(obj.functions.latest_version())
        num_of_functions = len(functions)

        if num_of_functions > 1:
            raise Exception(
                'Classification %s has more than one functions (%s)' %
                (obj.uuid, [function.uuid for function in functions])
            )

        return functions[0].uuid.hex if num_of_functions else None


class ClassificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Classification.objects.order_by('code').prefetch_related('functions')
    serializer_class = ClassificationSerializer
    lookup_field = 'uuid'
