from django.db import connection, models, transaction
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

    function_id = models.CharField(verbose_name=_('function ID'), max_length=16, db_index=True, null=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', blank=True, null=True)
    name = models.CharField(verbose_name=_('name'), max_length=256)
    error_count = models.PositiveIntegerField(default=0)
    is_template = models.BooleanField(verbose_name=_('is template'), default=False)
    version = models.PositiveIntegerField(db_index=True, default=1, null=True, blank=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=DRAFT)

    # Function attribute validation rules, hardcoded at least for now
    _attribute_validations = {
        'allowed': ['PersonalData', 'PublicityClass', 'SecurityPeriod', 'Restriction.SecurityPeriodStart',
                    'SecurityReason', 'RetentionPeriod', 'RetentionReason', 'RetentionPeriodStart',
                    'AdditionalInformation'],
        'required': ['PersonalData', 'PublicityClass', 'SecurityPeriod', 'Restriction.SecurityPeriodStart',
                     'SecurityReason', 'RetentionPeriod', 'RetentionReason', 'RetentionPeriodStart'],
        'conditionally_required': {
            'SecurityPeriod': {'PublicityClass': 'Salassa pidettävä'},
            'Restriction.SecurityPeriodStart': {'PublicityClass': 'Salassa pidettävä'},
            'SecurityReason': {'PublicityClass': 'Salassa pidettävä'}
        }
    }

    class Meta:
        verbose_name = _('function')
        verbose_name_plural = _('functions')
        unique_together = ('function_id', 'version')

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
