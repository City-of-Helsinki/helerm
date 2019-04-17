from copy import deepcopy

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from ..utils import create_new_function_version, update_nested_dictionary
from .base import TimeStampedModel, UUIDPrimaryKeyModel
from .function import Function


class BulkUpdate(TimeStampedModel, UUIDPrimaryKeyModel):
    # Add, change, and delete are Django default permissions. Approve is project specific.
    CAN_ADD = 'metarecord.add_bulkupdate'
    CAN_CHANGE = 'metarecord.change_bulkupdate'
    CAN_DELETE = 'metarecord.delete_bulkupdate'
    CAN_APPROVE = 'metarecord.approve_bulkupdate'

    description = models.CharField(verbose_name=_('description'), max_length=512, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('created by'),
        null=True,
        blank=True,
        related_name='%(class)s_created',
        editable=False,
        on_delete=models.SET_NULL
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('modified by'),
        null=True,
        blank=True,
        related_name='%(class)s_modified',
        editable=False,
        on_delete=models.SET_NULL
    )

    is_approved = models.BooleanField(verbose_name=_('is approved'), default=False)
    changes = JSONField(verbose_name=_('changes'), blank=True, default=dict)
    state = models.CharField(
        verbose_name=_('state'),
        max_length=20,
        choices=Function.STATE_CHOICES,
        help_text=_('The state that is assigned to functions after applying the updates'),
    )

    class Meta:
        verbose_name = _('bulk update')
        verbose_name_plural = _('bulk updates')
        permissions = (
            ('metarecord.approve_bulkupdate', _('Can approve bulk update')),
        )

    def _apply_changes_to_instance(self, instance, changes, fields=()):
        for field, value in changes.items():
            if field not in fields:
                continue
            old_value = getattr(instance, field, None)
            if isinstance(old_value, dict) and isinstance(value, dict):
                setattr(instance, field, update_nested_dictionary(old_value, value))
            else:
                setattr(instance, field, value)

    @transaction.atomic
    def approve(self, user):
        if not user.has_perm(self.CAN_APPROVE):
            raise PermissionDenied(_('No permission to approve.'))

        self.apply_changes(user)
        self.is_approved = True
        self.save(update_fields=['is_approved'])

    @transaction.atomic
    def apply_changes(self, user):
        """
        Iterate through the changes and apply the changes to functions and its related
        objects (phases, actions and records).
        """
        changes = deepcopy(self.changes)

        for key, function_updates in changes.items():
            phases = function_updates.pop('phases', {})

            # Dictionary key is expected to be '<uuid>__<version>'
            function_uuid, version_str = key.split('__')
            base_function = (Function.objects
                             .filter(uuid=function_uuid, version=int(version_str))
                             .prefetch_related(
                                 'phases',
                                 'phases__actions',
                                 'phases__actions__records')
                             .first())

            function = create_new_function_version(base_function, user)
            function.bulk_update = self
            function.state = self.state
            self._apply_changes_to_instance(function, function_updates, fields=('attributes',))
            function.save()

            for phase_uuid, phase_updates in phases.items():
                actions = phase_updates.pop('actions', {})
                phase = function.phases.get(uuid=phase_uuid)
                self._apply_changes_to_instance(phase, phase_updates, fields=('attributes',))
                phase.save()

                for action_uuid, action_updates in actions.items():
                    records = action_updates.pop('records', {})

                    action = phase.actions.get(uuid=action_uuid)
                    action_records = action.records.all()
                    self._apply_changes_to_instance(action, action_updates, fields=('attributes',))
                    action.save()

                    for record_uuid, record_updates in records.items():
                        record = action_records.get(uuid=record_uuid)
                        self._apply_changes_to_instance(record, record_updates, fields=('attributes',))
                        record.save()
