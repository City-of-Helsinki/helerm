from django.db import models
from django.utils.translation import ugettext_lazy as _

from .action import Action
from .structural_element import StructuralElement


class Record(StructuralElement):
    action = models.ForeignKey(Action, verbose_name=_('action'), related_name='records')
    parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', null=True, blank=True)

    # Record attribute validation rules, hardcoded at least for now
    _attribute_validations = {
        'allowed': (
            'AdditionalInformation', 'DataGroup', 'DisposePreviousVersions', 'InformationSystem', 'PersonalData',
            'PublicityClass', 'PublicityClassChange', 'RecordType', 'Restriction.ProtectionLevel',
            'Restriction.SecurityClass', 'Restriction.SecurityPeriodStart', 'RetentionPeriod', 'RetentionPeriodStart',
            'RetentionPeriodTotal', 'RetentionPeriodOffice', 'RetentionReason', 'ProtectionClass', 'SecurityPeriod',
            'SecurityReason', 'SocialSecurityNumber', 'StorageAccountable', 'StorageLocation', 'StorageOrder',
            'Subject.Scheme', 'Subject', 'TypeSpecifier'
        ),
        'required': (
            'PersonalData', 'PublicityClass', 'RecordType', 'RetentionPeriod', 'RetentionPeriodStart',
            'RetentionReason', 'SocialSecurityNumber'
        ),
        'conditionally_required': {
            'SecurityPeriod': {'PublicityClass': ('Salassa pidettävä', 'Osittain salassa pidettävä')},
            'Restriction.SecurityPeriodStart': {'PublicityClass': ('Salassa pidettävä', 'Osittain salassa pidettävä')},
            'SecurityReason': {'PublicityClass': ('Salassa pidettävä', 'Osittain salassa pidettävä')}
        },
        'multivalued': (
            'DataGroup', 'InformationSystem', 'RetentionReason', 'SecurityReason', 'Subject', 'Subject.Scheme',
        ),
        'all_or_none': (
            ('StorageLocation', 'RetentionPeriodOffice', 'StorageAccountable', 'StorageOrder', 'ProtectionClass'),
        )
    }

    class Meta:
        verbose_name = _('record')
        verbose_name_plural = _('records')
        ordering = ('action', 'index')

    def __str__(self):
        return '%s / %s' % (self.action, self.get_name() or '-')

    def get_name(self):
        type_specifier = self.attributes.get('TypeSpecifier')
        if type_specifier:
            return type_specifier
        return self.attributes.get('RecordType')
