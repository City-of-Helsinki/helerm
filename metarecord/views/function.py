from django.contrib.auth import get_user_model
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.partial:
            self.fields['state'].read_only = True

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

    def validate(self, data):
        if self.partial:
            if 'state' not in data:
                raise exceptions.ValidationError({'state': self.error_messages['required']})
            self.check_state_change(self.instance.state, data['state'])
        return data

    def create(self, validated_data):
        return self._create_new_version(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        user = self.context['request'].user

        if self.partial:
            state = validated_data['state']
            if instance.state == state:
                return instance

            # ignore other fields than state and do an actual update instead of a new version
            new_function = super().update(instance, {'state': validated_data['state']})
            new_function.create_metadata_version(user)
            return new_function

        if not user.has_perm(Function.CAN_EDIT):
            raise exceptions.PermissionDenied(_('No permission to edit.'))

        if instance.state in (Function.SENT_FOR_REVIEW, Function.WAITING_FOR_APPROVAL):
            raise exceptions.ValidationError(
                _('Cannot edit while in state "sent_for_review" or "waiting_for_approval"')
            )

        # if function_id is changed the function will need a new uuid as well
        if validated_data['function_id'] == instance.function_id:
            validated_data['uuid'] = instance.uuid
        else:
            validated_data.pop('uuid', None)

        new_function = self._create_new_version(validated_data)
        new_function.create_metadata_version(user)

        return new_function

    def check_state_change(self, old_state, new_state):
        user = self.context['request'].user

        if old_state == new_state:
            return

        valid_changes = {
            Function.DRAFT: {Function.SENT_FOR_REVIEW},
            Function.SENT_FOR_REVIEW: {Function.WAITING_FOR_APPROVAL, Function.DRAFT},
            Function.WAITING_FOR_APPROVAL: {Function.APPROVED, Function.DRAFT},
            Function.APPROVED: {Function.DRAFT},
        }
        if new_state not in valid_changes[old_state]:
            raise exceptions.ValidationError({'state': [_('Invalid state change.')]})

        state_change_required_perms = {
            Function.SENT_FOR_REVIEW: Function.CAN_EDIT,
            Function.WAITING_FOR_APPROVAL: Function.CAN_REVIEW,
            Function.APPROVED: Function.CAN_APPROVE,
        }

        relevant_state = new_state if new_state != Function.DRAFT else old_state
        required_perm = state_change_required_perms[relevant_state]

        if not user.has_perm(required_perm):
            raise exceptions.PermissionDenied(_('No permission for the state change.'))


class FunctionViewSet(DetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Function.objects.filter(is_template=False).prefetch_related('phases')
    serializer_class = FunctionListSerializer
    serializer_class_detail = FunctionDetailSerializer
    lookup_field = 'uuid'
    http_method_names = ['get', 'head', 'options', 'post', 'put', 'patch']

    def get_queryset(self):
        state = self.request.query_params.get('state')
        if state == 'approved':
            return self.queryset.latest_approved()
        return self.queryset.latest_version()
