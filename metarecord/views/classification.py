from django.db.models import Prefetch
from rest_framework import serializers, viewsets

from metarecord.models import Classification, Function
from metarecord.views.function import PhaseSerializer

from .base import HexRelatedField


class ClassificationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', format='hex', read_only=True)
    parent = HexRelatedField(read_only=True)
    phases = serializers.SerializerMethodField(method_name='_get_phases')

    class Meta:
        model = Classification
        fields = ('id', 'created_at', 'modified_at', 'code', 'title', 'parent', 'description', 'description_internal',
                  'related_classification', 'additional_information', 'function_allowed', 'phases')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_function(self, obj):
        functions = obj.prefetched_functions
        num_of_functions = len(functions)

        if num_of_functions > 1:
            raise Exception(
                'Classification %s has more than one functions (%s)' %
                (obj.uuid, [function.uuid for function in functions])
            )

        return functions[0] if num_of_functions else None

    def _append_function_fields_to_repr(self, obj, data):
        function = self._get_function(obj)
        if function:
            data['function'] = function.uuid.hex
            data['function_state'] = function.state
            data['function_attributes'] = function.attributes
        else:
            data['function'] = None
            data['function_state'] = None
            data['function_attributes'] = None

        return data

    def _get_phases(self, obj):
        phases = None
        function = self._get_function(obj)

        if function:
            phases = function.phases.all()

        serializer = PhaseSerializer(phases, many=True)

        return serializer.data

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data = self._append_function_fields_to_repr(obj, data)

        request = self.context['request']
        if request and not request.user.is_authenticated:
            data.pop('description_internal', None)
            data.pop('additional_information', None)

        return data


class ClassificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Classification.objects.order_by('code').select_related('parent').prefetch_related('children')
    serializer_class = ClassificationSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        user = self.request.user

        return super().get_queryset().prefetch_related(
            Prefetch(
                'functions', queryset=Function.objects.filter_for_user(user).latest_version(),
                to_attr='prefetched_functions'
            )
        )
