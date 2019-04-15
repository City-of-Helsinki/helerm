from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

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
