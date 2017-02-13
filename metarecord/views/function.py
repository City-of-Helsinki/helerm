from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers, viewsets

from metarecord.models import Action, Function, Phase, Record

from .base import DetailSerializerMixin, HexRelatedField, StructuralElementSerializer
from .phase import PhaseDetailSerializer


class FunctionListSerializer(StructuralElementSerializer):
    parent = HexRelatedField(queryset=Function.objects.all())
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
        phase_data = function_data.pop('phases', [])
        function = Function.objects.create(created_by=user, modified_by=user, **function_data)

        for phase_datum in phase_data:
            action_data = phase_datum.pop('actions', [])
            phase = Phase.objects.create(function=function, created_by=user, modified_by=user, **phase_datum)

            for action_datum in action_data:
                record_data = action_datum.pop('records', [])
                action = Action.objects.create(phase=phase, created_by=user, modified_by=user, **action_datum)

                for record_datum in record_data:
                    Record.objects.create(action=action, created_by=user, modified_by=user, **record_datum)

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
