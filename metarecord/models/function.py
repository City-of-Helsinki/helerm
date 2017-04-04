from django.db import connection, models, transaction
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .structural_element import StructuralElement


class FunctionQuerySet(models.QuerySet):
    def latest_version(self):
        return self.order_by('function_id', '-version').distinct('function_id')

    def latest_approved(self):
        return self.filter(state=Function.APPROVED).latest_version()


class Function(StructuralElement):
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

    CAN_EDIT = 'metarecord.can_edit'
    CAN_REVIEW = 'metarecord.can_review'
    CAN_APPROVE = 'metarecord.can_approve'

    function_id = models.CharField(verbose_name=_('function ID'), max_length=16, db_index=True, null=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', blank=True, null=True)
    name = models.CharField(verbose_name=_('name'), max_length=256)
    error_count = models.PositiveIntegerField(verbose_name=_('error count'), default=0)
    is_template = models.BooleanField(verbose_name=_('is template'), default=False)
    version = models.PositiveIntegerField(db_index=True, default=1, null=True, blank=True)
    state = models.CharField(verbose_name=_('state'), max_length=20, choices=STATE_CHOICES, default=DRAFT)

    # Function attribute validation rules, hardcoded at least for now
    _attribute_validations = {
        'allowed': (
            'AdditionalInformation', 'DataGroup', 'CollectiveProcessIDSource', 'InformationSystem', 'PersonalData',
            'ProcessInformation', 'ProcessOwner', 'PublicityClass', 'Restriction.ProtectionLevel',
            'Restriction.SecurityClass', 'Restriction.SecurityPeriodStart', 'RetentionPeriod', 'RetentionPeriodStart',
            'RetentionReason', 'SecurityPeriod', 'SecurityReason', 'Subject.Scheme', 'Subject',
        ),
        'required': (
            'PersonalData', 'PublicityClass', 'RetentionPeriod', 'RetentionPeriodStart', 'RetentionReason'
        ),
        'conditionally_required': {
            'SecurityPeriod': {'PublicityClass': 'Salassa pidettävä'},
            'Restriction.SecurityPeriodStart': {'PublicityClass': 'Salassa pidettävä'},
            'SecurityReason': {'PublicityClass': 'Salassa pidettävä'}
        }
    }

    class Meta:
        verbose_name = _('function')
        verbose_name_plural = _('functions')
        unique_together = (('function_id', 'version'), ('uuid', 'version'))
        permissions = (
            ('can_edit', _('Can edit')),
            ('can_review', _('Can review')),
            ('can_approve', _('Can approve'))
        )

    objects = FunctionQuerySet.as_manager()

    def __str__(self):
        if self.is_template:
            return '* %s * %s' % (_('template').upper(), self.name)

        return '%s %s' % (self.function_id, self.name)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.is_template:
            self.function_id = None
            self.version = None
            super().save(*args, **kwargs)
            return

        if not self.function_id:
            raise Exception('function_id cannot be empty or null.')

        if not self.id:

            # lock Function table to prevent possible race condition when adding the new latest version number
            with connection.cursor() as cursor:
                cursor.execute('LOCK TABLE %s' % self._meta.db_table)
            try:
                latest = Function.objects.latest_version().get(function_id=self.function_id)
                self.version = latest.version + 1
                self.uuid = latest.uuid
            except Function.DoesNotExist:
                self.version = 1

        super().save(*args, **kwargs)

    def create_metadata_version(self, modified_by=None):
        MetadataVersion.objects.create(
            function=self,
            modified_at=self.modified_at,
            modified_by=modified_by,
            state=self.state,
        )


class MetadataVersion(models.Model):
    function = models.ForeignKey(Function, verbose_name=_('function'), related_name='metadata_versions')
    modified_at = models.DateTimeField(verbose_name=_('modified at'))
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('modified by'), blank=True, null=True)
    state = models.CharField(
        verbose_name=_('state'), max_length=20, choices=Function.STATE_CHOICES, default=Function.DRAFT
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return ''  # because of admin UI
