from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers, viewsets

from metarecord.models import Action, Function, Phase, Record

from .base import DetailSerializerMixin, HexRelatedField, StructuralElementSerializer
from .phase import PhaseDetailSerializer


class FunctionListSerializer(StructuralElementSerializer):
    parent = HexRelatedField(queryset=Function.objects.all(), required=False, allow_null=True)
    phases = HexRelatedField(many=True, read_only=True)
    version = serializers.IntegerField(read_only=True)

    class Meta(StructuralElementSerializer.Meta):
        model = Function
        exclude = StructuralElementSerializer.Meta.exclude + ('index', 'is_template')


class FunctionDetailSerializer(FunctionListSerializer):
    phases = PhaseDetailSerializer(many=True)

    @transaction.atomic
    def _create_new_version(self, function_data):
        user = self.context['request'].user
        user_data = {'created_by': user, 'modified_by': user}

        phase_data = function_data.pop('phases', [])
        function_data.update(user_data)
        function = Function.objects.create(**function_data)

        for index, phase_datum in enumerate(phase_data, 1):
            action_data = phase_datum.pop('actions', [])
            phase_datum.update(user_data)
            phase = Phase.objects.create(function=function, index=index, **phase_datum)

            for index, action_datum in enumerate(action_data, 1):
                record_data = action_datum.pop('records', [])
                action_datum.update(user_data)
                action = Action.objects.create(phase=phase, index=index, **action_datum)

                for index, record_datum in enumerate(record_data, 1):
                    record_datum.update(user_data)
                    Record.objects.create(action=action, index=index, **record_datum)

        return function

    def validate_function_id(self, value):
        if not self.instance and Function.objects.filter(function_id=value).exists():
            raise exceptions.ValidationError(_('Function ID %s already exists.') % value)
        return value

    def create(self, validated_data):
        return self._create_new_version(validated_data)

    def update(self, instance, validated_data):
        # if function_id is changed the function will need a new uuid as well
        if validated_data['function_id'] == instance.function_id:
            validated_data['uuid'] = instance.uuid
        else:
            validated_data.pop('uuid', None)
        return self._create_new_version(validated_data)


class FunctionViewSet(DetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Function.objects.filter(is_template=False).prefetch_related('phases')
    serializer_class = FunctionListSerializer
    serializer_class_detail = FunctionDetailSerializer
    lookup_field = 'uuid'
    http_method_names = ['get', 'head', 'options', 'post', 'put']

    def get_queryset(self):
        state = self.request.query_params.get('state')
        if state == 'approved':
            return self.queryset.latest_approved()
        return self.queryset.latest_version()
