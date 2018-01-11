from rest_framework import serializers, viewsets

from metarecord.models import Classification

from .base import HexRelatedField


class ClassificationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', format='hex', read_only=True)
    parent = HexRelatedField(read_only=True)
    function_allowed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Classification
        fields = ('id', 'created_at', 'modified_at', 'code', 'title', 'parent', 'description', 'description_internal',
                  'related_classification', 'additional_information', 'function_allowed')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_function(self, obj):
        user = self.context['request'].user
        functions = list(obj.functions.filter_for_user(user).latest_version())
        num_of_functions = len(functions)

        if num_of_functions > 1:
            raise Exception(
                'Classification %s has more than one functions (%s)' %
                (obj.uuid, [function.uuid for function in functions])
            )

        return functions[0] if num_of_functions else None

    def to_representation(self, obj):
        data = super().to_representation(obj)
        function = self._get_function(obj)
        if function:
            data['function'] = function.uuid.hex
            data['function_state'] = function.state
        else:
            data['function'] = None
            data['function_state'] = None
        return data


class ClassificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Classification.objects.order_by('code').prefetch_related('functions')
    serializer_class = ClassificationSerializer
    lookup_field = 'uuid'
