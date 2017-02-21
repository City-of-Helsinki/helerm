from django.db import models
from django.utils.translation import ugettext_lazy as _

from .action import Action
from .structural_element import StructuralElement


class Record(StructuralElement):
    action = models.ForeignKey(Action, verbose_name=_('action'), related_name='records')
    name = models.CharField(verbose_name=_('type specifier'), max_length=256)
    parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', null=True, blank=True)

    # Record attribute validation rules, hardcoded at least for now
    _attribute_validations = {
        'allowed': ['PersonalData', 'PublicityClass', 'SecurityPeriod', 'Restriction.SecurityPeriodStart',
                    'SecurityReason', 'RetentionPeriod', 'RetentionReason', 'RetentionPeriodStart',
                    'AdditionalInformation', 'RetentionPeriodTotal', 'RetentionPeriodOffice', 'InformationSystem',
                    'SocialSecurityNumber', 'StorageAccountable', 'StorageLocation', 'StorageOrder',
                    'ProtectionClass', 'AdditionalInformation', 'RecordType'],
        'required': ['PersonalData', 'PublicityClass', 'SecurityPeriod', 'Restriction.SecurityPeriodStart',
                     'SecurityReason', 'RetentionPeriod', 'RetentionReason', 'RetentionPeriodStart', 'RecordType'],
        'conditionally_required': {
            'SecurityPeriod': {'PublicityClass': 'Salassa pidettävä'},
            'Restriction.SecurityPeriodStart': {'PublicityClass': 'Salassa pidettävä'},
            'SecurityReason': {'PublicityClass': 'Salassa pidettävä'}
        }
    }

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')
        ordering = ('action', 'index')

    def __str__(self):
        return '%s / %s' % (self.action, self.name)
