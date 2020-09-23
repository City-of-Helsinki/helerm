import uuid
from collections import Iterable

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from .base import TimeStampedModel


class ClassificationQuerySet(models.QuerySet):
    def latest_version(self):
        return self.order_by('code', '-version').distinct('code')

    def latest_approved(self):
        return self.filter(state=Classification.APPROVED).latest_version()


class Classification(TimeStampedModel):
    DRAFT = 'draft'
    SENT_FOR_REVIEW = 'sent_for_review'
    WAITING_FOR_APPROVAL = 'waiting_for_approval'
    APPROVED = 'approved'

    STATE_CHOICES = (
        (DRAFT, _('Draft')),
        (SENT_FOR_REVIEW, _('Sent for review')),
        (WAITING_FOR_APPROVAL, _('Waiting for approval')),
        (APPROVED, _('Approved')),
    )

    CAN_EDIT = 'metarecord.can_edit_classification'
    CAN_REVIEW = 'metarecord.can_review_classification'
    CAN_APPROVE = 'metarecord.can_approve_classification'
    CAN_VIEW_MODIFIED_BY = 'metarecord.can_view_classification_modified_by'

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    version = models.PositiveIntegerField(db_index=True, default=1, null=True, blank=True)
    state = models.CharField(verbose_name=_('state'), max_length=20, choices=STATE_CHOICES, default=DRAFT)
    valid_from = models.DateField(verbose_name=_('valid from'), null=True, blank=True)
    valid_to = models.DateField(verbose_name=_('valid to'), null=True, blank=True)
    created_by = models.ForeignKey(
        get_user_model(),
        verbose_name=_('created by'),
        null=True,
        blank=True,
        related_name='%(class)s_created',
        editable=False,
        on_delete=models.SET_NULL
    )
    modified_by = models.ForeignKey(
        get_user_model(),
        verbose_name=_('modified by'),
        null=True,
        blank=True,
        related_name='%(class)s_modified',
        editable=False,
        on_delete=models.SET_NULL
    )
    _created_by = models.CharField(verbose_name=_('created by (text)'), max_length=200, blank=True, editable=False)
    _modified_by = models.CharField(verbose_name=_('modified by (text)'), max_length=200, blank=True, editable=False)

    parent = models.ForeignKey(
        'self', verbose_name=_('parent'), related_name='children', blank=True, null=True, on_delete=models.SET_NULL
    )
    code = models.CharField(verbose_name=_('code'), max_length=16, db_index=True)
    title = models.CharField(verbose_name=_('title'), max_length=256)
    description = models.TextField(verbose_name=_('description'), blank=True)
    description_internal = models.TextField(verbose_name=_('description internal'), blank=True)
    related_classification = models.TextField(verbose_name=_('related classification'), blank=True)
    additional_information = models.TextField(verbose_name=_('additional information'), blank=True)
    function_allowed = models.BooleanField(verbose_name=_('function allowed'), default=False)

    objects = ClassificationQuerySet.as_manager()

    class Meta:
        verbose_name = _('classification')
        verbose_name_plural = _('classifications')
        unique_together = (('uuid', 'version'),)
        permissions = (
            ('can_edit_classification', _('Can edit classification')),
            ('can_review_classification', _('Can review classification')),
            ('can_approve_classification', _('Can approve classification')),
            ('can_view_classification_modified_by', _('Can view classification modified by')),
        )

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        # Only update `_created_by` and `_modified_by` value if the relations
        # are set set. Text values should persist even if related user is deleted.
        if self.created_by:
            self._created_by = self.created_by.get_full_name()

        if self.modified_by:
            self._modified_by = self.modified_by.get_full_name()

        super().save(*args, **kwargs)


@transaction.atomic
def update_function_allowed(classifications):
    if not isinstance(classifications, Iterable):
        classifications = (classifications,)

    for classification in classifications:
        classification.function_allowed = not classification.children.exists()
        classification.save(update_fields=('function_allowed',))
