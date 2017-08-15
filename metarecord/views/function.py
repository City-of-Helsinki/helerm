from django.db import transaction
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

import django_filters
from rest_framework import exceptions, serializers, viewsets

from metarecord.models import Action, Attribute, Function, Phase, Record

from .base import DetailSerializerMixin, HexRelatedField, StructuralElementSerializer
from .phase import PhaseDetailSerializer


class FunctionListSerializer(StructuralElementSerializer):
    parent = HexRelatedField(queryset=Function.objects.all(), required=False, allow_null=True)
    phases = HexRelatedField(many=True, read_only=True)
    version = serializers.IntegerField(read_only=True)
    modified_by = serializers.SerializerMethodField()

    class Meta(StructuralElementSerializer.Meta):
        model = Function
        exclude = StructuralElementSerializer.Meta.exclude + ('index', 'is_template')

    def get_modified_by(self, obj):
        if obj.modified_by:
            return '{} {}'.format(obj.modified_by.first_name, obj.modified_by.last_name).strip()
        return None


class FunctionDetailSerializer(FunctionListSerializer):
    phases = PhaseDetailSerializer(many=True)

    class Meta(FunctionListSerializer.Meta):
        read_only_fields = ('function_id',)

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

    def validate(self, data):
        new_valid_from = data.get('valid_from')
        new_valid_to = data.get('valid_to')
        if new_valid_from and new_valid_to and new_valid_from > new_valid_to:
            raise exceptions.ValidationError(_('"valid_from" cannot be after "valid_to".'))

        if self.partial:
            if not any(field in data for field in ('state', 'valid_from', 'valid_to')):
                raise exceptions.ValidationError(_('"state", "valid_from" or "valid_to" required.'))
            self.check_state_change(self.instance.state, data['state'])

            if self.instance.state == Function.DRAFT and data['state'] != Function.DRAFT:
                errors = self.get_attribute_validation_errors(self.instance)
                if errors:
                    raise exceptions.ValidationError(errors)
        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        user = self.context['request'].user

        if self.partial:
            allowed_fields = {'state', 'valid_from', 'valid_to'}
            data = {field: validated_data[field] for field in allowed_fields if field in validated_data}
            if not data:
                return instance

            # ignore other fields than state, valid_from and valid_to
            # and do an actual update instead of a new version
            new_function = super().update(instance, {
                'state': validated_data.get('state'),
                'valid_from': validated_data.get('valid_from'),
                'valid_to': validated_data.get('valid_to'),
            })
            new_function.create_metadata_version(user)
            return new_function

        if not user.has_perm(Function.CAN_EDIT):
            raise exceptions.PermissionDenied(_('No permission to edit.'))

        if instance.state in (Function.SENT_FOR_REVIEW, Function.WAITING_FOR_APPROVAL):
            raise exceptions.ValidationError(
                _('Cannot edit while in state "sent_for_review" or "waiting_for_approval"')
            )

        validated_data['function_id'] = instance.function_id
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


class FunctionFilterSet(django_filters.FilterSet):
    class Meta:
        model = Function
        fields = ('valid_at',)

    valid_at = django_filters.DateFilter(method='filter_valid_at')

    def filter_valid_at(self, queryset, name, value):
        # if neither date is set the function is considered not valid
        queryset = queryset.exclude(Q(valid_from__isnull=True) & Q(valid_to__isnull=True))

        # null value means there is no bound in that direction
        queryset = queryset.filter(
            (Q(valid_from__isnull=True) | Q(valid_from__lte=value)) &
            (Q(valid_to__isnull=True) | Q(valid_to__gte=value))
        )
        return queryset


class FunctionViewSet(DetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Function.objects.filter(is_template=False).select_related('modified_by').prefetch_related('phases')
    queryset = queryset.order_by('function_id')
    serializer_class = FunctionListSerializer
    serializer_class_detail = FunctionDetailSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = FunctionFilterSet
    lookup_field = 'uuid'
    http_method_names = ['get', 'head', 'options', 'put', 'patch']

    def get_queryset(self):
        state = self.request.query_params.get('state')
        if state == 'approved':
            return self.queryset.latest_approved()
        return self.queryset.latest_version()
