from django.conf import settings
from django.db import connection, models, transaction
from django.utils.translation import ugettext_lazy as _

from .classification import Classification
from .structural_element import StructuralElement


class FunctionQuerySet(models.QuerySet):
    def latest_version(self):
        return self.order_by('classification__code', '-version').distinct('classification__code')

    def latest_approved(self):
        return self.filter(state=Function.APPROVED).latest_version()

    def filter_for_user(self, user):
        if not user.is_authenticated:
            return self.filter(state=Function.APPROVED)
        return self

    def previous_versions(self, function):
        return self.filter(
            version__lt=function.version,
            classification__uuid=function.classification.uuid
        )

    def non_approved(self):
        return self.exclude(state=Function.APPROVED)


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
    CAN_VIEW_MODIFIED_BY = 'metarecord.can_view_modified_by'

    name = models.CharField(verbose_name=_('name'), max_length=256, blank=True)  # only templates use this field
    error_count = models.PositiveIntegerField(verbose_name=_('error count'), default=0)
    is_template = models.BooleanField(verbose_name=_('is template'), default=False)
    version = models.PositiveIntegerField(db_index=True, default=1, null=True, blank=True)
    state = models.CharField(verbose_name=_('state'), max_length=20, choices=STATE_CHOICES, default=DRAFT)
    valid_from = models.DateField(verbose_name=_('valid from'), null=True, blank=True)
    valid_to = models.DateField(verbose_name=_('valid to'), null=True, blank=True)
    classification = models.ForeignKey(
        Classification, verbose_name=_('classification'), null=True, blank=True, related_name='functions',
        on_delete=models.SET_NULL
    )
    bulk_update = models.ForeignKey(
        'metarecord.BulkUpdate',
        verbose_name=_('bulk update'),
        null=True,
        blank=True,
        related_name='functions',
        on_delete=models.SET_NULL,
    )

    # Function attribute validation rules, hardcoded at least for now
    _attribute_validations = {
        'allowed': (
            'AdditionalInformation', 'DataGroup', 'CollectiveProcessIDSource', 'InformationSystem', 'PersonalData',
            'ProcessOwner', 'PublicityClass', 'ProtectionClass', 'Restriction.ProtectionLevel',
            'Restriction.SecurityClass', 'Restriction.SecurityPeriodStart', 'RetentionPeriod', 'RetentionPeriodOffice',
            'RetentionPeriodStart', 'RetentionReason', 'SecurityPeriod', 'SecurityReason', 'SocialSecurityNumber',
            'StorageAccountable', 'StorageLocation', 'StorageOrder', 'Subject.Scheme', 'Subject'
        ),
        'required': (
            'PersonalData', 'PublicityClass', 'RetentionPeriod', 'RetentionPeriodStart', 'RetentionReason',
            'SocialSecurityNumber'
        ),
        'conditionally_required': {
            'SecurityPeriod': {'PublicityClass': ('Salassa pidettävä', 'Osittain salassa pidettävä')},
            'Restriction.SecurityPeriodStart': {'PublicityClass': ('Salassa pidettävä', 'Osittain salassa pidettävä')},
            'SecurityReason': {'PublicityClass': ('Salassa pidettävä', 'Osittain salassa pidettävä')}
        },
        'conditionally_disallowed': {
            'RetentionPeriodStart': {'RetentionPeriod': ('-1',)}
        },
        'multivalued': (
            'InformationSystem', 'Subject'
        ),
        'allow_values_outside_choices': (
            'InformationSystem', 'Subject'
        ),
    }

    class Meta:
        verbose_name = _('function')
        verbose_name_plural = _('functions')
        unique_together = (('uuid', 'version'),)
        permissions = (
            ('can_edit', _('Can edit')),
            ('can_review', _('Can review')),
            ('can_approve', _('Can approve')),
            ('can_view_modified_by', _('Can view modified by')),
        )

    objects = FunctionQuerySet.as_manager()

    def __str__(self):
        if self.is_template:
            return '* %s * %s' % (_('template').upper(), self.get_name())

        return '%s %s' % (self.get_classification_code(), self.get_name())

    def get_classification_code(self):
        return self.classification.code if self.classification else ''

    def get_name(self):
        if self.is_template:
            return self.name
        return self.classification.title if self.classification else ''

    def can_user_delete(self, user):
        if self.state != Function.DRAFT:
            return False

        if user.has_perm('metarecord.delete_function') or self.modified_by == user:
            return True

        return False

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.is_template:
            self.classification = None
            self.version = None
            super().save(*args, **kwargs)
            return

        if not self.classification:
            raise Exception('Classification is required.')

        if self.state == Function.APPROVED and self.classification.state != Classification.APPROVED:
            raise Exception('Approved function must have approved classification')

        if not self.id:
            # lock Function table to prevent possible race condition when adding the new latest version number
            with connection.cursor() as cursor:
                cursor.execute('LOCK TABLE %s' % self._meta.db_table)
            try:
                latest = Function.objects.latest_version().get(classification__uuid=self.classification.uuid)
                self.version = latest.version + 1
                self.uuid = latest.uuid
            except Function.DoesNotExist:
                self.version = 1

        super().save(*args, **kwargs)

        if self.state == Function.APPROVED:
            # Delete old non-approved versions leading to current version if newly saved version is approved.
            self.delete_old_non_approved_versions()

    def delete_old_non_approved_versions(self):
        if self.state != Function.APPROVED:
            raise Exception('Function must be approved before old non-approved versions can be deleted.')

        Function.objects.previous_versions(self).non_approved().delete()

    def create_metadata_version(self):
        MetadataVersion.objects.create(
            function=self,
            modified_at=self.modified_at,
            modified_by=self.modified_by,
            state=self.state,
            valid_from=self.valid_from,
            valid_to=self.valid_to,
        )

    def get_latest_metadata_version(self):
        try:
            return list(self.metadata_versions.all())[-1]
        except IndexError:
            return None


class MetadataVersion(models.Model):
    """
    Stores history of Function's "internal" meta data ie. information not meant for an operational system.
    """
    function = models.ForeignKey(
        Function, verbose_name=_('function'), related_name='metadata_versions', on_delete=models.CASCADE
    )
    modified_at = models.DateTimeField(verbose_name=_('modified at'))
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('modified by'), blank=True, null=True, on_delete=models.SET_NULL
    )
    _modified_by = models.CharField(verbose_name=_('modified by (text)'), max_length=200, blank=True, editable=False)
    state = models.CharField(
        verbose_name=_('state'), max_length=20, choices=Function.STATE_CHOICES, default=Function.DRAFT
    )
    valid_from = models.DateField(verbose_name=_('valid from'), null=True, blank=True)
    valid_to = models.DateField(verbose_name=_('valid to'), null=True, blank=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return ''  # because of admin UI

    def get_modified_by_display(self):
        return self._modified_by

    def save(self, *args, **kwargs):
        # Only update _modified_by value if modified_by is set.
        # _modified_by should persist even if related user is deleted.
        if self.modified_by:
            self._modified_by = self.modified_by.get_full_name()

        super().save(*args, **kwargs)
